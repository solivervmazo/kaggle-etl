from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.utils import generate_id, generate_token, expand_dict


class ProjectModel(Base):
    """
    Represents a project in the database.

    Attributes:
        id (int): The primary key ID of the project.
        source_app_id (int): The foreign key ID referencing the source app this project belongs to.
        project_path (str): The path of the project.
        project_title (str): The title of the project.
        source_app (SourceAppModel): The source app that this project belongs to.

    Methods:
        to_dict(): Returns a dictionary representation of the project model.
    """

    __tablename__ = "projects"
    __table_args__ = {"extend_existing": True}

    id = Column(String(255), primary_key=True)
    source_app_id = Column(String(255), ForeignKey("source_apps.id"), nullable=False)
    project_path = Column(String(255))
    project_title = Column(String(255))
    project_diagnosed = Column(Boolean, default=False)
    project_datasource_fetched = Column(Boolean, default=False)
    project_output_fetched = Column(Boolean, default=False)
    project_synced_date = Column(DateTime(True), server_default=func.now())
    project_token = Column(String(20))

    source_app = relationship("SourceAppModel", back_populates="projects")
    project_files = relationship(
        "PfileModel", back_populates="project", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        if "id" not in kwargs or kwargs["id"] is None:
            kwargs["id"] = generate_id(None, postfix=kwargs.get("project_title", ""))
        if "project_token" not in kwargs or kwargs["project_token"] is None:
            kwargs["project_token"] = generate_token(None)

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def to_dict(self, rel: dict = None) -> dict:
        value = {
            "id": self.id,
            "source_app_id": self.source_app_id,
            "project_path": self.project_path,
            "project_title": self.project_title,
            "project_diagnosed": self.project_diagnosed,
            "project_datasource_fetched": self.project_datasource_fetched,
            "project_output_fetched": self.project_output_fetched,
            "project_synced_date": self.project_synced_date,
            "project_token": self.project_token,
        }
        if rel:
            value = expand_dict(self, value, rel)
        return value
