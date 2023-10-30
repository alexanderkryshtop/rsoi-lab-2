package model

type Library struct {
	LibraryUID string `json:"libraryUid"`
	Name       string `json:"name"`
	City       string `json:"city"`
	Address    string `json:"address"`
}
