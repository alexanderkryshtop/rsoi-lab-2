import requests
import json
import uuid
from datetime import datetime
from http import client

from flask import current_app

from typing import Optional
from entity import Reservation, ReservationStatus
from repository import ReservationModel

class ReservationService:
    
    def take_book_in_library(self, username: str, book_uid: str, library_uid: str, till_date: str) -> Optional[dict]:
        rented_books_count = ReservationModel.query.filter(ReservationModel.username == username, ReservationModel.status == "RENTED").count()
        user_rating = self._get_user_rating(username)
        if not user_rating:
            return None

        star_count = user_rating["stars"]
        if star_count <= rented_books_count:
            return None
        
        new_availability = self._decrease_available_count(book_uid, library_uid)

        reservation = Reservation(
            id=None,
            reservation_uid=str(uuid.uuid4()),
            username=username,
            book_uid=book_uid,
            library_uid=library_uid,
            status=ReservationStatus.RENTED,
            start_date=datetime.now().strftime("%Y-%m-%d"),
            till_date=datetime.strptime(till_date, "%Y-%m-%d"),
        )
        reservation_model = ReservationModel.from_entity(reservation)
        ReservationModel.query.session.add(reservation_model)
        ReservationModel.query.session.commit()

        book = self._get_book(book_uid)
        library = self._get_library(library_uid)

        return {
            "reservationUid": reservation.reservation_uid,
            "status": reservation.status,
            "startDate": reservation.start_date,
            "tillDate": till_date,
            "book": book,
            "library": library,
            "rating": user_rating,
        }

    def _get_user_rating(self, username: str) -> dict:
        gateway_url_prefix = current_app.config["gateway"]
        url = f"{gateway_url_prefix}/api/v1/rating"
        result = requests.get(url, headers={"X-User-Name": username})
        json_result = result.json()
        return json_result

    def _decrease_available_count(self, book_uid: str, library_uid: str) -> Optional[int]:
        gateway_url_prefix = current_app.config["gateway"]
        url = f"{gateway_url_prefix}/api/v1/libraries/change_availability"
        
        json_body = json.dumps({
            "bookUid": book_uid,
            "libraryUid": library_uid,
            "delta": 1
        })

        result = requests.post(url, json=json_body)
        if result.status_code != client.OK:
            return None

        json_result = json.loads(result.text)
        availability = json_result["availability"]
        return availability
    
    def _get_book(self, book_uid: str) -> Optional[dict]:
        gateway_url_prefix = current_app.config["gateway"]
        url = f"{gateway_url_prefix}/api/v1/libraries/book/{book_uid}"
        
        result = requests.get(url)
        if result.status_code != client.OK:
            return None

        json_result = result.json()
        return json_result
    
    def _get_library(self, library_uid: str) -> Optional[dict]:
        gateway_url_prefix = current_app.config["gateway"]
        url = f"{gateway_url_prefix}/api/v1/libraries/library/{library_uid}"
        
        result = requests.get(url)
        if result.status_code != client.OK:
            return None

        json_result = result.json()
        return json_result