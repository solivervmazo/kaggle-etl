import os
import json
import random
from faker import Faker
from tests import ProjectModel

# Path to the JSON file containing mock project data
MOCK_JSON_PATH = f"{os.environ.get('TEST_JSON_PATH')}/projects.json"

class ProjectMocker:
    """
    A class to generate mock project data for testing purposes.
    """

    def __init__(self, mock: str = "faker") -> None:
        """
        Initialize the ProjectMocker instance.

        Args:
            mock (str): The chosen method for generating mock data ("faker", "path", or custom JSON).

        Returns:
            None
        """
        # Initialize a Faker instance for generating fake data
        self._fake = Faker()
        # List to hold generated ProjectModel instances
        self._projects = []
        # Specify the chosen mock data method
        self._mock = mock

    @property
    def projects(self):
        """
        Property to access the generated project instances.

        Returns:
            list: List of generated ProjectModel instances.
        """
        return self._projects

    def mock(self, count = 0, source_apps:list=[]):
        """
        Generate mock project data based on the chosen method.

        Args:
            count (int): The number of projects to generate (only applicable for "faker" method).
            source_apps (list): List of source applications for project associations.

        Returns:
            list: List of generated ProjectModel instances.
        """
        if self._mock.strip().lower() == "faker":
            # Generate mock data using the Faker library
            for _ in range(count):
                # Generate a random reference for the project
                ref = '-'.join([self._fake.word() for _ in range(4)])
                src_app = random.choice(source_apps)
                # Create a new ProjectModel instance and add it to the list
                self._projects.append(ProjectModel(
                    source_app_id= src_app.get("id"),
                    project_path=f"{src_app.get('app_username')}/{ref}",
                    project_title=ref.replace("-", " ").capitalize(),
                ))
        else:
            # Generate mock data from a JSON file
            json_file_path = MOCK_JSON_PATH if self._mock == "path" else self._mock
            json_source_app = []

            # Read JSON data from the specified file
            with open(json_file_path) as json_file:
                json_source_app = json.load(json_file)

            # Create ProjectModel instances based on the JSON data
            for s in json_source_app:
                self._projects.append(
                    ProjectModel(
                        source_app_id=random.choice(source_apps).get("id"),
                        project_path=s.get("project_path"),
                        project_title=s.get("project_title")
                    )
                )
        
        # Return the list of generated ProjectModel instances
        return self._projects
