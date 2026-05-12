from tkinter import ttk

def create_dashboard(parent):

    dashboard = ttk.Frame(parent)

    status_frame = ttk.LabelFrame(dashboard, text="System Status")
    today_title = ttk.Label(
        status_frame,
        text="Labels Today",
        font=("Segoe UI",14)
    )
    today_title.pack(anchor="w", padx=10)

    status_frame.pack(fill="x", padx=20, pady=20)

    count_label = ttk.Label(
        status_frame,
        text="0",
        font=("Segoe UI",40,"bold"),
        foreground="#0078D7"
    )
    count_label.pack(anchor="w", padx=10, pady=5)

    last_title = ttk.Label(
        status_frame,
        text="Last UL Processed",
        font=("Segoe UI",14)
    )
    last_title.pack(anchor="w", padx=10, pady=(10,0))

    last_label = ttk.Label(
        status_frame,
        text="-",
        font=("Segoe UI",24,"bold")
    )
    last_label.pack(anchor="w", padx=10, pady=5)

    return dashboard, count_label, last_label
