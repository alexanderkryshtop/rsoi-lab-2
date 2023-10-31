package repository

import (
	"context"
	"github.com/jackc/pgx/v5/pgxpool"
	"reservation/internal/model"
)

type Repository interface {
	GetReservation(username string) (*model.Reservation, error)
	CreateReservation(reservation *model.Reservation) error
	GetRentedBooksCount(username string) (int, error)
}

type ReservationRepository struct {
	dbPool *pgxpool.Pool
}

func NewReservationRepository(dbPool *pgxpool.Pool) *ReservationRepository {
	return &ReservationRepository{
		dbPool: dbPool,
	}
}

func (repository *ReservationRepository) GetReservation(username string) (*model.Reservation, error) {
	query := `
		SELECT
		    reservation_uid,
		    username,
		    book_uid,
		    library_uid,
		    status,
		    start_date,
		    till_date
		FROM
		    reservation
		WHERE username = $1
	`
	reservation := new(model.Reservation)
	err := repository.dbPool.QueryRow(
		context.Background(),
		query,
		username,
	).Scan(
		&reservation.ReservationUID,
		&reservation.Username,
		&reservation.BookUID,
		&reservation.LibraryUID,
		&reservation.Status,
		&reservation.StartDate,
		&reservation.TillDate,
	)

	if err != nil {
		return nil, err
	}
	return reservation, nil
}

func (repository *ReservationRepository) CreateReservation(reservation *model.Reservation) error {
	query := `
		INSERT INTO
			reservation(reservation_uid, username, book_uid, library_uid, status, start_date, till_date)
		VALUES ($1, $2, $3, $4, $5, $6, $7)
	`
	_, err := repository.dbPool.Exec(
		context.Background(),
		query,
		reservation.ReservationUID,
		reservation.Username,
		reservation.BookUID,
		reservation.LibraryUID,
		reservation.Status,
		reservation.StartDate,
		reservation.TillDate,
	)

	return err
}

func (repository *ReservationRepository) GetRentedBooksCount(username string) (int, error) {
	query := `
		SELECT
			count(*)
		FROM
		    reservation
		WHERE
			username = $1 AND status = 'RENTED'
	`

	var count int
	err := repository.dbPool.QueryRow(
		context.Background(),
		query,
		username,
	).Scan(&count)

	if err != nil {
		return 0, err
	}

	return count, nil
}
