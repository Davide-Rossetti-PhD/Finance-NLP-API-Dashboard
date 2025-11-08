# 💸 FinNLP — AI-Powered Financial Data API and Dashboard

**FinNLP** is a full-stack finance project powered by **FastAPI**, **Streamlit**, **SQLite**, and **OpenAI GPT**.  
It generates synthetic financial data, provides smart visual analytics, and creates **AI-written financial reports** and **natural language Q&A**.

> 🚀 Built for personal projects, AI financial dashboards, and API Hackaton.  
> Everything runs automatically with **one single command**.

---

## 🧩 Features

✅ Synthetic dataset generation with Faker  
✅ SQLite database for fast querying  
✅ REST API with FastAPI  
✅ Interactive Streamlit dashboard  
✅ AI-generated financial reports  
✅ Natural language Q&A assistant  
✅ PDF export and HTML visualization  
✅ One-click launcher script

---

## 🧠 Tech Stack

- **Python 3.10+**
- **FastAPI** — backend REST API  
- **SQLite + Pandas** — data management  
- **Streamlit** — web dashboard  
- **OpenAI GPT-4o-mini** — NLP and report generation  
- **Matplotlib** — charts and insights  
- **ReportLab** — export to PDF  

---

## ⚙️ Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/Davide-Rossetti-PhD/Finance-NLP-API-Dashboard
.git
cd FinNLP/App
pip install -r requirements.txt
```

---

## 🧱 Components Overview

| Component              | Description                                         |
| ---------------------- | --------------------------------------------------- |
| `Dataset_Generator.py` | Generates synthetic financial transactions          |
| `Database.py`          | Creates the SQLite database from the dataset        |
| `Seed_Visual.py`       | Displays dataset previews and quick summaries       |
| `Main.py`              | Defines all FastAPI endpoints and AI logic          |
| `Run_Server.py`        | Starts the backend API server                       |
| `Dashboard.py`     | Streamlit web dashboard for insights & AI           |
| `Launch_Demo.py`        | One-click script that runs everything automatically |


---

## 🔑 OpenAI API Key

Paste your key there — no terminal or system setup required.
You can create your API key here:
👉 https://platform.openai.com/api-keys
If no key is inserted, FinNLP works in demo mode, generating example AI responses.

---

## 🧰 API Endpoints

| Endpoint               | Method | Description                              |
| ---------------------- | ------ | ---------------------------------------- |
| `/`                    | GET    | API status check                         |
| `/transactions`        | GET    | Returns all transactions (JSON)          |
| `/transactions/view`   | GET    | Returns transactions as HTML table       |
| `/transactions/filter` | GET    | Filter by category or merchant           |
| `/insights`            | GET    | Financial summary metrics                |
| `/ai/report`           | POST   | Generates an AI-written financial report |
| `/ai/question`         | POST   | Answers natural-language questions       |

---

## 💻 Dashboard Sections

| Section             | Description                                       |
| ------------------- | ------------------------------------------------- |
| 🏠 **Home**         | API connection test and project overview          |
| 📜 **Transactions** | Displays transaction data with charts             |
| 🔍 **Filter**       | Filter transactions by merchant or category       |
| 📈 **Insights**     | View financial KPIs, totals, and bar charts       |
| 🤖 **AI Report**    | Generate AI-written summaries and export PDF      |
| 💬 **AI Q&A**       | Ask AI natural language questions about your data |

---

## 📦 Folder Structure

```bash
FinNLP/
├── App/
│   ├── Launch_Demo.py
│   ├── Run_Server.py
│   ├── Main.py
│   ├── Dashboard.py
│   ├── Dataset_Generator.py
│   ├── Database.py
│   ├── Seed_Visual.py
│   └── requirements.txt
└── Data/
    ├── synthetic_transactions.csv
    └── finllm.db
