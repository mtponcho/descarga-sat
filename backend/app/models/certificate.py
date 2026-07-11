from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from datetime import datetime

from app.db.database import Base


class Certificate(Base):

    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True)

    rfc = Column(String(13), nullable=False)

    cer_file = Column(String(255), nullable=False)

    key_file = Column(String(255), nullable=False)

    created = Column(DateTime, default=datetime.utcnow)
