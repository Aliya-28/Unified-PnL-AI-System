import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet


# ---------------------------------------
# REVENUE vs EXPENSE (SMART CHART)
# ---------------------------------------
def revenue_expense_chart(df, freq):

    df = df.copy()

    # Fix date
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df = df.dropna(subset=["date"])

    df = df.set_index("date")

    freq_map = {
        "Daily": "D",
        "Weekly": "W",
        "Monthly": "M",
        "Quarterly": "Q",
        "Half-Yearly": "2Q",
        "Yearly": "Y"
    }

    df_grouped = df.resample(freq_map[freq]).sum().reset_index()

    # Smart switch
    if len(df_grouped) <= 2:
        fig = px.bar(
            df_grouped,
            x="date",
            y=["revenue", "expense"],
            barmode="group",
            title=f"Revenue vs Expense ({freq})",
            template="plotly_dark"
        )
    else:
        fig = px.line(
            df_grouped,
            x="date",
            y=["revenue", "expense"],
            title=f"Revenue vs Expense ({freq})",
            template="plotly_dark"
        )

    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        xaxis=dict(title="Date", showgrid=False),
        yaxis=dict(title="Amount (₹)", showgrid=True, gridcolor="#2a2f3a"),
        legend=dict(orientation="h", y=1.1)
    )

    return fig


# ---------------------------------------
# PROFIT TREND
# ---------------------------------------
def profit_trend_chart(df):

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values("date")

    if "profit" not in df.columns:
        df["profit"] = df["revenue"] - df["expense"]

    fig = px.line(
        df,
        x="date",
        y="profit",
        title="Profit Trend",
        template="plotly_dark"
    )

    fig.update_traces(line=dict(color="#00FF9C", width=3))

    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#2a2f3a")
    )

    return fig


# ---------------------------------------
# DEPARTMENT PERFORMANCE
# ---------------------------------------
def department_performance_chart(df):

    dept_df = df.groupby("department", as_index=False)["profit"].sum()

    fig = px.bar(
        dept_df,
        x="department",
        y="profit",
        title="Department Performance",
        template="plotly_dark",
        color="profit",
        color_continuous_scale="Tealgrn"
    )

    return fig


# ---------------------------------------
# ANOMALY CHART
# ---------------------------------------
def anomaly_chart(df):

    fig = px.scatter(
        df,
        x="revenue",
        y="expense",
        color="anomaly",
        title="Anomaly Detection",
        template="plotly_dark",
        color_continuous_scale=["#00FF9C", "#FF4B4B"]
    )

    return fig


# ---------------------------------------
# FORECAST (PROPHET)
# ---------------------------------------
def forecast_chart(df):

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df = df.dropna(subset=["date"])

    prophet_df = df[["date", "revenue"]].rename(columns={
        "date": "ds",
        "revenue": "y"
    })

    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=prophet_df["ds"],
        y=prophet_df["y"],
        name="Actual",
        line=dict(color="#00C2FF")
    ))

    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        name="Forecast",
        line=dict(color="#00FF9C", dash="dash")
    ))

    fig.update_layout(
        title="Revenue Forecast (Next 30 Days)",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white")
    )

    return fig