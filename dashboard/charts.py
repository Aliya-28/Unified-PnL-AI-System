import pandas as pd
import plotly.express as px


# ---------------------------------------
# REVENUE vs EXPENSE (SMART CHART)
# ---------------------------------------
def revenue_expense_chart(df, freq):

    df = df.copy()

    # Fix date format
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

    # Smart chart switching
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
        xaxis=dict(title="Date", showgrid=False),
        yaxis=dict(title="Profit (₹)", showgrid=True, gridcolor="#2a2f3a")
    )

    return fig


# ---------------------------------------
# DEPARTMENT PERFORMANCE (MULTI-COLOR)
# ---------------------------------------
def department_performance_chart(df):

    dept_df = df.groupby("department", as_index=False)["profit"].sum()

    fig = px.bar(
        dept_df,
        x="department",
        y="profit",
        title="Department Performance",
        template="plotly_dark",

        # 🔥 Different color per department
        color="department",

        # 🎨 Custom colors
        color_discrete_map={
            "Finance": "#00C2FF",
            "HR": "#FFB347",
            "IT": "#FF4B4B",
            "Marketing": "#00FF9C",
            "Operations": "#8A2BE2",
            "Sales": "#FFD700"
        }
    )

    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        xaxis_title="Department",
        yaxis_title="Profit (₹)",
        showlegend=False
    )

    # Hover improvement
    fig.update_traces(
        hovertemplate="Department: %{x}<br>Profit: ₹ %{y:,.0f}"
    )

    return fig


# ---------------------------------------
# ANOMALY DETECTION CHART
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

    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        xaxis_title="Revenue (₹)",
        yaxis_title="Expense (₹)"
    )

    return fig