import os
import tkinter as tk
from tkinter import ttk

from database.db import export_excel, search_logs, get_db_path


def create_logs(parent):

    logs = ttk.Frame(parent)

    # ==============================
    # SEARCH BAR
    # ==============================

    search_frame = ttk.Frame(logs, padding=10)
    search_frame.pack(fill="x", padx=15, pady=10)

    search_label = ttk.Label(search_frame, text="Search:")
    search_label.pack(side="left")

    search_var = tk.StringVar()

    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side="left", padx=5)

    search_button = ttk.Button(search_frame, text="Search")
    search_button.pack(side="left", padx=5)

    # ==============================
    # EXPORT BUTTONS
    # ==============================

    export_frame = ttk.Frame(logs)
    export_frame.pack(fill="x", padx=15, pady=(0, 10))

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

    # ==============================
    # TABLE
    # ==============================

    table_frame = ttk.Frame(logs)
    table_frame.pack(fill="both", expand=True, padx=10)

    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    tree = ttk.Treeview(
        table_frame,
        columns=("Date", "Time", "Plant", "UL", "EDI", "Qty", "Created", "Status", "PDF"),
        show="headings",
        yscrollcommand=scrollbar.set
    )

    tree.pack(fill="both", expand=True)

    scrollbar.config(command=tree.yview)

    # ==============================
    # ROW STYLES
    # ==============================

    tree.tag_configure("selected_row", background="#dbeafe")
    tree.tag_configure("odd", background="#f7f9fc")
    tree.tag_configure("even", background="#ffffff")

    # ==============================
    # TABLE HEADERS
    # ==============================

    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Plant", text="Plant")
    tree.heading("UL", text="UL Counter")
    tree.heading("EDI", text="EDI")
    tree.heading("Qty", text="Qty")
    tree.heading("Created", text="Created By")
    tree.heading("Status", text="Status")
    tree.heading("PDF", text="")

    tree.column("Date", width=90, anchor="center")
    tree.column("Time", width=80, anchor="center")
    tree.column("Plant", width=70, anchor="center")
    tree.column("UL", width=140)
    tree.column("EDI", width=120)
    tree.column("Qty", width=80, anchor="center")
    tree.column("Created", width=110)
    tree.column("Status", width=100)
    tree.column("PDF", width=0, stretch=False)

    # ==============================
    # ROW SELECT HIGHLIGHT
    # ==============================

    def on_row_select(event):

        selected = tree.selection()

        for item in tree.get_children():

            tags = list(tree.item(item, "tags"))

            if "selected_row" in tags:
                tags.remove("selected_row")

            tree.item(item, tags=tags)

        for item in selected:

            tags = list(tree.item(item, "tags"))

            if "selected_row" not in tags:
                tags.append("selected_row")

            tree.item(item, tags=tags)

    tree.bind("<<TreeviewSelect>>", on_row_select)

    # ==============================
    # OPEN PDF ON DOUBLE CLICK
    # ==============================

    def open_pdf(event):

        if tree.identify_region(event.x, event.y) != "cell":
            return
        
        selected = tree.selection()

        if not selected:
            return

        item = tree.item(selected[0])

        pdf_path = item["values"][8]

        if os.path.exists(pdf_path):
            os.startfile(pdf_path)

    tree.bind("<Double-1>", open_pdf)

    # ==============================
    # SEARCH FUNCTION
    # ==============================

    def run_search():

        text = search_var.get()

        search_logs(tree, text)

    search_button.config(command=run_search)
    search_entry.bind("<Return>", lambda e: run_search())

    return logs, tree, search_var
