# invoice.py
# Generate invoice PDF using reportlab (installed in your environment)
# This is a practical real-life output.

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from models import Invoice

def generate_invoice_pdf(invoice: Invoice, output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    filename = f"invoice_{invoice.invoice_no}.pdf"
    path = os.path.join(output_dir, filename)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Music Lesson Invoice")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Invoice No.: {invoice.invoice_no}")
    y -= 18
    c.drawString(50, y, f"Month: {invoice.month}")
    y -= 18
    c.drawString(50, y, f"Student: {invoice.student_name}")
    y -= 18
    c.drawString(50, y, f"Instrument: {invoice.instrument}    Grade: {invoice.grade}")
    y -= 25

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Lesson Dates:")
    y -= 18
    c.setFont("Helvetica", 11)
    for dt in invoice.lesson_dates:
        c.drawString(70, y, f"- {dt}")
        y -= 16
        if y < 80:
            c.showPage()
            y = height - 60
            c.setFont("Helvetica", 11)

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Fee per lesson (HKD): {invoice.fee_hkd}")
    y -= 18
    c.drawString(50, y, f"Total (HKD): {invoice.total_hkd}")

    c.setFont("Helvetica", 9)
    c.drawString(50, 40, f"Generated at {datetime.now().isoformat(timespec='seconds')}")

    c.save()
    return path