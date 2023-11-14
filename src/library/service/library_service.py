from typing import Optional
from entity import Library
from entity import Book
from repository import LibraryModel
from repository import BookModel
from repository import LibraryBooksModel

class LibraryService:
    
    def get_libraries(self, city: str, page: Optional[int] = None, size: Optional[int] = None) -> list[Library]:
        libraryModels: list[LibraryModel] = LibraryModel.query.filter(LibraryModel.city == city).all()
        libraries = [model.to_entity() for model in libraryModels]
        return libraries
    
    def get_library(self, library_uid: str) -> Optional[Library]:
        library_model: LibraryModel = LibraryModel.query.filter(LibraryModel.library_uid == library_uid).one_or_none()
        if not library_model:
            return None
        return library_model.to_entity()

    def get_books_in_library(
        self,
        library_uid: str,
        page: Optional[int] = None,
        size: Optional[int] = None,
        show_all: bool = False
    ) -> list[Book]:
        libraryModel: LibraryModel = LibraryModel.query.filter(
            LibraryModel.library_uid == library_uid
        ).one_or_none()

        if not libraryModel:
            return []

        bookModels: list[BookModel] = BookModel.query.join(LibraryBooksModel).filter(
            LibraryBooksModel.library_id == libraryModel.id
        ).all()

        books = [model.to_entity() for model in bookModels]
        return books
    
    def get_book(self, book_uid: str) -> Optional[Book]:
        book_model: BookModel = BookModel.query.filter(BookModel.book_uid == book_uid).one_or_none()
        if not book_model:
            return None
        return book_model.to_entity()
    
    def change_book_availability(self, library_uid: str, book_uid: str, delta: int) -> Optional[int]:
        libraryModel: LibraryModel = LibraryModel.query.filter(LibraryModel.library_uid == library_uid).one_or_none()
        bookModel: BookModel = BookModel.query.filter(BookModel.book_uid == book_uid).one_or_none()
        if not libraryModel or not bookModel:
            return None

        libraryBooksModel: LibraryBooksModel = LibraryBooksModel.query.filter(
            LibraryBooksModel.library_id == libraryModel.id, LibraryBooksModel.book_id == bookModel.id
        ).one_or_none()
        if not libraryBooksModel:
            return None
        
        libraryBooksModel.query.update({LibraryBooksModel.available_count: LibraryBooksModel.available_count + delta})
        libraryBooksModel.query.session.commit()

        return libraryBooksModel.available_count