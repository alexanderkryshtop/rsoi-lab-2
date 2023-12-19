from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class ReservationAPI:
    reservation_uid: UUID
    status: str
    start_date: date
    till_date: date

    def to_dict(self) -> dict:
        return {
            "reservationUid": self.reservation_uid,
            "status": self.status,
            "startDate": self.start_date.strftime("%Y-%m-%d"),
            "endDate": self.till_date.strftime("%Y-%m-%d"),
        }


@dataclass
class BookCheckoutRequestAPI:
    book_uid: UUID
    library_uid: UUID
