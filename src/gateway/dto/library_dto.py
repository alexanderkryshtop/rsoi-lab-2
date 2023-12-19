from dataclasses import dataclass

from uuid import UUID


@dataclass
class BookDTO:
    book_uid: UUID
    name: str
    author: str
    genre: str

    def to_dict(self) -> dict:
        return {
            "bookUid": self.book_uid,
            "name": self.name,
            "author": self.author,
            "genre": self.genre,
        }


@dataclass
class LibraryDTO:
    library_uid: UUID
    name: str
    address: str
    city: str

    def to_dict(self) -> dict:
        return {
            "libraryUid": self.library_uid,
            "name": self.name,
            "address": self.address,
            "city": self.city,
        }
