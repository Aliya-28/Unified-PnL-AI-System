import pandas as pd

# Load dataset
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


# Total revenue calculation
def calculate_total_revenue(df):
    return df["revenue"].sum()


# Total expense calculation
def calculate_total_expense(df):
    return df["expense"].sum()


# Net profit or loss
def calculate_net_profit(df):
    revenue = calculate_total_revenue(df)
    expense = calculate_total_expense(df)
    return revenue - expense


# Department wise P&L
def department_performance(df):
    summary = df.groupby("department")[["revenue", "expense"]].sum()
    summary["profit"] = summary["revenue"] - summary["expense"]
    return summary


# Main execution
if __name__ == "__main__":

    file_path = "data/financial_data.csv"

    df = load_data(file_path)

    total_revenue = calculate_total_revenue(df)
    total_expense = calculate_total_expense(df)
    net_profit = calculate_net_profit(df)

    dept_summary = department_performance(df)

    print("\n------ Financial Summary ------")

    print("Total Revenue:", total_revenue)
    print("Total Expense:", total_expense)
    print("Net Profit/Loss:", net_profit)

    print("\n------ Department-wise Performance ------")

    print(dept_summary)