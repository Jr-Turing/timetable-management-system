from typing import Optional

from sqlmodel import SQLModel


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------
class LoginRequest(SQLModel):
    username: str
    password: str
    role: str  # "admin", "teacher" or "student"


# ---------------------------------------------------------------------------
# Teacher
# ---------------------------------------------------------------------------
class TeacherCreate(SQLModel):
    name: str
    email: str
    phone: str
    username: str
    password: str


class TeacherUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------
class StudentCreate(SQLModel):
    name: str
    email: str
    roll_number: str
    class_name: str
    Semester: str
    username: str
    password: str


class StudentUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    roll_number: Optional[str] = None
    class_name: Optional[str] = None
    Semester: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


# ---------------------------------------------------------------------------
# Subject
# ---------------------------------------------------------------------------
class SubjectCreate(SQLModel):
    name: str
    code: str


class SubjectUpdate(SQLModel):
    name: Optional[str] = None
    code: Optional[str] = None


# ---------------------------------------------------------------------------
# Timetable
# ---------------------------------------------------------------------------
class TimetableCreate(SQLModel):
    class_name: str
    semester: Optional[str] = None
    day: str
    period: int
    start_time: str
    end_time: str
    # subject_id/teacher_id are optional so that non-subject activities
    # (e.g. "Mentoring", "Library", "TPO Class") can be stored too.
    subject_id: Optional[int] = None
    teacher_id: Optional[int] = None
    activity: Optional[str] = None
    room: Optional[str] = None


class TimetableUpdate(SQLModel):
    class_name: Optional[str] = None
    semester: Optional[str] = None
    day: Optional[str] = None
    period: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    subject_id: Optional[int] = None
    teacher_id: Optional[int] = None
    activity: Optional[str] = None
    room: Optional[str] = None
