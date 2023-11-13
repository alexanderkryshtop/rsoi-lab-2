from uuid import UUID
from flask import Blueprint, request

from service.reservation_service import ReservationService

reservation_app = Blueprint("reservation", __name__, url_prefix="/reservations")

reservation_service = ReservationService()

@reservation_app.route("/")
def take_book_in_library():
    username = request.headers.get("X-User-Name")

    libs = reservation_service.get_libraries(city, page, size)

    return f"{libs}", 200

@reservation_app.route("/<reservation_uid>/return")
def get_books_in_library(library_uid: str):
    page = request.args.get("page")
    size = request.args.get("size")
    show_all = request.args.get("showAll")

    books = reservation_service.get_books_in_library(library_uid=library_uid)

    return f"{books}", 200