import os
from app.create import create_app
from config import Config


env = os.environ.get("ENV")
config = Config(env=env)
app = create_app(__name__)
print(f"ON ENV:{env}")
if __name__ == "__main__":
    app.run()
