from db.models import ReservationModel
from db.models import ReservationModelStatus
from domain.entities import Reservation


class ReservationRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_reservation(self, reservation: Reservation) -> Reservation:
        reservation_model = self._from_entity(reservation)
        self.db_session.add(reservation_model)
        self.db_session.commit()
        reservation.id = reservation_model.id
        return reservation

    def list_by_username(self, username: str) -> list[Reservation]:
        reservation_models = self.db_session.query(ReservationModel).filter(
            ReservationModel.username == username).all()
        return [self._to_entity(reservation) for reservation in reservation_models]

    @staticmethod
    def _from_entity(entity: Reservation) -> ReservationModel:
        return ReservationModel(
            reservation_uid=entity.reservation_uid,
            username=entity.username,
            book_uid=entity.book_uid,
            library_uid=entity.library_uid,
            status=ReservationModelStatus(entity.status.value),
            start_date=entity.start_date,
            till_date=entity.till_date,
        )

    @staticmethod
    def _to_entity(model: ReservationModel) -> Reservation:
        return Reservation(
            id=model.id,
            reservation_uid=model.reservation_uid,
            username=model.username,
            book_uid=model.book_uid,
            library_uid=model.library_uid,
            status=model.status,
            start_date=model.start_date,
            till_date=model.till_date,
        )
