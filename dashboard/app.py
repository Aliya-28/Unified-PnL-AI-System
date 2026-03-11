import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

from charts import revenue_expense_chart
from charts import department_performance_chart
from charts import profit_trend_chart
from charts import anomaly_chart


# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Unified P&L AI Dashboard", layout="wide")

st.title("Unified P&L AI Financial Dashboard")


# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("data/financial_data.csv")

# Create profit column
df["profit"] = df["revenue"] - df["expense"]


# ----------------------------
# KPI Cards
# ----------------------------
st.subheader("Financial Overview")

col1, col2, col3 = st.columns(3)

total_revenue = df["revenue"].sum()
total_expense = df["expense"].sum()
total_profit = df["profit"].sum()

col1.metric("Total Revenue", total_revenue)
col2.metric("Total Expense", total_expense)
col3.metric("Total Profit", total_profit)


# ----------------------------
# Charts Section
# ----------------------------
st.subheader("Financial Trends")

st.plotly_chart(revenue_expense_chart(df), use_container_width=True)

st.plotly_chart(profit_trend_chart(df), use_container_width=True)


# ----------------------------
# Department Analysis
# ----------------------------
st.subheader("Department Performance")

st.plotly_chart(department_performance_chart(df), use_container_width=True)


# ----------------------------
# AI Anomaly Detection
# ----------------------------
st.subheader("AI Anomaly Detection")

model = IsolationForest(contamination=0.05)

df["anomaly"] = model.fit_predict(df[["revenue", "expense"]])

st.plotly_chart(anomaly_chart(df), use_container_width=True)

anomalies = df[df["anomaly"] == -1]

st.write("Detected Anomalies")
st.dataframe(anomalies)


# ----------------------------
# Dataset View
# ----------------------------
st.subheader("Complete Financial Dataset")

st.dataframe(df)