from typing import Tuple, Any

import requests
from flask import current_app
from service.rating_service import RatingService
from service.library_service import LibraryService


class ReservationService:

    @staticmethod
    def _get_rented_reservations_count(username: str) -> int:
        result = requests.get(
            f"{current_app.config['reservation']}/reservations/rented",
            headers={"X-User-Name": username}
        )
        json_data = result.json()
        return json_data["count"]

    @staticmethod
    def _create_reservation(username: str, book_uid: str, library_uid: str, till_date: str):
        json_body = {
            "bookUid": book_uid,
            "libraryUid": library_uid,
            "tillDate": till_date
        }
        url = f"{current_app.config['reservation']}/reservations"
        result = requests.post(url, json=json_body, headers={"X-User-Name": username})

        json_data = result.json()
        return json_data, result.status_code

    @staticmethod
    def reservation_process(
            username: str,
            book_uid: str,
            library_uid: str,
            till_date: str
    ) -> Tuple[Any, int]:
        rating, status_code = RatingService.get_user_rating(username)
        if status_code != 200:
            return {"message": "rating error"}, status_code

        available_count = LibraryService.get_book_available_count(book_uid, library_uid)
        if available_count <= 0:
            return {"message": "book is not available"}, 404

        rented_count = ReservationService._get_rented_reservations_count(username)
        if rating.stars <= rented_count:
            return {"message": "not enough stars"}, 200



        reservation, status_code = ReservationService._create_reservation(username, book_uid, library_uid, till_date)


