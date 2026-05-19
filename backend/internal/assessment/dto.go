package assessment

type CreateAssessmentRequest struct {
	AssessmentName string `json:"assessment_name" validate:"required,max=100"`
	AssessmentType string `json:"assessment_type" validate:"required,oneof=Formatif Sumatif Proyek UTS UAS"`
	AssessmentDate string `json:"assessment_date" validate:"required"` // YYYY-MM-DD
}

type UpdateAssessmentRequest struct {
	AssessmentName string `json:"assessment_name" validate:"omitempty,max=100"`
	AssessmentType string `json:"assessment_type" validate:"omitempty,oneof=Formatif Sumatif Proyek UTS UAS"`
	AssessmentDate string `json:"assessment_date"` // YYYY-MM-DD
}

type ScoreItem struct {
	StudentID string  `json:"student_id" validate:"required,uuid"`
	Score     float64 `json:"score" validate:"min=0,max=100"`
	Notes     string  `json:"notes"`
}

type UpsertScoresRequest struct {
	Scores []ScoreItem `json:"scores" validate:"required,dive"`
}

type AttendanceItem struct {
	StudentID string `json:"student_id" validate:"required,uuid"`
	Status    string `json:"status" validate:"required,oneof=HADIR SAKIT IZIN ALPA"`
	Notes     string `json:"notes"`
}

type UpsertAttendancesRequest struct {
	Attendances []AttendanceItem `json:"attendances" validate:"required,dive"`
}
