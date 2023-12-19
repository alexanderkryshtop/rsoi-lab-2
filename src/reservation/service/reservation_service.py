import uuid
from datetime import date
from uuid import UUID

from db.models import db
from db.repositories import ReservationRepository
from dto.api.reservation_dto import ReservationAPI
from domain.entities import Reservation
from domain.entities import ReservationStatus
from mapper import reservation_mapper


class ReservationService:

    def __init__(self):
        self._reservation_repository = ReservationRepository(db.session)

    def create_reservation(self, username: str, book_uid: UUID, library_uid: UUID, till_date: str) -> ReservationAPI:
        reservation = Reservation(
            id=None,
            reservation_uid=uuid.uuid4(),
            username=username,
            book_uid=book_uid,
            library_uid=library_uid,
            status=ReservationStatus.RENTED,
            start_date=date.today(),
            till_date=date.fromisoformat(till_date),
        )
        reservation = self._reservation_repository.create_reservation(reservation)
        return reservation_mapper.reservation_to_dto(reservation)
