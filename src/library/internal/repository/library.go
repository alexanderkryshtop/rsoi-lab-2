package repository

import (
	"context"
	"github.com/jackc/pgx/v5/pgxpool"
	"library/internal/model"
)

type Repository interface {
	GetAll(city string) ([]*model.Library, error)
	GetBooks(libraryUID string) ([]*model.Book, error)
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
		library_uid,
		name,
		city,
		address
	FROM
	    library
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

func (repository *LibraryRepository) GetBooks(libraryUID string) ([]*model.Book, error) {
	var books []*model.Book

	query := `
	SELECT
		book_uid,
		name,
		author,
		genre,
		condition,
		available_count
	FROM
	    books INNER JOIN library_books ON books.id = library_books.book_id
	WHERE
	    library_books.library_id = $1
	`
	rows, err := repository.dbPool.Query(
		context.Background(),
		query,
		libraryUID,
	)
	defer rows.Close()

	if err != nil {
		return nil, err
	}

	for rows.Next() {
		book := new(model.Book)
		if err := rows.Scan(
			&book.BookUID,
			&book.Name,
			&book.Author,
			&book.Genre,
			&book.Condition,
			&book.AvailableCount,
		); err != nil {
			return nil, err
		}
		books = append(books, book)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}

	return books, nil
}
