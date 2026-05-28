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


processing_queue = queue.Queue()


def get_queue_size():
    return processing_queue.qsize()


class TXTHandler(FileSystemEventHandler):

    def __init__(self, input_folder):
        self.input_folder = input_folder

    def on_created(self, event):

        if not event.src_path.endswith(".txt"):
            return

        print("File detected:", event.src_path)

        processing_queue.put(event.src_path)


def wait_for_file_complete(file_path):

    last_size = -1

    while True:

        size = os.path.getsize(file_path)

        if size == last_size:
            break

        last_size = size
        time.sleep(0.3)


def worker(output_folder, error_folder, log_callback):

    while True:

        file_path = processing_queue.get()

        try:

            wait_for_file_complete(file_path)

            with open(file_path, "r") as f:
                line = f.read().strip()

            if not line:
                raise Exception("Empty TXT file")

            parts = line.split(",")

            if len(parts) < 6:
                raise Exception("Invalid TXT format")

            # ==============================
            # Duplicate UL Check
            # ==============================

            conn = sqlite3.connect(get_db_path())
            cur = conn.cursor()

            existing = cur.execute(
                "SELECT ul FROM labels WHERE ul=?",
                (parts[1],)
            ).fetchone()

            conn.close()

            if existing:
                print("Duplicate UL detected → moving to error folder:", parts[1])

                shutil.move(
                    file_path,
                    os.path.join(error_folder, os.path.basename(file_path))
                )

                continue

            # ==============================
            # Generate Label
            # ==============================

            pdf = generate_label(parts, output_folder)

            print_pdf(pdf)

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

                shutil.move(
                    file_path,
                    os.path.join(error_folder, os.path.basename(file_path))
                )

                continue

            # ==============================
            # Delete TXT after success
            # ==============================

            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:

            print("Processing error:", e)

            try:
                shutil.move(
                    file_path,
                    os.path.join(error_folder, os.path.basename(file_path))
                )
            except:
                pass

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
