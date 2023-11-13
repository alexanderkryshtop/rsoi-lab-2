from dataclasses import dataclass

@dataclass
class Library:
    id: int
    library_uid: str
    name: str
    city: str
    address: str