package ppdb

type RegisterPPDBRequest struct {
	SchoolYearID    string `json:"school_year_id" validate:"required,uuid"`
	AdmissionPathID string `json:"admission_path_id" validate:"required,uuid"`

	// Student
	FullName   string `json:"full_name" validate:"required"`
	NIK        string `json:"nik" validate:"required,len=16"`
	NISN       string `json:"nisn"`
	BirthPlace string `json:"birth_place" validate:"required"`
	BirthDate  string `json:"birth_date" validate:"required"` // YYYY-MM-DD
	Gender     string `json:"gender" validate:"required,oneof=L P"`
	Religion   string `json:"religion" validate:"required"`

	// Address
	Address            string  `json:"address" validate:"required"`
	Village            string  `json:"village"`
	District           string  `json:"district"`
	Regency            string  `json:"regency"`
	Province           string  `json:"province"`
	PostalCode         string  `json:"postal_code"`
	DistanceToSchoolKm float64 `json:"distance_to_school_km"`

	// Parents
	FatherName       string `json:"father_name"`
	FatherNIK        string `json:"father_nik"`
	FatherOccupation string `json:"father_occupation"`
	MotherName       string `json:"mother_name"`
	MotherNIK        string `json:"mother_nik"`
	MotherOccupation string `json:"mother_occupation"`
	PhoneNumber      string `json:"phone_number" validate:"required"`
}

type VerifyPPDBRequest struct {
	Status string `json:"status" validate:"required,oneof=Verified Accepted Rejected"`
	Notes  string `json:"notes"`
}
