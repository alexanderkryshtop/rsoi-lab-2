package service

import (
	"reservation/internal/model"
	"reservation/internal/repository"
)

type Service interface {
	GetReservation(username string) (*model.Reservation, error)
	CreateReservation(username string, bookUID string, libraryUID string, tillDate string) (*model.Reservation, error)
}

type ReservationService struct {
	repository repository.Repository
}

func NewReservationService(repository repository.Repository) *ReservationService {
	return &ReservationService{
		repository: repository,
	}
}

func (service *ReservationService) GetReservation(username string) (*model.Reservation, error) {
	return service.repository.GetReservation(username)
}

func (service *ReservationService) CreateReservation(
	username string,
	bookUID string,
	libraryUID string,
	tillDate string,
) (*model.Reservation, error) {
	_, err := service.repository.GetRentedBooksCount(username)
	if err != nil {
		return nil, err
	}

	// return service.repository.CreateReservation(nil) // TODO
	return nil, err

}
