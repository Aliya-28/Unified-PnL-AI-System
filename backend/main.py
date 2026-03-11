import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import authentication
from authentication import authenticate_user

# import modules
from pnl_engine import calculate_total_revenue, calculate_total_expense, calculate_net_profit

# import agents
from agents.pnl_agent import run_pnl_analysis
from agents.anomaly_agent import detect_anomalies
from agents.recommendation_agent import generate_recommendations


def main():

    print("===== Unified P&L AI System =====")

    # ------------------------------
    # 1 LOGIN
    # ------------------------------
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    user = authenticate_user(username, password)

    if not user:
        print("Authentication Failed")
        return

    print("Login Successful")
    print("Role:", user["role"])

    # ------------------------------
    # 2 LOAD DATASET
    # ------------------------------

    print("\nLoading financial dataset...")

    df = pd.read_csv("data/financial_data.csv")

    print("Dataset Loaded Successfully")
    print(df)

    # ------------------------------
    # 3 P&L CALCULATIONS
    # ------------------------------

    total_revenue = calculate_total_revenue(df)
    total_expense = calculate_total_expense(df)
    profit = calculate_net_profit(df)

    print("\n----- P&L SUMMARY -----")

    print("Total Revenue:", total_revenue)
    print("Total Expense:", total_expense)
    print("Net Profit/Loss:", profit)

    # ------------------------------
    # 4 AI AGENT 1 (P&L Analysis)
    # ------------------------------

    print("\nRunning P&L Analysis Agent...")

    analysis = run_pnl_analysis("data/financial_data.csv")

    print(analysis)

    # ------------------------------
    # 5 AI AGENT 2 (Anomaly Detection)
    # ------------------------------

    print("\nRunning Anomaly Detection Agent...")

    anomalies = detect_anomalies("data/financial_data.csv")

    print(anomalies)

    # ------------------------------
    # 6 AI AGENT 3 (Recommendation)
    # ------------------------------

    print("\nRunning Recommendation Agent...")

    recommendations = generate_recommendations("data/financial_data.csv")

    print(recommendations)

    print("\nSystem Execution Completed")


if __name__ == "__main__":
    main()