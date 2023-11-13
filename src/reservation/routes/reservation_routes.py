from uuid import UUID
from flask import Blueprint, request

from service.reservation_service import ReservationService

reservation_app = Blueprint("reservation", __name__, url_prefix="/reservations")

reservation_service = ReservationService()

@reservation_app.route("/", methods=["POST"])
def take_book_in_library():
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    bookUid = json_body["bookUid"]
    libraryUid = json_body["libraryUid"]
    tillDate = json_body["tillDate"]

    libs = reservation_service.take_book_in_library(username, bookUid, libraryUid, tillDate)

    return f"{libs}", 200

@reservation_app.route("/<reservation_uid>/return")
def get_books_in_library(library_uid: str):
    page = request.args.get("page")
    size = request.args.get("size")
    show_all = request.args.get("showAll")

    books = reservation_service.get_books_in_library(library_uid=library_uid)

    return f"{books}", 200