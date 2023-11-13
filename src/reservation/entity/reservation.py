from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class ReservationStatus(Enum):
    RENTED = "RENTED"
    RETURNED = "RETURNED"
    EXPIRED = "EXPIRED"

@dataclass
class Reservation:
    id: int
    reservation_uid: str
    username: str
    book_uid: str
    library_uid: str
    status: ReservationStatus
    start_date: datetime
    till_date: datetime
