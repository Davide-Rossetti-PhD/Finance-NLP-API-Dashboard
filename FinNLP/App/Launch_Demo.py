"""
launch_app.py
-------------
FinNLP Demo Launcher
Runs the entire FinNLP project in one command.
"""

import os
import time
import subprocess
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR
DATA_DIR = BASE_DIR.parent / "Data"

print("🚀 FinNLP DEMO LAUNCHER")
print("------------------------")

# Step 1 — Generate synthetic transactions if not present
csv_path = DATA_DIR / "synthetic_transactions.csv"
print(csv_path)
if not csv_path.exists():
    print("📄 Generating synthetic dataset...")
    subprocess.run(["python", "Dataset_Generator.py"], cwd=APP_DIR)
else:
    print("✅ Synthetic dataset already exists.")

# Step 2 — Build / seed database
db_path = DATA_DIR / "finllm.db"
if not db_path.exists():
    print("🧱 Building SQLite database...")
    subprocess.run(["python", "Database.py"], cwd=APP_DIR)
else:
    print("✅ Database already exists.")

# Step 3 — Optional visualization
print("👁️  Visualizing dataset")
time.sleep(1)
try:
    subprocess.run(["python", "Seed_Visual.py"], cwd=APP_DIR)
except Exception:
    print("⚠️ Visualization skipped (optional).")


# Step 4 — Start API server
print("🌐 Starting FastAPI backend...")
api_process = subprocess.Popen(["python", "Run_Server.py"], cwd=APP_DIR)

# Step 5 — Wait a few seconds for server to be ready
print("⌛ Waiting for API to initialize...")
time.sleep(3)

# Step 6 — Start Streamlit dashboard
print("📊 Launching Streamlit dashboard...")
try:
    subprocess.run(["streamlit", "run", "Dashboard.py"], cwd=APP_DIR)
except KeyboardInterrupt:
    print("🛑 Shutting down demo...")
finally:
    api_process.terminate()
    print("✅ Demo stopped cleanly.")