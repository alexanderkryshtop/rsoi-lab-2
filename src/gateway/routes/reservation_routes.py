import requests
from uuid import UUID
from flask import Blueprint, request, current_app

reservation_app = Blueprint("reservation", __name__, url_prefix="/api/v1/reservations")

@reservation_app.route("/", methods=["POST"])
def take_book_in_library():
    username = request.headers.get("X-User-Name")
    json_body = request.get_json()

    prefix = current_app.config['reservation']

    url = f"{prefix}/reservations"
    result = requests.post(url, json=json_body, headers={"X-User-Name": username})
    result_content_type = result.headers.get("Content-Type")

    return result.text, result.status_code, {"Content-Type": result_content_type}

def get_reservation():
    username = request.headers.get("X-User-Name")

    prefix = current_app.config['reservation']

    url = f"{prefix}/reservation"
    result = requests.get(url, headers={"X-User-Name": username})
    result_content_type = result.headers.get("Content-Type")

    return result.text, result.status_code, {"Content-Type": result_content_type}