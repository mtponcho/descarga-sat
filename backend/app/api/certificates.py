from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.certificate_service import CertificateService
from app.models.certificate import Certificate

router = APIRouter()


@router.post("/certificates")
async def upload_certificate(
    cer: UploadFile = File(...),
    key: UploadFile = File(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    service = CertificateService(db)

    return service.register(
        cer_file=cer,
        key_file=key,
        password=password,
    )


@router.get("/certificates")
def list_certificates(
    db: Session = Depends(get_db),
):

    certificates = db.query(
        Certificate
    ).all()

    return [
        {
            "id": cert.id,
            "taxpayer_id": cert.taxpayer_id,
            "serial_number": cert.serial_number,
            "not_after": cert.not_after,
            "created": cert.created,
        }
        for cert in certificates
    ]
