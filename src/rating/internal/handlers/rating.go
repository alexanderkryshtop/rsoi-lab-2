package handlers

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

func (handler *Handler) GetRating() func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		defer func(Body io.ReadCloser) {
			_ = Body.Close()
		}(r.Body)

		username := r.Header.Get("X-User-Name")
		if username == "" {
			http.Error(w, fmt.Sprintf("wrong username: %+v", username), http.StatusBadRequest)
			return
		}

		rating, err := handler.service.GetRating(username)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot get rating: %+v", err), http.StatusInternalServerError)
			return
		}

		response := &struct {
			Stars int `json:"stars"`
		}{
			Stars: rating.Stars,
		}

		jsonResponse, err := json.Marshal(response)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot marshal response: %+v", err), http.StatusInternalServerError)
			return
		}

		w.Header().Add("Content-Type", "application/json")
		_, _ = w.Write(jsonResponse)
	}
}
