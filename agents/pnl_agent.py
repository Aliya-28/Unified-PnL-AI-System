import sys
import os
import pandas as pd

# Get current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add backend folder to Python path
backend_path = os.path.join(current_dir, "..", "backend")
sys.path.append(backend_path)

# Import backend functions
from pnl_engine import calculate_total_revenue
from pnl_engine import calculate_total_expense
from pnl_engine import calculate_net_profit
from pnl_engine import department_performance


def run_pnl_analysis(file_path):

    df = pd.read_csv(file_path)

    revenue = calculate_total_revenue(df)
    expense = calculate_total_expense(df)
    profit = calculate_net_profit(df)

    dept_summary = department_performance(df)

    print("\n------ AI P&L ANALYSIS AGENT ------")

    print("Total Revenue:", revenue)
    print("Total Expense:", expense)
    print("Net Profit:", profit)

    print("\nDepartment Performance")
    print(dept_summary)


if __name__ == "__main__":

    # Dataset path
    data_path = os.path.join(current_dir, "..", "data", "financial_data.csv")

    run_pnl_analysis(data_path)