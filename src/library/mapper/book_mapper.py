from dto.api.book_dto import BookWithCountAPI
from dto.repository.book_dto import BookWithCountRepository


def repository_to_api(book_with_count_repository: BookWithCountRepository) -> BookWithCountAPI:
    return BookWithCountAPI(
        book_uid=book_with_count_repository.book.book_uid,
        name=book_with_count_repository.book.name,
        author=book_with_count_repository.book.author,
        genre=book_with_count_repository.book.genre,
        condition=book_with_count_repository.book.condition,
        available_count=book_with_count_repository.available_count,
    )
