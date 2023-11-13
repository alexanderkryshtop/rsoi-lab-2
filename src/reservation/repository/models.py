from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

db = SQLAlchemy()

from entity import Reservation


class ReservationModel(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    reservation_uid = db.Column(db.String)
    username = db.Column(db.String)
    book_uid = db.Column(db.String)
    library_uid = db.Column(db.String)
    status = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    till_date = db.Column(db.DateTime)

    def to_entity(self) -> Reservation:
        return Reservation(
            id=self.id,
            reservation_uid=self.reservation_uid,
            username=self.username,
            book_uid=self.book_uid,
            library_uid=self.library_uid,
            status=self.status,
            start_date=self.start_date,
            till_date=self.till_date,
        )

    def __repr__(self) -> str:
        return f"""<id='{self.id}', reservation_uid='{self.reservation_uid}', username='{self.username}', 
                book_uid='{self.book_uid}', library_uid='{self.library_uid}', status='{self.status}', 
                start_date='{self.start_date}', till_date='{self.till_date}'>"""

