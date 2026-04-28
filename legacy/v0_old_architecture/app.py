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


# ---------------------------------------------------
# Theme Toggle 
# ---------------------------------------------------

class ThemeToggle(tk.Frame):

    def __init__(self, parent, root):
        super().__init__(parent)

        self.root = root
        self.dark = False

        self.canvas = tk.Canvas(self, width=70, height=30, highlightthickness=0, bg=self.master.cget("bg"))
        self.canvas.pack()

        self.bg = self.canvas.create_oval(2,2,68,28, fill="#1db954", outline="")
        self.knob = self.canvas.create_oval(4,4,26,26, fill="white", outline="")
        self.icon = self.canvas.create_text(15,15,text="☀",font=("Segoe UI",10,"bold"))

        self.canvas.bind("<Button-1>", self.toggle)

    def animate(self, direction):

        steps = 12
        move = 2.5 if direction == "right" else -2.5

        for _ in range(steps):
            self.canvas.move(self.knob, move, 0)
            self.canvas.move(self.icon, move, 0)
            self.canvas.update()
            self.canvas.after(10)

    def toggle(self, event=None):

        if self.dark:

            self.animate("left")
            self.root.style.theme_use("litera")
            self.canvas.itemconfig(self.bg, fill="#1db954")
            self.canvas.itemconfig(self.icon, text="☀")

        else:

            self.animate("right")
            self.root.style.theme_use("cyborg")
            self.canvas.itemconfig(self.bg, fill="#444")
            self.canvas.itemconfig(self.icon, text="🌙")

        self.dark = not self.dark

# ---------------------------------------------------
# Database Setup 
# ---------------------------------------------------

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


root = tk.Window(themename="litera")
root.style.configure("Treeview", rowheight=28)
root.style.configure(".", font=("Segoe UI",10))

root.title("Label Printing System")
root.geometry("1200x720")
root.minsize(1000,600)

topbar = tk.Frame(root)
topbar.pack(fill="x")

toggle = ThemeToggle(topbar, root)
toggle.pack(side="right", padx=15, pady=10)

title = ttk.Label(topbar, text="Label Printing System", font=("Segoe UI",14,"bold"))
title.pack(side="left", padx=15)


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


generator.py
import os
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter


def draw_label(c, plant, ul, edi, inv, qty, created, time):

    c.setFont("Courier-Bold",9)

    c.drawString(3*mm,34*mm,f"U/L COUNTER : {ul}")
    c.drawRightString(72*mm,34*mm,plant)

    c.drawString(3*mm,30*mm,f"EDI NUMBER : {edi}")
    c.drawString(3*mm,26*mm,f"INV/DATE : {inv}")
    c.drawString(3*mm,22*mm,f"EDI/REC. QTY : {qty}")
    c.drawString(3*mm,18*mm,f"CREATED BY : {created}")
    c.drawString(3*mm,14*mm,f"C. DATE/TIME : {time}")

    options = {
        "write_text": False,
        "module_width": 0.28,
        "module_height": 6,
        "quiet_zone": 1
    }

    code = barcode.get('code128', ul, writer=ImageWriter())
    barcode_file = code.save("temp_barcode", options)

    c.drawImage(barcode_file,5*mm,2*mm,width=60*mm,height=9*mm)

    os.remove(barcode_file)


def generate_label(data, output_folder):

    plant, ul, edi, inv, qty, created, time = data

    pdf_path = os.path.join(output_folder, f"{ul}.pdf")

    # correct sticker size
    c = canvas.Canvas(pdf_path, pagesize=(75*mm,38*mm))

    # page 1
    draw_label(c, plant, ul, edi, inv, qty, created, time)
    c.showPage()

    # page 2
    draw_label(c, plant, ul, edi, inv, qty, created, time)
    c.showPage()

    # page 3
    draw_label(c, plant, ul, edi, inv, qty, created, time)

    c.save()

    return pdf_path


atcher.py
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
