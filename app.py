import os
import ttkbootstrap as tk
from ttkbootstrap.constants import *
from tkinter import ttk

from database.db import init_db, add_log, load_logs, search_logs, export_excel, dashboard_stats
from services.watcher import start_watcher, get_queue_size
from services.printer_monitor import get_printer_status

from ui.dashboard import create_dashboard
from ui.logs import create_logs
from ui.sidebar import create_sidebar
from ui.errors import create_errors


# ==============================
# FOLDERS
# ==============================

INPUT_FOLDER = "yet_to_print"
PDF_FOLDER = "pdf"
ERROR_FOLDER = "error_files"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(ERROR_FOLDER, exist_ok=True)


# ==============================
# DATABASE
# ==============================

conn, cur = init_db()


# ==============================
# MAIN WINDOW
# ==============================

root = tk.Window(themename="litera")
root.title("Label Printing System")
root.geometry("1200x720")
root.minsize(1000, 600)

root.style.configure("Treeview", rowheight=28)
root.style.configure(".", font=("Segoe UI", 10))


# ==============================
# MAIN CONTAINER
# ==============================

main_container = ttk.Frame(root)
main_container.pack(fill="both", expand=True)


# ==============================
# TOP BAR
# ==============================

topbar = ttk.Frame(main_container, padding=(20, 12))
topbar.pack(fill="x")

title = ttk.Label(
    topbar,
    text="Label Printing System",
    font=("Segoe UI", 18, "bold")
)
title.pack(side="left")


# ==============================
# THEME TOGGLE
# ==============================

theme_var = tk.BooleanVar()


def toggle_theme():
    if theme_var.get():
        root.style.theme_use("cyborg")
    else:
        root.style.theme_use("litera")


theme_switch = ttk.Checkbutton(
    topbar,
    text="🌙 Dark Mode",
    variable=theme_var,
    command=toggle_theme,
    bootstyle="switch"
)

theme_switch.pack(side="right")


# ==============================
# STATUS BAR
# ==============================

status_frame = ttk.Frame(main_container)
status_frame.pack(fill="x", side="bottom")

status_label = ttk.Label(
    status_frame,
    text="Watching Folder | Queue: 0 | Printer: Ready",
    anchor="w",
    font=("Segoe UI", 10)
)

status_label.pack(fill="x", padx=10, pady=5)


# ==============================
# BODY LAYOUT
# ==============================

body = ttk.Frame(main_container)
body.pack(fill="both", expand=True)

content = ttk.Frame(body)
content.pack(side="right", fill="both", expand=True)


# ==============================
# CONTENT PAGES
# ==============================

dashboard, count_label, last_label = create_dashboard(content)
logs_frame, tree, search_var = create_logs(content)
errors_frame = create_errors(content)

dashboard.place(relwidth=1, relheight=1)
logs_frame.place(relwidth=1, relheight=1)
errors_frame.place(relwidth=1, relheight=1)

dashboard.lift()


# ==============================
# PAGE SWITCHERS
# ==============================

def show_dashboard():
    dashboard.lift()


def show_logs():
    logs_frame.lift()


def show_errors():
    errors_frame.lift()


# ==============================
# SIDEBAR
# ==============================

sidebar = create_sidebar(
    body,
    show_dashboard,
    show_logs,
    show_errors
)


# ==============================
# WATCHER START
# ==============================

observer = start_watcher(
    INPUT_FOLDER,
    PDF_FOLDER,
    ERROR_FOLDER,
    add_log
)


# ==============================
# INITIAL DATA LOAD
# ==============================

load_logs(tree, cur)

count, last_ul = dashboard_stats()

count_label.config(text=str(count))
last_label.config(text=last_ul)


# ==============================
# STATUS MONITOR
# ==============================

def update_status():

    queue_size = get_queue_size()
    printer_status = get_printer_status()

    icon = "🟢"

    if printer_status != "Ready":
        icon = "🟡"

    if printer_status in ["Offline", "Error", "Not Found"]:
        icon = "🔴"

    status_label.config(
        text=f"{icon} Watching Folder | Queue: {queue_size} | Printer: {printer_status}"
    )

    root.after(1000, update_status)


update_status()


# ==============================
# START UI
# ==============================

root.mainloop()


# ==============================
# CLEAN SHUTDOWN
# ==============================

observer.stop()
observer.join()
