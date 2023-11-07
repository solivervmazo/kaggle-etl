from sqlalchemy import Column, ForeignKey, String, Enum, JSON, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.utils import generate_id, expand_dict


class PfileModel(Base):
    __tablename__ = "pfiles"

    id = Column(String(255), primary_key=True)
    ref = Column(String(255), nullable=False)
    pfile_name = Column(String(255), nullable=False)
    pfile_url = Column(String(999))
    project_id = Column(String(255), ForeignKey("projects.id"), nullable=False)
    pfile_type = Column(Enum("datasource", "output", "schema"), nullable=False)
    pfile_of_id = Column(String(255))  # Self relationship
    # json value of columns and it's type
    pfile_col_types = Column(JSON(), default={})
    synced_date = Column(DateTime(True), server_default=func.now())
    token = Column(String(20), nullable=False)

    project = relationship("ProjectModel", back_populates="project_files")

    def __init__(self, **kwargs):
        if "id" not in kwargs or kwargs["id"] is None:
            kwargs["id"] = generate_id(None, postfix=kwargs.get("pfile_type", ""))
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def to_dict(self, rel: dict = None) -> dict:
        value = {
            "id": self.id,
            "ref": self.ref,
            "pfile_name": self.pfile_name,
            "pfile_url": self.pfile_url,
            "project_id": self.project_id,
            "pfile_type": self.pfile_type,
            "pfile_of_id": self.pfile_of_id,
            "pfile_col_types": self.pfile_col_types,
            "synced_date": self.synced_date,
            "token": self.token,
        }
        if rel:
            value = expand_dict(self, value, rel)
        return value
