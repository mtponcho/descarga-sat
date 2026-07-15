from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.database import Base


class DownloadPackage(Base):

    __tablename__ = "download_packages"

    id = Column(
        Integer,
        primary_key=True,
    )

    download_request_id = Column(
        Integer,
        ForeignKey("download_requests.id"),
        nullable=False,
    )

    package_id = Column(
        String(255),
        nullable=False,
    )

    file_path = Column(
        String(500),
        nullable=False,
    )

    created = Column(
        DateTime,
        default=datetime.utcnow,
    )
