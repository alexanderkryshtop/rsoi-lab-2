from dataclasses import dataclass
from enum import Enum

class BookCondition(Enum):
    EXCELLENT = 'EXCELLENT',
    GOOD = 'GOOD',
    BAD = 'BAD',

@dataclass
class Book:
    id: int
    book_uid: str
    name: str
    author: str
    genre: str
    condition: BookCondition