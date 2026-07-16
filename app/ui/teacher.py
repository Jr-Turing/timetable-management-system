"""
ui/teacher.py
Teacher Dashboard
"""

from sqlmodel import select
from nicegui import ui, app

from app.database import get_db_session
from app.models import Subject, Teacher
from app.services import timetable_service as service
from app.ui.timetable import render_timetable_grid


@ui.page("/teacher")
def teacher_page():

    if not app.storage.user.get("logged_in") or app.storage.user.get("role") != "teacher":
        ui.navigate.to("/")
        return

    teacher_id = app.storage.user.get("user_id")
    teacher_name = app.storage.user.get("name")

    with ui.header().classes("bg-blue-800 text-white items-center justify-between"):
        ui.label(f"Welcome, {teacher_name} (Teacher)").classes("text-lg")

        ui.button(
            "Logout",
            on_click=lambda: (
                app.storage.user.clear(),
                ui.navigate.to("/")
            ),
        ).props("flat color=white")

    with ui.column().classes("w-full p-6"):

        ui.label("My Weekly Timetable").classes(
            "text-2xl font-bold"
        )

        # ---------------- Semester Dropdown ----------------

        semester = ui.select(
            ["1","2","3","4","5","6","7","8"],
            value="6",
            label="Semester",
        ).classes("w-40")

        timetable_container = ui.column().classes("w-full")

        def load_timetable():

            timetable_container.clear()

            with get_db_session() as session:

                entries = service.get_timetable_by_teacher(
                    session,
                    teacher_id,
                )

                # Filter timetable by semester
                filtered_entries = [
                    e for e in entries
                    if (e.semester or "").strip().lower() == semester.value.strip().lower()
                ]

                subjects_map = {
                    s.id: s
                    for s in session.exec(select(Subject)).all()
                }

                teachers_map = {
                    t.id: t
                    for t in session.exec(select(Teacher)).all()
                }

            with timetable_container:

                if not filtered_entries:
                    ui.label("No timetable entries found for this semester.").classes(
                        "text-grey-6 text-center text-lg q-pa-md"
                    )
                else:
                    render_timetable_grid(
                        filtered_entries,
                        subjects_map,
                        teachers_map,
                    )

        semester.on_value_change(lambda _: load_timetable())

        load_timetable()

        ui.separator()

        # ---------------- Send Notice ----------------

        with ui.card().classes("w-full"):

            ui.label("Send Notice").classes(
                "text-lg font-bold"
            )

            notice = ui.textarea(
                label="Message",
                placeholder="Example: I will be absent today."
            ).classes("w-full")

            def send_notice():

                if not notice.value:
                    ui.notify(
                        "Please enter a message",
                        color="negative"
                    )
                    return

                with get_db_session() as session:
                    service.create_notice(
                        session,
                        teacher_id,
                        notice.value,
                    )

                notice.value = ""

                ui.notify(
                    "Notice sent successfully",
                    color="positive"
                )

            ui.button(
                "Send Notice",
                icon="send",
                on_click=send_notice,
            ).props("color=primary")