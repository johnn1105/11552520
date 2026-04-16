#==========================================================
# Invoice creation and PDF export
#==========================================================
from __future__ import annotations

from datetime import datetime  # For timestamp in PDF
from pathlib import Path  # Handle file paths

from reportlab.lib.pagesizes import A4, A5  # PDF page sizes
from reportlab.pdfgen import canvas  # Core PDF drawing tool

from constants import DEFAULT_OUTPUT_DIR  # Default output folder
from models import Invoice  # Data model for invoice


class InvoiceService:
    # Build invoice data and export PDF files.

    def __init__(self, student_service):
        # Inject student service
        self.student_service = student_service

    def build_invoice(self, student_id: int, year: int, month: int) -> Invoice:
        # Create an invoice object for one student and month.
        student = self.student_service.get_student_by_id(student_id)
        if not student:
            raise ValueError("Student not found.")
        # Filter out cancelled lessons and prepare invoice details
        active_occurrences = [
            occurrence
            for occurrence in self.student_service.lesson_occurrences_for_student_in_month(student_id, year, month)
            if not occurrence["cancelled"]
        ]
        # Extract lesson dates and details for the invoice
        lesson_dates = [occurrence["date"] for occurrence in active_occurrences]
        # Format lesson details as "YYYY-MM-DD - HHMM-HHMM (Xmin)"
        lesson_details = [
            f"{occurrence['date']} - {occurrence['start_time']}-{occurrence['end_time']} ({occurrence['lesson_minutes']}min)"
            for occurrence in active_occurrences
        ]
        # Calculate total fee based on active lessons
        total_hkd = student.fee_hkd * len(active_occurrences)
        return Invoice(
            invoice_no=f"{year}{month:02d}-{student_id}-0001",
            month=f"{year:04d}-{month:02d}",
            student_name=student.name,
            instrument=student.instrument,
            grade=student.grade,
            lesson_dates=lesson_dates,
            lesson_details=lesson_details,
            fee_hkd=student.fee_hkd,
            total_hkd=total_hkd,
        )

    def export_invoice_pdf(self, invoice: Invoice, output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
        # Write one invoice PDF.
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        # Define PDF file path
        pdf_path = output_path / f"invoice_{invoice.invoice_no}.pdf"
        
        pdf_canvas = canvas.Canvas(str(pdf_path), pagesize=A5)
        _, page_height = A5
        y_position = page_height - 60
        # Draw invoice header and details
        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(50, y_position, "Music Lesson Invoice")
        y_position -= 30
        # Draw student and lesson details
        pdf_canvas.setFont("Helvetica", 11)
        for line_text in [
            f"Invoice No.: {invoice.invoice_no}",
            f"Month: {invoice.month}",
            f"Student: {invoice.student_name}",
            f"Instrument: {invoice.instrument}    Grade: {invoice.grade}",
        ]:
            pdf_canvas.drawString(50, y_position, line_text)
            y_position -= 18
        # Draw lesson details with a header
        y_position -= 7
        pdf_canvas.setFont("Helvetica-Bold", 12)
        pdf_canvas.drawString(50, y_position, "Lesson Details:")
        y_position -= 18

        pdf_canvas.setFont("Helvetica", 11)
        for lesson_detail in invoice.lesson_details:
            pdf_canvas.drawString(70, y_position, f"- {lesson_detail}")
            y_position -= 16
            if y_position < 80:
                pdf_canvas.showPage()
                y_position = page_height - 60
                pdf_canvas.setFont("Helvetica", 11)
        # Draw fee and total at the end
        y_position -= 10
        pdf_canvas.setFont("Helvetica-Bold", 12)
        pdf_canvas.drawString(50, y_position, f"Fee per lesson (HKD): {invoice.fee_hkd}")
        y_position -= 18
        pdf_canvas.drawString(50, y_position, f"Total (HKD): {invoice.total_hkd}")
        # Draw generation timestamp at the bottom
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawString(50, 40, f"Generated at {datetime.now().isoformat(timespec='seconds')}")
        pdf_canvas.save()
        return str(pdf_path)

    def export_monthly_income_pdf(self, statement: dict, output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
        # Write the monthly income statement PDF.
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        pdf_path = output_path / f"monthly_income_{statement['month']}.pdf"

        pdf_canvas = canvas.Canvas(str(pdf_path), pagesize=A4)
        _, page_height = A4
        y_position = page_height - 50
        # Draw header
        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(50, y_position, "Monthly Income Statement")
        y_position -= 28
        # Draw month and table header
        pdf_canvas.setFont("Helvetica", 11)
        pdf_canvas.drawString(50, y_position, f"Month: {statement['month']}")
        y_position -= 25
        # Draw table header
        pdf_canvas.setFont("Helvetica-Bold", 10)
        for x_position, header_text in [(50, "ID"), (85, "Name"), (220, "Instrument"), (310, "Grade"), (360, "Lessons"), (420, "Fee"), (490, "Total")]:
            pdf_canvas.drawString(x_position, y_position, header_text)
        y_position -= 16
        # Draw a line under the header
        pdf_canvas.setFont("Helvetica", 10)
        for row in statement["rows"]:
            row_values = [
                (50, str(row["student_id"])),
                (85, str(row["name"])),
                (220, str(row["instrument"])),
                (310, str(row["grade"])),
                (360, str(row["lesson_count"])),
                (420, f"HKD {row['fee_per_lesson']}"),
                (490, f"HKD {row['student_total']}"),
            ]
            for x_position, value_text in row_values:
                pdf_canvas.drawString(x_position, y_position, value_text)
            y_position -= 16
            if y_position < 80:
                pdf_canvas.showPage()
                y_position = page_height - 50
                pdf_canvas.setFont("Helvetica", 10)
        # Draw total income at the end
        y_position -= 15
        pdf_canvas.setFont("Helvetica-Bold", 12)
        pdf_canvas.drawString(50, y_position, f"Total Monthly Income: HKD {statement['total_income']}")
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawString(50, 30, f"Generated at {datetime.now().isoformat(timespec='seconds')}")
        pdf_canvas.save()
        return str(pdf_path)
