from uuid import UUID

import requests
from flask import current_app


class LibraryService:

    @staticmethod
    def get_book_available_count(book_uid: str, library_uid: str) -> int:
        json_body = {
            "bookUid": book_uid,
            "libraryUid": library_uid,
        }
        result = requests.post(
            f"{current_app.config['library']}/libraries/book/count",
            json=json_body
        )
        json_data = result.json()
        return json_data["count"]
