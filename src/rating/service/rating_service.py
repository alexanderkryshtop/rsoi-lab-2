from typing import Optional
from entity import Rating
from repository import RatingModel

class RatingService:
    
    def get_star_count(self, username: str) -> Optional[int]:
        ratingModel: RatingModel = RatingModel.query.filter(RatingModel.username == username).one_or_none()
        if not ratingModel:
            return None
        return ratingModel.stars
