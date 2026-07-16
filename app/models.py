"""
This file defines all the database tables for the Time Table Management
System using SQLModel. Each class below represents one table in PostgreSQL.
"""

from typing import Optional

from sqlmodel import SQLModel, Field


class Teacher(SQLModel, table=True):
    """Represents a teacher who can log in and view their own timetable."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    username: str = Field(unique=True, index=True)
    password: str  # stored as a hashed value, see utils/helper.py


class Student(SQLModel, table=True):
    """Represents a student who can log in and view their class timetable."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    roll_number: str
    class_name: str  # e.g. "10-A", used to match the correct timetable rows
    Semester: str # e.g. "6th Semester", used to match the correct timetable rows
    username: str = Field(unique=True, index=True)
    password: str  # stored as a hashed value, see utils/helper.py


class Subject(SQLModel, table=True):
    """Represents a subject that is taught, e.g. 'Mathematics'."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    code: str = Field(unique=True, index=True)


class Timetable(SQLModel, table=True):
    """
    Represents a single period/slot inside the weekly timetable.
    Most rows are a subject taught by a teacher, on one day, during one
    period, for one class. Some real college routines also include
    non-subject slots (e.g. "Mentoring", "Library", "TPO Class") which do
    not have a formal Subject - the optional `activity` field covers these.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    class_name: str  # e.g. "10-A" or "CS-6TH-SEM" - which class this belongs to
    semester: Optional[str] = None
    day: str  # "Monday", "Tuesday", ...
    period: int  # 1, 2, 3, ... the period number within that day
    start_time: str  # e.g. "09:00"
    end_time: str  # e.g. "09:45"

    # A normal academic period has a subject and a teacher. These are
    # optional so that non-subject activities (see `activity` below) can
    # be stored without needing a fake Subject row.
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
    teacher_id: Optional[int] = Field(default=None, foreign_key="teacher.id")

    # Free-text label used for non-subject slots (e.g. "Mentoring",
    # "Library", "TPO Class", "Research Based Learning") or as a short tag
    # attached to a subject period (e.g. "Remedial/Special"). Optional.
    activity: Optional[str] = None

    # Optional room/lab name, e.g. "ACD-408A" for a lab session.
    room: Optional[str] = None
