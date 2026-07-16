"""
ui/dashboard.py

A small router page: after logging in, the user is sent here first, and
this page immediately redirects them to the correct dashboard based on
their role (admin/teacher/student).
"""

from nicegui import ui, app


@ui.page("/dashboard")
def dashboard_page():
    """Redirect the logged-in user to the page that matches their role."""
    if not app.storage.user.get("logged_in"):
        ui.navigate.to("/")
        return

    role = app.storage.user.get("role")
    if role == "admin":
        ui.navigate.to("/admin")
    elif role == "teacher":
        ui.navigate.to("/teacher")
    elif role == "student":
        ui.navigate.to("/student")
    else:
        ui.navigate.to("/")
