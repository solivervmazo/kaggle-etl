from app.services.core.sql_service import SqlService
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from app.models.sql.log_model import LogModel
from app.services.log_service import LogService


class LoggerService(SqlService):
    def __init__(
        self, db_engine: Engine, token: str = None, logging: bool = True
    ) -> None:
        super().__init__(db_engine=db_engine, token=token)
        self._logging = logging

    def _create_log(
        self,
        log_category: str,
        log_from_id: str,
        log_type: str,
        log_msg: str = "",
        log_category1: str = None,
        log_category2: str = None,
        log_from_root_id: str = None,
        log_resolved: bool = False,
    ):
        return LogModel(
            log_category=log_category,
            log_category1=log_category1,
            log_category2=log_category2,
            log_from_id=log_from_id,
            log_from_root_id=log_from_root_id,
            log_type=log_type,
            log_msg=log_msg,
            log_resolved=log_resolved,
            token=self._token,
        )

    def _clean_log_residues(self, log_from_id: str):
        try:
            self._create_session()
            records_to_delete = (
                self._session.query(LogModel)
                .filter(LogModel.log_from_id == log_from_id)
                .filter(LogModel.token == "")
                .all()
            )
            for record in records_to_delete:
                self._session.delete(record)
            self._session.commit()
            return self._response(200, [])
        except Exception as e:
            # Does not need to break
            pass
        finally:
            self._close_session()

    def _create_log_service(self):
        if self._db_engine is None:
            return Exception("Unable to insert logs without engine")
        svc = LogService(db_engine=self._db_engine, session=self._session)
        return svc, []
