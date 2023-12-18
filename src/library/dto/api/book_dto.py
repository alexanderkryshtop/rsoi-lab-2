from dataclasses import dataclass
from uuid import UUID


@dataclass
class BookWithCountAPI:
    book_uid: UUID
    name: str
    author: str
    genre: str
    condition: str
    available_count: int
