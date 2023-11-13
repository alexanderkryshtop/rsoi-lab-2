from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class LibraryModel(db.Model):
    __tablename__ = 'library'

    id = db.Column(db.Integer, primary_key=True)
    library_uid = db.Column(db.String)
    name = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)

    def __repr__(self) -> str:
        return "<id {}>".format(self.id)