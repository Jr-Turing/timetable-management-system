"""
main.py

This is the entry point of the Time Table Management System.
It creates the FastAPI application, includes all the API routers,
attaches the NiceGUI user interface to it, and creates the database
tables when the app starts.

Run this file with:
    uvicorn app.main:app --reload

Then open http://localhost:8000 in your browser.
"""

from fastapi import FastAPI
from nicegui import ui

from app.database import create_db_and_tables
from app.routes import admin, teacher, student, timetable, pdf

# Import the UI pages so that their @ui.page routes get registered with
# NiceGUI. They are not called directly here - simply importing the file
# runs the @ui.page decorators inside it, which registers each page.
from app.ui import login, dashboard, teacher as teacher_ui  # noqa: F401
from app.ui import student as student_ui, admin as admin_ui  # noqa: F401

# Create the main FastAPI application.
app = FastAPI(title="Time Table Management System")

# Register all the API routers. Each router handles one area of the app.
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(teacher.router, prefix="/api/teacher", tags=["Teacher"])
app.include_router(student.router, prefix="/api/student", tags=["Student"])
app.include_router(timetable.router, prefix="/api/timetable", tags=["Timetable"])
app.include_router(pdf.router, prefix="/api/pdf", tags=["PDF Export"])


@app.on_event("startup")
def on_startup() -> None:
    """Create the database tables the first time the app runs."""
    create_db_and_tables()


# Attach the NiceGUI frontend to the FastAPI backend.
# storage_secret is required by NiceGUI to keep track of logged-in users
# using a signed browser cookie - this is simple session storage, NOT
# JWT or OAuth.
ui.run_with(app, storage_secret="timetable_secret_key_change_me")
