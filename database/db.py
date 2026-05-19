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
    ul TEXT UNIQUE,
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

    try:

        cur.execute(
            """INSERT INTO labels(date,time,plant,ul,edi,qty,created_by,status,pdf)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (now_date, now_time, plant, ul, edi, qty, created_by, status, pdf)
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()

        return False


def load_logs(tree, cur):

    for i in tree.get_children():
        tree.delete(i)

    for row in cur.execute(
        "SELECT date,time,plant,ul,edi,qty,created_by,status,pdf FROM labels ORDER BY id DESC"
    ):
        index = len(tree.get_children())

        tag = "even" if index % 2 == 0 else "odd"

        tree.insert("", "end", values=row, tags=(tag,))


def search_logs(tree, cur, text):

    for i in tree.get_children():
        tree.delete(i)

    query = """
    SELECT date,time,plant,ul,edi,qty,created_by,status,pdf
    FROM labels
    WHERE
        ul LIKE ?
        OR plant LIKE ?
        OR edi LIKE ?
        OR date LIKE ?
    ORDER BY id DESC
    """

    rows = cur.execute(
        query,
        (f"%{text}%", f"%{text}%", f"%{text}%", f"%{text}%")
    )

    for row in rows:
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

def dashboard_stats():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    from datetime import datetime
    today = datetime.now().strftime("%d/%m/%Y")

    count = cur.execute(
        "SELECT COUNT(*) FROM labels WHERE date=?",
        (today,)
    ).fetchone()[0]

    last = cur.execute(
        "SELECT ul FROM labels ORDER BY id DESC LIMIT 1"
    ).fetchone()

    conn.close()

    last_ul = last[0] if last else "-"

    return count, last_ul
