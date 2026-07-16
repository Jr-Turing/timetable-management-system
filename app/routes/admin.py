"""
routes/admin.py

API endpoints used by the Admin to manage Teachers, Students and Subjects.
These are plain REST endpoints - you can try them directly at /docs.
"""

from typing import List

from fastapi import APIRouter, HTTPException

from app.database import get_db_session
from app.models import Teacher, Student, Subject
from app.schemas import (
    TeacherCreate,
    TeacherUpdate,
    StudentCreate,
    StudentUpdate,
    SubjectCreate,
    SubjectUpdate,
)
from app.services import timetable_service as service

router = APIRouter()


# ---------------------------------------------------------------------------
# Teacher endpoints
# ---------------------------------------------------------------------------
@router.get("/teachers", response_model=List[Teacher])
def list_teachers():
    with get_db_session() as session:
        return service.get_teachers(session)


@router.post("/teachers", response_model=Teacher)
def add_teacher(data: TeacherCreate):
    with get_db_session() as session:
        return service.create_teacher(session, data)


@router.put("/teachers/{teacher_id}", response_model=Teacher)
def edit_teacher(teacher_id: int, data: TeacherUpdate):
    with get_db_session() as session:
        teacher = service.update_teacher(session, teacher_id, data)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return teacher


@router.delete("/teachers/{teacher_id}")
def remove_teacher(teacher_id: int):
    with get_db_session() as session:
        deleted = service.delete_teacher(session, teacher_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return {"message": "Teacher deleted successfully"}


# ---------------------------------------------------------------------------
# Student endpoints
# ---------------------------------------------------------------------------
@router.get("/students", response_model=List[Student])
def list_students():
    with get_db_session() as session:
        return service.get_students(session)


@router.post("/students", response_model=Student)
def add_student(data: StudentCreate):
    with get_db_session() as session:
        return service.create_student(session, data)


@router.put("/students/{student_id}", response_model=Student)
def edit_student(student_id: int, data: StudentUpdate):
    with get_db_session() as session:
        student = service.update_student(session, student_id, data)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student


@router.delete("/students/{student_id}")
def remove_student(student_id: int):
    with get_db_session() as session:
        deleted = service.delete_student(session, student_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}


# ---------------------------------------------------------------------------
# Subject endpoints
# ---------------------------------------------------------------------------
@router.get("/subjects", response_model=List[Subject])
def list_subjects():
    with get_db_session() as session:
        return service.get_subjects(session)


@router.post("/subjects", response_model=Subject)
def add_subject(data: SubjectCreate):
    with get_db_session() as session:
        return service.create_subject(session, data)


@router.put("/subjects/{subject_id}", response_model=Subject)
def edit_subject(subject_id: int, data: SubjectUpdate):
    with get_db_session() as session:
        subject = service.update_subject(session, subject_id, data)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        return subject


@router.delete("/subjects/{subject_id}")
def remove_subject(subject_id: int):
    with get_db_session() as session:
        deleted = service.delete_subject(session, subject_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Subject not found")
        return {"message": "Subject deleted successfully"}
