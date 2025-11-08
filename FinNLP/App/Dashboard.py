"""
dashboard_app.py
----------------
FinNLP Dashboard 3.0 — Functional Version
Integrates with FastAPI backend for:
- Viewing and filtering transactions
- Insights visualization
- AI-generated report
- AI-powered Q&A
"""

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# -----------------------------------------------------------
# CONFIG
# -----------------------------------------------------------
BASE_URL = "http://127.0.0.1:8000"  # FastAPI deve essere avviato prima
st.set_page_config(page_title="FinNLP AI Dashboard", layout="wide", page_icon="💸")

# -----------------------------------------------------------
# SIDEBAR — SETTINGS
# -----------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    api_key_input = st.text_input("🔑 Enter your OpenAI API Key:", type="password")

    if api_key_input:
        st.session_state["OPENAI_API_KEY"] = api_key_input
        st.success("✅ API key saved for this session!")
    elif "OPENAI_API_KEY" in st.session_state:
        st.info("Using previously saved API key.")
    else:
        st.warning("⚠️ No API key set. AI features will be disabled.")

    selected = option_menu(
        menu_title="💸 FinNLP Dashboard",
        options=["Home", "Transactions", "Filter", "Insights", "AI Report", "AI Q&A"],
        icons=["house", "table", "funnel", "bar-chart-line", "file-text", "robot"],
        menu_icon="cast",
        default_index=0,
    )

# -----------------------------------------------------------
# HELPER — GET DATA
# -----------------------------------------------------------
def fetch_json(endpoint: str):
    """Fetch data from FastAPI backend and return DataFrame"""
    try:
        r = requests.get(f"{BASE_URL}/{endpoint}")
        if r.status_code == 200:
            return pd.DataFrame(r.json())
        else:
            st.error(f"❌ API returned {r.status_code}")
    except Exception as e:
        st.error(f"⚠️ Could not reach API server: {e}")
    return pd.DataFrame()

# -----------------------------------------------------------
# HOME
# -----------------------------------------------------------
if selected == "Home":
    st.title("💸 FinNLP — AI Financial Assistant")
    st.markdown("""
    Welcome to **FinNLP**, a Generative AI-powered dashboard for financial data.

    **Features:**
    - 🧾 View & filter transactions  
    - 📈 Generate automatic insights  
    - 🤖 Create AI-written financial reports  
    - 💬 Ask AI natural-language questions about your data
    """)

    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200:
            st.success("✅ API connected successfully!")
        else:
            st.warning("⚠️ API reachable but returned an error.")
    except Exception:
        st.error("❌ API not reachable. Please run `python Run_Server.py` first.")

# -----------------------------------------------------------
# TRANSACTIONS
# -----------------------------------------------------------
elif selected == "Transactions":
    st.header("📜 Transactions Viewer")

    limit = st.slider("How many transactions to display?", 5, 200, 20)
    df = fetch_json(f"transactions?limit={limit}")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.subheader("💰 Transaction Distribution")
        fig, ax = plt.subplots()
        df["amount"].plot(kind="hist", bins=30, ax=ax, color="#3498db", alpha=0.7)
        ax.set_xlabel("Amount (€)")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.info("No data available.")

# -----------------------------------------------------------
# FILTER
# -----------------------------------------------------------
elif selected == "Filter":
    st.header("🔍 Filter Transactions")

    category = st.text_input("Filter by category (optional):", placeholder="e.g. Food, Transport")
    merchant = st.text_input("Filter by merchant (optional):", placeholder="e.g. Uber, Starbucks")
    limit = st.slider("Results:", 5, 100, 20)

    if st.button("Apply Filter"):
        params = []
        if category:
            params.append(f"category={category}")
        if merchant:
            params.append(f"merchant={merchant}")
        query = "&".join(params)
        df = fetch_json(f"transactions/filter?{query}&limit={limit}")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No transactions match your filter.")

# -----------------------------------------------------------
# INSIGHTS
# -----------------------------------------------------------
elif selected == "Insights":
    st.header("📈 Financial Insights")

    try:
        r = requests.get(f"{BASE_URL}/insights")
        if r.status_code == 200:
            data = r.json()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Transactions", data["total_transactions"])
            col2.metric("Top Category", data["top_category"])
            col3.metric("Total Spent (€)", abs(data["total_spent"]))
            col4.metric("Total Income (€)", data["total_income"])

            st.markdown(f"**Average Expense:** {abs(data['average_expense']):.2f} €")
            summary = data["summary"].replace(". ", ".<br>")
            st.markdown(f"<div style='line-height:1.6; font-size:16px;'>{summary}</div>", unsafe_allow_html=True)

            # Chart
            st.subheader("💶 Total Income vs Expenses")
            fig, ax = plt.subplots()
            ax.bar(["Income", "Expenses"],
                   [data["total_income"], abs(data["total_spent"])],
                   color=["#2ecc71", "#e74c3c"])
            ax.set_ylabel("€ Amount")
            st.pyplot(fig)
        else:
            st.error("❌ Could not fetch insights.")
    except Exception as e:
        st.error(f"⚠️ Could not fetch insights: {e}")

# -----------------------------------------------------------
# AI REPORT
# -----------------------------------------------------------
elif selected == "AI Report":
    st.header("🤖 Generate AI Financial Report")

    api_key = st.session_state.get("OPENAI_API_KEY")
    limit = st.slider("Transactions analyzed:", 50, 500, 200)

    if st.button("Generate Report"):
        if not api_key:
            st.error("⚠️ Please enter your OpenAI API key in the sidebar first.")
        else:
            with st.spinner("Generating AI report..."):
                try:
                    r = requests.post(f"{BASE_URL}/ai/report", json={"limit": limit, "api_key": api_key})
                    if r.status_code != 200:
                        st.error(f"❌ Backend error ({r.status_code}): {r.text}")
                    else:
                        data = r.json()
                        report = data.get("report")
                        if not report:
                            st.error(data.get("error", "No report returned."))
                        else:
                            st.success("✅ Report generated successfully!")
                            st.text_area("AI Financial Report", report, height=250)

                            # Export as PDF
                            if st.button("📄 Download Report as PDF"):
                                buffer = BytesIO()
                                pdf = canvas.Canvas(buffer, pagesize=A4)
                                pdf.setFont("Helvetica", 12)
                                pdf.drawString(50, 800, "FinNLP AI Financial Report")
                                y = 780
                                for line in report.split("\n"):
                                    pdf.drawString(50, y, line[:100])
                                    y -= 14
                                    if y < 50:
                                        pdf.showPage()
                                        pdf.setFont("Helvetica", 12)
                                        y = 780
                                pdf.save()
                                buffer.seek(0)
                                st.download_button("Download PDF", buffer,
                                                   file_name="FinNLP_Report.pdf",
                                                   mime="application/pdf")
                except Exception as e:
                    st.error(f"AI report generation failed: {e}")

# -----------------------------------------------------------
# AI Q&A
# -----------------------------------------------------------
elif selected == "AI Q&A":
    st.header("💬 Ask AI about your financial data")

    api_key = st.session_state.get("OPENAI_API_KEY")
    user_q = st.text_input("Enter your question:", placeholder="e.g. How much did I spend on Food?")

    if st.button("Ask AI"):
        if not api_key:
            st.error("⚠️ Please enter your OpenAI API key in the sidebar first.")
        elif not user_q:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    r = requests.post(f"{BASE_URL}/ai/question", json={"question": user_q, "api_key": api_key})
                    if r.status_code != 200:
                        st.error(f"❌ Backend error ({r.status_code}): {r.text}")
                    else:
                        data = r.json()
                        answer = data.get("answer")
                        if not answer:
                            st.warning(data.get("error", "No answer returned."))
                        else:
                            st.markdown("### 🧠 AI Answer:")
                            st.write(answer)
                except Exception as e:
                    st.error(f"AI Q&A failed: {e}")
