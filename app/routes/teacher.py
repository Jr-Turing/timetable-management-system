"""
routes/teacher.py

API endpoints used by a Teacher to view their own timetable.
"""

from typing import List

from fastapi import APIRouter, HTTPException

from app.database import get_db_session
from app.models import Teacher, Timetable
from app.services import timetable_service as service

router = APIRouter()


@router.get("/{teacher_id}/timetable", response_model=List[Timetable])
def get_teacher_timetable(teacher_id: int):
    """Return the full weekly timetable for the given teacher."""
    with get_db_session() as session:
        teacher = session.get(Teacher, teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return service.get_timetable_by_teacher(session, teacher_id)


@router.get("/", response_model=List[Teacher])
def list_teachers():
    """Return the list of all teachers (used to populate dropdowns)."""
    with get_db_session() as session:
        return service.get_teachers(session)
