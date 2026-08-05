from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UniqueConstraint,
)

from app.db.database import Base


class DownloadPackageDocument(Base):

    __tablename__ = "download_package_documents"

    id = Column(
        Integer,
        primary_key=True,
    )

    download_package_id = Column(
        Integer,
        ForeignKey("download_packages.id"),
        nullable=False,
    )

    cfdi_document_id = Column(
        Integer,
        ForeignKey("cfdi_documents.id"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "download_package_id",
            "cfdi_document_id",
            name="uq_download_package_document",
        ),
    )
