from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from io import BytesIO

import matplotlib.pyplot as plt


def generate_report(df, recommendations):

    buffer = BytesIO()

    # 📄 Document Setup
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    # -----------------------
    # 🧾 TITLE
    # -----------------------
    elements.append(Paragraph("<b>AI Financial Analysis Report</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    # -----------------------
    # 📊 SUMMARY
    # -----------------------
    revenue = df["revenue"].sum()
    expense = df["expense"].sum()
    profit = df["profit"].sum()

    summary_data = [
        ["Metric", "Value"],
        ["Total Revenue", f"₹ {revenue:,.0f}"],
        ["Total Expense", f"₹ {expense:,.0f}"],
        ["Net Profit", f"₹ {profit:,.0f}"]
    ]

    table = Table(summary_data, colWidths=[200, 200])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    elements.append(Paragraph("<b>Financial Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(table)
    elements.append(Spacer(1, 25))

    # -----------------------
    # 📈 GRAPH (Revenue vs Expense)
    # -----------------------
    plt.figure()

    plt.plot(df["revenue"], label="Revenue")
    plt.plot(df["expense"], label="Expense")

    plt.title("Revenue vs Expense Trend")
    plt.legend()

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()

    img_buffer.seek(0)

    img = Image(img_buffer, width=5 * inch, height=3 * inch)

    elements.append(Paragraph("<b>Trend Analysis</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(img)
    elements.append(Spacer(1, 25))

    # -----------------------
    # 💡 RECOMMENDATIONS
    # -----------------------
    elements.append(Paragraph("<b>AI Recommendations</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    for rec in recommendations:
        elements.append(Paragraph(f"• {rec}", styles["Normal"]))
        elements.append(Spacer(1, 5))

    # -----------------------
    # 🧱 BORDER FUNCTION
    # -----------------------
    def add_border(canvas, doc):
        canvas.saveState()
        width, height = A4

        canvas.setStrokeColor(colors.black)
        canvas.rect(20, 20, width - 40, height - 40)

        canvas.restoreState()

    # -----------------------
    # BUILD PDF
    # -----------------------
    doc.build(elements, onFirstPage=add_border, onLaterPages=add_border)

    buffer.seek(0)

    return buffer