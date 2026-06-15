import os
import time
import queue
import threading
import shutil
import sqlite3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.generator import generate_label
from services.printer import print_pdf
from database.db import get_db_path
from collections import deque


processing_queue = queue.Queue()


def get_queue_size():
    return processing_queue.qsize()


class TXTHandler(FileSystemEventHandler):

    def __init__(self, input_folder):
        self.input_folder = input_folder
        self.recent_files = set()
        self.recent_files_order = deque(maxlen=500)   # ← add this line

    def on_created(self, event):

        if not event.src_path.endswith(".txt"):
            return

        print("File detected:", event.src_path)

        if event.src_path not in self.recent_files:

            if len(self.recent_files_order) >= self.recent_files_order.maxlen:
                old = self.recent_files_order.popleft()
                self.recent_files.discard(old)

            self.recent_files.add(event.src_path)
            self.recent_files_order.append(event.src_path)

            processing_queue.put(event.src_path)


def wait_for_file_complete(file_path, timeout=10):

    last_size = -1
    start = time.time()

    while True:

        if not os.path.exists(file_path):
            raise Exception("File disappeared during write")

        size = os.path.getsize(file_path)

        if size == last_size:
            return

        last_size = size

        if time.time() - start > timeout:
            raise Exception("File write timeout")

        time.sleep(0.3)


def safe_move(src, dest_folder):

    name = os.path.basename(src)
    dest = os.path.join(dest_folder, name)

    if os.path.exists(dest):
        base, ext = os.path.splitext(name)
        timestamp = int(time.time())
        dest = os.path.join(dest_folder, f"{base}_{timestamp}{ext}")

    shutil.move(src, dest)


def worker(output_folder, error_folder, log_callback):

    while True:

        try:
            file_path = processing_queue.get(timeout=1)
        except queue.Empty:
            continue

        try:

            if not os.path.exists(file_path):
                processing_queue.task_done()
                continue

            wait_for_file_complete(file_path)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                line = f.read().strip()

            if not line:
                raise Exception("Empty TXT file")

            parts = [p.strip() for p in line.split(",")]
            parts = [p for p in parts if p]
            parts = parts[:7]

            if len(parts) < 7:
                raise Exception(f"Invalid TXT format: {parts}")

            print("Parsed TXT:", parts)

            # ==============================
            # Duplicate UL Check
            # ==============================

            conn = sqlite3.connect(get_db_path())
            cur = conn.cursor()

            try:
                existing = cur.execute(
                    "SELECT ul FROM labels WHERE ul=?",
                    (parts[1],)
                ).fetchone()
            except sqlite3.OperationalError:
                existing = None

            conn.close()

            if existing:
                print("Duplicate UL detected → moving to error folder:", parts[1])

                safe_move(file_path, error_folder)

                continue

            # ==============================
            # Generate Label
            # ==============================

            pdf = generate_label(parts, output_folder)

            # ==============================
            # Log Entry
            # ==============================

            result = log_callback(
                parts[1], parts[0], parts[2],
                parts[4], parts[5],
                "SUCCESS",
                pdf
            )

            if result is False:

                print("Duplicate UL detected at DB level → moving file to error folder")

                safe_move(file_path, error_folder)

                continue

            print_pdf(pdf)

            # ==============================
            # Delete TXT after success
            # ==============================

            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:

            print("Processing error:", e)

            try:
                safe_move(file_path, error_folder)
            except Exception as move_error:
                print("Failed to move file to error folder:", move_error)

        finally:

            processing_queue.task_done()


def start_watcher(input_folder, output_folder, error_folder, log_callback):

    event_handler = TXTHandler(input_folder)

    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()

    worker_thread = threading.Thread(
        target=worker,
        args=(output_folder, error_folder, log_callback),
        daemon=True
    )

    worker_thread.start()

    return observer
