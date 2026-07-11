from fastapi import FastAPI

from app.api.health import router as health_router


app = FastAPI(
    title="Descarga SAT API",
    version="0.1.0",
    description="Servicio para descarga masiva de CFDI del SAT"
)


app.include_router(
    health_router,
    tags=["health"]
)
