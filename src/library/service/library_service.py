from uuid import UUID

from db.models import db
from db.repositories import BookRepository
from db.repositories import LibraryRepository
from dto.api.book_dto import BookWithCountAPI
from dto.api.library_dto import LibraryAPI
from mapper import book_mapper
from mapper import library_mapper


class LibraryService:

    def __init__(self):
        self._library_repository = LibraryRepository(db.session)
        self._book_repository = BookRepository(db.session)

    def get_libraries(self, city: str) -> list[LibraryAPI]:
        libraries = self._library_repository.get_libraries_by_city(city)
        return [library_mapper.library_to_dto(library) for library in libraries]

    def get_books_in_library(self, library_uid: UUID) -> list[BookWithCountAPI]:
        books_with_available_count = self._book_repository.find_books_by_library_uid(library_uid)
        return [book_mapper.repository_to_api(book) for book in books_with_available_count]

    #
    # def get_libraries(self, city: str, page: Optional[int] = None, size: Optional[int] = None) -> list[Library]:
    #     libraryModels: list[LibraryModel] = LibraryModel.query.filter(LibraryModel.city == city).all()
    #     libraries = [model.to_entity() for model in libraryModels]
    #     return libraries
    #
    # def get_library(self, library_uid: str) -> Optional[Library]:
    #     library_model: LibraryModel = LibraryModel.query.filter(LibraryModel.library_uid == library_uid).one_or_none()
    #     if not library_model:
    #         return None
    #     return library_model.to_entity()
    #
    # def get_books_in_library(
    #         self,
    #         library_uid: str,
    #         page: Optional[int] = None,
    #         size: Optional[int] = None,
    #         show_all: bool = False
    # ) -> dict[Book, int]:
    #     libraryModel: LibraryModel = LibraryModel.query.filter(
    #         LibraryModel.library_uid == library_uid
    #     ).one_or_none()
    #
    #     if not libraryModel:
    #         return []
    #
    #     query_result = BookModel.query.join(LibraryBooksModel).filter(
    #         LibraryBooksModel.library_id == libraryModel.id
    #     ).with_entities(BookModel, LibraryBooksModel.available_count.label("available_count")).all()
    #
    #     books = {}
    #     for result in query_result:
    #         book_model: BookModel = result.BookModel
    #         available_count = result.available_count
    #         books[book_model.to_entity()] = available_count
    #
    #     return books
    #
    # def get_book(self, book_uid: str) -> Optional[Book]:
    #     book_model: BookModel = BookModel.query.filter(BookModel.book_uid == book_uid).one_or_none()
    #     if not book_model:
    #         return None
    #     return book_model.to_entity()
    #
    # def change_book_availability(self, library_uid: str, book_uid: str, delta: int) -> Optional[int]:
    #     libraryModel: LibraryModel = LibraryModel.query.filter(LibraryModel.library_uid == library_uid).one_or_none()
    #     bookModel: BookModel = BookModel.query.filter(BookModel.book_uid == book_uid).one_or_none()
    #     if not libraryModel or not bookModel:
    #         return None
    #
    #     libraryBooksModel: LibraryBooksModel = LibraryBooksModel.query.filter(
    #         LibraryBooksModel.library_id == libraryModel.id, LibraryBooksModel.book_id == bookModel.id
    #     ).one_or_none()
    #     if not libraryBooksModel:
    #         return None
    #
    #     libraryBooksModel.query.update({LibraryBooksModel.available_count: LibraryBooksModel.available_count + delta})
    #     libraryBooksModel.query.session.commit()
    #
    #     return libraryBooksModel.available_count
