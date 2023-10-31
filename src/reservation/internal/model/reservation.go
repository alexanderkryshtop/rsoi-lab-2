package model

type Reservation struct {
	ReservationUID string `json:"reservationUid"`
	Username       string `json:"username"`
	BookUID        string `json:"bookUid"`
	LibraryUID     string `json:"libraryUid"`
	Status         string `json:"status"`
	StartDate      string `json:"startDate"`
	TillDate       string `json:"tillDate"`
}

type ReservationRequest struct {
	BookUID    string `json:"bookUid"`
	LibraryUID string `json:"libraryUid"`
	TillDate   string `json:"tillDate"`
}
