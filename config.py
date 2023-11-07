import os
from dotenv import load_dotenv


class Config:
    def __init__(self, env: str = None):
        if env:
            env_path = f".env.{env}"
        else:
            env_path = ".env"
        load_dotenv(dotenv_path=env_path, override=True)

        self.ENV = os.environ.get("ENV")
        self.TEST_JSON_PATH = os.environ.get("TEST_JSON_PATH")

        self.DB_CONNECTION = os.environ.get("DB_CONNECTION")

        self.API_BASE_PATH = os.environ.get("API_BASE_PATH")
        self.ODATA_BASE_PATH = os.environ.get("ODATA_BASE_PATH")
