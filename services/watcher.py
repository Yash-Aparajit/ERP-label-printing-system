import os
import time
import queue
import threading
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.generator import generate_label
from services.printer import print_pdf
import sqlite3

processing_queue = queue.Queue()

class TXTHandler(FileSystemEventHandler):

    def __init__(self, input_folder):
        self.input_folder = input_folder

    def on_created(self, event):

        if not event.src_path.endswith(".txt"):
            return

        print("File detected:", event.src_path)

        processing_queue.put(event.src_path)


def worker(output_folder, error_folder, log_callback):

    while True:

        file_path = processing_queue.get()

        try:

            size1 = os.path.getsize(file_path)
            time.sleep(0.5)
            size2 = os.path.getsize(file_path)

            if size1 != size2:
                time.sleep(0.5)

            with open(file_path, "r") as f:
                line = f.read().strip()

            parts = line.split(",")

            # Duplicate UL check
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()

            existing = cur.execute(
                "SELECT ul FROM labels WHERE ul=?",
                (parts[1],)
            ).fetchone()

            conn.close()

            if existing:
                print("Duplicate UL detected. Skipping:", parts[1])
                os.remove(file_path)
                continue

            pdf = generate_label(parts, output_folder)

            print_pdf(pdf)

            os.remove(file_path)

            log_callback(parts[1], parts[0], pdf)

        except Exception as e:

            print("Processing error:", e)
            shutil.move(file_path, os.path.join(error_folder, os.path.basename(file_path)))

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

