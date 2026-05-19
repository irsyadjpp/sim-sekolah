package enrollment

type CreateEnrollmentRequest struct {
	StudentID string `json:"student_id" validate:"required,uuid"`
}

// BulkEnrollRequest untuk mendaftarkan banyak siswa sekaligus ke satu kelas
type BulkEnrollRequest struct {
	StudentIDs []string `json:"student_ids" validate:"required,min=1,dive,uuid"`
}
