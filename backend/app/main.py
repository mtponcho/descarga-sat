from fastapi import FastAPI
from app.api.health import router as health_router
from app.api import reports
from app.api.certificates import router as certificate_router
from app.api.downloads import router as download_router
from app.db.database import engine
from app.db.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Descarga SAT API",
    version="0.1.0",
    description="Servicio para descarga masiva de CFDI del SAT",
)

app.include_router(
    health_router,
    tags=["Sistema"],
)

app.include_router(
    certificate_router,
    tags=["Certificados"],
)

app.include_router(
   download_router,
   tags=["Descargas"],
)

app.include_router(
   reports.router,
   tags=["Reportes"],
)
