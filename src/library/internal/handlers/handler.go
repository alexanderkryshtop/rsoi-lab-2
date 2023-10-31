package handlers

import (
	"github.com/go-chi/chi/v5"
	"library/internal/service"
	"net/http"
)

type Handler struct {
	service service.Service
}

func NewHandler(service service.Service) *Handler {
	return &Handler{
		service: service,
	}
}

func (handler *Handler) Routes() http.Handler {
	mux := chi.NewMux()
	mux.Get("/api/v1/libraries", handler.GetLibraries())
	mux.Get("/api/v1/{libraryUid}/books", handler.GetBooksInLibrary())
	return mux
}
