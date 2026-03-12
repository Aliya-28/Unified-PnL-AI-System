from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(df, recommendations):

    file_path = "financial_report.pdf"

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AI Financial Analysis Report", styles['Title']))
    elements.append(Spacer(1,20))

    revenue = df["revenue"].sum()
    expense = df["expense"].sum()
    profit = df["profit"].sum()

    elements.append(Paragraph(f"Total Revenue: {revenue}", styles['Normal']))
    elements.append(Paragraph(f"Total Expense: {expense}", styles['Normal']))
    elements.append(Paragraph(f"Total Profit: {profit}", styles['Normal']))

    elements.append(Spacer(1,20))
    elements.append(Paragraph("AI Recommendations", styles['Heading2']))

    for rec in recommendations:
        elements.append(Paragraph(rec, styles['Normal']))

    pdf = SimpleDocTemplate(file_path)
    pdf.build(elements)

    return file_path