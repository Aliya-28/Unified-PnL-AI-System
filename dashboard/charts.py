import plotly.express as px
import pandas as pd


# Revenue vs Expense Trend
def revenue_expense_chart(df):

    fig = px.line(
        df,
        x="date",
        y=["revenue", "expense"],
        title="Revenue vs Expense Trend"
    )

    return fig


# Department Performance
def department_performance_chart(df):

    dept_perf = df.groupby("department")[["revenue", "expense"]].sum().reset_index()
    dept_perf["profit"] = dept_perf["revenue"] - dept_perf["expense"]

    fig = px.bar(
        dept_perf,
        x="department",
        y="profit",
        color="department",
        title="Department Profit Comparison"
    )

    return fig


# Profit Trend Chart
def profit_trend_chart(df):

    df["profit"] = df["revenue"] - df["expense"]

    fig = px.line(
        df,
        x="date",
        y="profit",
        title="Profit Trend Over Time"
    )

    return fig


# Anomaly Scatter Chart
def anomaly_chart(df):

    fig = px.scatter(
        df,
        x="revenue",
        y="expense",
        color="anomaly",
        title="Anomaly Detection Chart"
    )

    return fig