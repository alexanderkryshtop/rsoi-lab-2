package service

import (
	"rating/internal/model"
	"rating/internal/repository"
)

type Service interface {
	GetRating(username string) (*model.Rating, error)
}

type RatingService struct {
	repository repository.Repository
}

func NewRatingService(repository repository.Repository) *RatingService {
	return &RatingService{
		repository: repository,
	}
}

func (service *RatingService) GetRating(username string) (*model.Rating, error) {
	return service.repository.GetRating(username)
}
