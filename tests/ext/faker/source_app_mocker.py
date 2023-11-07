import json
from faker import Faker
from tests import SourceAppModel

MOCK_JSON_PATH = "tests/ext/json/source_apps.json"


class SourceAppMocker:
    """
    A utility class for generating mock Source app data using either Faker or JSON data.

    Attributes:
        mock (str): The mock method to use. Can be "faker" for Faker-generated data or a path to a JSON file.
    """

    def __init__(self, mock: str = "faker"):
        """
        Initialize the MockSourceApp instance.

        Args:
            mock (str, optional): The mock method to use. Defaults to "faker".
                                  Can be "faker" for generating Faker-generated data,
                                  or a path to a JSON file containing mock source app data.
                                  If "path" is provided, the default JSON path will be used.
        """

        self._fake = Faker()
        self._source_apps = []
        self._mock = (MOCK_JSON_PATH if mock ==
                      "path" else mock) if mock is not None else None

    @property
    def source_apps(self):
        """
        Property to access the list of mock source apps.

        Returns:
            list: A list of mock source app data.
        """
        return self._source_apps

    def mock(self, sources: list = None):
        """
        Generate mock source app data using either Faker or JSON data.

        Args:
            sources (list, optional): A list of dictionaries containing source app data.
                                      Only applicable when using Faker-generated data. Defaults to None.

        Returns:
            list: A list of generated mock source app data.
        """
        if self._mock.strip().lower() == "faker":
            if sources is None:
                sources = [
                    {"app_name": "kaggle", "app_username": "solivermazo",
                        "app_enabled": True, "app_linked": True},
                    {"app_name": "bigQuery", "app_username": "solivermazo",
                        "app_enabled": True, "app_linked": False}
                ]

            for s in sources:
                src = SourceAppModel(
                    app_name=s.get("app_name"),
                    app_username=s.get("app_username"),
                    app_enabled=s.get("app_enabled"),
                    app_linked=s.get("app_linked"),
                )
                self._source_apps.append(src)
        else:
            # Load data from the JSON file based on the provided mock value
            json_file_path = self._mock
            json_source_app = []
            with open(json_file_path) as json_file:
                json_source_app = json.load(json_file)
            for s in json_source_app:
                self._source_apps.append(
                    SourceAppModel(
                        id=s.get("id"),
                        app_name=s.get("app_name"),
                        app_username=s.get("app_username"),
                        app_enabled=s.get("app_enabled"),
                        app_linked=s.get("app_linked"),
                    )
                )

        return self._source_apps
