import tkinter as tk
from tkinter import ttk
import sqlite3
import os
from watcher import start_watcher

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

    tree.yview_moveto(1)


def reprint():

    item = tree.selection()

    if not item:
        return

    values = tree.item(item)["values"]

    pdf_path = os.path.abspath(values[2])

    if os.path.exists(pdf_path):
        os.startfile(pdf_path)


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
