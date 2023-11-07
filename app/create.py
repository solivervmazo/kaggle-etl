from flask import Flask
from flask_cors import CORS


def create_app(name, config=None):
    app = Flask(name)

    # Apply Cors Origin
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}})

    # Import and register blueprints
    from app.routes import (
        project_routes,
    )

    app.register_blueprint(project_routes.blueprint)
    return app
