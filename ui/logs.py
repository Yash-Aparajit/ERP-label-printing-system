import tkinter as tk
from tkinter import ttk

def create_logs(parent):

    logs = ttk.Frame(parent)
    search_frame = ttk.Frame(logs)
    search_frame.pack(fill="x", padx=10, pady=5)

    search_label = ttk.Label(search_frame, text="Search:")
    search_label.pack(side="left")

    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.bind("<Return>", lambda e: run_search())
    search_button = ttk.Button(search_frame, text="Search")
    search_button.pack(side="left", padx=5)
    search_entry.pack(side="left", padx=5)

    table_frame = ttk.Frame(logs)
    table_frame.pack(fill="both", expand=True, padx=10)

    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    tree = ttk.Treeview(
        table_frame,
        columns=("Date","Time","Plant","UL","EDI","Qty","Created","Status","PDF"),
        show="headings",
        yscrollcommand=scrollbar.set
    )

    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Plant", text="Plant")
    tree.heading("UL", text="UL Counter")
    tree.heading("EDI", text="EDI")
    tree.heading("Qty", text="Qty")
    tree.heading("Created", text="Created By")
    tree.heading("Status", text="Status")
    tree.heading("PDF", text="PDF File")

    tree.pack(fill="both", expand=True)

    scrollbar.config(command=tree.yview)

    search_var = tk.StringVar()

    def run_search():
        text = search_var.get()
        from database.db import search_logs
        import sqlite3

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        search_logs(tree, cur, text)

        conn.close()

    search_button.config(command=run_search)

    return logs, tree, search_var
