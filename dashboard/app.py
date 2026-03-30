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


# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Unified P&L AI System", layout="wide")


# -----------------------
# CSS (CARD UI)
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


# -----------------------
# METRIC CARD
# -----------------------
def metric_card(title, value, subtitle, color):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="{color}">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


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
        else:
            st.error("Invalid credentials")

def answer_query(question, df):

    question = question.lower()

    if "total revenue" in question:
        return f"Total Revenue is ₹ {df['revenue'].sum():,.0f}"

    elif "total expense" in question:
        return f"Total Expense is ₹ {df['expense'].sum():,.0f}"

    elif "total profit" in question:
        return f"Total Profit is ₹ {df['profit'].sum():,.0f}"

    elif "highest revenue" in question:
        row = df.loc[df["revenue"].idxmax()]
        return f"Highest revenue was ₹ {row['revenue']} on {row['date']}"

    elif "highest expense" in question:
        row = df.loc[df["expense"].idxmax()]
        return f"Highest expense was ₹ {row['expense']} on {row['date']}"

    elif "loss" in question:
        losses = df[df["profit"] < 0]
        return f"There are {len(losses)} loss days."

    else:
        return "Sorry, I can answer questions like total revenue, expense, profit, highest values, etc."
# -----------------------
# DASHBOARD
# -----------------------
def dashboard():

    # 🔥 SIDEBAR WITH ICONS
    st.sidebar.markdown("## 📊 P&L AI System")

    page = st.sidebar.radio(
        "Navigate",
        ["📊 Dashboard", "🏢 Department Analysis", "🚨 Anomaly Detection", "📂 Dataset"]
    )

    df = pd.read_csv("data/financial_data.csv")
    df["profit"] = df["revenue"] - df["expense"]

    # -----------------------
    # DASHBOARD PAGE
    # -----------------------
    if page == "📊 Dashboard":

        # 🔥 TOP HEADER WITH ICON
        st.markdown("## 💼 Unified P&L AI System")
        st.caption("AI-driven Financial Intelligence Platform")

        # TABS WITH ICONS
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Trends", "🧠 Insights"])

        # -----------------------
        # OVERVIEW
        # -----------------------
        with tab1:

            st.markdown("## 📊 Financial Overview")

            col1, col2, col3 = st.columns(3)

            total_revenue = df["revenue"].sum()
            total_expense = df["expense"].sum()
            total_profit = df["profit"].sum()

            with col1:
                metric_card("💰 Total Revenue", f"₹ {total_revenue:,.0f}", "Total inflow", "green")

            with col2:
                metric_card("📉 Total Expense", f"₹ {total_expense:,.0f}", "Total outflow", "red")

            with col3:
                metric_card("📈 Total Profit", f"₹ {total_profit:,.0f}", "Net gain", "green")

            # DOWNLOAD BUTTON
            st.markdown("### 📥 Reports")

            if st.button("📄 Download AI Financial Report"):
                recs = generate_recommendations(df)
                path = generate_report(df, recs)

                with open(path, "rb") as f:
                    st.download_button("Download Report", f, "report.pdf")

            # 🔥 ASK AI
            st.markdown("## 🤖 Ask AI About Financial Data")

            question = st.text_input("Ask a question")

            if question:
               answer = answer_query(question, df)

               st.success("AI Answer:")
               st.write(answer)

        # -----------------------
        # TRENDS
        # -----------------------
        with tab2:

            st.markdown("## 📈 Revenue vs Expense")

            df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

            start_date, end_date = st.date_input(
                "Select Date Range",
                [df["date"].min(), df["date"].max()]
            )

            filtered_df = df[
                (df["date"] >= pd.to_datetime(start_date)) &
                (df["date"] <= pd.to_datetime(end_date))
            ]

            freq = st.selectbox(
                "Aggregation",
                ["Daily", "Weekly", "Monthly", "Quarterly", "Half-Yearly", "Yearly"]
            )

            st.plotly_chart(
                revenue_expense_chart(filtered_df, freq),
                use_container_width=True
            )

            st.markdown("## 📊 Profit Trend")

            st.plotly_chart(
                profit_trend_chart(filtered_df),
                use_container_width=True
            )

        # -----------------------
        # INSIGHTS
        # -----------------------
        with tab3:

            st.markdown("## 🧠 AI Insights")

            with st.spinner("Analyzing..."):
                recs = generate_recommendations(df)

            for r in recs:
                st.info(f"💡 {r}")

    # -----------------------
    # DEPARTMENT
    # -----------------------
    elif page == "🏢 Department Analysis":

        st.markdown("## 🏢 Department Performance")

        st.plotly_chart(
            department_performance_chart(df),
            use_container_width=True
        )

    # -----------------------
    # ANOMALY
    # -----------------------
    elif page == "🚨 Anomaly Detection":

        st.markdown("## 🚨 Anomaly Detection")

        with st.spinner("Detecting anomalies..."):
            model = IsolationForest(contamination=0.05)
            df["anomaly"] = model.fit_predict(df[["revenue", "expense"]])

        st.plotly_chart(
            anomaly_chart(df),
            use_container_width=True
        )

        st.dataframe(df[df["anomaly"] == -1])

    # -----------------------
    # DATASET
    # -----------------------
    elif page == "📂 Dataset":

        st.markdown("## 📂 Dataset")

        st.dataframe(df)


# -----------------------
# RUN APP
# -----------------------
if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
else:
    dashboard()