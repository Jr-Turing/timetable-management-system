"""
services/pdf_service.py

This file generates a printable PDF of a class timetable using ReportLab.
The PDF shows a weekly grid: days across the top, periods down the side.
"""

import io

from sqlmodel import Session, select
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from app.models import Timetable, Subject, Teacher
from app.utils.helper import DAYS_OF_WEEK


def generate_class_timetable_pdf(session: Session, class_name: str) -> io.BytesIO:
    """
    Build a weekly timetable grid (days as columns, periods as rows) for the
    given class and return it as an in-memory PDF file (a BytesIO buffer).
    """
    # Fetch all timetable entries that belong to this class.
    statement = select(Timetable).where(Timetable.class_name == class_name)
    entries = session.exec(statement).all()

    # Load all subjects and teachers once, so we don't query the database
    # again for every single cell while building the table.
    subjects = {s.id: s for s in session.exec(select(Subject)).all()}
    teachers = {t.id: t for t in session.exec(select(Teacher)).all()}

    # Work out how many periods exist, so the grid has enough rows.
    # If there are no entries yet, we still show a grid with 1 period.
    max_period = max((entry.period for entry in entries), default=1)

    semester = next((entry.semester for entry in entries if entry.semester), None)

    # Build a lookup dictionary: grid[day][period] = display text for that cell.
    grid = {day: {} for day in DAYS_OF_WEEK}
    for entry in entries:
        lines = []

        if entry.subject_id:
            # A normal academic period: show the subject name, optionally
            # tagged as Remedial/Special via the `activity` field.
            subject = subjects.get(entry.subject_id)
            subject_name = subject.name if subject else "Unknown"
            if entry.activity:
                lines.append(f"{subject_name} ({entry.activity})")
            else:
                lines.append(subject_name)
        elif entry.activity:
            # A non-subject activity, e.g. "Mentoring", "Library", "TPO Class".
            lines.append(entry.activity)
        else:
            lines.append("-")

        if entry.teacher_id:
            teacher = teachers.get(entry.teacher_id)
            teacher_name = teacher.name if teacher else "Unknown"
            lines.append(f"({teacher_name})")

        if entry.room:
            lines.append(entry.room)

        lines.append(f"{entry.start_time}-{entry.end_time}")
        grid[entry.day][entry.period] = "\n".join(lines)

    # Build the table data. The first row is the header: Period, Mon, Tue...
    table_data = [["Period"] + DAYS_OF_WEEK]
    for period in range(1, max_period + 1):
        row = [f"Period {period}"]
        for day in DAYS_OF_WEEK:
            row.append(grid[day].get(period, "-"))
        table_data.append(row)

    # Create the PDF document in memory (no file is saved to disk).
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=0.4 * cm, rightMargin=0.4 * cm, topMargin=0.5 * cm, bottomMargin=0.5 * cm,)
    styles = getSampleStyleSheet()

    elements = []
    if semester:
        title_text = f"Weekly Timetable - {semester} {class_name}"
    else:
        title_text = f"Weekly Timetable - {semester} {class_name}"
    title = Paragraph(title_text.replace("Class ", "Branch "), styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 0.5 * cm))

    # Build the table and style it with borders and a colored header row.
    col_widths = [2.2 * cm] + [3.5 * cm] * len(DAYS_OF_WEEK)
    table = Table( table_data, colWidths=col_widths, rowHeights=[0.8 * cm] + [1.6 * cm] * max_period, repeatRows=1,)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ]
        )
    )
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
