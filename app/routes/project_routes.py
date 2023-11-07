from flask import Blueprint
import os

blueprint = Blueprint("projects", __name__)
base_url = os.environ.get("API_BASE_PATH")
slug = "projects"

headers = {"Content-Type": "application/json"}


@blueprint.route(f"/{base_url}/{slug}/", methods=["GET"])
def fetch_projects():
    return {"data": "projects"}, 200, headers


@blueprint.route(f"/{base_url}/{slug}/<path:id>", methods=["GET"])
def fetch_project(id: str):
    return {"data": {"id": id}}, 200, headers
