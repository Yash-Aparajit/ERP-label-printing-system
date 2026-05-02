import sqlite3
from datetime import datetime
import pandas as pd
import os

def init_db():

    conn = sqlite3.connect("database.db", check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS labels(
    id INTEGER PRIMARY KEY,
    date TEXT,
    time TEXT,
    plant TEXT,
    ul TEXT,
    edi TEXT,
    qty TEXT,
    created_by TEXT,
    status TEXT,
    pdf TEXT
    )
    """)

    conn.commit()

    return conn, cur


def add_log(ul, plant, edi, qty, created_by, status, pdf):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    now_time = datetime.now().strftime("%H:%M:%S")
    now_date = datetime.now().strftime("%d/%m/%Y")

    cur.execute(
        """INSERT INTO labels(date,time,plant,ul,edi,qty,created_by,status,pdf)
        VALUES(?,?,?,?,?,?,?,?,?)""",
        (now_date, now_time, plant, ul, edi, qty, created_by, status, pdf)
    )

    conn.commit()
    conn.close()


def load_logs(tree, cur):

    for i in tree.get_children():
        tree.delete(i)

    for row in cur.execute(
        "SELECT date,time,plant,ul,edi,qty,created_by,status,pdf FROM labels ORDER BY id DESC"
    ):
        tree.insert("", "end", values=row)


def search_logs(tree, cur, text):

    for i in tree.get_children():
        tree.delete(i)

    query = "SELECT ul,plant,pdf,time FROM labels ORDER BY id DESC"

    for row in cur.execute(query):

        if text.lower() in row[0].lower():
            tree.insert("", "end", values=row)


def export_excel():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    rows = list(cur.execute(
        "SELECT date,time,plant,ul,edi,qty,created_by,status,pdf FROM labels"
    ))

    if not rows:
        return

    df = pd.DataFrame(rows, columns=["Date","Time","Plant","UL Counter","EDI","Qty","Created By","Status","PDF"])

    filename = f"label_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    df.to_excel(filename, index=False)
    os.startfile(filename)
