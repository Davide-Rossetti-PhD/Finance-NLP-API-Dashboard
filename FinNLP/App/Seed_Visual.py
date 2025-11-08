"""
seed.py
-------
Reads the synthetic_transactions.csv file
and loads it into a local SQLite database (finllm.db)
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "Data"

# Paths to the CSV and database
CSV_PATH = DATA_DIR / "synthetic_transactions.csv"
DB_PATH = DATA_DIR / "finllm.db"


def seed_database():
    """Load data from CSV into SQLite database."""
    # Check if the CSV file exists
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"❌ CSV file not found: {CSV_PATH}")

    print("📥 Loading CSV data...")
    df = pd.read_csv(CSV_PATH)
    print(f"✅ Loaded {len(df)} transactions.")

    # Ensure the database folder exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect (create DB if missing)
    conn = sqlite3.connect(DB_PATH)

    # Write to a table named 'transactions'
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    conn.close()

    print(f"✅ Database seeded successfully → {DB_PATH}")


def visualize():
    """Display a sample of the CSV data."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"❌ CSV file not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    print("📊 Sample of synthetic transactions:")
    print(df.head(10).to_string(index=False))  # Show first 10 rows neatly


if __name__ == "__main__":
    visualize()
    seed_database()
