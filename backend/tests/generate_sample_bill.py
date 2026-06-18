from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_sample_bill():
    output_path = os.path.join(os.path.dirname(__file__), "sample_aws_bill.pdf")
    c = canvas.Canvas(output_path, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "AWS Billing Statement - May 2026")

    # Divider line
    c.line(100, 740, 500, 740)

    # Column headers
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 715, "Service")
    c.drawString(350, 715, "Cost (USD)")

    # Bill line items
    c.setFont("Helvetica", 12)
    services = [
        ("Amazon EC2", "$450.00"),
        ("Amazon RDS", "$210.00"),
        ("Amazon S3", "$32.50"),
        ("AWS Lambda", "$12.00"),
        ("Data Transfer", "$45.00"),
    ]

    y = 690
    for service, cost in services:
        c.drawString(100, y, service)
        c.drawString(350, y, cost)
        y -= 25

    # Total
    c.line(100, y, 500, y)
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, "Total")
    c.drawString(350, y, "$749.50")

    c.save()
    print(f"Sample bill created at: {output_path}")

create_sample_bill()