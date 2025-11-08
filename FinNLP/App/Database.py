"""
database.py
-----------
Creates and manages a connection to the local SQLite database.
Used by all API endpoints that read or write transaction data.
"""

import sqlite3
from pathlib import Path

# Path to the local SQLite database
DB_PATH = Path("../Data/finllm.db")

def get_connection():
    """
    Opens a connection to the SQLite database (creates the file if it doesn’t exist).
    Returns:
        sqlite3.Connection: an active connection object
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows returning dict-like rows, how to give back data
    return conn
print("fatto")