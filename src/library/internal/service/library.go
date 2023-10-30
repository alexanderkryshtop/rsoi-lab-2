package service

import (
	"library/internal/model"
	"library/internal/repository"
)

type Service interface {
	GetLibraries(page int, size int, city string) ([]*model.Library, error)
}

type LibraryService struct {
	repository repository.Repository
}

func NewLibraryService(repository repository.Repository) *LibraryService {
	return &LibraryService{
		repository: repository,
	}
}

func (service *LibraryService) GetLibraries(page int, size int, city string) ([]*model.Library, error) {
	return service.repository.GetAll(city)
}
