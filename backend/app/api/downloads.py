from datetime import date

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.download_service import DownloadService

from app.services.download_status_service import DownloadStatusService
from app.services.package_service import PackageService

from app.services.cfdi_service import CfdiService

from app.services.cfdi_query_service import CfdiQueryService

from fastapi.responses import PlainTextResponse
from app.models.cfdi_document import CfdiDocument
from app.models.download_package import DownloadPackage


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

@router.post("/downloads/{download_id}/process")
def process_download(
    download_id: int,
    db: Session = Depends(get_db),
):

    service = CfdiService(db)

    return service.process(download_id)

@router.get("/downloads/{download_id}/summary")
def cfdi_summary(
    download_id: int,
    db: Session = Depends(get_db),
):

    service = CfdiQueryService(db)

    return service.summary(download_id)

@router.get(
    "/downloads/{download_id}/summary/tsv",
    response_class=PlainTextResponse,
)
def cfdi_summary_tsv(
    download_id: int,
    db: Session = Depends(get_db),
):

    rows = (
        db.query(CfdiDocument)
        .join(
            DownloadPackage,
            CfdiDocument.download_package_id == DownloadPackage.id
        )
        .filter(
            DownloadPackage.download_request_id == download_id
        )
        .order_by(
            CfdiDocument.fecha
        )
        .all()
    )

    output = []

    output.append(
        "Fecha\tRFC\tTotal\tIVA"
    )

    total = 0
    iva = 0

    for cfdi in rows:

        output.append(
            f"{cfdi.fecha.date()}\t"
            f"{cfdi.rfc_emisor}\t"
            f"{cfdi.total}\t"
            f"{cfdi.iva_trasladado}"
        )

        total += cfdi.total
        iva += cfdi.iva_trasladado


    output.append(
        f"TOTAL\t\t{total}\t{iva}"
    )

    return "\n".join(output)
