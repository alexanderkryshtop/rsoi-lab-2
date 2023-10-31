package handlers

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"reservation/internal/model"
)

func (handler *Handler) CreateReservation() func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		requestBody, err := io.ReadAll(r.Body)

		defer func(Body io.ReadCloser) {
			_ = Body.Close()
		}(r.Body)

		if err != nil {
			http.Error(w, fmt.Sprintf("http request body read: %+v", err), http.StatusInternalServerError)
			return
		}

		reservationRequest := new(model.ReservationRequest)
		err = json.Unmarshal(requestBody, reservationRequest)
		if err != nil {
			http.Error(w, fmt.Sprintf("json unmarshal: %+v", err), http.StatusInternalServerError)
			return
		}

		//username := r.Header.Get("X-User-Name")

	}
}
