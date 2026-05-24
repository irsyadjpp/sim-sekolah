package curriculum

import "github.com/google/uuid"

type InitializeCurriculumRequest struct {
	AcademicYearID           uuid.UUID `json:"academic_year_id" validate:"required"`
	SchoolID                 uuid.UUID `json:"school_id" validate:"required"`
	CurriculumType           string    `json:"curriculum_type" validate:"omitempty,oneof=INTRAKURIKULER KOKURIKULER EKSTRAKURIKULER"`
	CurriculumClassification string    `json:"curriculum_classification" validate:"omitempty"`
}

type TriggerChapterRequest struct {
	CurriculumDocumentID uuid.UUID `json:"curriculum_document_id" validate:"required"`
	ChapterNumber        int       `json:"chapter_number" validate:"required"`
	Title                string    `json:"title" validate:"required"`
}

type UpdateCurriculumTypeRequest struct {
	CurriculumType string `json:"curriculum_type" validate:"required"`
}

type UpdateChapterRequest struct {
	Content string `json:"content" validate:"required"`
}

type ReadinessResponse struct {
	SchoolID              uuid.UUID `json:"school_id"`
	IsReadyToFormulate    bool      `json:"is_ready_to_formulate"`
	ReadinessScorePercent float64   `json:"readiness_score_percent"`
	MissingParameters     []string  `json:"missing_parameters"`
}

type TriggerChapterResponse struct {
	Message string    `json:"message"`
	QueueID uuid.UUID `json:"queue_id"`
	Status  string    `json:"status"`
}

// Co-curricular Activity DTOs
type CreateKokurikulerActivityRequest struct {
	CurriculumDocumentID string `json:"curriculum_document_id" binding:"required"`
	ActivityName         string `json:"activity_name" binding:"required,max=100"`
	LinkedSubjectID      string `json:"linked_subject_id"`
	Description          string `json:"description"`
	Schedule             string `json:"schedule"`
	IsActive             *bool  `json:"is_active"`
}

type UpdateKokurikulerActivityRequest struct {
	ActivityName    string `json:"activity_name" binding:"omitempty,max=100"`
	LinkedSubjectID string `json:"linked_subject_id"`
	Description     string `json:"description"`
	Schedule        string `json:"schedule"`
	IsActive        *bool  `json:"is_active"`
}

type KokurikulerActivityResponse struct {
	ID                   string `json:"id"`
	CurriculumDocumentID string `json:"curriculum_document_id"`
	ActivityName         string `json:"activity_name"`
	LinkedSubjectID      string `json:"linked_subject_id"`
	LinkedSubjectName    string `json:"linked_subject_name,omitempty"`
	Description          string `json:"description"`
	Schedule             string `json:"schedule"`
	IsActive             bool   `json:"is_active"`
	CreatedAt            string `json:"created_at"`
	UpdatedAt            string `json:"updated_at"`
}

// Extra-curricular Activity DTOs
type CreateEkstrakurikulerActivityRequest struct {
	CurriculumDocumentID string `json:"curriculum_document_id" binding:"required"`
	ActivityName         string `json:"activity_name" binding:"required,max=100"`
	ActivityCategory     string `json:"activity_category" binding:"required"`
	Description          string `json:"description"`
	Schedule             string `json:"schedule"`
	InstructorID         string `json:"instructor_id"`
	IsActive             *bool  `json:"is_active"`
}

type UpdateEkstrakurikulerActivityRequest struct {
	ActivityName     string `json:"activity_name" binding:"omitempty,max=100"`
	ActivityCategory string `json:"activity_category" binding:"omitempty"`
	Description      string `json:"description"`
	Schedule         string `json:"schedule"`
	InstructorID     string `json:"instructor_id"`
	IsActive         *bool  `json:"is_active"`
}

type EkstrakurikulerActivityResponse struct {
	ID                   string `json:"id"`
	CurriculumDocumentID string `json:"curriculum_document_id"`
	ActivityName         string `json:"activity_name"`
	ActivityCategory     string `json:"activity_category"`
	CategoryDescription  string `json:"category_description,omitempty"`
	Description          string `json:"description"`
	Schedule             string `json:"schedule"`
	InstructorID         string `json:"instructor_id"`
	InstructorName       string `json:"instructor_name,omitempty"`
	IsActive             bool   `json:"is_active"`
	CreatedAt            string `json:"created_at"`
	UpdatedAt            string `json:"updated_at"`
}
