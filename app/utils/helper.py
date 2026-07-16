"""
utils/helper.py

Small helper functions and constants shared across the project.
"""

import hashlib

# The days of the week used to build the weekly timetable grid, and the
# add/edit forms in the Admin panel.
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Hardcoded admin login. This is a college project, so instead of building a
# full user-management system for the admin account, we keep a single admin
# username/password pair here.
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()


def hash_password(plain_password: str) -> str:
    """
    Turn a plain text password into a SHA-256 hash before storing it in the
    database. This avoids storing raw passwords in the database.
    (For a real production system you would use a stronger, salted
    algorithm such as bcrypt, but SHA-256 is fine for a college project.)
    """
    return hashlib.sha256(plain_password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain text password against a stored hash."""
    return hash_password(plain_password) == hashed_password
