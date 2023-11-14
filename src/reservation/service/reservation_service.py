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
    
    def take_book_in_library(self, username: str, book_uid: str, library_uid: str, till_date: str):
        rented_books_count = ReservationModel.query.filter(ReservationModel.username == username, ReservationModel.status == "RENTED").count()
        star_count = self._get_user_stars(username)
        if star_count <= rented_books_count:
            return
        
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

        pass

    def _get_user_stars(self, username: str) -> int:
        gateway_url_prefix = current_app.config["gateway"]
        url = f"{gateway_url_prefix}/api/v1/rating"
        result = requests.get(url, headers={"X-User-Name": username})
        json_result = json.loads(result.text)
        star_count = json_result["stars"]
        return star_count

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