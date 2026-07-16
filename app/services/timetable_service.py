"""
services/timetable_service.py

This file contains all the "business logic" of the application: creating,
reading, updating and deleting Teachers, Students, Subjects and Timetable
entries, plus the login check. Keeping this logic in one place (instead of
directly inside the routes or UI code) makes it reusable from both the
FastAPI API routes and the NiceGUI pages.
"""

from typing import List, Optional

from sqlmodel import Session, select

from app.models import Teacher, Student, Subject, Timetable
from app.schemas import (
    TeacherCreate,
    TeacherUpdate,
    StudentCreate,
    StudentUpdate,
    SubjectCreate,
    SubjectUpdate,
    TimetableCreate,
    TimetableUpdate,
)
from app.utils.helper import (
    hash_password,
    verify_password,
    ADMIN_USERNAME,
    ADMIN_PASSWORD_HASH,
)


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
def authenticate_user(
    session: Session, username: str, password: str, role: str
) -> Optional[dict]:
    """
    Check the given username/password against the correct table based on
    the selected role. Returns a small dictionary describing the logged-in
    user if the login is correct, otherwise returns None.
    """
    if role == "admin":
        if username == ADMIN_USERNAME and verify_password(password, ADMIN_PASSWORD_HASH):
            return {"id": 0, "name": "Administrator", "role": "admin"}
        return None

    if role == "teacher":
        statement = select(Teacher).where(Teacher.username == username)
        teacher = session.exec(statement).first()
        if teacher and verify_password(password, teacher.password):
            return {"id": teacher.id, "name": teacher.name, "role": "teacher"}
        return None

    if role == "student":
        statement = select(Student).where(Student.username == username)
        student = session.exec(statement).first()
        if student and verify_password(password, student.password):
            return {
                "id": student.id,
                "name": student.name,
                "role": "student",
                "class_name": student.class_name,
            }
        return None

    return None


# ---------------------------------------------------------------------------
# Teacher CRUD
# ---------------------------------------------------------------------------
def get_teachers(session: Session) -> List[Teacher]:
    return session.exec(select(Teacher)).all()


def get_teacher(session: Session, teacher_id: int) -> Optional[Teacher]:
    return session.get(Teacher, teacher_id)


def create_teacher(session: Session, data: TeacherCreate) -> Teacher:
    teacher = Teacher(
        name=data.name,
        email=data.email,
        phone=data.phone,
        username=data.username,
        password=hash_password(data.password),
    )
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher


def update_teacher(
    session: Session, teacher_id: int, data: TeacherUpdate
) -> Optional[Teacher]:
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        return None
    update_data = data.dict(exclude_unset=True, exclude_none=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for key, value in update_data.items():
        setattr(teacher, key, value)
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher


def delete_teacher(session: Session, teacher_id: int) -> bool:
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        return False

    # Keep existing timetable rows valid when a teacher is removed.
    # Without this, the database can reject the delete because timetable
    # rows still reference the teacher via a foreign key.
    timetable_entries = session.exec(
        select(Timetable).where(Timetable.teacher_id == teacher_id)
    ).all()
    for entry in timetable_entries:
        entry.teacher_id = None
        session.add(entry)

    session.delete(teacher)
    session.commit()
    return True


# ---------------------------------------------------------------------------
# Student CRUD
# ---------------------------------------------------------------------------
def get_students(session: Session) -> List[Student]:
    return session.exec(select(Student)).all()


def get_student(session: Session, student_id: int) -> Optional[Student]:
    return session.get(Student, student_id)


def create_student(session: Session, data: StudentCreate) -> Student:
    student = Student(
        name=data.name,
        email=data.email,
        roll_number=data.roll_number,
        class_name=data.class_name,
        Semester=data.Semester,
        username=data.username,
        password=hash_password(data.password),
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def update_student(
    session: Session, student_id: int, data: StudentUpdate
) -> Optional[Student]:
    student = session.get(Student, student_id)
    if not student:
        return None
    update_data = data.dict(exclude_unset=True, exclude_none=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for key, value in update_data.items():
        setattr(student, key, value)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def delete_student(session: Session, student_id: int) -> bool:
    student = session.get(Student, student_id)
    if not student:
        return False
    session.delete(student)
    session.commit()
    return True


# ---------------------------------------------------------------------------
# Subject CRUD
# ---------------------------------------------------------------------------
def get_subjects(session: Session) -> List[Subject]:
    return session.exec(select(Subject)).all()


def get_subject(session: Session, subject_id: int) -> Optional[Subject]:
    return session.get(Subject, subject_id)


def create_subject(session: Session, data: SubjectCreate) -> Subject:
    subject = Subject(name=data.name, code=data.code)
    session.add(subject)
    session.commit()
    session.refresh(subject)
    return subject


def update_subject(
    session: Session, subject_id: int, data: SubjectUpdate
) -> Optional[Subject]:
    subject = session.get(Subject, subject_id)
    if not subject:
        return None
    update_data = data.dict(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(subject, key, value)
    session.add(subject)
    session.commit()
    session.refresh(subject)
    return subject


def delete_subject(session: Session, subject_id: int) -> bool:
    subject = session.get(Subject, subject_id)
    if not subject:
        return False
    session.delete(subject)
    session.commit()
    return True


# ---------------------------------------------------------------------------
# Timetable CRUD
# ---------------------------------------------------------------------------
def get_all_timetable(session: Session) -> List[Timetable]:
    return session.exec(select(Timetable)).all()


def get_timetable_by_class(session: Session, class_name: str) -> List[Timetable]:
    statement = select(Timetable).where(Timetable.class_name == class_name)
    return session.exec(statement).all()


def get_timetable_by_teacher(session: Session, teacher_id: int) -> List[Timetable]:
    statement = select(Timetable).where(Timetable.teacher_id == teacher_id)
    return session.exec(statement).all()


def has_teacher_conflict(
    session: Session,
    teacher_id: Optional[int],
    day: str,
    period: int,
    exclude_id: Optional[int] = None,
) -> bool:
    """
    Check whether the given teacher is already teaching another class at the
    same day and period. Used to prevent double-booking a teacher when
    creating or updating a timetable entry.
    Activities with no teacher assigned (teacher_id is None) can never
    conflict, since there is nobody to double-book.
    """
    if teacher_id is None:
        return False

    statement = select(Timetable).where(
        Timetable.teacher_id == teacher_id,
        Timetable.day == day,
        Timetable.period == period,
    )
    existing_entries = session.exec(statement).all()
    for entry in existing_entries:
        if entry.id != exclude_id:
            return True
    return False


def create_timetable_entry(session: Session, data: TimetableCreate) -> Timetable:
    entry = Timetable(
        class_name=data.class_name,
        semester=data.semester,
        day=data.day,
        period=data.period,
        start_time=data.start_time,
        end_time=data.end_time,
        subject_id=data.subject_id,
        teacher_id=data.teacher_id,
        activity=data.activity,
        room=data.room,
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def update_timetable_entry(
    session: Session, entry_id: int, data: TimetableUpdate
) -> Optional[Timetable]:
    entry = session.get(Timetable, entry_id)
    if not entry:
        return None
    update_data = data.dict(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(entry, key, value)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def delete_timetable_entry(session: Session, entry_id: int) -> bool:
    entry = session.get(Timetable, entry_id)
    if not entry:
        return False
    session.delete(entry)
    session.commit()
    return True
