from flask import Blueprint, request

from service.library_service import LibraryService

library_app = Blueprint("library", __name__, url_prefix="/libraries")

library_service = LibraryService()


@library_app.route("/")
def get_libraries():
    page = request.args.get("page")
    size = request.args.get("size")
    city = request.args.get("city")

    libraries = library_service.get_libraries(city, page, size)

    items = []
    for library in libraries:
        items.append({
            "libraryUid": library.library_uid,
            "name": library.name,
            "address": library.address,
            "city": library.city,
        })

    response = {
        "page": int(page),
        "pageSize": int(size),
        "totalElements": len(items),
        "items": items,
    }

    return response, 200, {"Content-Type": "application/json"}


@library_app.route("/library/<library_uid>")
def get_library(library_uid: str):
    library = library_service.get_library(library_uid)
    if not library:
        return {}, 404
    response = {
        "libraryUid": library.library_uid,
        "name": library.name,
        "address": library.address,
        "city": library.city,
    }
    return response, 200, {"Content-Type": "application/json"}


@library_app.route("/<library_uid>/books")
def get_books_in_library(library_uid: str):
    page = request.args.get("page")
    size = request.args.get("size")
    show_all = request.args.get("showAll")

    items = []
    books = library_service.get_books_in_library(library_uid=library_uid)
    for book in books:
        items.append({
            "bookUid": book.book_uid,
            "name": book.name,
            "author": book.author,
            "genre": book.genre,
            "condition": book.condition,
            "availableCount": books[book]
        })

    response = {
        "page": int(page),
        "pageSize": int(size),
        "totalElements": len(items),
        "items": items
    }

    return response, 200, {"Content-Type": "application/json"}


@library_app.route("/book/<book_uid>")
def get_book(book_uid: str):
    book = library_service.get_book(book_uid)
    if not book:
        return {}, 404
    response = {
        "bookUid": book.book_uid,
        "name": book.name,
        "author": book.author,
        "genre": book.genre,
    }
    return response, 200, {"Content-Type": "application/json"}


@library_app.route("/change_availability", methods=["POST"])
def change_available_count_by_delta():
    json_request = request.get_json()
    library_uid = json_request["libraryUid"]
    book_uid = json_request["bookUid"]
    delta = json_request["delta"]
    book_availability = library_service.change_book_availability(library_uid, book_uid, delta)
    return {"availability": book_availability}, 200
