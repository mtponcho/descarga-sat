from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Numeric,
)

from app.db.database import Base


class CfdiDocument(Base):

    __tablename__ = "cfdi_documents"

    id = Column(
        Integer,
        primary_key=True,
    )

    download_package_id = Column(
        Integer,
        ForeignKey("download_packages.id"),
        nullable=False,
    )

    uuid = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    rfc_emisor = Column(
        String(20),
        nullable=False,
    )

    fecha = Column(
        DateTime,
        nullable=False,
    )

    total = Column(
        Numeric(12, 2),
        nullable=False,
    )

    iva_trasladado = Column(
        Numeric(12, 2),
        nullable=False,
    )

    xml_file = Column(
        String(500),
        nullable=False,
    )

    created = Column(
        DateTime,
        default=datetime.utcnow,
    )
