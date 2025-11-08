import os
import subprocess
from pathlib import Path

port = 8000

# Percorso alla cartella corrente (App/)
APP_DIR = Path(__file__).resolve().parent
PYTHON_PATH = "/opt/miniconda3/bin/python"  # il tuo interprete Conda

print(f"🌐 Starting FastAPI server on port {port}...")

# 1️⃣ Libera la porta se è già occupata
result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
if result.stdout.strip():
    pids = result.stdout.strip().split("\n")
    for pid in pids:
        os.system(f"kill -9 {pid}")
    print(f"✅ Freed port {port} (killed process {', '.join(pids)})")
else:
    print(f"ℹ️  Port {port} was already free.")

# 2️⃣ Avvia uvicorn nella stessa cartella del file
try:
    subprocess.run(
        [PYTHON_PATH, "-m", "uvicorn", "Main:app", "--reload", "--port", str(port)],
        cwd=APP_DIR,  # 👈 Esegui uvicorn dentro App/
        check=True
    )
except KeyboardInterrupt:
    print("\n🛑 Server stopped manually.")
except Exception as e:
    print(f"❌ Failed to start server: {e}")
