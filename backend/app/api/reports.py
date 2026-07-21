from datetime import date

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.report_service import ReportService

router = APIRouter()


@router.post("/reports/iva")
def iva_report(
    certificate_id: int = Form(...),
    password: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    db: Session = Depends(get_db),
):

    service = ReportService(db)

    return service.generate_iva_report(
        certificate_id,
        password,
        start_date,
        end_date,
    )
