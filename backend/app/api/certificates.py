from pathlib import Path
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.db.database import SessionLocal
from app.models.certificate import Certificate
from app.sat.certificate import read_certificate

router = APIRouter()

STORAGE = Path("/app/app/storage/certificates")
STORAGE.mkdir(parents=True, exist_ok=True)


@router.post("/certificates")
async def upload_certificate(
    rfc: str = Form(...),
    cer: UploadFile = File(...),
    key: UploadFile = File(...),
    password: str = Form(...)
):
    cer_path = STORAGE / f"{rfc}.cer"
    key_path = STORAGE / f"{rfc}.key"

    with cer_path.open("wb") as buffer:
        shutil.copyfileobj(cer.file, buffer)

    with key_path.open("wb") as buffer:
        shutil.copyfileobj(key.file, buffer)

    try:
        cert_info = read_certificate(str(cer_path))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No fue posible leer el certificado: {e}")

    db = SessionLocal()

    certificate = Certificate(
        rfc=rfc,
        cer_file=str(cer_path),
        key_file=str(key_path),
        serial_number=cert_info["serial_number"],
        subject=cert_info["subject"],
        issuer=cert_info["issuer"],
        not_before=cert_info["not_before"],
        not_after=cert_info["not_after"],
    )

    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    db.close()

    return {
        "id": certificate.id,
        "message": "uploaded",
        "certificate": cert_info,
    }

@router.get("/certificates")
def list_certificates():

    db = SessionLocal()

    certificates = db.query(Certificate).all()

    result = []

    for cert in certificates:
        result.append(
            {
                "id": cert.id,
                "rfc": cert.rfc,
                "serial_number": cert.serial_number,
                "not_after": cert.not_after,
                "created": cert.created,
            }
        )

    db.close()

    return result
