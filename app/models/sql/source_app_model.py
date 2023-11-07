from app.db.base import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.utils import generate_id, expand_dict


class SourceAppModel(Base):
    __tablename__ = "source_apps"

    id = Column(String(255), primary_key=True)
    app_name = Column(String(99), nullable=False)
    app_username = Column(String(99), nullable=False)
    app_enabled = Column(Boolean, default=False)
    app_linked = Column(Boolean, default=False)

    projects = relationship("ProjectModel", back_populates="source_app")

    def __init__(self, **kwargs):
        if "id" not in kwargs or kwargs["id"] is None:
            kwargs["id"] = generate_id(None, postfix=kwargs.get("app_name", ""))
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def to_dict(self, rel: dict = None) -> dict:
        value = {
            "id": self.id,
            "app_name": self.app_name,
            "app_username": self.app_username,
            "app_enabled": self.app_enabled,
            "app_linked": self.app_linked,
        }
        if rel:
            value = expand_dict(self, value, rel)
        return value
