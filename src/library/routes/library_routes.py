from uuid import UUID
from flask import Blueprint, request

from service.library_service import LibraryService

library_app = Blueprint("library", __name__, url_prefix="/libraries")

library_service = LibraryService()

@library_app.route("/")
def get_libraries_with_pagination():
    page = request.args.get("page")
    size = request.args.get("size")
    city = request.args.get("city")

    libs = library_service.get_libraries(city, page, size)

    return f"{libs}", 200

@library_app.route("/<library_uid>/books")
def get_books_in_library(library_uid: str):
    page = request.args.get("page")
    size = request.args.get("size")
    show_all = request.args.get("showAll")

    books = library_service.get_books_in_library(library_uid=library_uid)

    return f"{books}", 200