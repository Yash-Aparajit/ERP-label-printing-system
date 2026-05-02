from tkinter import ttk

def create_logs(parent):

    logs = ttk.Frame(parent)

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

    search_var = None
    return logs, tree, search_var
