from typing import Optional
from entity import Library
from repository import LibraryModel

class LibraryService:
    
    def get_libraries(self, city: str, page: Optional[int] = None, size: Optional[int] = None) -> list[Library]:
        a = LibraryModel.query.all()
        print(a)
        pass