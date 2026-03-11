import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# Load dataset
df = pd.read_csv("C:/Users/HP/Unified-PnL-AI-System/Unified-PnL-AI-System/data/financial_data.csv")

st.title("Unified P&L AI Dashboard")

st.write("Financial Overview Dashboard")

# -----------------------
# Revenue vs Expense
# -----------------------

st.subheader("Revenue vs Expense")

fig = px.bar(
    df,
    x="department",
    y=["revenue", "expense"],
    barmode="group",
    title="Revenue vs Expense by Department"
)

st.plotly_chart(fig)

# -----------------------
# Department Performance
# -----------------------

st.subheader("Department Performance")

dept = df.groupby("department")[["revenue", "expense"]].sum()
dept["profit"] = dept["revenue"] - dept["expense"]

st.dataframe(dept)

fig2 = px.bar(
    dept,
    y="profit",
    title="Department Profitability"
)

st.plotly_chart(fig2)

# -----------------------
# Anomaly Detection
# -----------------------

st.subheader("Financial Anomaly Alerts")

model = IsolationForest(contamination=0.05)

df["anomaly"] = model.fit_predict(df[["revenue", "expense"]])

anomalies = df[df["anomaly"] == -1]

st.write("Detected Anomalies")

st.dataframe(anomalies[["date", "department", "revenue", "expense"]])

