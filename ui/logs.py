import tkinter as tk
from tkinter import ttk
from database.db import export_excel

def create_logs(parent):

    logs = ttk.Frame(parent)
    search_frame = ttk.Frame(logs, padding=10)
    search_frame.pack(fill="x", padx=15, pady=10)

    # ==============================
    # EXPORT BUTTONS
    # ==============================

    export_frame = ttk.Frame(logs)
    export_frame.pack(fill="x", padx=15, pady=(0,10))

    btn_24h = ttk.Button(
        export_frame,
        text="Export 24h",
        command=lambda: export_excel("24h")
    )

    btn_week = ttk.Button(
        export_frame,
        text="Export Week",
        command=lambda: export_excel("week")
    )

    btn_month = ttk.Button(
        export_frame,
        text="Export Month",
        command=lambda: export_excel("month")
    )

    btn_full = ttk.Button(
        export_frame,
        text="Export Full",
        command=lambda: export_excel("full")
    )

    btn_24h.pack(side="left", padx=5)
    btn_week.pack(side="left", padx=5)
    btn_month.pack(side="left", padx=5)
    btn_full.pack(side="left", padx=5)


    search_label = ttk.Label(search_frame, text="Search:")
    search_label.pack(side="left")

    search_var = tk.StringVar()

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

    tree.tag_configure("selected_row", background="#dbeafe")

    def on_row_select(event):

        for item in tree.get_children():
            tree.item(item, tags=())

        selected = tree.selection()

        for item in selected:
            tree.item(item, tags=("selected_row",))

    def on_hover(event):

        row = tree.identify_row(event.y)

        if row != tree.focus():
            tree.selection_remove(tree.selection())
            tree.selection_set(row)

    tree.bind("<Motion>", on_hover)

    tree.bind("<<TreeviewSelect>>", on_row_select)

    tree.tag_configure("odd", background="#f7f9fc")
    tree.tag_configure("even", background="#ffffff")

    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Plant", text="Plant")
    tree.heading("UL", text="UL Counter")
    tree.heading("EDI", text="EDI")
    tree.heading("Qty", text="Qty")
    tree.heading("Created", text="Created By")
    tree.heading("Status", text="Status")
    tree.heading("PDF", text="PDF File")
    tree.column("Date", width=90, anchor="center")
    tree.column("Time", width=80, anchor="center")
    tree.column("Plant", width=70, anchor="center")
    tree.column("UL", width=140)
    tree.column("EDI", width=120)
    tree.column("Qty", width=80, anchor="center")
    tree.column("Created", width=110)
    tree.column("Status", width=100)
    tree.column("PDF", width=200)

    tree.pack(fill="both", expand=True)

    scrollbar.config(command=tree.yview)

    def run_search():
        text = search_var.get()
        from database.db import search_logs
        import sqlite3

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        search_logs(tree, cur, text)

        conn.close()

    search_button.config(command=run_search)
    search_entry.bind("<Return>", lambda e: run_search())

    return logs, tree, search_var
