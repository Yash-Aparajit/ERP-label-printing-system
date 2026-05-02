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
    ul TEXT,
    plant TEXT,
    pdf TEXT,
    time TEXT
    )
    """)

    conn.commit()

    return conn, cur


def add_log(ul, plant, pdf):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    now = datetime.now().strftime("%H:%M:%S")

    cur.execute(
        "INSERT INTO labels(ul,plant,pdf,time) VALUES(?,?,?,?)",
        (ul, plant, pdf, now)
    )

    conn.commit()
    conn.close()


def load_logs(tree, cur):

    for i in tree.get_children():
        tree.delete(i)

    for row in cur.execute("SELECT ul,plant,pdf,time FROM labels ORDER BY id DESC"):
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

    rows = list(cur.execute("SELECT ul,plant,pdf,time FROM labels"))

    if not rows:
        return

    df = pd.DataFrame(rows, columns=["UL Counter", "Plant", "PDF File", "Time"])

    filename = f"label_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    df.to_excel(filename, index=False)

    os.startfile(filename)
