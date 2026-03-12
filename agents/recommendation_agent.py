import pandas as pd

def generate_recommendations(df):

    recommendations = []

    dept = df.groupby("department")[["revenue","expense"]].sum()

    dept["profit"] = dept["revenue"] - dept["expense"]

    for department, row in dept.iterrows():

        if row["profit"] < 0:
            recommendations.append(
                f"{department}: Department is running in loss. Reduce expenses."
            )

        elif row["profit"] < 50000:
            recommendations.append(
                f"{department}: Profit is low. Improve revenue strategies."
            )

        else:
            recommendations.append(
                f"{department}: Performing well. Maintain strategy."
            )

    return recommendations