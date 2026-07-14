from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Taxpayer(Base):
    __tablename__ = "taxpayers"

    id = Column(Integer, primary_key=True)

    rfc = Column(
        String(13),
        unique=True,
        nullable=False,
        index=True,
    )

    certificates = relationship(
        "Certificate",
        back_populates="taxpayer",
    )

    created = Column(
        DateTime,
        default=datetime.utcnow,
    )
