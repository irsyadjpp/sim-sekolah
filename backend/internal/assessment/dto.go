package assessment

type CreateAssessmentRequest struct {
	AssessmentName     string `json:"assessment_name" validate:"required,max=100"`
	AssessmentType     string `json:"assessment_type" validate:"required,oneof=Formatif Sumatif Proyek UTS UAS"`
	AgeAppropriateType string `json:"age_appropriate_type" validate:"omitempty"` // SD-specific types
	AssessmentDate     string `json:"assessment_date" validate:"required"`       // YYYY-MM-DD
}

type UpdateAssessmentRequest struct {
	AssessmentName     string `json:"assessment_name" validate:"omitempty,max=100"`
	AssessmentType     string `json:"assessment_type" validate:"omitempty,oneof=Formatif Sumatif Proyek UTS UAS"`
	AgeAppropriateType string `json:"age_appropriate_type" validate:"omitempty"`
	AssessmentDate     string `json:"assessment_date"` // YYYY-MM-DD
}

type AgeAppropriateTypeResponse struct {
	ID          string `json:"id"`
	Description string `json:"description"`
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

// SD Assessment Criteria DTOs
type CreateSDAssessmentCriteriaRequest struct {
	AssessmentType string `json:"assessment_type" binding:"required"`
	PhaseID        string `json:"phase_id"`
	CriteriaName   string `json:"criteria_name" binding:"required,max=100"`
	Description    string `json:"description" binding:"required"`
	RubricElements string `json:"rubric_elements"` // JSON string
	IsActive       *bool  `json:"is_active"`
}

type UpdateSDAssessmentCriteriaRequest struct {
	AssessmentType string `json:"assessment_type" binding:"omitempty"`
	PhaseID        string `json:"phase_id"`
	CriteriaName   string `json:"criteria_name" binding:"omitempty,max=100"`
	Description    string `json:"description" binding:"omitempty"`
	RubricElements string `json:"rubric_elements"`
	IsActive       *bool  `json:"is_active"`
}

type SDAssessmentCriteriaResponse struct {
	ID              string `json:"id"`
	AssessmentType  string `json:"assessment_type"`
	PhaseID         string `json:"phase_id"`
	CriteriaName    string `json:"criteria_name"`
	Description     string `json:"description"`
	RubricElements  string `json:"rubric_elements"`
	IsActive        bool   `json:"is_active"`
	TypeDescription string `json:"type_description,omitempty"`
	CreatedAt       string `json:"created_at"`
	UpdatedAt       string `json:"updated_at"`
}

type SDAssessmentCriteriaListResponse struct {
	Criteria []SDAssessmentCriteriaResponse `json:"criteria"`
	Total    int                            `json:"total"`
}
