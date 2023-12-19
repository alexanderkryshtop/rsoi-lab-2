from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class ReservationAPI:
    reservation_uid: UUID
    status: str
    start_date: date
    till_date: date


@dataclass
class BookCheckoutRequestAPI:
    book_uid: UUID
    library_uid: UUID
