import os
import time
import queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from generator import generate_label


processing_queue = queue.Queue()


class TXTHandler(FileSystemEventHandler):

    def __init__(self, input_folder):
        self.input_folder = input_folder

    def on_created(self, event):

        if not event.src_path.endswith(".txt"):
            return

        print("File detected:", event.src_path)

        processing_queue.put(event.src_path)


def worker(output_folder, log_callback):

    while True:

        file_path = processing_queue.get()

        try:

            time.sleep(1)

            with open(file_path, "r") as f:
                line = f.read().strip()

            parts = line.split(",")

            pdf = generate_label(parts, output_folder)

            os.remove(file_path)

            log_callback(parts[1], parts[0], pdf)

        except Exception as e:

            print("Processing error:", e)

        finally:

            processing_queue.task_done()


def start_watcher(input_folder, output_folder, log_callback):

    event_handler = TXTHandler(input_folder)

    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()

    worker_thread = threading.Thread(
        target=worker,
        args=(output_folder, log_callback),
        daemon=True
    )

    worker_thread.start()

    return observer
