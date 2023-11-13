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

    return f'{libs}', 200