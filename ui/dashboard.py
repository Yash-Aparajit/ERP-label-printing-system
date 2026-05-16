from tkinter import ttk


def create_dashboard(parent):

    dashboard = ttk.Frame(parent)

    container = ttk.Frame(dashboard)
    container.pack(fill="both", expand=True, padx=40, pady=40)

    style = ttk.Style()

    style.configure(
        "Card.TFrame",
        background="#ffffff",
        relief="flat"
    )

    style.configure(
        "CardTitle.TLabel",
        font=("Segoe UI",12)
    )

    style.configure(
        "CardValue.TLabel",
        font=("Segoe UI",38,"bold"),
        foreground="#0d6efd"
    )

    # ---------- CARD GRID ----------
    card1 = ttk.Frame(container, style="Card.TFrame", padding=25)
    card1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

    ttk.Label(
        card1,
        text="Labels Today",
        style="CardTitle.TLabel"
    ).pack(anchor="w")

    count_label = ttk.Label(
        card1,
        text="0",
        style="CardValue.TLabel"
    )
    count_label.pack(anchor="w", pady=10)

    card2 = ttk.Frame(container, style="Card.TFrame", padding=25)
    card2.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

    ttk.Label(
        card2,
        text="Last UL Processed",
        style="CardTitle.TLabel"
    ).pack(anchor="w")

    last_label = ttk.Label(
        card2,
        text="-",
        font=("Segoe UI",20,"bold")
    )
    last_label.pack(anchor="w", pady=10)

    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)

    return dashboard, count_label, last_label
