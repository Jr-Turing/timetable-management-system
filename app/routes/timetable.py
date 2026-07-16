"""
routes/timetable.py

API endpoints for creating, viewing, updating and deleting timetable
entries. This is mainly used by the Admin to build the weekly schedule.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from app.database import get_db_session
from app.models import Timetable
from app.schemas import TimetableCreate, TimetableUpdate
from app.services import timetable_service as service

router = APIRouter()


@router.get("/", response_model=List[Timetable])
def list_timetable(class_name: Optional[str] = None, teacher_id: Optional[int] = None):
    """
    Return timetable entries. Optionally filter by class name or teacher id.
    Example: /api/timetable/?class_name=10-A
    """
    with get_db_session() as session:
        if class_name:
            return service.get_timetable_by_class(session, class_name)
        if teacher_id:
            return service.get_timetable_by_teacher(session, teacher_id)
        return service.get_all_timetable(session)


@router.post("/", response_model=Timetable)
def add_timetable_entry(data: TimetableCreate):
    with get_db_session() as session:
        conflict = service.has_teacher_conflict(
            session, data.teacher_id, data.day, data.period
        )
        if conflict:
            raise HTTPException(
                status_code=400,
                detail="This teacher already has another class at the same day and period.",
            )
        return service.create_timetable_entry(session, data)


@router.put("/{entry_id}", response_model=Timetable)
def edit_timetable_entry(entry_id: int, data: TimetableUpdate):
    with get_db_session() as session:
        entry = service.update_timetable_entry(session, entry_id, data)
        if not entry:
            raise HTTPException(status_code=404, detail="Timetable entry not found")
        return entry


@router.delete("/{entry_id}")
def remove_timetable_entry(entry_id: int):
    with get_db_session() as session:
        deleted = service.delete_timetable_entry(session, entry_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Timetable entry not found")
        return {"message": "Timetable entry deleted successfully"}
