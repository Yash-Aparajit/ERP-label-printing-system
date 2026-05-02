from tkinter import ttk

def create_sidebar(root):

    sidebar = ttk.Frame(root, width=200)
    sidebar.pack(side="left", fill="y")

    ttk.Label(sidebar, text="Navigation", font=("Segoe UI",12,"bold")).pack(pady=10)

    ttk.Button(sidebar, text="Dashboard").pack(fill="x", padx=10, pady=5)
    ttk.Button(sidebar, text="Logs").pack(fill="x", padx=10, pady=5)
    ttk.Button(sidebar, text="Settings").pack(fill="x", padx=10, pady=5)

    return sidebar
