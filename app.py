import ttkbootstrap as tk
from ttkbootstrap.constants import *
from tkinter import ttk
import os

from database.db import init_db, add_log, load_logs, search_logs, export_excel, dashboard_stats
from services.watcher import start_watcher, get_queue_size
from ui.dashboard import create_dashboard
from ui.logs import create_logs
from ui.sidebar import create_sidebar

INPUT_FOLDER = "yet_to_print"
PDF_FOLDER = "pdf"
ERROR_FOLDER = "error_files"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(ERROR_FOLDER, exist_ok=True)

conn, cur = init_db()

root = tk.Window(themename="litera")
root.title("Label Printing System")
root.geometry("1200x720")
root.minsize(1000,600)

root.style.configure("Treeview", rowheight=28)
root.style.configure(".", font=("Segoe UI",10))

topbar = tk.Frame(root, padding=(20,12))
topbar.pack(fill="x")

title = ttk.Label(topbar, text="Label Printing System", font=("Segoe UI",18,"bold"))
title.pack(side="left")

sidebar = create_sidebar(root)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

status_frame = ttk.Frame(root)
status_frame.pack(fill="x", side="bottom")

status_label = ttk.Label(
    status_frame,
    text="Watching Folder | Queue: 0 | Printer: Ready",
    anchor="w",
    font=("Segoe UI",10)
)

status_label.pack(fill="x", padx=10, pady=5)

dashboard, count_label, last_label = create_dashboard(notebook)
logs_frame, tree, search_var = create_logs(notebook)

notebook.add(dashboard, text="Dashboard")
notebook.add(logs_frame, text="Logs & Reprint")

observer = start_watcher(INPUT_FOLDER, PDF_FOLDER, ERROR_FOLDER, add_log)

load_logs(tree, cur)
count, last_ul = dashboard_stats()

count_label.config(text=str(count))
last_label.config(text=last_ul)

def update_status():

    queue_size = get_queue_size()

    status_label.config(
        text=f"🟢 Watching Folder | Queue: {queue_size} | Printer: Ready"
    )

    root.after(1000, update_status)

update_status()


root.mainloop()

observer.stop()
observer.join()

