import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from generator import generate_label


class TXTHandler(FileSystemEventHandler):

    def __init__(self, input_folder, output_folder, log_callback):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.log_callback = log_callback

    def on_created(self, event):

        if not event.src_path.endswith(".txt"):
            return

        time.sleep(1.5)

        with open(event.src_path, "r") as f:
            line = f.read().strip()

        parts = line.split(",")

        pdf = generate_label(parts, self.output_folder)

        os.remove(event.src_path)

        self.log_callback(parts[1], parts[0], pdf)


def start_watcher(input_folder, output_folder, log_callback):

    event_handler = TXTHandler(input_folder, output_folder, log_callback)

    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()

    return observer
