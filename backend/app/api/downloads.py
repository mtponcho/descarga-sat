from datetime import date

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.download_service import DownloadService

from app.services.download_status_service import DownloadStatusService
from app.services.package_service import PackageService


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

@router.get("/downloads/{download_id}/status")
def download_status(
    download_id: int,
    password: str,
    db: Session = Depends(get_db),
):

    service = DownloadStatusService(db)

    return service.get_status(
        download_id,
        password,
    )

@router.get("/downloads/{download_id}/download")
def download_packages(
    download_id: int,
    password: str,
    db: Session = Depends(get_db),
):

    service = PackageService(db)

    return service.download_all(
        download_id,
        password,
    )
