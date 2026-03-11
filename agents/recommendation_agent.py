import pandas as pd
import os


def generate_recommendations(file_path):

    # Load dataset
    df = pd.read_csv(file_path)

    # Group by department
    dept_summary = df.groupby("department")[["revenue", "expense"]].sum()

    # Calculate profit
    dept_summary["profit"] = dept_summary["revenue"] - dept_summary["expense"]

    print("\n------ RECOMMENDATION AGENT ------\n")

    for dept in dept_summary.index:

        revenue = dept_summary.loc[dept, "revenue"]
        expense = dept_summary.loc[dept, "expense"]
        profit = dept_summary.loc[dept, "profit"]

        if profit < 0:
            print(f"{dept}: High expenses detected. Consider cost reduction.")

        elif profit < 20000:
            print(f"{dept}: Profit margin low. Optimize operational costs.")

        else:
            print(f"{dept}: Performing well. Maintain current strategy.")


if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(current_dir, "..", "data", "financial_data.csv")

    generate_recommendations(file_path)