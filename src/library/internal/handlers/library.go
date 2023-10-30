package handlers

import (
	"encoding/json"
	"fmt"
	"io"
	"library/internal/model"
	"net/http"
	"strconv"
)

func (handler *Handler) GetLibraries() func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		defer func(Body io.ReadCloser) {
			_ = Body.Close()
		}(r.Body)

		city := r.URL.Query().Get("city")
		page, err := strconv.ParseInt(r.URL.Query().Get("page"), 10, 32)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot parse: %+v", err), http.StatusBadRequest)
		}

		size, err := strconv.ParseInt(r.URL.Query().Get("size"), 10, 32)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot parse: %+v", err), http.StatusBadRequest)
		}

		libraries, err := handler.service.GetLibraries(int(page), int(size), city)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot get libraries: %+v", err), http.StatusInternalServerError)
		}

		response := &struct {
			Page          int              `json:"page"`
			PageSize      int              `json:"pageSize"`
			TotalElements int              `json:"totalElements"`
			Items         []*model.Library `json:"items"`
		}{
			Page:          int(page),
			PageSize:      int(size),
			TotalElements: len(libraries),
			Items:         libraries,
		}

		jsonResponse, err := json.Marshal(response)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot marshal response: %+v", err), http.StatusInternalServerError)
		}

		w.Header().Add("Content-Type", "application/json")
		_, _ = w.Write(jsonResponse)
	}
}
