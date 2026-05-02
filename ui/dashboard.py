from tkinter import ttk

def create_dashboard(parent):

    dashboard = ttk.Frame(parent)

    status_frame = ttk.LabelFrame(dashboard, text="System Status")
    status_frame.pack(fill="x", padx=20, pady=20)

    count_label = ttk.Label(status_frame, text="Labels Generated: 0", font=("Segoe UI",16,"bold"))
    count_label.pack(anchor="w", padx=10, pady=5)

    last_label = ttk.Label(status_frame, text="Last Label: -", font=("Segoe UI",14))
    last_label.pack(anchor="w", padx=10, pady=5)

    return dashboard, count_label, last_label

