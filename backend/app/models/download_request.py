from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.database import Base


class DownloadRequest(Base):
    __tablename__ = "download_requests"

    id = Column(Integer, primary_key=True)

    certificate_id = Column(
        Integer,
        ForeignKey("certificates.id"),
        nullable=False,
    )

    request_id = Column(String(100))
    direction = Column(String(20))
    status = Column(String(30))

    created = Column(DateTime, default=datetime.utcnow)
