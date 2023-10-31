package repository

import (
	"context"
	"github.com/jackc/pgx/v5/pgxpool"
	"rating/internal/model"
)

type Repository interface {
	GetRating(username string) (*model.Rating, error)
}

type RatingRepository struct {
	dbPool *pgxpool.Pool
}

func NewRatingRepository(dbPool *pgxpool.Pool) *RatingRepository {
	return &RatingRepository{
		dbPool: dbPool,
	}
}

func (repository *RatingRepository) GetRating(username string) (*model.Rating, error) {
	query := `
		SELECT
		    username,
			stars
		FROM
		    rating
		WHERE username = $1
	`
	rating := new(model.Rating)
	err := repository.dbPool.QueryRow(
		context.Background(),
		query,
		username,
	).Scan(
		&rating.Username,
		&rating.Stars,
	)

	if err != nil {
		return nil, err
	}
	return rating, nil
}
