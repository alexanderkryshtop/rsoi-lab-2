from dataclasses import dataclass
from uuid import UUID

from dto.library_dto import BookDTO, LibraryDTO
from dto.rating_dto import RatingResponseDTO


@dataclass
class ReservationResponseDTO:
    reservation_uid: UUID
    status: str
    start_date: str
    till_date: str
    book: BookDTO
    library: LibraryDTO
    rating: RatingResponseDTO

    def to_dict(self) -> dict:
        return {
            "reservationUid": self.reservation_uid,
            "status": self.status,
            "startDate": self.start_date,
            "tillDate": self.till_date,
            "book": self.book.to_dict(),
            "library": self.library.to_dict(),
            "rating": self.rating,
        }


@dataclass
class ReservationErrorResponseDTO:
    message: str
