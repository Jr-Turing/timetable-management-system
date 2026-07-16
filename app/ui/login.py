from nicegui import ui, app
from app.database import get_db_session
from app.services import timetable_service as service


@ui.page("/")
def login_page():

    ui.query("body").style("""
        background:linear-gradient(135deg,#eaf3ff,#ffffff);
    """)

    with ui.card().classes("absolute-center items-center").style("""
        width:420px;
        padding:28px;
        border-radius:20px;
        box-shadow:0 10px 35px rgba(0,0,0,.12);
        gap:8px;
    """):

        ui.image("app/assets/bbit_logo.png").style(
            "width:250px;margin-bottom:-8px;"
        )

        ui.label("Time Table Management System").classes(
            "text-2xl font-bold text-center w-full"
        ).style("margin:0")

        ui.label("Manage Timetables Efficiently").classes(
            "text-sm text-center text-grey-6 mb-2"
        )

        ui.separator()

        role = ui.select(
            {"admin":"Admin","teacher":"Teacher","student":"Student"},
            value="admin",
            label="Login As",
        ).props("outlined rounded").classes("w-full")

        username = ui.input(
            label="Username",
            placeholder="Enter username"
        ).props("outlined rounded clearable").classes("w-full")

        password = ui.input(
            label="Password",
            placeholder="Enter password",
            password=True,
            password_toggle_button=True,
        ).props("outlined rounded").classes("w-full")

        error = ui.label("").classes("text-red text-caption")

        def do_login():

            if not username.value or not password.value:
                error.text = "Please enter username and password."
                return

            with get_db_session() as session:
                user = service.authenticate_user(
                    session,
                    username.value.strip(),
                    password.value.strip(),
                    role.value,
                )

            if not user:
                error.text = "Invalid username or password."
                return

            app.storage.user.update({
                "logged_in": True,
                "role": user["role"],
                "user_id": user["id"],
                "name": user["name"],
            })

            if role.value == "student":
                app.storage.user["class_name"] = user.get("class_name")

            ui.navigate.to("/dashboard")

        ui.button(
            "LOGIN",
            icon="login",
            on_click=do_login,
        ).props("unelevated color=primary").classes(
            "w-full"
        ).style("""
            height:48px;
            border-radius:12px;
            font-weight:bold;
        """)

        ui.label("© 2026 TEAM BLUE • Version 1.0").classes(
            "text-xs text-grey-6 mt-2"
        )

        ui.add_head_html("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <style>body{font-family:'Poppins',sans-serif;}</style>
        """)

        ui.query("body").style("""
        background:
        radial-gradient(circle at top left,#dbeafe,#ffffff 40%),
        radial-gradient(circle at bottom right,#bfdbfe,#ffffff 40%);
        """)