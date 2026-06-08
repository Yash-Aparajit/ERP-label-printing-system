import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import os


# ==============================
# DATABASE FOLDER
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FOLDER = os.path.join(BASE_DIR, "data")

os.makedirs(DB_FOLDER, exist_ok=True)


# ==============================
# GET CURRENT DB FILE
# ==============================

def get_db_path():

    year = datetime.now().year

    return os.path.join(DB_FOLDER, f"labels_{year}.db")


# ==============================
# INIT DATABASE
# ==============================

def init_db():

    db_path = get_db_path()

    conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = conn.cursor()

    ensure_schema(cur)

    conn.commit()

    return conn, cur


def ensure_schema(cur):

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


# ==============================
# ADD LOG
# ==============================

def add_log(ul, plant, edi, qty, created_by, status, pdf):

    db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    ensure_schema(cur)

    now = datetime.now()

    now_time = now.strftime("%H:%M:%S")
    now_date = now.strftime("%d/%m/%Y")

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


# ==============================
# LOAD LOGS (CURRENT YEAR)
# ==============================

def load_logs(tree, cur):

    for i in tree.get_children():
        tree.delete(i)

    for row in cur.execute(
        "SELECT date,time,plant,ul,edi,qty,created_by,status,pdf FROM labels ORDER BY id DESC"
    ):

        index = len(tree.get_children())

        tag = "even" if index % 2 == 0 else "odd"

        tree.insert("", "end", values=row, tags=(tag,))


# ==============================
# SEARCH LOGS
# ==============================

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


# ==============================
# GET ALL DATABASE FILES
# ==============================

def get_all_databases():

    dbs = []

    for file in os.listdir(DB_FOLDER):

        if file.endswith(".db"):
            dbs.append(os.path.join(DB_FOLDER, file))

    return sorted(dbs)


# ==============================
# EXPORT LOGS
# ==============================

def export_excel(mode="full"):

    rows = []

    now = datetime.now()

    if mode == "24h":
        cutoff = now - timedelta(hours=24)

    elif mode == "week":
        cutoff = now - timedelta(days=7)

    elif mode == "month":
        cutoff = now - timedelta(days=30)

    else:
        cutoff = None

    for db in get_all_databases():

        conn = sqlite3.connect(db)
        cur = conn.cursor()

        try:
            data = cur.execute(
                "SELECT date,time,plant,ul,edi,qty,created_by,status,pdf FROM labels"
            ).fetchall()
        except sqlite3.OperationalError:
            conn.close()
            continue

        conn.close()

        for r in data:

            dt = datetime.strptime(f"{r[0]} {r[1]}", "%d/%m/%Y %H:%M:%S")

            if cutoff and dt < cutoff:
                continue

            rows.append(r)

    if not rows:
        return

    df = pd.DataFrame(
        rows,
        columns=[
            "Date", "Time", "Plant", "UL Counter",
            "EDI", "Qty", "Created By", "Status", "PDF"
        ]
    )

    filename = f"label_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    df.to_excel(filename, index=False)

    os.startfile(filename)


# ==============================
# DASHBOARD STATS
# ==============================

def dashboard_stats():

    db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

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
