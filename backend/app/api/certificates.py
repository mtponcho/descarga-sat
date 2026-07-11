from pathlib import Path
import shutil

from fastapi import APIRouter
from fastapi import File
from fastapi import Form
from fastapi import UploadFile

router = APIRouter()

STORAGE = Path("/app/app/storage/certificates")

STORAGE.mkdir(parents=True, exist_ok=True)


@router.post("/certificates")
async def upload_certificate(
    rfc: str = Form(...),
    cer: UploadFile = File(...),
    key: UploadFile = File(...),
):

    cer_path = STORAGE / f"{rfc}.cer"
    key_path = STORAGE / f"{rfc}.key"

    with cer_path.open("wb") as buffer:
        shutil.copyfileobj(cer.file, buffer)

    with key_path.open("wb") as buffer:
        shutil.copyfileobj(key.file, buffer)

    return {
        "message": "uploaded",
        "rfc": rfc,
    }
