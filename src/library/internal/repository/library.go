package repository

import (
	"context"
	"github.com/jackc/pgx/v5/pgxpool"
	"library/internal/model"
)

type Repository interface {
	GetAll(city string) ([]*model.Library, error)
}

type LibraryRepository struct {
	dbPool *pgxpool.Pool
}

func NewLibraryRepository(dbPool *pgxpool.Pool) *LibraryRepository {
	return &LibraryRepository{
		dbPool: dbPool,
	}
}

func (repository *LibraryRepository) GetAll(city string) ([]*model.Library, error) {
	var libraries []*model.Library

	query := `
	SELECT
		*
	FROM
	    libraries
	WHERE
	    city = $1
	`
	rows, err := repository.dbPool.Query(
		context.Background(),
		query,
		city,
	)
	defer rows.Close()

	if err != nil {
		return nil, err
	}

	for rows.Next() {
		library := new(model.Library)
		if err := rows.Scan(
			&library.LibraryUID,
			&library.Name,
			&library.City,
			&library.Address,
		); err != nil {
			return nil, err
		}
		libraries = append(libraries, library)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}

	return libraries, nil
}
