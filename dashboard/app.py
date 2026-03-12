import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from agents.recommendation_agent import generate_recommendations
from sklearn.ensemble import IsolationForest
from backend.report_generator import generate_report
from charts import revenue_expense_chart
from charts import department_performance_chart
from charts import profit_trend_chart
from charts import anomaly_chart


# -----------------------
# PAGE CONFIG
# -----------------------

st.set_page_config(page_title="Unified P&L AI System", layout="wide")


# -----------------------
# LOGIN FUNCTION
# -----------------------

def login():

    st.title("Unified P&L AI System Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state["login"] = True
            st.success("Login Successful")
        else:
            st.error("Invalid Credentials")


# -----------------------
# DASHBOARD FUNCTION
# -----------------------

def dashboard():

    # Sidebar
    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Go to",
        [
            "Dashboard",
            "Department Analysis",
            "Anomaly Detection",
            "Dataset"
        ]
    )

    # Load dataset
    df = pd.read_csv("data/financial_data.csv")

    df["profit"] = df["revenue"] - df["expense"]

    # -----------------------
    # MAIN DASHBOARD
    # -----------------------
    if page == "Dashboard":

        st.title("Financial Overview")
    #KPI cards
        col1, col2, col3 = st.columns(3)

        total_revenue = df["revenue"].sum()
        total_expense = df["expense"].sum()
        total_profit = df["profit"].sum()

        col1.metric(
        label="Total Revenue",
        value=f"₹ {total_revenue:,.0f}",
        delta="Positive growth"
        )

        col2.metric(
        label="Total Expense",
        value=f"₹ {total_expense:,.0f}",
        delta="Operational spending"
        )

        col3.metric(
        label="Total Profit",
        value=f"₹ {total_profit:,.0f}",
        delta="Net gain"
        )
        #charts
        st.subheader("Revenue vs Expense Trend")

        st.plotly_chart(revenue_expense_chart(df), use_container_width=True)

        st.subheader("Profit Trend")

        st.plotly_chart(profit_trend_chart(df), use_container_width=True)
        #ai recommendation
        st.subheader("AI Financial Recommendations")

        recommendations = generate_recommendations(df)

        for rec in recommendations:
                    st.warning(rec)
        #Download report
        if st.button("Download AI Financial Report"):

            report_path = generate_report(df, recommendations)

            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download Report",
                    data=file,
                    file_name="AI_Financial_Report.pdf",
                    mime="application/pdf"
                    )
        st.subheader("Ask AI About Financial Data")

        question = st.text_input("Ask a question")

        if question:

            if "revenue" in question.lower():
                st.write(f"Total revenue is {df['revenue'].sum()}")

            elif "expense" in question.lower():
                st.write(f"Total expense is {df['expense'].sum()}")

            elif "profit" in question.lower():
                st.write(f"Total profit is {df['profit'].sum()}")

            elif "best department" in question.lower():
                dept = df.groupby("department")["profit"].sum().idxmax()
                st.write(f"Best performing department is {dept}")

            else:
                st.write("AI could not understand the question")    
    # -----------------------
    # DEPARTMENT ANALYSIS
    # -----------------------

    elif page == "Department Analysis":

        st.title("Department Performance")

        st.plotly_chart(
            department_performance_chart(df),
            use_container_width=True
        )

    # -----------------------
    # ANOMALY DETECTION
    # -----------------------

    elif page == "Anomaly Detection":

        st.title("AI Financial Anomaly Detection")

        model = IsolationForest(contamination=0.05)

        df["anomaly"] = model.fit_predict(df[["revenue", "expense"]])

        anomalies = df[df["anomaly"] == -1]

        st.plotly_chart(anomaly_chart(df), use_container_width=True)

        st.subheader("Detected Anomalies")

        st.dataframe(anomalies)

    # -----------------------
    # DATASET PAGE
    # -----------------------

    elif page == "Dataset":

        st.title("Financial Dataset")

        st.dataframe(df)


# -----------------------
# SESSION CONTROL
# -----------------------

if "login" not in st.session_state:
    st.session_state["login"] = False


if st.session_state["login"] == False:
    login()
else:
    dashboard()