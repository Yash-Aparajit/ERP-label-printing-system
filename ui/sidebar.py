from tkinter import ttk

def create_sidebar(root, show_dashboard, show_logs):

    sidebar = ttk.Frame(root, width=200)
    sidebar.pack(side="left", fill="y")

    ttk.Label(sidebar, text="Navigation", font=("Segoe UI",12,"bold")).pack(pady=10)

    dashboard_btn = ttk.Button(sidebar, text="Dashboard")
    dashboard_btn.pack(fill="x", padx=10, pady=5)

    logs_btn = ttk.Button(sidebar, text="Logs")
    logs_btn.pack(fill="x", padx=10, pady=5)
    ttk.Button(sidebar, text="Settings").pack(fill="x", padx=10, pady=5)

    dashboard_btn.config(command=show_dashboard)
    logs_btn.config(command=show_logs)

    return sidebar
