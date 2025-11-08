"""
Main.py
-------
FinNLP API — Financial Data and AI Report Generator
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import sqlite3

# ⚠️ Usa SOLO questa import della libreria OpenAI (niente "import openai")
from openai import OpenAI

# ----------------------------------------------------------
# APP & CORS
# ----------------------------------------------------------
app = FastAPI(title="FinNLP API", version="1.1", description="Financial data API + AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # semplifica per la demo (Streamlit localhost)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------
# DB
# ----------------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "Data" / "finllm.db"

def get_transactions(limit=100):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM transactions LIMIT {limit}", conn)
    conn.close()
    return df

# ----------------------------------------------------------
# MODELS
# ----------------------------------------------------------
class ReportRequest(BaseModel):
    limit: int = 200
    api_key: str | None = None

class QuestionRequest(BaseModel):
    question: str
    api_key: str | None = None

# ----------------------------------------------------------
# INSIGHTS (funzione interna + endpoint semplificato)
# ----------------------------------------------------------
def compute_insights():
    df = get_transactions(1000)
    total_income = df[df["amount"] > 0]["amount"].sum()
    total_spent = df[df["amount"] < 0]["amount"].sum()
    avg_expense = df[df["amount"] < 0]["amount"].mean()
    top_category = df["category"].value_counts().idxmax()
    summary = (
        f"Your top spending category is {top_category}. "
        f"You spent an average of {abs(avg_expense):.2f} € per transaction. "
        f"Total spent: {abs(total_spent):.2f} €, total income: {total_income:.2f} €."
    )
    return {
        "total_transactions": int(len(df)),
        "total_income": round(float(total_income), 2),
        "total_spent": round(float(total_spent), 2),
        "average_expense": round(float(avg_expense), 2),
        "top_category": str(top_category),
        "summary": summary
    }

# ----------------------------------------------------------
# ROUTES BASE
# ----------------------------------------------------------
@app.get("/")
def root():
    return {"message": "FinNLP API is running!"}

@app.get("/transactions")
def list_transactions(limit: int = Query(10, ge=1, le=200)):
    df = get_transactions(limit)
    return df.to_dict(orient="records")

@app.get("/transactions/view", response_class=HTMLResponse)
def view_transactions(limit: int = Query(10, ge=1, le=200)):
    df = get_transactions(limit)
    html = df.to_html(index=False)
    return f"<html><body><h2>Transactions (Top {limit})</h2>{html}</body></html>"

@app.get("/transactions/filter")
def filter_transactions(
    category: str | None = Query(None),
    merchant: str | None = Query(None),
    limit: int = Query(50, ge=1, le=500)
):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM transactions WHERE 1=1"
    if category:
        query += f" AND category LIKE '%{category}%'"
    if merchant:
        query += f" AND merchant LIKE '%{merchant}%'"
    query += f" LIMIT {limit}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/insights")
def insights():
    return compute_insights()

# ----------------------------------------------------------
# AI ENDPOINTS (USANO LA CHIAVE INVIATA DAL FRONTEND)
# ----------------------------------------------------------
@app.post("/ai/report")
def ai_report(req: ReportRequest):
    """Generate a natural-language report based on financial insights."""
    if not req.api_key or not req.api_key.startswith("sk-"):
        raise HTTPException(status_code=400, detail="Missing or invalid OpenAI API key in request.")

    df = get_transactions(req.limit)
    stats = compute_insights()

    prompt = (
        "Write a clear, concise financial report based on these stats and transactions.\n"
        f"Stats: {stats}\n"
        f"Transactions (sample): {df.head(10).to_dict(orient='records')}\n"
        "The report should sound like a financial summary, around 150 words."
    )

    try:
        client = OpenAI(api_key=req.api_key)  # ← nessun client globale
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"report": response.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI report generation failed: {e}")

@app.post("/ai/question")
def ai_question(req: QuestionRequest):
    """Answer natural language questions about financial data."""
    if not req.api_key or not req.api_key.startswith("sk-"):
        raise HTTPException(status_code=400, detail="Missing or invalid OpenAI API key in request.")
    if not req.question:
        raise HTTPException(status_code=400, detail="Missing question in request.")

    df = get_transactions(200)
    prompt = (
        f"Based on this transaction dataset: {df.to_dict(orient='records')[:30]},\n"
        f"answer the following question briefly and accurately:\n{req.question}"
    )

    try:
        client = OpenAI(api_key=req.api_key)  # ← nessun client globale
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"answer": response.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI question failed: {e}")
