"""
ui/timetable.py

A reusable function that draws a weekly timetable as a clean HTML grid.
This is used by the Admin, Teacher and Student pages so the timetable
always looks the same everywhere.
"""

from nicegui import ui

from app.utils.helper import DAYS_OF_WEEK


def render_timetable_grid(entries, subjects_map, teachers_map):
    """
    Draw a weekly timetable grid: days across the top, periods down the
    side, and each cell showing the subject, teacher and time.

    entries: list of Timetable rows to display
    subjects_map: dict of {subject_id: Subject}
    teachers_map: dict of {teacher_id: Teacher}
    """
    if not entries:
        ui.label("No timetable entries found yet.").classes("text-gray-500 italic")
        return

    # Work out how many periods to show (this decides the number of rows).
    max_period = max(entry.period for entry in entries)

    # Build a lookup: grid[day][period] = matching Timetable entry
    grid = {day: {} for day in DAYS_OF_WEEK}
    for entry in entries:
        grid[entry.day][entry.period] = entry

    # Draw the grid using plain HTML table elements for a clean look.
    with ui.element("table").classes("w-full border-collapse"):
        with ui.element("thead"):
            with ui.element("tr"):
                with ui.element("th").classes("border p-2 bg-gray-800 text-white"):
                    ui.label("Period")
                for day in DAYS_OF_WEEK:
                    with ui.element("th").classes("border p-2 bg-gray-800 text-white"):
                        ui.label(day)

        with ui.element("tbody"):
            for period in range(1, max_period + 1):
                with ui.element("tr"):
                    with ui.element("td").classes("border p-2 text-center font-bold bg-gray-100"):
                        ui.label(f"Period {period}")
                    for day in DAYS_OF_WEEK:
                        entry = grid[day].get(period)
                        with ui.element("td").classes("border p-2 text-center align-middle"):
                            if not entry:
                                ui.label("-").classes("text-gray-300")
                                continue

                            if entry.subject_id:
                                # A normal academic period.
                                subject = subjects_map.get(entry.subject_id)
                                title = subject.name if subject else "Unknown"
                                if entry.activity:
                                    title += f" ({entry.activity})"
                            elif entry.activity:
                                # A non-subject activity, e.g. "Mentoring".
                                title = entry.activity
                            else:
                                title = "-"
                            ui.label(title).classes("font-semibold block")

                            if entry.teacher_id:
                                teacher = teachers_map.get(entry.teacher_id)
                                teacher_name = teacher.name if teacher else "Unknown"
                                ui.label(teacher_name).classes("text-xs text-gray-500 block")

                            if entry.room:
                                ui.label(entry.room).classes("text-xs text-gray-400 block")

                            ui.label(f"{entry.start_time} - {entry.end_time}").classes(
                                "text-xs text-gray-400 block"
                            )
