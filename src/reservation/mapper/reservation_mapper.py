from domain.entities import Reservation
from dto.api.reservation_dto import ReservationAPI


def reservation_to_dto(reservation: Reservation) -> ReservationAPI:
    return ReservationAPI(
        reservation_uid=reservation.reservation_uid,
        status=str(reservation.status),
        start_date=reservation.start_date,
        till_date=reservation.till_date,
    )
