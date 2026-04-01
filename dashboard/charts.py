import pandas as pd
import plotly.express as px


def resample_data(df, freq):

    freq_map = {
        "Daily": "D",
        "Weekly": "W",
        "Monthly": "M",
        "Quarterly": "Q",
        "Half-Yearly": "2Q",
        "Yearly": "Y"
    }

    df = df.set_index("date").resample(freq_map[freq]).sum().reset_index()
    return df


def revenue_expense_chart(df, freq):

    df = resample_data(df.copy(), freq)

    fig = px.line(
        df,
        x="date",
        y=["revenue", "expense"],
        template="plotly_dark"
    )

    fig.update_traces(line=dict(width=3))
    return fig


def profit_trend_chart(df, freq):

    df = resample_data(df.copy(), freq)

    fig = px.line(
        df,
        x="date",
        y="profit",
        template="plotly_dark"
    )

    fig.update_traces(line=dict(color="#00FF9C", width=3))
    return fig


def department_performance_chart(df):

    dept_df = df.groupby("department")["profit"].sum().reset_index()

    fig = px.bar(
        dept_df,
        x="department",
        y="profit",
        color="department",
        template="plotly_dark"
    )

    return fig


def anomaly_chart(df):

    fig = px.scatter(
        df,
        x="revenue",
        y="expense",
        color="anomaly",
        template="plotly_dark"
    )

    return fig