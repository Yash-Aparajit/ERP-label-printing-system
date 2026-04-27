import ttkbootstrap as tk
from ttkbootstrap.constants import *
from tkinter import ttk
import sqlite3
import os
from watcher import start_watcher
from datetime import datetime
import pandas as pd

INPUT_FOLDER = "yet_to_print"
PDF_FOLDER = "pdf"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS labels(
id INTEGER PRIMARY KEY,
ul TEXT,
plant TEXT,
pdf TEXT,
time TEXT
)
""")

conn.commit()


def add_log(ul, plant, pdf):

    now = datetime.now().strftime("%H:%M:%S")

    cur.execute(
        "INSERT INTO labels(ul,plant,pdf,time) VALUES(?,?,?,?)",
        (ul, plant, pdf, now)
    )

    conn.commit()

    load_logs()
    update_dashboard()


def load_logs(filter_text=""):

    for i in tree.get_children():
        tree.delete(i)

    query = "SELECT ul,plant,pdf,time FROM labels ORDER BY id DESC"

    for row in cur.execute(query):

        if filter_text.lower() in row[0].lower():
            tree.insert("", tk.END, values=row)

    tree.yview_moveto(1)


def search_logs():

    text = search_var.get()
    load_logs(text)


def reprint():

    item = tree.selection()

    if not item:
        return

    values = tree.item(item)["values"]

    pdf_path = os.path.abspath(values[2])

    if os.path.exists(pdf_path):
        os.startfile(pdf_path)


def export_excel():

    rows = list(cur.execute("SELECT ul,plant,pdf,time FROM labels"))

    if not rows:
        return

    df = pd.DataFrame(rows, columns=["UL Counter", "Plant", "PDF File", "Time"])

    filename = f"label_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    df.to_excel(filename, index=False)

    os.startfile(filename)


def open_pdf_folder():

    os.startfile(os.path.abspath(PDF_FOLDER))


def update_dashboard():

    total = cur.execute("SELECT COUNT(*) FROM labels").fetchone()[0]

    count_label.config(text=f"Labels Generated: {total}")

    last = cur.execute(
        "SELECT ul FROM labels ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if last:
        last_label.config(text=f"Last Label: {last[0]}")


root = tk.Window(themename="flatly")

root.title("Label Printing System")
root.geometry("1100x650")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ---------------------------------------------------
# Dashboard Tab
# ---------------------------------------------------

dashboard = ttk.Frame(notebook)
notebook.add(dashboard, text="Dashboard")

status_frame = ttk.LabelFrame(dashboard, text="System Status")
status_frame.pack(fill="x", padx=20, pady=20)

status_label = ttk.Label(status_frame, text="Watching Folder: yet_to_print")
status_label.pack(anchor="w", padx=10, pady=5)

count_label = ttk.Label(status_frame, text="Labels Generated: 0")
count_label.pack(anchor="w", padx=10, pady=5)

last_label = ttk.Label(status_frame, text="Last Label: -")
last_label.pack(anchor="w", padx=10, pady=5)

# ---------------------------------------------------
# Logs Tab
# ---------------------------------------------------

logs = ttk.Frame(notebook)
notebook.add(logs, text="Logs & Reprint")

top_bar = ttk.Frame(logs)
top_bar.pack(fill="x", padx=10, pady=10)

export_btn = ttk.Button(top_bar, text="Export Excel", command=export_excel)
export_btn.pack(side="left", padx=5)

open_folder_btn = ttk.Button(top_bar, text="Open PDF Folder", command=open_pdf_folder)
open_folder_btn.pack(side="left", padx=5)

search_var = tk.StringVar()

search_entry = ttk.Entry(top_bar, textvariable=search_var, width=30)
search_entry.pack(side="right", padx=5)

search_btn = ttk.Button(top_bar, text="Search", command=search_logs)
search_btn.pack(side="right")

table_frame = ttk.Frame(logs)
table_frame.pack(fill="both", expand=True, padx=10)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(
    table_frame,
    columns=("UL", "Plant", "PDF", "Time"),
    show="headings",
    yscrollcommand=scrollbar.set
)

tree.heading("UL", text="UL Counter")
tree.heading("Plant", text="Plant")
tree.heading("PDF", text="PDF File")
tree.heading("Time", text="Time")

tree.pack(fill="both", expand=True)

scrollbar.config(command=tree.yview)

reprint_btn = ttk.Button(logs, text="Reprint Selected", command=reprint)
reprint_btn.pack(pady=10)

# ---------------------------------------------------
# Settings Tab
# ---------------------------------------------------

settings = ttk.Frame(notebook)
notebook.add(settings, text="Settings")

settings_frame = ttk.LabelFrame(settings, text="Folders")
settings_frame.pack(fill="x", padx=20, pady=20)

ttk.Label(settings_frame, text=f"Input Folder : {INPUT_FOLDER}").pack(anchor="w", padx=10, pady=5)
ttk.Label(settings_frame, text=f"Output Folder: {PDF_FOLDER}").pack(anchor="w", padx=10, pady=5)

# ---------------------------------------------------

observer = start_watcher(INPUT_FOLDER, PDF_FOLDER, add_log)

load_logs()
update_dashboard()

root.mainloop()

observer.stop()
observer.join()
