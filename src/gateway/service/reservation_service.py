from typing import Tuple, Any

import requests
from flask import current_app

from service.library_service import LibraryService
from service.rating_service import RatingService


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
    def reservation_process(username: str, book_uid: str, library_uid: str, till_date: str) -> Tuple[Any, int]:
        rating, status_code = RatingService.get_user_rating(username)
        if status_code != 200:
            return {"message": "rating error"}, status_code

        available_count, status_code = LibraryService.get_book_available_count(book_uid, library_uid)
        if available_count <= 0:
            return {"message": "book is not available"}, 404

        rented_count = ReservationService._get_rented_reservations_count(username)
        if rating <= rented_count:
            return {"message": "not enough stars"}, 200

        reservation, status_code = ReservationService._create_reservation(username, book_uid, library_uid, till_date)
        status_code = LibraryService.checkout_book(book_uid, library_uid)

        book, status_code = LibraryService.get_book(book_uid)
        library, status_code = LibraryService.get_library(library_uid)

        result = {
            "reservationUid": reservation["reservationUid"],
            "status": reservation["status"],
            "startDate": reservation["startDate"],
            "tillDate": reservation["endDate"],
            "book": book,
            "library": library,
            "rating": rating,
        }

        return result, 200


    @staticmethod
    def return_reservation(reservation_uid: str, username: str, condition: str, date: str) -> Tuple[dict, int]:

        pass