from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

from entity import Library
from entity import Book


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
            library_uid=str(self.library_uid),
            name=self.name,
            city=self.city,
            address=self.address,
        )

    def __repr__(self) -> str:
        return f"<id='{self.id}', uid='{self.library_uid}', name='{self.name}', city='{self.city}', address='{self.address}'>"


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_uid = db.Column(db.String)
    name = db.Column(db.String)
    author = db.Column(db.String)
    genre = db.Column(db.String)
    condition = db.Column(db.String)

    def to_entity(self) -> Book:
        return Book(
            id=self.id,
            book_uid=str(self.book_uid),
            name=self.name,
            author=self.author,
            genre=self.genre,
            condition=self.condition,
        )
    
    def __repr__(self) -> str:
        return f"<id='{self.id}', uid='{self.book_uid}', name='{self.name}', author='{self.author}', genre='{self.genre}', condition='{self.condition}'>"


class LibraryBooksModel(db.Model):
    __tablename__ = 'library_books'

    book_id = db.Column(db.Integer, ForeignKey('books.id'), primary_key=True)
    library_id = db.Column(db.Integer, ForeignKey('library.id'), primary_key=True)
    available_count = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"<book_id='{self.book_id}', library_id='{self.library_id}', available_count='{self.available_count}'>"
