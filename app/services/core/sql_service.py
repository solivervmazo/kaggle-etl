from app.services.core.base_service import BaseService
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker


class SqlService(BaseService):
    def __init__(self, db_engine: Engine, token: str = None) -> None:
        super().__init__(token=token)
        self._db_engine = db_engine
        self._session = None

    def _close_session(self):
        """
        Close the active database session.

        Returns:
            None: This method closes the active database session of the PfileService instance.
        """
        if self._db_engine is None:
            return False
        self._session.close()

    def _create_session(self, session=None):
        """
        Create a database session using the provided database engine or an existing session.

        This method initializes a new database session using the specified database engine
        if `session` is not provided, and sets the '_session' attribute of the Service instance
        to the newly created session. If `session` is provided, it sets the '_session' attribute
        to the existing session.

        Args:
            session (sqlalchemy.orm.session.Session, optional): An existing SQLAlchemy database session.

        Returns:
            sqlalchemy.orm.session.Session: A SQLAlchemy database session.

        Raises:
            None

        Example:
            pfile_service = PfileService()
            session = pfile_service._create_session()
            # Now you can use 'session' to perform database operations.

            # Alternatively, you can pass an existing session:
            existing_session = some_existing_session()
            session = pfile_service._create_session(session=existing_session)
            # 'session' will now be set to the provided existing session.
        """
        if self._db_engine is None:
            return False
        if session:
            self._session = session
        else:
            Session = sessionmaker(bind=self._db_engine)
            self._session = Session()
        return self._session

    def _rollback_session(self):
        """
        Close the active database session and roll back any pending changes.

        This method is used to close the active database session of the Service
        instance and roll back any pending changes that have not been committed. It
        ensures that the database remains in a consistent state even if an error
        occurs during data manipulation operations.

        Returns:
            None

        Raises:
            None

        Example:
            service = Service()
            try:
                # Perform some database operations
                self._rollback_session()
            except Exception as e:
                # An error occurred, so roll back any changes made in the session
                pass
        """
        if self._db_engine is None:
            return False
        self._session.rollback()
