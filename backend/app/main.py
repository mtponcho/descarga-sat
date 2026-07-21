from fastapi import FastAPI

from app.api.health import router as health_router

from app.api import reports

app = FastAPI(
    title="Descarga SAT API",
    version="0.1.0",
    description="Servicio para descarga masiva de CFDI del SAT"
)


app.include_router(
    health_router,
    tags=["health"]
)

from app.db.database import Base
from app.db.database import engine

Base.metadata.create_all(bind=engine)


from app.api.certificates import router as certificate_router

app.include_router(
    certificate_router,
    tags=["certificates"],
)


from app.api.downloads import router as download_router

app.include_router(
   download_router
)


app.include_router(
   reports.router
)
