import requests
from uuid import UUID
from flask import Blueprint, request, current_app

from service.library_service import LibraryService

library_app = Blueprint("library", __name__, url_prefix="/api/v1/libraries")

library_service = LibraryService()

@library_app.route("/")
def get_libraries_with_pagination():
    page = request.args.get("page")
    size = request.args.get("size")
    city = request.args.get("city")
    if not city:
        return "", 400

    decoded_query_string = request.query_string.decode()
    prefix = current_app.config['library']
    url = f"{prefix}/libraries?{decoded_query_string}"
    result = requests.get(url)

    return result.text, result.status_code

@library_app.route("/<library_uid>/books")
def get_books_in_library(library_uid: str):
    page = request.args.get("page")
    size = request.args.get("size")
    show_all = request.args.get("showAll")

    books = library_service.get_books_in_library(library_uid=library_uid)

    return f"{books}", 200