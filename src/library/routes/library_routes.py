from uuid import UUID

from flask import Blueprint
from flask import Response
from flask import abort
from flask import jsonify
from flask import request

from dto.api.book_dto import BookCheckoutRequestAPI
from exceptions import exceptions
from service.library_service import LibraryService

library_app = Blueprint("library", __name__, url_prefix="/libraries")

library_service = LibraryService()


@library_app.route("/")
def get_libraries():
    page = request.args.get("page", default=1, type=int)
    size = request.args.get("size", default=10, type=int)
    city = request.args.get("city", type=str)

    if city is None:
        abort(400, description="Parameter 'city' is required.")

    libraries = library_service.get_libraries(city)

    return jsonify({
        "page": page,
        "pageSize": size,
        "totalElements": len(libraries),
        "items": libraries,
    })


@library_app.route("/<library_uid>/book")
def get_books_in_library(library_uid: UUID):
    page = request.args.get("page", default=1, type=int)
    size = request.args.get("size", default=10, type=int)
    show_all = request.args.get("showAll", type=bool)

    books = library_service.get_books_in_library(library_uid=library_uid)

    return jsonify({
        "page": page,
        "pageSize": size,
        "totalElements": len(books),
        "items": books
    })


@library_app.route("/book/checkout", methods=["POST"])
def checkout_book():
    json_data = request.get_json()
    book_checkout_request = BookCheckoutRequestAPI(
        book_uid=json_data["bookUid"],
        library_uid=json_data["libraryUid"],
    )
    try:
        library_service.checkout_book(book_checkout_request.book_uid, book_checkout_request.library_uid)
    except (exceptions.BookNotAvailable, exceptions.LibraryNotFound, exceptions.BookNotFoundInLibrary):
        abort(404)
    return Response(status=200)


@library_app.route("/book/return", methods=["POST"])
def return_book():
    json_data = request.get_json()
    book_checkout_request = BookCheckoutRequestAPI(
        book_uid=json_data["bookUid"],
        library_uid=json_data["libraryUid"],
    )
    try:
        library_service.return_book(book_checkout_request.book_uid, book_checkout_request.library_uid)
    except (exceptions.BookNotAvailable, exceptions.LibraryNotFound, exceptions.BookNotFoundInLibrary):
        abort(404)
    return Response(status=200)


@library_app.route("/book/<book_uid>")
def get_book(book_uid: UUID):
    book = library_service.get_book(book_uid)
    return jsonify(book)


@library_app.route("/<library_uid>")
def get_library(library_uid: UUID):
    library = library_service.get_library(library_uid)
    return jsonify(library)
