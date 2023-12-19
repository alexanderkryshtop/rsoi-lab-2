import requests
from flask import Blueprint, request, current_app, jsonify

reservation_app = Blueprint("reservation", __name__, url_prefix="/api/v1/reservations")

from service.reservation_service import ReservationService


@reservation_app.route("/", methods=["POST"])
def take_book_in_library():
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    book_uid = json_body["bookUid"]
    library_uid = json_body["libraryUid"]
    till_date = json_body["tillDate"]

    resp = ReservationService.create_reservation(username, book_uid, library_uid, till_date)

    return jsonify(resp)


@reservation_app.route("/<reservation_uid>/return", methods=["POST"])
def return_book_to_library(reservation_uid: str):
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    prefix = current_app.config['reservation']

    url = f"{prefix}/reservations/{reservation_uid}/return"
    result = requests.post(url, json=json_body, headers={"X-User-Name": username})
    result_content_type = result.headers.get("Content-Type")

    return result.text, result.status_code, {"Content-Type": result_content_type}


@reservation_app.route("/", methods=["GET"])
def get_all_reservations():
    username = request.headers.get("X-User-Name")

    prefix = current_app.config['reservation']
    url = f"{prefix}/reservations/"
    result = requests.get(url, headers={"X-User-Name": username})
    result_content_type = result.headers.get("Content-Type")

    return result.text, result.status_code, {"Content-Type": result_content_type}
