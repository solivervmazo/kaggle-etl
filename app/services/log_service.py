from sqlalchemy import Engine, select
from app.models import ProjectModel, SourceAppModel, LogModel
from app.enums import LogType
from app.services.core.sql_service import SqlService


class LogService(SqlService):
    def __init__(self, db_engine: Engine, token: str = None, session=None) -> None:
        super().__init__(db_engine=db_engine, token=token)
        if session:
            self._create_session(session)

    def fetch_logs(
        self,
        log_from_id: str = None,
        log_category: str = None,
        log_category1: str = None,
        log_category2: str = None,
        log_type: LogType = None,
        log_resolved: bool = None,
        token: str = None,
    ):
        try:
            query = (
                select(LogModel)
                .join(SourceAppModel, SourceAppModel.id == LogModel.log_from_root_id)
                .where(SourceAppModel.app_linked == True)
            )
            if log_from_id:
                query = query.where(LogModel.log_from_id == log_from_id)
            if log_category:
                query = query.where(LogModel.log_category == log_category)
            if log_category1:
                query = query.where(LogModel.log_category1 == log_category1)
            if log_category2:
                query = query.where(LogModel.log_category2 == log_category2)
            if log_type:
                query = query.where(LogModel.log_type == log_type)
            if log_resolved is not None:
                query = query.where(LogModel.log_resolved == log_resolved)
            if token is not None:
                query = query.where(LogModel.token == token)
            result = self._session.scalars(query).all()
            return self._response(200, data=result)
        except Exception as e:
            return self._response(500, error=str(e))
        finally:
            pass

    def insert_log(self, logs: list[LogModel]):
        try:
            self._session.add_all(logs)
            self._session.commit()
            return self._response(200, data=logs)
        except Exception as e:
            return self._response(500, error=str(e))
        finally:
            pass
