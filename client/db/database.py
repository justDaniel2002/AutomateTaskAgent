import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "automateTaskAgent.db"
SCHEMA_PATH = Path(__file__).parent / "automateTaskAgent.sql"


def get_db_connection():
    print(f"Database path: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())