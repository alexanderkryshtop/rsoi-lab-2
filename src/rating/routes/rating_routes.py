from uuid import UUID
from flask import Blueprint, request

from service.rating_service import RatingService

rating_app = Blueprint("rating", __name__, url_prefix="/rating")

rating_service = RatingService()

@rating_app.route("/")
def get_libraries_with_pagination():
    username = request.headers.get("X-User-Name")
    user_stars_count = rating_service.get_star_count(username)

    response = {
        "stars": user_stars_count
    }

    return response, 200