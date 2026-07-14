from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True)

    rfc = Column(String(13), nullable=False)

    cer_file = Column(String(255), nullable=False)
    key_file = Column(String(255), nullable=False)

    serial_number = Column(String(100), nullable=False)
    subject = Column(String(1000), nullable=False)
    issuer = Column(String(1000), nullable=False)
    not_before = Column(String(50), nullable=False)
    not_after = Column(String(50), nullable=False)

    created = Column(DateTime, default=datetime.utcnow)
