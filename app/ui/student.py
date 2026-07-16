"""
ui/student.py

The Student dashboard. A student can only VIEW the timetable for their
own class - this is the class routine displayed in a clean weekly grid.
"""

from sqlmodel import select
from nicegui import ui, app

from app.database import get_db_session
from app.models import Subject, Teacher
from app.services import timetable_service as service
from app.ui.timetable import render_timetable_grid


@ui.page("/student")
def student_page():
    """Show the logged-in student's class timetable."""
    if not app.storage.user.get("logged_in") or app.storage.user.get("role") != "student":
        ui.navigate.to("/")
        return

    class_name = app.storage.user.get("class_name")
    student_name = app.storage.user.get("name")

    with ui.header().classes("bg-green-800 text-white items-center justify-between"):
        # Build a friendly header. year/semester can be stored in app.storage.user
        # if available; otherwise fall back to sensible defaults shown in UI.
        year = app.storage.user.get("year", "3rd Year")
        semester = app.storage.user.get("semester", "Sem 6")
        ui.column().classes("items-start").style("gap:0")
        ui.label(f"Welcome back, {student_name} 👋").classes("text-lg font-semibold")
        ui.label(f"Student • {class_name} • {year} • {semester}").classes("text-sm")
        ui.button(
            "Logout",
            on_click=lambda: (app.storage.user.clear(), ui.navigate.to("/")),
        ).props("flat color=white")

    with ui.column().classes("w-full p-6"):
        ui.label(f"{class_name} Branch - Weekly Timetable").classes("text-2xl font-bold mb-4")

        # Download PDF button for students to get their class timetable
        def download_pdf_for_student():
            ui.navigate.to(f"/api/pdf/timetable/{class_name}", new_tab=True)

        ui.button("Download Timetable PDF", on_click=download_pdf_for_student).props("color=primary").classes("mb-4")

        # Load the timetable entries for this student's class, plus the
        # subject/teacher names needed to display each cell nicely.
        with get_db_session() as session:
            entries = service.get_timetable_by_class(session, class_name)
            subjects_map = {s.id: s for s in session.exec(select(Subject)).all()}
            teachers_map = {t.id: t for t in session.exec(select(Teacher)).all()}

        render_timetable_grid(entries, subjects_map, teachers_map)
