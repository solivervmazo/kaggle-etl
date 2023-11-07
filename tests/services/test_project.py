import os
import random
import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from tests import Base, AssertCommons, ProjectModel, SourceAppService, ProjectService
from tests.ext.faker.project_mocker import ProjectMocker
from tests.ext.faker.source_app_mocker import SourceAppMocker
from app.utils import generate_token


class TestProject(unittest.TestCase):
    def setUp(self) -> None:
        self.db_engine = create_engine(os.environ.get("DB_CONNECTION"))
        Base.metadata.create_all(self.db_engine)
        self.session = sessionmaker(bind=self.db_engine)

    def tearDown(self):
        Base.metadata.drop_all(self.db_engine)

    def mock_source_apps(self):
        session = self.session()
        mocker = SourceAppMocker(mock="faker")
        sources = [
            {
                "app_name": "kaggle",
                "app_username": "solivermazo",
                "app_enabled": True,
                "app_linked": True,
            }
        ]
        mocked = mocker.mock(sources=sources)
        session.add_all(mocked)
        session.commit()
        mocked = random.choice(mocked)
        mocked = mocked.to_dict()
        session.close()
        return mocked

    def test_insert_projects(self):
        source_apps = self.mock_source_apps()
        mocker = ProjectMocker(mock="faker")
        mocked = mocker.mock(count=5, source_apps=[source_apps])
        svc = ProjectService(db_engine=self.db_engine)
        with svc._create_session() as session:
            # Use case
            result = svc.insert_projects(projects=mocked)

            AssertCommons.in_results(self, result=result)
            AssertCommons.should_length_and_values_matched(
                self, result=result.get("data"), expected=mocked, ignore_keys=["id"]
            )
            svc._close_session()

    def test_fetch_projects(self):
        mocked_source_app = self.mock_source_apps()
        mocker = ProjectMocker(mock="faker")
        mocked = mocker.mock(count=5, source_apps=[mocked_source_app])
        svc = ProjectService(db_engine=self.db_engine)
        with svc._create_session() as session:
            session.add_all(mocked)
            session.commit()

            # Use case fetch all projects
            result = svc.fetch_projects()
            AssertCommons.in_results(self, result=result)
            AssertCommons.should_length_and_values_matched(
                self, result=result.get("data"), expected=mocked, ignore_keys=["id"]
            )

            # Use case fetch single project
            mocked_one = random.choice(mocked)
            result = svc.fetch_projects(id=mocked_one.id)
            AssertCommons.in_results(self, result=result)
            AssertCommons.should_length_and_values_matched(
                self,
                result=[result.get("data")],
                expected=[mocked_one],
                ignore_keys=["id"],
            )

            session.close()

    # Test update project
    def test_update_project(self):
        source_apps = self.mock_source_apps()
        mocker = ProjectMocker(mock="faker")
        mocked = mocker.mock(count=5, source_apps=[source_apps])
        svc = ProjectService(db_engine=self.db_engine)
        with svc._create_session() as session:
            session.add_all(mocked)
            mocked_project = random.choice(mocked)
            token = generate_token(None)
            # mocked_project.project_token = token
            result = svc.update_project(
                id=mocked_project.id,
                updates={"project_token": token},
            )
            AssertCommons.in_results(self, result=result)
            AssertCommons.in_db_update(
                self, result=result.get("data"), expected=mocked_project
            )
            svc._close_session()


if __name__ == "__main__":
    unittest.main()
