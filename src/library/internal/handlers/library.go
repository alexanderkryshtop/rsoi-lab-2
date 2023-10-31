package handlers

import (
	"encoding/json"
	"fmt"
	"github.com/go-chi/chi/v5"
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
			return
		}

		size, err := strconv.ParseInt(r.URL.Query().Get("size"), 10, 32)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot parse: %+v", err), http.StatusBadRequest)
			return
		}

		libraries, err := handler.service.GetLibraries(int(page), int(size), city)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot get libraries: %+v", err), http.StatusInternalServerError)
			return
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
			return
		}

		w.Header().Add("Content-Type", "application/json")
		_, _ = w.Write(jsonResponse)
	}
}

func (handler *Handler) GetBooksInLibrary() func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		defer func(Body io.ReadCloser) {
			_ = Body.Close()
		}(r.Body)

		libraryUID := chi.URLParam(r, "libraryUid")
		if libraryUID == "" {
			http.Error(w, fmt.Sprintf("cannot parse libraryUid: %+v", libraryUID), http.StatusBadRequest)
			return
		}

		pageStr := r.URL.Query().Get("page")
		page, err := strconv.ParseInt(pageStr, 10, 32)
		if pageStr != "" && err != nil {
			http.Error(w, fmt.Sprintf("cannot parse: %+v", err), http.StatusBadRequest)
			return
		}

		sizeStr := r.URL.Query().Get("size")
		size, err := strconv.ParseInt(sizeStr, 10, 32)
		if sizeStr != "" && err != nil {
			http.Error(w, fmt.Sprintf("cannot parse: %+v", err), http.StatusBadRequest)
			return
		}

		books, err := handler.service.GetBooksInLibrary(libraryUID)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot get libraries: %+v", err), http.StatusInternalServerError)
			return
		}

		response := &struct {
			Page          int           `json:"page"`
			PageSize      int           `json:"pageSize"`
			TotalElements int           `json:"totalElements"`
			Items         []*model.Book `json:"items"`
		}{
			Page:          int(page),
			PageSize:      int(size),
			TotalElements: len(books),
			Items:         books,
		}

		jsonResponse, err := json.Marshal(response)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot marshal response: %+v", err), http.StatusInternalServerError)
		}

		w.Header().Add("Content-Type", "application/json")
		_, _ = w.Write(jsonResponse)
	}
}

func (handler *Handler) GetBookFromLibrary() func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		defer func(Body io.ReadCloser) {
			_ = Body.Close()
		}(r.Body)

		libraryUID := chi.URLParam(r, "libraryUid")
		if libraryUID == "" {
			http.Error(w, fmt.Sprintf("cannot parse libraryUid: %+v", libraryUID), http.StatusBadRequest)
			return
		}

		pageStr := r.URL.Query().Get("page")
		page, err := strconv.ParseInt(pageStr, 10, 32)
		if pageStr != "" && err != nil {
			http.Error(w, fmt.Sprintf("cannot parse: %+v", err), http.StatusBadRequest)
			return
		}

		sizeStr := r.URL.Query().Get("size")
		size, err := strconv.ParseInt(sizeStr, 10, 32)
		if sizeStr != "" && err != nil {
			http.Error(w, fmt.Sprintf("cannot parse: %+v", err), http.StatusBadRequest)
			return
		}

		books, err := handler.service.GetBooksInLibrary(libraryUID)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot get libraries: %+v", err), http.StatusInternalServerError)
			return
		}

		response := &struct {
			Page          int           `json:"page"`
			PageSize      int           `json:"pageSize"`
			TotalElements int           `json:"totalElements"`
			Items         []*model.Book `json:"items"`
		}{
			Page:          int(page),
			PageSize:      int(size),
			TotalElements: len(books),
			Items:         books,
		}

		jsonResponse, err := json.Marshal(response)
		if err != nil {
			http.Error(w, fmt.Sprintf("cannot marshal response: %+v", err), http.StatusInternalServerError)
		}

		w.Header().Add("Content-Type", "application/json")
		_, _ = w.Write(jsonResponse)
	}
}
