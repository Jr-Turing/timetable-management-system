"""
ui/admin.py

The Admin dashboard. From here the admin can manage Teachers, Students,
Subjects and the Timetable, and export any class's timetable as a PDF.

Each management area follows the same simple pattern:
1. A table showing all current rows (with their ID visible).
2. An "Add New" expansion panel with a form to create a new row.
3. An "Edit or Delete" expansion panel where the admin types in the ID of
   the row (from the table above) plus the new values, then clicks
   Update or Delete.
This keeps the code simple and beginner-friendly, without needing custom
pop-up dialogs wired to individual table rows.
"""

from nicegui import ui, app

from app.database import get_db_session
from app.services import timetable_service as service
from app.utils.helper import DAYS_OF_WEEK

SEMESTER_OPTIONS = [f"Sem {i}" for i in range(1, 9)]


@ui.page("/admin")
def admin_page():
    """Render the full admin dashboard with tabs for every management area."""
    if not app.storage.user.get("logged_in") or app.storage.user.get("role") != "admin":
        ui.navigate.to("/")
        return

    with ui.header().classes("bg-indigo-800 text-white items-center justify-between"):
        ui.label("Admin Dashboard - Time Table Management System").classes("text-lg")
        ui.button(
            "Logout",
            on_click=lambda: (app.storage.user.clear(), ui.navigate.to("/")),
        ).props("flat color=white")

    with ui.tabs().classes("w-full") as tabs:
        teachers_tab = ui.tab("Teachers")
        students_tab = ui.tab("Students")
        subjects_tab = ui.tab("Subjects")
        timetable_tab = ui.tab("Timetable")
        pdf_tab = ui.tab("Export PDF")

    with ui.tab_panels(tabs, value=teachers_tab).classes("w-full p-4"):
        with ui.tab_panel(teachers_tab):
            build_teachers_panel()
        with ui.tab_panel(students_tab):
            build_students_panel()
        with ui.tab_panel(subjects_tab):
            build_subjects_panel()
        with ui.tab_panel(timetable_tab):
            build_timetable_panel()
        with ui.tab_panel(pdf_tab):
            build_pdf_panel()


# ---------------------------------------------------------------------------
# Teachers panel
# ---------------------------------------------------------------------------
def build_teachers_panel():
    ui.label("Manage Teachers").classes("text-xl font-bold mb-2")

    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "name", "label": "Name", "field": "name"},
        {"name": "email", "label": "Email", "field": "email"},
        {"name": "phone", "label": "Phone", "field": "phone"},
        {"name": "username", "label": "Username", "field": "username"},
    ]
    table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full mb-4")

    def refresh():
        with get_db_session() as session:
            teachers = service.get_teachers(session)
        rows = [t.dict() for t in teachers]
        rows.sort(key=lambda r: r.get("id") or 0)
        table.rows = rows
        table.update()

    with ui.expansion("Add New Teacher", icon="add").classes("w-full mb-2"):
        with ui.row().classes("items-end gap-2"):
            name = ui.input("Name")
            email = ui.input("Email")
            phone = ui.input("Phone")
            username = ui.input("Username")
            password = ui.input("Password", password=True)

            def add_teacher():
                from app.schemas import TeacherCreate

                if not (name.value and email.value and username.value and password.value):
                    ui.notify("Please fill in all required fields", type="negative")
                    return
                with get_db_session() as session:
                    service.create_teacher(
                        session,
                        TeacherCreate(
                            name=name.value,
                            email=email.value,
                            phone=phone.value or "",
                            username=username.value,
                            password=password.value,
                        ),
                    )
                name.value = email.value = phone.value = username.value = password.value = ""
                refresh()
                ui.notify("Teacher added successfully", type="positive")

            ui.button("Add", on_click=add_teacher).props("color=primary")

    with ui.expansion("Edit or Delete a Teacher", icon="edit").classes("w-full mb-2"):
        ui.label("Enter the Teacher ID from the table above, then fill in the fields you want to change.")
        with ui.row().classes("items-end gap-2"):
            edit_id = ui.number("Teacher ID", format="%d")
            edit_name = ui.input("New Name (optional)")
            edit_email = ui.input("New Email (optional)")
            edit_phone = ui.input("New Phone (optional)")
            edit_password = ui.input("New Password (optional)", password=True)

            def edit_teacher():
                from app.schemas import TeacherUpdate

                if not edit_id.value:
                    ui.notify("Please enter a Teacher ID", type="negative")
                    return
                with get_db_session() as session:
                    updated = service.update_teacher(
                        session,
                        int(edit_id.value),
                        TeacherUpdate(
                            name=edit_name.value or None,
                            email=edit_email.value or None,
                            phone=edit_phone.value or None,
                            password=edit_password.value or None,
                        ),
                    )
                if updated:
                    ui.notify("Teacher updated successfully", type="positive")
                else:
                    ui.notify("Teacher not found", type="negative")
                refresh()

            def delete_teacher():
                if not edit_id.value:
                    ui.notify("Please enter a Teacher ID", type="negative")
                    return
                with get_db_session() as session:
                    deleted = service.delete_teacher(session, int(edit_id.value))
                if deleted:
                    ui.notify("Teacher deleted successfully", type="warning")
                else:
                    ui.notify("Teacher not found", type="negative")
                refresh()

            ui.button("Update", on_click=edit_teacher).props("color=primary")
            ui.button("Delete", on_click=delete_teacher).props("color=red")

    refresh()


# ---------------------------------------------------------------------------
# Students panel
# ---------------------------------------------------------------------------
def build_students_panel():
    ui.label("Manage Students").classes("text-xl font-bold mb-2")

    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "name", "label": "Name", "field": "name"},
        {"name": "email", "label": "Email", "field": "email"},
        {"name": "roll_number", "label": "Roll No.", "field": "roll_number"},
        {"name": "class_name", "label": "Branch", "field": "class_name"},
        {"name": "Semester", "label": "Semester", "field": "Semester"},
        {"name": "username", "label": "Username", "field": "username"},
    ]
    table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full mb-4")

    def refresh():
        with get_db_session() as session:
            students = service.get_students(session)
        rows = [s.dict() for s in students]
        rows.sort(key=lambda r: r.get("id") or 0)
        table.rows = rows
        table.update()

    with ui.expansion("Add New Student", icon="add").classes("w-full mb-2"):
        with ui.row().classes("items-end gap-2"):
            name = ui.input("Name")
            email = ui.input("Email")
            roll_number = ui.input("Roll Number")
            class_name = ui.input("Branch (e.g. CSE)")
            Semester = ui.select(options=SEMESTER_OPTIONS, value=SEMESTER_OPTIONS[0], label="Semester")
            username = ui.input("Username")
            password = ui.input("Password", password=True)

            def add_student():
                from app.schemas import StudentCreate

                if not (
                    name.value
                    and email.value
                    and class_name.value
                    and Semester.value
                    and username.value
                    and password.value
                ):
                    ui.notify("Please fill in all required fields", type="negative")
                    return
                with get_db_session() as session:
                    service.create_student(
                        session,
                        StudentCreate(
                            name=name.value,
                            email=email.value,
                            roll_number=roll_number.value or "",
                            class_name=class_name.value,
                            Semester=Semester.value or "",
                            username=username.value,
                            password=password.value,
                        ),
                    )
                name.value = email.value = roll_number.value = class_name.value = Semester.value = ""
                username.value = password.value = ""
                refresh()
                ui.notify("Student added successfully", type="positive")

            ui.button("Add", on_click=add_student).props("color=primary")

    with ui.expansion("Edit or Delete a Student", icon="edit").classes("w-full mb-2"):
        ui.label("Enter the Student ID from the table above, then fill in the fields you want to change.")
        with ui.row().classes("items-end gap-2"):
            edit_id = ui.number("Student ID", format="%d")
            edit_name = ui.input("New Name (optional)")
            edit_class = ui.input("New Class (optional)")
            edit_Semester = ui.select(options=SEMESTER_OPTIONS, value=None, label="New Semester (optional)")
            edit_password = ui.input("New Password (optional)", password=True)

            def edit_student():
                from app.schemas import StudentUpdate

                if not edit_id.value:
                    ui.notify("Please enter a Student ID", type="negative")
                    return
                with get_db_session() as session:
                    updated = service.update_student(
                        session,
                        int(edit_id.value),
                        StudentUpdate(
                            name=edit_name.value or None,
                            class_name=edit_class.value or None,
                            Semester=edit_Semester.value or None,
                            password=edit_password.value or None,
                        ),
                    )
                if updated:
                    ui.notify("Student updated successfully", type="positive")
                else:
                    ui.notify("Student not found", type="negative")
                refresh()

            def delete_student():
                if not edit_id.value:
                    ui.notify("Please enter a Student ID", type="negative")
                    return
                with get_db_session() as session:
                    deleted = service.delete_student(session, int(edit_id.value))
                if deleted:
                    ui.notify("Student deleted successfully", type="warning")
                else:
                    ui.notify("Student not found", type="negative")
                refresh()

            ui.button("Update", on_click=edit_student).props("color=primary")
            ui.button("Delete", on_click=delete_student).props("color=red")

    refresh()


# ---------------------------------------------------------------------------
# Subjects panel
# ---------------------------------------------------------------------------
def build_subjects_panel():
    ui.label("Manage Subjects").classes("text-xl font-bold mb-2")

    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "name", "label": "Name", "field": "name"},
        {"name": "code", "label": "Code", "field": "code"},
    ]
    table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full mb-4")

    def refresh():
        with get_db_session() as session:
            subjects = service.get_subjects(session)
        rows = [s.dict() for s in subjects]
        rows.sort(key=lambda r: r.get("id") or 0)
        table.rows = rows
        table.update()

    with ui.expansion("Add New Subject", icon="add").classes("w-full mb-2"):
        with ui.row().classes("items-end gap-2"):
            name = ui.input("Subject Name")
            code = ui.input("Subject Code")

            def add_subject():
                from app.schemas import SubjectCreate

                if not (name.value and code.value):
                    ui.notify("Please fill in all fields", type="negative")
                    return
                with get_db_session() as session:
                    service.create_subject(
                        session, SubjectCreate(name=name.value, code=code.value)
                    )
                name.value = code.value = ""
                refresh()
                ui.notify("Subject added successfully", type="positive")

            ui.button("Add", on_click=add_subject).props("color=primary")

    with ui.expansion("Edit or Delete a Subject", icon="edit").classes("w-full mb-2"):
        with ui.row().classes("items-end gap-2"):
            edit_id = ui.number("Subject ID", format="%d")
            edit_name = ui.input("New Name (optional)")
            edit_code = ui.input("New Code (optional)")

            def edit_subject():
                from app.schemas import SubjectUpdate

                if not edit_id.value:
                    ui.notify("Please enter a Subject ID", type="negative")
                    return
                with get_db_session() as session:
                    updated = service.update_subject(
                        session,
                        int(edit_id.value),
                        SubjectUpdate(
                            name=edit_name.value or None, code=edit_code.value or None
                        ),
                    )
                if updated:
                    ui.notify("Subject updated successfully", type="positive")
                else:
                    ui.notify("Subject not found", type="negative")
                refresh()

            def delete_subject():
                if not edit_id.value:
                    ui.notify("Please enter a Subject ID", type="negative")
                    return
                with get_db_session() as session:
                    deleted = service.delete_subject(session, int(edit_id.value))
                if deleted:
                    ui.notify("Subject deleted successfully", type="warning")
                else:
                    ui.notify("Subject not found", type="negative")
                refresh()

            ui.button("Update", on_click=edit_subject).props("color=primary")
            ui.button("Delete", on_click=delete_subject).props("color=red")

    refresh()


# ---------------------------------------------------------------------------
# Timetable panel
# ---------------------------------------------------------------------------
def build_timetable_panel():
    ui.label("Manage Timetable").classes("text-xl font-bold mb-2")

    # Load subjects and teachers once to build dropdown option lists.
    with get_db_session() as session:
        subjects = service.get_subjects(session)
        teachers = service.get_teachers(session)

    subject_options = {s.id: f"{s.name} ({s.code})" for s in subjects}
    teacher_options = {t.id: t.name for t in teachers}

    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "class_name", "label": "Branch", "field": "class_name"},
        {"name": "semester", "label": "Semester", "field": "semester"},
        {"name": "day", "label": "Day", "field": "day"},
        {"name": "period", "label": "Period", "field": "period"},
        {"name": "start_time", "label": "Start", "field": "start_time"},
        {"name": "end_time", "label": "End", "field": "end_time"},
        {"name": "subject_name", "label": "Subject / Activity", "field": "subject_name"},
        {"name": "teacher_name", "label": "Teacher", "field": "teacher_name"},
        {"name": "room", "label": "Room", "field": "room"},
    ]
    table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full mb-4")

    def refresh():
        with get_db_session() as session:
            entries = service.get_all_timetable(session)
        rows = []
        for entry in entries:
            row = entry.dict()
            if row.get("semester") and not str(row["semester"]).startswith("Sem "):
                row["semester"] = f"Sem {row['semester']}"
            # A period either has a formal Subject, or is a free-text
            # activity like "Mentoring" or "Library" (see models.py).
            if entry.subject_id:
                label = subject_options.get(entry.subject_id, "Unknown Subject")
                if entry.activity:
                    label += f" ({entry.activity})"
                row["subject_name"] = label
            else:
                row["subject_name"] = entry.activity or "-"
            row["teacher_name"] = teacher_options.get(entry.teacher_id, "-")
            row["room"] = entry.room or "-"
            rows.append(row)
        rows.sort(key=lambda r: r.get("id") or 0)
        table.rows = rows
        table.update()

    if not subject_options or not teacher_options:
        ui.label(
            "Tip: add Subjects and Teachers first if you want to create normal "
            "academic periods. Non-subject activities (Mentoring, Library, "
            "TPO Class, etc.) can be added without them."
        ).classes("text-orange-600 italic mb-2")

    with ui.expansion("Add New Timetable Entry", icon="add").classes("w-full mb-2"):
        ui.label(
            "For a normal class, pick a Subject and Teacher. For a non-subject "
            "slot (e.g. Mentoring, Library, TPO Class, Soft Skill), leave "
            "Subject/Teacher empty and type an Activity name instead."
        ).classes("text-sm text-gray-500 mb-1")
        with ui.row().classes("items-end gap-2"):
            class_name = ui.input("Branch Name (e.g. CSE-CS)")
            semester = ui.select(options=SEMESTER_OPTIONS, value=SEMESTER_OPTIONS[0], label="Semester")
            day = ui.select(options=DAYS_OF_WEEK, value=DAYS_OF_WEEK[0], label="Day")
            period = ui.number("Period", value=1, format="%d")
            start_time = ui.input("Start Time (e.g. 09:00)")
            end_time = ui.input("End Time (e.g. 09:45)")
        with ui.row().classes("items-end gap-2"):
            subject_select = ui.select(options=subject_options, label="Subject (optional)")
            teacher_select = ui.select(options=teacher_options, label="Teacher (optional)")
            activity_input = ui.input("Activity (e.g. Mentoring, Remedial)")
            room_input = ui.input("Room (optional, e.g. ACD-408A)")

            def add_entry():
                from app.schemas import TimetableCreate

                if not (class_name.value and start_time.value and end_time.value):
                    ui.notify("Please fill in class name, start time and end time", type="negative")
                    return
                if not subject_select.value and not activity_input.value:
                    ui.notify(
                        "Please choose a Subject or type an Activity name", type="negative"
                    )
                    return

                with get_db_session() as session:
                    if teacher_select.value:
                        conflict = service.has_teacher_conflict(
                            session, teacher_select.value, day.value, int(period.value)
                        )
                        if conflict:
                            ui.notify(
                                "This teacher already has a class at that day and period.",
                                type="negative",
                            )
                            return
                    service.create_timetable_entry(
                        session,
                        TimetableCreate(
                            class_name=class_name.value,
                            semester=semester.value or None,
                            day=day.value,
                            period=int(period.value),
                            start_time=start_time.value,
                            end_time=end_time.value,
                            subject_id=subject_select.value or None,
                            teacher_id=teacher_select.value or None,
                            activity=activity_input.value or None,
                            room=room_input.value or None,
                        ),
                    )
                refresh()
                ui.notify("Timetable entry added successfully", type="positive")

            ui.button("Add", on_click=add_entry).props("color=primary")

    with ui.expansion("Delete a Timetable Entry", icon="delete").classes("w-full mb-2"):
        ui.label("Enter the entry ID from the table above to delete it.")
        with ui.row().classes("items-end gap-2"):
            delete_id = ui.number("Entry ID", format="%d")

            def delete_entry():
                if not delete_id.value:
                    ui.notify("Please enter an Entry ID", type="negative")
                    return
                with get_db_session() as session:
                    deleted = service.delete_timetable_entry(session, int(delete_id.value))
                if deleted:
                    ui.notify("Timetable entry deleted", type="warning")
                else:
                    ui.notify("Entry not found", type="negative")
                refresh()

            ui.button("Delete", on_click=delete_entry).props("color=red")

    refresh()


# ---------------------------------------------------------------------------
# PDF export panel
# ---------------------------------------------------------------------------
def build_pdf_panel():
    ui.label("Export Timetable as PDF").classes("text-xl font-bold mb-2")
    ui.label(
        "Enter a branch name and click Download to get a printable PDF of "
        "that branch's weekly timetable."
    ).classes("text-gray-600 mb-2")

    class_name_input = ui.input("Branch Name (e.g. CSE-CS)").classes("w-64")

    def download_pdf():
        if not class_name_input.value:
            ui.notify("Please enter a class name", type="negative")
            return
        # Open the PDF export API endpoint in a new browser tab. The
        # endpoint sets a Content-Disposition header, so the browser
        # automatically downloads the file instead of just displaying it.
        ui.navigate.to(f"/api/pdf/timetable/{class_name_input.value}", new_tab=True)

    ui.button("Download PDF", on_click=download_pdf).props("color=primary")
