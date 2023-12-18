from dataclasses import dataclass
from uuid import UUID


@dataclass
class LibraryAPI:
    library_uid: UUID
    name: str
    city: str
    address: str
