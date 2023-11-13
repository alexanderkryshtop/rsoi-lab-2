from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from entity import Library


class LibraryModel(db.Model):
    __tablename__ = 'library'

    id = db.Column(db.Integer, primary_key=True)
    library_uid = db.Column(db.String)
    name = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)

    def to_entity(self) -> Library:
        return Library(
            id=self.id,
            library_uid=self.library_uid,
            name=self.name,
            city=self.city,
            address=self.address,
        )

    def __repr__(self) -> str:
        return f"<id='{self.id}', uid='{self.library_uid}', name='{self.name}', city='{self.city}', address='{self.address}'>"