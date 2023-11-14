from uuid import UUID
from flask import Blueprint, request

from service.reservation_service import ReservationService

reservation_app = Blueprint("reservation", __name__, url_prefix="/reservations")

reservation_service = ReservationService()

@reservation_app.route("/", methods=["POST"])
def take_book_in_library():
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    book_uid = json_body["bookUid"]
    library_uid = json_body["libraryUid"]
    till_date = json_body["tillDate"]

    result = reservation_service.take_book_in_library(username, book_uid, library_uid, till_date)

    return result, 200, {"Content-Type": "application/json"}

@reservation_app.route("/<reservation_uid>/return", methods=["POST"])
def return_book_to_library(reservation_uid: str):
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    condition = json_body["condition"]
    date = json_body["date"]

    returned = reservation_service.return_book_to_library(reservation_uid, condition, date)
    if not returned:
        return {"message": "not found"}, 404, {"Content-Type": "application/json"}

    return "", 204, {"Content-Type": "application/json"}

@reservation_app.route("/", methods=["GET"])
def get_all_reservations():
    username = request.headers.get("X-User-Name")
    reservations = reservation_service.get_all_reservations(username)
    return reservations, 200, {"Content-Type": "application/json"}
