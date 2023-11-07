from app.services.core.logger_service import LoggerService
from sqlalchemy import Engine, select
from app.models import SourceAppModel, ProjectModel
from app.enums import LogType

LOG_CATEGORY = "project"


class ProjectService(LoggerService):
    def __init__(self, db_engine: Engine, token: str = None, session=None) -> None:
        super().__init__(db_engine=db_engine, token=token)
        if session:
            self._create_session(session)

    def fetch_projects(self, id: str = None, rel: dict = None):
        try:
            query = (
                select(ProjectModel)
                .join(SourceAppModel, ProjectModel.source_app_id == SourceAppModel.id)
                .where(SourceAppModel.app_linked == True)
            )
            if id is None:
                result = self._session.scalars(query).all()
            else:
                query = query.where(ProjectModel.id == id)
                result = self._session.scalar(query)
            return self._response(200, data=result)
        except Exception as e:
            return self._response(500, error=str(e))
        finally:
            pass

    def insert_projects(self, projects: list = [], log_action: bool = True):
        try:
            self._session.add_all(projects)
            (logger, logs) = self._create_log_service()
            for project in self._models_to_dict(models=projects):
                (project_id, source_app_id) = (
                    project.get("id"),
                    project.get("source_app_id"),
                )
                logs.append(
                    self._create_log(
                        log_category=LOG_CATEGORY,
                        log_from_id=project_id,
                        log_type=LogType.INFO,
                        log_from_root_id=source_app_id,
                        log_msg=f"Project with id {project_id} added.",
                        log_resolved=True,
                    )
                )
                logs.append(
                    self._create_log(
                        log_category=LOG_CATEGORY,
                        log_from_id=project_id,
                        log_type=LogType.WARN,
                        log_from_root_id=source_app_id,
                        log_category1="undiagnosed",
                        log_msg=f"Project with id {project_id} undiagnosed.",
                        log_resolved=False,
                    )
                )

            if self._logging:
                logger.insert_log(logs=logs)
            return self._response(200, self._models_to_dict(models=projects))
        except Exception as e:
            return self._response(500, error=str(e))
        finally:
            pass

    def update_project(self, id: str, updates: dict, rel: dict = None, log_action=True):
        try:
            query = (
                select(ProjectModel)
                .join(ProjectModel.source_app)
                .where(SourceAppModel.app_linked == True)
                .where(ProjectModel.id == id)
            )
            project = self._session.scalar(query)
            if not project:
                raise Exception("Project not found")
            for k in updates:
                if hasattr(project, k):
                    setattr(project, k, updates.get(k))

            return {"status": 200, "data": project.to_dict(rel=rel)}
        except Exception as e:
            return {"status": 500, "data": [], "error": str(e)}
        finally:
            pass
