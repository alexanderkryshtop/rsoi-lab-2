package handlers

import (
	"github.com/go-chi/chi/v5"
	"net/http"
	"reservation/internal/service"
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
	mux.Post("/api/v1/reservation", handler.CreateReservation())
	return mux
}
