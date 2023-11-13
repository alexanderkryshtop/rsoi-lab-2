from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ReservationStatus(str, Enum):
    RENTED = "RENTED"
    RETURNED = "RETURNED"
    EXPIRED = "EXPIRED"

@dataclass
class Reservation:
    id: Optional[int]
    reservation_uid: str
    username: str
    book_uid: str
    library_uid: str
    status: ReservationStatus
    start_date: datetime
    till_date: datetime
