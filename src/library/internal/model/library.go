package model

type Library struct {
	LibraryUID string `json:"libraryUid"`
	Name       string `json:"name"`
	City       string `json:"city"`
	Address    string `json:"address"`
}

type Book struct {
	BookUID        string `json:"bookUid"`
	Name           string `json:"name"`
	Author         string `json:"author"`
	Genre          string `json:"genre"`
	Condition      string `json:"condition"`
	AvailableCount int    `json:"availableCount"`
}
