import pandas as pd
import plotly.express as px


# -----------------------------
# EXISTING (UNCHANGED)
# -----------------------------
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


# -----------------------------
# UPDATED DEPARTMENT CHART (ENHANCED VISUAL)
# -----------------------------
def department_performance_chart(df):

    df["profit"] = df["revenue"] - df["expense"]

    dept = df.groupby("department").agg({
        "revenue": "sum",
        "expense": "sum",
        "profit": "sum"
    }).reset_index()

    dept["profit_margin"] = (dept["profit"] / dept["expense"]) * 100

    dept = dept.sort_values(by="profit", ascending=False)

    import plotly.express as px

    fig = px.bar(
        dept,
        x="department",
        y="profit",
        color="department",  # ✅ CHANGED HERE
        text=dept["profit_margin"].round(1).astype(str) + "%",
        color_discrete_sequence=px.colors.qualitative.Set2  # ✅ OPTIONAL
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        title="🏢 Department Performance (Profit + Margin %)",
        xaxis_title="Department",
        yaxis_title="Profit",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="white"),
        showlegend=True  # optional: shows department colors
    )

    return fig


# -----------------------------
# UPDATED ANOMALY CHART (CLEAN)
# -----------------------------
def anomaly_chart(df):

    # Sample if large dataset
    if len(df) > 2000:
        df = df.sample(2000)

    normal = df[df["anomaly"] == 1]
    anomaly = df[df["anomaly"] == -1]

    import plotly.graph_objects as go

    fig = go.Figure()

    # -----------------------
    # NORMAL POINTS
    # -----------------------
    fig.add_trace(go.Scatter(
        x=normal["revenue"],
        y=normal["expense"],
        mode="markers",
        name="Normal",
        marker=dict(color="gray", size=6, opacity=0.4),

        # 🔥 ADD HOVER DATA
        customdata=normal[["department", "date"]],
        hovertemplate=
        "<b>Department:</b> %{customdata[0]}<br>" +
        "<b>Date:</b> %{customdata[1]|%Y-%m-%d}<br>" +
        "<b>Revenue:</b> %{x}<br>" +
        "<b>Expense:</b> %{y}<extra></extra>"
    ))

    # -----------------------
    # ANOMALY POINTS
    # -----------------------
    fig.add_trace(go.Scatter(
        x=anomaly["revenue"],
        y=anomaly["expense"],
        mode="markers",
        name="Anomaly",
        marker=dict(color="red", size=10),

        # 🔥 ADD HOVER DATA
        customdata=anomaly[["department", "date"]],
        hovertemplate=
        "<b>🚨 Anomaly</b><br>" +
        "<b>Department:</b> %{customdata[0]}<br>" +
        "<b>Date:</b> %{customdata[1]|%Y-%m-%d}<br>" +
        "<b>Revenue:</b> %{x}<br>" +
        "<b>Expense:</b> %{y}<extra></extra>"
    ))

    fig.update_layout(
        title="🚨 Anomaly Detection (Highlighted)",
        xaxis_title="Revenue",
        yaxis_title="Expense",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="white")
    )

    return fig


# -----------------------------
# NEW: KPI GROWTH FUNCTION
# -----------------------------
def calculate_growth_metrics(df):

    df = df.sort_values("date")

    if len(df) < 14:
        return 0

    last = df.tail(7)["revenue"].sum()
    prev = df.tail(14).head(7)["revenue"].sum()

    if prev == 0:
        return 0

    growth = ((last - prev) / prev) * 100
    return round(growth, 2)


# -----------------------------
# NEW: TOP DEPARTMENT FUNCTION
# -----------------------------
def top_department(df):

    df["profit"] = df["revenue"] - df["expense"]

    return df.groupby("department")["profit"].sum().idxmax()