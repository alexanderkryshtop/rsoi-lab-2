from typing import Tuple

import requests
from flask import current_app


class RatingService:

    @staticmethod
    def get_user_rating(username: str) -> Tuple[int, int]:
        result = requests.get(
            f"{current_app.config['rating']}/rating",
            headers={"X-User-Name": username}
        )
        json_data = result.json()
        return json_data["stars"], result.status_code