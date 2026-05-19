package academic_year

type CreateAcademicYearRequest struct {
	YearName string `json:"year_name" validate:"required,max=20"`
	Semester string `json:"semester" validate:"required,oneof=Ganjil Genap"`
	IsActive bool   `json:"is_active"`
}

type UpdateAcademicYearRequest struct {
	YearName string `json:"year_name" validate:"omitempty,max=20"`
	Semester string `json:"semester" validate:"omitempty,oneof=Ganjil Genap"`
	IsActive *bool  `json:"is_active"` // Pointer agar bisa deteksi false explicit
}
