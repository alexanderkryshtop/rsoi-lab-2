package service

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"reservation/cmd/configuration"
	"reservation/internal/model"
	"reservation/internal/repository"
	"time"

	"github.com/google/uuid"
)

const (
	YYYYMMDD = "2006-01-02"
)

type Service interface {
	GetReservation(username string) (*model.Reservation, error)
	CreateReservation(username string, bookUID string, libraryUID string, tillDate string) (*model.Reservation, error)
}

type ReservationService struct {
	repository      repository.Repository
	gatewayEndpoint configuration.EndpointConfig
}

func NewReservationService(
	repository repository.Repository,
	gatewayEndpoint configuration.EndpointConfig,
) *ReservationService {
	return &ReservationService{
		repository:      repository,
		gatewayEndpoint: gatewayEndpoint,
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
	books, err := service.repository.GetRentedBooksCount(username)
	if err != nil {
		return nil, err
	}

	url := fmt.Sprintf("http://%s:%d/api/v1/rating")
	stars, err := service.getStarCount(username, url)
	if err != nil {
		return nil, err
	}

	if stars <= books {
		return nil, fmt.Errorf("not enough stars")
	}

	reservation := &model.Reservation{
		ReservationUID: uuid.New().String(),
		Username:       username,
		BookUID:        bookUID,
		LibraryUID:     libraryUID,
		Status:         "RENTED",
		StartDate:      time.Now().Format(YYYYMMDD),
		TillDate:       tillDate,
	}

	err = service.repository.CreateReservation(reservation)
	if err != nil {
		return nil, err
	}

	// return service.repository.CreateReservation(nil) // TODO
	return nil, err

}

func (service *ReservationService) getStarCount(username string, url string) (int, error) {
	client := http.Client{}
	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return 0, err
	}
	req.Header.Set("X-User-Name", username)
	resp, err := client.Do(req)
	if err != nil {
		return 0, err
	}

	responseBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return 0, err
	}

	ratingResponse := new(struct {
		Stars int `json:"stars"`
	})

	err = json.Unmarshal(responseBytes, ratingResponse)
	if err != nil {
		return 0, err
	}

	return ratingResponse.Stars, nil
}
