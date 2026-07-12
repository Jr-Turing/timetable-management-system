<div align="center">

# 📅 Time Table Management System (TMS)

### A Modern University Timetable Management System built with **FastAPI**, **NiceGUI**, **SQLModel**, and **PostgreSQL**

<p align="center">

<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
<img src="https://img.shields.io/badge/NiceGUI-Modern_UI-blue?style=for-the-badge">
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
<img src="https://img.shields.io/badge/SQLModel-ORM-orange?style=for-the-badge">
<img src="https://img.shields.io/badge/ReportLab-PDF-red?style=for-the-badge">
<img src="https://img.shields.io/badge/MIT-License-green?style=for-the-badge">
<img src="https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge">

</p>

A role-based timetable management system that helps educational institutions efficiently manage class schedules, teachers, students, and subjects through an intuitive web interface.

---

### 🔗 Quick Links

[✨ Features](#-features) •
[🛠 Tech Stack](#-technology-stack) •
[🏗 Architecture](#-system-architecture) •
[🚀 Installation](#-installation) •
[📂 Project Structure](#-project-structure) •
[👥 Team](#-team-members)

</div>

---

# 📖 Project Overview

The **Time Table Management System (TMS)** is a full-stack web application developed to simplify timetable management for educational institutions.

Instead of manually preparing class schedules, administrators can efficiently create and manage timetables while teachers and students can access their schedules through dedicated dashboards.

The application is built using modern Python technologies including **FastAPI**, **NiceGUI**, **SQLModel**, and **PostgreSQL**.

---

# ✨ Features

## 🔐 Login Page

<table>
<tr>
<td width="50%" valign="top">

### Authentication

- Secure Login
- Role-based Authentication
- Admin Login
- Teacher Login
- Student Login
- Password Validation
- User-friendly Interface

</td>

<td width="50%" align="center">

<img src="Docs/login_page.png" alt="Login Page"/>

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top">

## 👨‍💼 Admin

- Secure Login
- Dashboard
- Add / Edit / Delete Teachers
- Add / Edit / Delete Students
- Manage Subjects
- Create Timetables
- Update Timetables
- Delete Timetables
- Export Timetable as PDF

</td>

<td width="50%" align="center">

<img src="Docs/admin.png" />

</td>
</tr>
</table>

## 👨‍🏫 Teacher
<table>
<tr>
<td width="50%" valign="top">

- Secure Login
- View Personal Timetable
- Semester-wise Timetable Filter
- Send Notice *(UI Only)*

</td>

<td width="%"50 align="center">

<img src="Docs/teacher.png" />

</td>
</tr>
</table>

## 👨‍🎓 Student
<table>
<tr>
<td width="50%" valign="top">
  
- Secure Login
- View Class Routine
- Export Timetable as PDF

</td>

<td width="50%" align="center">

<img src="Docs/student.png" />

</td>
</tr>
</table>


## 📄 PDF Export

- Professional timetable layout
- Landscape A4 format
- Weekly schedule
- Printable PDF

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python 3.12 |
| Backend Framework | FastAPI |
| Frontend Framework | NiceGUI |
| ORM | SQLModel |
| Database | PostgreSQL |
| PDF Generator | ReportLab |
| Package Manager | uv |
| API Documentation | Swagger UI |

---

# 🏗 System Architecture

```
                    +----------------------+
                    |      NiceGUI UI      |
                    |      (Frontend)      |
                    +----------+-----------+
                               |
                               |
                      FastAPI Application
                           (Backend)
                               |
              +----------------+----------------+
              |                                 |
      Business Services                     API Routes
              |                                 |
              +----------------+----------------+
                               |
                         SQLModel ORM
                               |
                      PostgreSQL Database
```

---

# 📂 Project Structure

```text
TMS/
│
├── app/
│   │
│   ├── assets/                    # Frontend Assets
│   │   ├── bbit_logo.png          # BBIT Logo used in UI
│   │   └── ...
│   │
│   ├── ui/                        # Frontend (NiceGUI Pages)
│   │   ├── login.py
│   │   ├── dashboard.py
│   │   ├── admin.py
│   │   ├── teacher.py
│   │   ├── student.py
│   │   └── timetable.py
│   │
│   ├── routes/                    # Backend API Routes
│   │   ├── admin.py
│   │   ├── teacher.py
│   │   ├── student.py
│   │   ├── timetable.py
│   │   └── pdf.py
│   │
│   ├── services/                  # Backend Business Logic
│   │   ├── timetable_service.py
│   │   └── pdf_service.py
│   │
│   ├── database.py                # Database Configuration
│   ├── models.py                  # SQLModel Models
│   ├── schemas.py                 # Request / Response Schemas
│   ├── seed_data.py               # Demo Data Generator
│   ├── utils/                     # Helper Functions
│   └── main.py                    # Application Entry Point
│
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── README.md
└── .env
```

---

# 🖥 Frontend

The frontend is built using **NiceGUI**, allowing responsive and interactive web pages directly in Python.

### Frontend Components

- Login Page
- Admin Dashboard
- Teacher Dashboard
- Student Dashboard
- Timetable View
- Forms
- Navigation
- PDF Download Buttons
- BBIT Branding (Logo)

```
⚙ Backend

The backend is powered by **FastAPI**.

### Backend Responsibilities

- Authentication
- CRUD Operations
- Timetable Management
- Subject Management
- Teacher Management
- Student Management
- PDF Generation
- Database Operations
- API Endpoints

🗄 Database

The application uses **PostgreSQL** together with **SQLModel ORM**.

Current Models include

- Teachers
- Students
- Subjects
- Timetable
```

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Jr-turing/timetable-management-system.git
cd timetable-management-system
```

---

## 2️⃣ Install uv

```bash
pip install uv
```

---

## 3️⃣ Create Virtual Environment

```bash
uv venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
uv sync
```

---

## 5️⃣ Configure Environment Variables

Create a `.env` file

```env
DATABASE_URL=postgresql://username:password@localhost:5432/timetable_db

SECRET_KEY=your-secret-key
```

---

## 6️⃣ Seed Database

```bash
python -m app.seed_data
```

---

## 7️⃣ Run Application

```bash
uv run python -m app.main
```

or

```bash
python -m app.main
```

---

# 🌐 Access the Application

| Service | URL |
|----------|-----|
| Application | http://127.0.0.1:8000 |
| Swagger API | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

# 🚧 Future Improvements

- JWT Authentication
- Role-Based Access Control (RBAC)
- Teacher Notice Backend
- Timetable Conflict Detection
- Dashboard Analytics
- Docker Support
- CI/CD Pipeline
- Dark Mode

---

## 👥 Team Members

| Name | Role |
|------|------|
| **[Parthapratim Rana](https://github.com/partha811)** | Project Lead/ Backend Developer |
| **[Arvind Kumar](https://github.com/Jr-Turing)** | Backend Developer |
| **[Sumit Kumar](https://github.com/sumitkumar-04)** | Frontend Developer |
| **[Priya Ghosh](https://github.com/priya98000ghosh-lab)** | Frontend Developer |
| **[Shubham Srivastava](https://github.com/shubhamsrivastava08)** | Testing & Documentation |
---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

## ⭐ Acknowledgment

This project was developed as part of an academic initiative to modernize university timetable management through automation and structured system design. Special thanks to our faculty advisor and all contributing team members.

---

<div align="center">

**Made with ❤️ by Team Blue | BBIT**

⭐ *If you found this project helpful, please give it a star!* ⭐

</div>
