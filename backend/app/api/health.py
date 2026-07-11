from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import SessionLocal

router = APIRouter()


@router.get("/health")
def health():

    try:
        db = SessionLocal()

        db.execute(text("SELECT 1"))

        db.close()

        database = "up"

    except Exception as e:
        database = str(e)

    return {
        "status": "ok",
        "database": database
    }
