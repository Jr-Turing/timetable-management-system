"""
routes/student.py

API endpoints used by a Student to view their class timetable.
"""

from typing import List

from fastapi import APIRouter, HTTPException

from app.database import get_db_session
from app.models import Student, Timetable
from app.services import timetable_service as service

router = APIRouter()


@router.get("/{student_id}/timetable", response_model=List[Timetable])
def get_student_timetable(student_id: int):
    """Return the weekly timetable for the class the student belongs to."""
    with get_db_session() as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return service.get_timetable_by_class(session, student.class_name)


@router.get("/", response_model=List[Student])
def list_students():
    """Return the list of all students (used to populate dropdowns)."""
    with get_db_session() as session:
        return service.get_students(session)
