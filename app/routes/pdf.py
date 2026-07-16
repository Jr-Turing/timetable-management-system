"""
routes/pdf.py

API endpoint to export a class timetable as a downloadable PDF file.
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.database import get_db_session
from app.services import pdf_service

router = APIRouter()


@router.get("/timetable/{class_name}")
def export_timetable_pdf(class_name: str):
    """Generate and return a PDF of the timetable for the given class."""
    with get_db_session() as session:
        pdf_buffer = pdf_service.generate_class_timetable_pdf(session, class_name)

    headers = {
        "Content-Disposition": f'attachment; filename="timetable_{class_name}.pdf"'
    }
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)
