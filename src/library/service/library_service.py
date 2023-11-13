from typing import Optional
from entity import Library
from repository import LibraryModel

class LibraryService:
    
    def get_libraries(self, city: str, page: Optional[int] = None, size: Optional[int] = None) -> list[Library]:
        libraryModels: list[LibraryModel] = LibraryModel.query.filter(LibraryModel.city == city).all()
        libraries = [model.to_entity() for model in libraryModels]
        return libraries