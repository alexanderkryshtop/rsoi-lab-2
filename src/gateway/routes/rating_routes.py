import requests
from uuid import UUID
from flask import Blueprint, request, current_app

rating_app = Blueprint("rating", __name__, url_prefix="/api/v1/rating")

@rating_app.route("/")
def get_rating():
    username = request.headers.get("X-User-Name")

    prefix = current_app.config['rating']

    url = f"{prefix}/rating"
    result = requests.get(url, headers={"X-User-Name": username})
    result_content_type = result.headers.get("Content-Type")

    return result.text, result.status_code, {"Content-Type": result_content_type}