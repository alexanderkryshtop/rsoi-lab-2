from dataclasses import dataclass
from enum import Enum
from typing_extensions import Self

class BookCondition(Enum):
    EXCELLENT = 'EXCELLENT',
    GOOD = 'GOOD',
    BAD = 'BAD',

@dataclass(frozen=True)
class Book:
    id: int
    book_uid: str
    name: str
    author: str
    genre: str
    condition: BookCondition
