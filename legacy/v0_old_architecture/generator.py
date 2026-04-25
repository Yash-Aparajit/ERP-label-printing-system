from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter
import os


def generate_label(data, output_folder):

    plant, ul, edi, inv, qty, created, time = data

    pdf_path = os.path.join(output_folder, f"{ul}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(75*mm,38*mm))

    c.setFont("Courier",10)

    c.drawString(3*mm,34*mm,f"U/L COUNTER : {ul}")
    c.drawRightString(72*mm,34*mm,plant)

    c.drawString(3*mm,30*mm,f"EDI NUMBER : {edi}")
    c.drawString(3*mm,26*mm,f"INV/DATE : {inv}")
    c.drawString(3*mm,22*mm,f"EDI/REC. QTY : {qty}")
    c.drawString(3*mm,18*mm,f"CREATED BY : {created}")
    c.drawString(3*mm,14*mm,f"C. DATE/TIME : {time}")

    code = barcode.get('code128', ul, writer=ImageWriter())
    barcode_file = code.save("temp_barcode")

    c.drawImage(barcode_file,3*mm,2*mm,width=65*mm,height=10*mm)

    c.save()

    return pdf_path


watcher.py

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from generator import generate_label


class TXTHandler(FileSystemEventHandler):

    def __init__(self, input_folder, output_folder, log_callback):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.log_callback = log_callback

    def on_created(self, event):

        if event.src_path.endswith(".txt"):

            with open(event.src_path,"r") as f:
                line = f.read().strip()

            parts = line.split(",")

            pdf = generate_label(parts, self.output_folder)

            self.log_callback(parts[1], parts[0], pdf)


def start_watcher(input_folder, output_folder, log_callback):

    event_handler = TXTHandler(input_folder, output_folder, log_callback)

    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()

    return observer


app.py

import tkinter as tk
from tkinter import ttk
import sqlite3
import os
from watcher import start_watcher
from generator import generate_label

INPUT_FOLDER = "yet_to_print"
PDF_FOLDER = "pdf"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS labels(
id INTEGER PRIMARY KEY,
ul TEXT,
plant TEXT,
pdf TEXT
)
""")

conn.commit()


def add_log(ul, plant, pdf):

    cur.execute("INSERT INTO labels(ul,plant,pdf) VALUES(?,?,?)",(ul,plant,pdf))
    conn.commit()

    load_logs()


def load_logs():

    for i in tree.get_children():
        tree.delete(i)

    for row in cur.execute("SELECT ul,plant,pdf FROM labels ORDER BY id DESC"):
        tree.insert("",tk.END,values=row)


def reprint():

    item = tree.selection()

    if not item:
        return

    values = tree.item(item)["values"]

    os.startfile(values[2])


root = tk.Tk()
root.title("Label Generator")

frame = ttk.Frame(root)
frame.pack(fill="both",expand=True,padx=10,pady=10)

tree = ttk.Treeview(frame,columns=("UL","Plant","PDF"),show="headings")

tree.heading("UL",text="UL Counter")
tree.heading("Plant",text="Plant")
tree.heading("PDF",text="PDF File")

tree.pack(fill="both",expand=True)

btn = ttk.Button(root,text="Reprint Selected",command=reprint)
btn.pack(pady=5)

observer = start_watcher(INPUT_FOLDER, PDF_FOLDER, add_log)

load_logs()

root.mainloop()

observer.stop()
observer.join()
