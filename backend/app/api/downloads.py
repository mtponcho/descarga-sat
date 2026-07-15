from datetime import date

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.download_service import DownloadService


router = APIRouter()


@router.post("/downloads")
def create_download(
    certificate_id: int = Form(...),
    password: str = Form(...),
    direction: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    db: Session = Depends(get_db),
):

    service = DownloadService(db)

    return service.create(
        certificate_id,
        password,
        direction,
        start_date,
        end_date,
    )
