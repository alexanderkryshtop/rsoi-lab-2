from typing import Optional
from entity import Rating
from repository import RatingModel

class RatingService:
    
    def get_star_count(self, username: str) -> Optional[int]:
        ratingModel: RatingModel = RatingModel.query.filter(RatingModel.username == username).one_or_none()
        if not ratingModel:
            return None
        return ratingModel.stars

    def change_star_count(self, username: str, delta: int) -> Optional[int]:
        ratingModel: RatingModel = RatingModel.query.filter(RatingModel.username == username).one_or_none()
        if not ratingModel:
            return None
        new_rating = ratingModel.stars + delta
        if new_rating >= 100:
            new_rating = 100
        if new_rating <= 1:
            new_rating = 1
        ratingModel.stars = new_rating
        RatingModel.query.session.commit()
        return ratingModel.stars
