from uuid import UUID

from db.models import LibraryModel, BookModel, LibraryBooksModel
from domain.entities import Library, Book
from dto.repository.book_dto import BookWithCountRepository


class LibraryRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_library_by_id(self, id) -> Library:
        library_model = self.db_session.query(LibraryModel).get(id)
        return library_model.to_entity() if library_model else None

    def get_libraries_by_city(self, city: str) -> list[Library]:
        library_models = LibraryModel.query.filter_by(city=city).all()
        return [self._to_entity(model) for model in library_models]

    @staticmethod
    def _to_entity(model: LibraryModel):
        return Library(
            id=model.id,
            library_uid=model.library_uid,
            name=model.name,
            city=model.city,
            address=model.address,
        )


class BookRepository:

    def __init__(self, db_session):
        self.db_session = db_session

    def get_book_by_id(self, id) -> Book:
        book_model = self.db_session.query(BookModel).get(id)
        return book_model.to_entity() if book_model else None

    def find_books_by_library_uid(self, library_uid: UUID) -> list[BookWithCountRepository]:
        book_with_available_counts = self.db_session.query(
            BookModel,
            LibraryBooksModel.available_count
        ).join(
            LibraryBooksModel,
            BookModel.id == LibraryBooksModel.book_id
        ).join(
            LibraryModel,
            LibraryBooksModel.library_id == LibraryModel.id
        ).filter(
            LibraryModel.library_uid == library_uid
        ).all()

        books_with_count = []

        for book_model, available_count in book_with_available_counts:
            book = self._to_entity(book_model)
            book_with_count = BookWithCountRepository(book, available_count)
            books_with_count.append(book_with_count)

        return books_with_count

    @staticmethod
    def _to_entity(model: BookModel):
        return Book(
            id=model.id,
            book_uid=model.book_uid,
            name=model.name,
            author=model.author,
            genre=model.genre,
            condition=model.condition,
        )
