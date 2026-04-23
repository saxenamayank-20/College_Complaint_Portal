import sqlite3
import os

DB_FILE = "complaint_portal.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    return conn
