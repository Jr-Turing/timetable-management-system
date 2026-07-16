from sqlmodel import Session, select

from app.database import engine, create_db_and_tables
from app.models import Teacher, Student, Subject, Timetable
from app.utils.helper import hash_password

# The class this routine belongs to (B.Tech 3rd Year, 6th Sem, CS, ACD 406).
CLASS_NAME = "CSE-CS"

# Default password used for every seeded teacher/student login. The Admin
# can change these later from the Admin dashboard.
DEFAULT_TEACHER_PASSWORD = "teacher123"
DEFAULT_STUDENT_PASSWORD = "student123"

# ---------------------------------------------------------------------------
# Subjects taken from the routine's "SUBJECT NAME / SUBJECT CODE" table.
# ---------------------------------------------------------------------------
SUBJECTS = [
    {"name": "Database Management Systems", "code": "PCC CS 603"},
    {"name": "Cryptography and Network Security", "code": "PCC CS 601"},
    {"name": "Infrastructure Security", "code": "PCCCS602"},
    {"name": "Ethical Hacking", "code": "PECICB601C"},
    {"name": "Organizational Behavior", "code": "OECICB601D"},
    {"name": "Research Methodology", "code": "PROJ-CS601"},
    {"name": "Network Security Lab", "code": "PCCCS691"},
    {"name": "DBMS Lab", "code": "PCC CS 692"},
]

# ---------------------------------------------------------------------------
# Teachers taken from the routine's "FACULTY LIST". The `initials` value
# matches the short code used throughout the routine grid (e.g. "MYA").
# ---------------------------------------------------------------------------
TEACHERS = [
    {"initials": "MYA", "name": "Dr. Munshi Yusuf Alam", "username": "mya"},
    {"initials": "ND", "name": "Mrs. Nivedita Das", "username": "nd"},
    {"initials": "KB", "name": "Mr. Kaustav Bandyopadhyay", "username": "kb"},
    {"initials": "AM", "name": "Mr. Arindam Mitra", "username": "am"},
    {"initials": "SGS", "name": "Dr. Shefalika Ghosh Samaddar", "username": "sgs"},
    {"initials": "AP", "name": "Mr. Ashis Pramanick", "username": "ap"},
    {"initials": "PM", "name": "Mr. Pradip Kumar Mandal", "username": "pm"},
    {"initials": "MR", "name": "Ms. Mili Mitra Roy", "username": "mr"},
    {"initials": "SG", "name": "Ms. Snigdha Giri", "username": "sg"},
    {"initials": "TSR", "name": "Ms. Tanaya Singha Roy", "username": "tsr"},
    {"initials": "TM", "name": "Ms. Trisha Mondal", "username": "tm"},
]

# The 8 daily periods and their clock times, as printed on the routine.
PERIOD_TIMES = {
    1: ("09:00", "09:50"),
    2: ("09:50", "10:40"),
    3: ("10:40", "11:30"),
    4: ("11:30", "12:20"),
    # 12:20 - 13:00 is the lunch break (not a teaching period)
    5: ("13:00", "13:50"),
    6: ("13:50", "14:40"),
    7: ("14:40", "15:30"),
    8: ("15:30", "16:20"),
}

# ---------------------------------------------------------------------------
# The full weekly routine, transcribed period-by-period from the PDF.
# Each entry is a dict describing one period:
#   day, period, subject (code from SUBJECTS or None), teacher (initials
#   from TEACHERS or None), activity (free text or None), room (or None)
# ---------------------------------------------------------------------------
ROUTINE = [
    # ---------------- Monday ----------------
    {"day": "Monday", "period": 1, "subject": "PCC CS 603", "teacher": "MYA"},
    {"day": "Monday", "period": 2, "subject": "PECICB601C", "teacher": "SGS"},
    {"day": "Monday", "period": 3, "subject": "PCC CS 601", "teacher": "KB"},
    {"day": "Monday", "period": 4, "subject": "PCCCS602", "teacher": "SGS"},
    {"day": "Monday", "period": 5, "activity": "Research Based Learning", "teacher": "MYA"},
    {"day": "Monday", "period": 6, "subject": "PCC CS 601", "teacher": "KB"},
    {"day": "Monday", "period": 7, "activity": "TPO Class"},
    {"day": "Monday", "period": 8, "activity": "TPO Class"},
    # ---------------- Tuesday ----------------
    {"day": "Tuesday", "period": 1, "subject": "PROJ-CS601", "teacher": "TSR"},
    {"day": "Tuesday", "period": 2, "subject": "PCCCS602", "teacher": "SGS"},
    {"day": "Tuesday", "period": 3, "subject": "PCCCS602", "teacher": "SGS"},
    {"day": "Tuesday", "period": 4, "subject": "PECICB601C", "teacher": "SGS"},
    {"day": "Tuesday", "period": 5, "activity": "Gate Preparatory Class", "teacher": "ND"},
    {"day": "Tuesday", "period": 6, "subject": "OECICB601D", "teacher": "SG"},
    {"day": "Tuesday", "period": 7, "subject": "PECICB601C", "teacher": "SGS", "activity": "Remedial"},
    {"day": "Tuesday", "period": 8, "activity": "Library"},
    # ---------------- Wednesday ----------------
    {"day": "Wednesday", "period": 1, "activity": "Gate Preparatory Class", "teacher": "ND"},
    {"day": "Wednesday", "period": 2, "subject": "PCC CS 603", "teacher": "MYA"},
    {"day": "Wednesday", "period": 3, "subject": "PECICB601C", "teacher": "SGS"},
    {"day": "Wednesday", "period": 4, "subject": "OECICB601D", "teacher": "PM"},
    {"day": "Wednesday", "period": 5, "subject": "PCCCS691", "teacher": "SGS", "room": "ACD-408B"},
    {"day": "Wednesday", "period": 6, "subject": "PCCCS691", "teacher": "SGS", "room": "ACD-408B"},
    {"day": "Wednesday", "period": 7, "subject": "PCCCS691", "teacher": "SGS", "room": "ACD-408B"},
    {"day": "Wednesday", "period": 8, "subject": "PCCCS602", "teacher": "SGS", "activity": "Remedial/Special"},
    # ---------------- Thursday ----------------
    {"day": "Thursday", "period": 1, "subject": "OECICB601D", "teacher": "MR"},
    {"day": "Thursday", "period": 2, "subject": "PCC CS 603", "teacher": "MYA"},
    {"day": "Thursday", "period": 3, "activity": "Problem Based Learning", "teacher": "TM"},
    {"day": "Thursday", "period": 4, "subject": "PCC CS 601", "teacher": "KB"},
    {"day": "Thursday", "period": 5, "subject": "PROJ-CS601", "teacher": "TSR"},
    {"day": "Thursday", "period": 6, "activity": "Research Based Learning", "teacher": "AP"},
    {"day": "Thursday", "period": 7, "activity": "Mentoring"},
    {"day": "Thursday", "period": 8, "subject": "PCC CS 603", "teacher": "MYA", "activity": "Remedial/Special"},
    # ---------------- Friday ----------------
    {"day": "Friday", "period": 1, "subject": "PROJ-CS601", "teacher": "TSR"},
    {"day": "Friday", "period": 2, "subject": "PCC CS 692", "teacher": "MYA", "room": "ACD-408A"},
    {"day": "Friday", "period": 3, "subject": "PCC CS 692", "teacher": "MYA", "room": "ACD-408A"},
    {"day": "Friday", "period": 4, "subject": "PCC CS 692", "teacher": "MYA", "room": "ACD-408A"},
    {"day": "Friday", "period": 5, "activity": "Mentoring"},
    {"day": "Friday", "period": 6, "activity": "Soft Skill (UZ)"},
    {"day": "Friday", "period": 7, "subject": "PCC CS 601", "teacher": "KB", "activity": "Remedial/Special"},
    {"day": "Friday", "period": 8, "subject": "PCC CS 601", "teacher": "KB", "activity": "Remedial/Special"},
]


def seed() -> None:
    """Insert the subjects, teachers, demo student and routine if not already present."""
    create_db_and_tables()

    with Session(engine) as session:
        # ------------------------------------------------------------------
        # Skip everything if this class has already been seeded, so running
        # this script twice does not create duplicate rows.
        # ------------------------------------------------------------------
        existing = session.exec(
            select(Timetable).where(Timetable.class_name == CLASS_NAME)
        ).first()
        if existing:
            print(f"Class '{CLASS_NAME}' already has timetable data. Skipping seeding.")
            return

        # ------------------------------------------------------------------
        # Subjects: create any that don't already exist (matched by code).
        # ------------------------------------------------------------------
        subject_id_by_code = {}
        for item in SUBJECTS:
            existing_subject = session.exec(
                select(Subject).where(Subject.code == item["code"])
            ).first()
            if existing_subject:
                subject_id_by_code[item["code"]] = existing_subject.id
                continue
            subject = Subject(name=item["name"], code=item["code"])
            session.add(subject)
            session.commit()
            session.refresh(subject)
            subject_id_by_code[item["code"]] = subject.id

        # ------------------------------------------------------------------
        # Teachers: create any that don't already exist (matched by username).
        # ------------------------------------------------------------------
        teacher_id_by_initials = {}
        for item in TEACHERS:
            existing_teacher = session.exec(
                select(Teacher).where(Teacher.username == item["username"])
            ).first()
            if existing_teacher:
                teacher_id_by_initials[item["initials"]] = existing_teacher.id
                continue
            teacher = Teacher(
                name=item["name"],
                email=f"{item['username']}@bbit.edu",
                phone="0000000000",
                username=item["username"],
                password=hash_password(DEFAULT_TEACHER_PASSWORD),
            )
            session.add(teacher)
            session.commit()
            session.refresh(teacher)
            teacher_id_by_initials[item["initials"]] = teacher.id

        # ------------------------------------------------------------------
        # Demo student in this class, so you can log in as a student too.
        # ------------------------------------------------------------------
        existing_student = session.exec(
            select(Student).where(Student.username == "student1")
        ).first()
        if not existing_student:
            student = Student(
                name="Demo Student",
                email="student1@bbit.edu",
                roll_number="01",
                class_name=CLASS_NAME,
                username="student1",
                password=hash_password(DEFAULT_STUDENT_PASSWORD),
            )
            session.add(student)
            session.commit()

        # ------------------------------------------------------------------
        # Timetable entries: one row per period, using the lookups above.
        # ------------------------------------------------------------------
        for slot in ROUTINE:
            start_time, end_time = PERIOD_TIMES[slot["period"]]
            subject_id = subject_id_by_code.get(slot.get("subject")) if slot.get("subject") else None
            teacher_id = teacher_id_by_initials.get(slot.get("teacher")) if slot.get("teacher") else None

            entry = Timetable(
                class_name=CLASS_NAME,
                day=slot["day"],
                period=slot["period"],
                start_time=start_time,
                end_time=end_time,
                subject_id=subject_id,
                teacher_id=teacher_id,
                activity=slot.get("activity"),
                room=slot.get("room"),
            )
            session.add(entry)

        session.commit()
        print(f"Seeded {len(ROUTINE)} timetable entries for class '{CLASS_NAME}'.")
        print(f"Created {len(SUBJECTS)} subjects and {len(TEACHERS)} teachers.")
        print(
            f"Demo student login -> username: student1, password: {DEFAULT_STUDENT_PASSWORD}"
        )
        print(f"All teacher logins use password: {DEFAULT_TEACHER_PASSWORD}")


if __name__ == "__main__":
    seed()
