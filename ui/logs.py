from tkinter import ttk

def create_logs(parent):

    logs = ttk.Frame(parent)

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

    search_var = None

    return logs, tree, search_var
