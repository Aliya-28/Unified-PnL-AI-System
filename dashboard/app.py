import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

from charts import (
    revenue_expense_chart,
    profit_trend_chart,
    department_performance_chart,
    anomaly_chart
)

from agents.recommendation_agent import generate_recommendations
from backend.report_generator import generate_report


st.set_page_config(page_title="Unified P&L AI System", layout="wide")


# -----------------------
# CSS (UI IMPROVEMENT)
# -----------------------
st.markdown("""
<style>
.metric-card {
    background: #1C1F26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
}
.metric-title {
    font-size: 14px;
    color: #aaa;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
}
.green { color: #00FF9C; }
.red { color: #FF4B4B; }
</style>
""", unsafe_allow_html=True)


def metric_card(title, value, subtitle, color):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="{color}">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------
# ASK AI
# -----------------------
def answer_query(q, df):
    q = q.lower()

    if "revenue" in q:
        return f"₹ {df['revenue'].sum():,.0f}"
    elif "expense" in q:
        return f"₹ {df['expense'].sum():,.0f}"
    elif "profit" in q:
        return f"₹ {df['profit'].sum():,.0f}"
    else:
        return "Try asking revenue, expense or profit."


# -----------------------
# CLEAN DATA
# -----------------------
def clean_dataset(df):
    df.columns = [c.lower() for c in df.columns]

    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["date"])

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["expense"] = pd.to_numeric(df["expense"], errors="coerce")

    df = df.dropna(subset=["revenue", "expense"])

    df["department"] = df["department"].astype(str).str.strip().str.title()

    return df


# -----------------------
# LOGIN
# -----------------------
def login():
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "admin123":
            st.session_state["login"] = True
            st.session_state["page"] = "upload"
        else:
            st.error("Invalid credentials")


# -----------------------
# UPLOAD
# -----------------------
def upload_page():
    st.title("📂 Upload Dataset")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        df = clean_dataset(df)

        st.session_state["data"] = df

        st.success("✅ Data uploaded")

        if st.button("Go to Dashboard"):
            st.session_state["page"] = "dashboard"


# -----------------------
# DASHBOARD
# -----------------------
def dashboard():

    df = st.session_state["data"]
    df["profit"] = df["revenue"] - df["expense"]

    # Sidebar
    st.sidebar.markdown("## 📊 P&L AI System")

    page = st.sidebar.radio(
        "Navigate",
        ["📊 Dashboard", "🏢 Department Analysis", "🚨 Anomaly Detection", "📂 Dataset"]
    )

    # -----------------------
    # MAIN DASHBOARD
    # -----------------------
    if page == "📊 Dashboard":

        # HEADER (LIKE IMAGE)
        st.markdown("## 💼 Unified P&L AI System")
        st.caption("AI-driven Financial Intelligence Platform")

        tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Trends", "🧠 Insights"])

        # -----------------------
        # OVERVIEW
        # -----------------------
        with tab1:

            st.markdown("### 📊 Financial Overview")
            st.markdown("#### 💰 Key Metrics")

            col1, col2, col3 = st.columns(3)

            with col1:
                metric_card("💰 Total Revenue", f"₹ {df['revenue'].sum():,.0f}", "Total inflow", "green")

            with col2:
                metric_card("📉 Total Expense", f"₹ {df['expense'].sum():,.0f}", "Total outflow", "red")

            with col3:
                metric_card("📈 Total Profit", f"₹ {df['profit'].sum():,.0f}", "Net gain", "green")

            # REPORT BUTTON (UI ONLY)
            st.markdown("### 📥 Download AI Financial Report")
            st.button("📄 Download Report")

            # ASK AI SECTION
            st.markdown("## 🤖 Ask AI About Financial Data")

            q = st.text_input("Ask a question")

            if q:
                st.success(answer_query(q, df))

        # -----------------------
        # TRENDS
        # -----------------------
        with tab2:

            df["date"] = pd.to_datetime(df["date"])

            start, end = st.date_input(
                "📅 Date Range",
                (df["date"].min().date(), df["date"].max().date())
            )

            filtered = df[
                (df["date"] >= pd.to_datetime(start)) &
                (df["date"] <= pd.to_datetime(end))
            ]

            freq = st.selectbox(
                "📊 Aggregation",
                ["Daily", "Weekly", "Monthly", "Quarterly", "Half-Yearly", "Yearly"]
            )

            st.markdown("### 📈 Revenue vs Expense Trend")
            st.plotly_chart(revenue_expense_chart(filtered, freq), use_container_width=True)

            st.markdown("### 📊 Profit Trend Over Time")
            st.plotly_chart(profit_trend_chart(filtered, freq), use_container_width=True)

        # -----------------------
        # INSIGHTS
        # -----------------------
        with tab3:

            st.markdown("### 🧠 AI Insights")

            recs = generate_recommendations(df)

            for r in recs:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(90deg, #00c2ff, #007bff);
                    padding: 15px;
                    border-radius: 12px;
                    margin-bottom: 10px;
                    color: white;
                    font-size: 16px;
                    font-weight: 500;
                ">
                {r}
                </div>
                """, unsafe_allow_html=True)

    elif page == "🏢 Department Analysis":
        st.markdown("## 🏢 Department Performance")
        st.plotly_chart(department_performance_chart(df), use_container_width=True)

    elif page == "🚨 Anomaly Detection":
        st.markdown("## 🚨 Anomaly Detection")

        model = IsolationForest(contamination=0.05)
        df["anomaly"] = model.fit_predict(df[["revenue", "expense"]])

        st.plotly_chart(anomaly_chart(df), use_container_width=True)

    else:
        st.markdown("## 📂 Dataset Overview")
        st.dataframe(df)


# -----------------------
# RUN
# -----------------------
if "login" not in st.session_state:
    st.session_state["login"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "upload"

if not st.session_state["login"]:
    login()
else:
    if st.session_state["page"] == "upload":
        upload_page()
    else:
        dashboard()