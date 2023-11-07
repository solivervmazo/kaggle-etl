from sqlalchemy import Engine, select
from app.services.core.logger_service import LoggerService

from app.models.sql.source_app_model import SourceAppModel
from app.services.project_service import ProjectModel, ProjectService
from app.services.log_service import LogModel, LogService

LOG_CATEGORY = "source_app"


class SourceAppService(LoggerService):
    def __init__(
        self, db_engine: Engine, token: str = None, logging: bool = True, session=None
    ) -> None:
        super().__init__(db_engine=db_engine, token=token, logging=logging)
        if session:
            self._create_session(session)

    def fetch_source_apps(self, id: str = None):
        try:
            query = select(SourceAppModel)
            if id is not None:
                query = query.where(SourceAppModel.id == id)
                result = self._session.scalar(query)
                if result:
                    return self._response(200, result)
                else:
                    return self._response(404, error="App not found")
            else:
                result = self._session.scalars(query).all()
                return self._response(200, data=result)
        except Exception as e:
            return self._response(500, error=str(e))
        finally:
            pass

    def insert_source_apps(self, source_apps: list = []):
        try:
            self._session.add_all(source_apps)
            return self._response(200, data=source_apps)
        except Exception as e:
            return self._response(500, error=str(e))
        finally:
            pass
