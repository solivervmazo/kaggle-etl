from sqlalchemy import Column, Boolean, String, DateTime, Enum
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils import generate_id, expand_dict
from app.enums import LogType


class LogModel(Base):
    __tablename__ = "logs"

    id = Column(String(255), primary_key=True)
    log_category = Column(String(99), nullable=False)
    log_category1 = Column(String(99))
    log_category2 = Column(String(99))
    log_from_id = Column(String(255), nullable=False)
    log_from_root_id = Column(String(255), nullable=False)
    log_type = Column(Enum(LogType), nullable=False)
    log_msg = Column(String(255))
    log_date = Column(DateTime(True), server_default=func.now())
    log_resolved = Column(Boolean(), default=False)
    token = Column(String(99))

    def __init__(self, **kwargs):
        if "id" not in kwargs or kwargs["id"] is None:
            kwargs["id"] = generate_id(None, postfix=kwargs.get("log_category", ""))
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def to_dict(self, rel: dict = None) -> dict:
        value = {
            "id": self.id,
            "log_category": self.log_category,
            "log_category1": self.log_category1,
            "log_category2": self.log_category2,
            "log_from_id": self.log_from_id,
            "log_from_root_id": self.log_from_root_id,
            "log_type": LogType(self.log_type),
            "log_msg": self.log_msg,
            "log_date": self.log_date,
            "log_resolved": self.log_resolved,
            "token": self.token,
        }
        if rel:
            value = expand_dict(self, value, rel)
        return value
