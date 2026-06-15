import tkinter as tk
import os
from tkinter import ttk


def create_sidebar(root, show_dashboard, show_logs, show_errors):

    sidebar = ttk.Frame(root, width=230)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # ---------- STYLE ----------
    style = ttk.Style()

    style.configure(
        "Sidebar.TButton",
        font=("Segoe UI", 11),
        anchor="w",
        padding=12
    )

    style.configure(
        "SidebarActive.TButton",
        font=("Segoe UI", 11, "bold"),
        anchor="w",
        padding=12
    )

    style.map(
        "Sidebar.TButton",
        background=[("active", "#e6f0ff")]
    )

    # ---------- LOGO ----------
    logo_frame = ttk.Frame(sidebar)
    logo_frame.pack(fill="x", pady=(20, 10))

    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "assets", "logo.png")

        logo = tk.PhotoImage(file=logo_path)
        logo_label = ttk.Label(logo_frame, image=logo)
        logo_label.image = logo
        logo_label.pack()
    except Exception:
        ttk.Label(
            logo_frame,
            text="COMPANY",
            font=("Segoe UI", 16, "bold")
        ).pack()

    # ---------- NAV TITLE ----------
    ttk.Label(
        sidebar,
        text="Navigation",
        font=("Segoe UI", 11, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))

    # ---------- BUTTONS ----------
    dashboard_btn = ttk.Button(
        sidebar,
        text="📊  Dashboard",
        style="SidebarActive.TButton"
    )

    logs_btn = ttk.Button(
        sidebar,
        text="📄  Logs",
        style="Sidebar.TButton"
    )

    settings_btn = ttk.Button(
        sidebar,
        text="⚙️  Settings",
        style="Sidebar.TButton"
    )

    errors_btn = ttk.Button(
        sidebar,
        text="❌  Errors",
        style="Sidebar.TButton"
    )

    dashboard_btn.pack(fill="x", padx=15, pady=4)
    logs_btn.pack(fill="x", padx=15, pady=4)
    errors_btn.pack(fill="x", padx=15, pady=4)
    settings_btn.pack(fill="x", padx=15, pady=4)

    # ---------- ACTIVE SWITCH ----------
    def activate(btn):

        dashboard_btn.configure(style="Sidebar.TButton")
        logs_btn.configure(style="Sidebar.TButton")
        errors_btn.configure(style="Sidebar.TButton")

        btn.configure(style="SidebarActive.TButton")

    # ---------- COMMANDS ----------
    def dash_cmd():
        activate(dashboard_btn)
        show_dashboard()

    def logs_cmd():
        activate(logs_btn)
        show_logs()

    def errors_cmd():
        activate(errors_btn)
        show_errors()

    dashboard_btn.configure(command=dash_cmd)
    logs_btn.configure(command=logs_cmd)
    errors_btn.configure(command=errors_cmd)

    return sidebar
