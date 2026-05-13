import tkinter as tk
from tkinter import ttk


def create_sidebar(root, show_dashboard, show_logs):

    sidebar = ttk.Frame(root, width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # ---------- LOGO ----------
    logo_frame = ttk.Frame(sidebar)
    logo_frame.pack(fill="x", pady=(20,10))

    try:
        logo = tk.PhotoImage(file="assets/logo.png")
        logo_label = ttk.Label(logo_frame, image=logo)
        logo_label.image = logo
        logo_label.pack()
    except:
        ttk.Label(
            logo_frame,
            text="COMPANY",
            font=("Segoe UI",16,"bold")
        ).pack()

    # ---------- NAV TITLE ----------
    ttk.Label(
        sidebar,
        text="Navigation",
        font=("Segoe UI",11,"bold")
    ).pack(anchor="w", padx=20, pady=(10,10))

    # ---------- BUTTON STYLE ----------
    style = ttk.Style()

    style.configure(
        "Sidebar.TButton",
        font=("Segoe UI",11),
        anchor="w",
        padding=10
    )

    style.map(
        "Sidebar.TButton",
        background=[("active","#e8f0fe")]
    )

    style.configure(
        "SidebarActive.TButton",
        font=("Segoe UI",11,"bold"),
        anchor="w",
        padding=10,
        background="#d2e3fc"
    )

    # ---------- BUTTONS ----------
    dashboard_btn = ttk.Button(
        sidebar,
        text="  Dashboard",
        style="SidebarActive.TButton"
    )

    logs_btn = ttk.Button(
        sidebar,
        text="  Logs",
        style="Sidebar.TButton"
    )

    settings_btn = ttk.Button(
        sidebar,
        text="  Settings",
        style="Sidebar.TButton"
    )

    dashboard_btn.pack(fill="x", padx=15, pady=3)
    logs_btn.pack(fill="x", padx=15, pady=3)
    settings_btn.pack(fill="x", padx=15, pady=3)

    # ---------- ACTIVE STATE ----------
    def activate(btn):

        dashboard_btn.configure(style="Sidebar.TButton")
        logs_btn.configure(style="Sidebar.TButton")

        btn.configure(style="SidebarActive.TButton")

    # ---------- COMMANDS ----------
    def dash_cmd():
        activate(dashboard_btn)
        show_dashboard()

    def logs_cmd():
        activate(logs_btn)
        show_logs()

    dashboard_btn.configure(command=dash_cmd)
    logs_btn.configure(command=logs_cmd)

    return sidebar
