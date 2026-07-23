from datetime import date

from fastapi import APIRouter, Depends, Form
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.download_service import DownloadService
from app.services.download_status_service import DownloadStatusService
from app.services.package_service import PackageService
from app.services.cfdi_service import CfdiService
from app.services.cfdi_query_service import CfdiQueryService


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


@router.get(
    "/downloads/{download_id}/download",
    include_in_schema=False,
)
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


@router.post(
    "/downloads/{download_id}/process",
    include_in_schema=False,
)
def process_download(
    download_id: int,
    db: Session = Depends(get_db),
):

    service = CfdiService(db)

    return service.process(download_id)


@router.get(
    "/downloads/{download_id}/summary",
    include_in_schema=False,
)
def cfdi_summary(
    download_id: int,
    db: Session = Depends(get_db),
):

    service = CfdiQueryService(db)

    return service.summary(download_id)


@router.get(
    "/downloads/{download_id}/summary/tsv",
    response_class=PlainTextResponse,
    include_in_schema=False,
)
def cfdi_summary_tsv(
    download_id: int,
    db: Session = Depends(get_db),
):

    service = CfdiQueryService(db)

    return service.summary_tsv(download_id)
