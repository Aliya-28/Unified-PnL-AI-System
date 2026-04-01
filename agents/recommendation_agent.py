def generate_recommendations(df):

    insights = []

    # Add profit column
    df["profit"] = df["revenue"] - df["expense"]

    # Group by department
    dept_df = df.groupby("department").agg({
        "revenue": "sum",
        "expense": "sum",
        "profit": "sum"
    }).reset_index()

    for _, row in dept_df.iterrows():

        dept = row["department"]
        revenue = row["revenue"]
        expense = row["expense"]
        profit = row["profit"]

        if expense == 0:
            continue

        margin = profit / expense

        # -----------------------
        # IMPROVED CONDITIONS
        # -----------------------
        if profit < 0:
            insights.append(f"{dept}: Loss detected. Immediate action required.")

        elif margin < 0.1:
            insights.append(f"{dept}: Very low profit. Cost optimization needed.")

        elif margin < 0.3:
            insights.append(f"{dept}: Moderate performance. Can improve efficiency.")

        else:
            insights.append(f"{dept}: Strong performance. Continue growth strategy.")

    return insights