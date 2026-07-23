from datetime import date

from fastapi import APIRouter, Depends, Form
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.report_service import ReportService


router = APIRouter()


@router.post(
    "/reports/iva",
    summary="Generar reporte de IVA trasladado",
    description="""
Ejecuta automáticamente todo el proceso de descarga de CFDI:

- Solicita la descarga al SAT.
- Espera hasta que la solicitud esté lista.
- Descarga todos los paquetes disponibles.
- Procesa los XML contenidos en los ZIP.
- Calcula el IVA trasladado.
- Devuelve una tabla TSV lista para copiar y pegar en Excel.
""",
    response_description="Tabla TSV con el IVA trasladado por CFDI",
    response_class=PlainTextResponse,
)
def iva_report(
    certificate_id: int = Form(
        ...,
        description="ID del certificado previamente registrado",
        example=1,
    ),
    password: str = Form(
        ...,
        description="Contraseña de la llave privada (.key)",
    ),
    start_date: date = Form(
        ...,
        description="Fecha inicial del período (AAAA-MM-DD)",
        example="2026-06-01",
    ),
    end_date: date = Form(
        ...,
        description="Fecha final del período (AAAA-MM-DD)",
        example="2026-06-30",
    ),
    db: Session = Depends(get_db),
):

    service = ReportService(db)

    return service.generate_iva_report(
        certificate_id,
        password,
        start_date,
        end_date,
    )
