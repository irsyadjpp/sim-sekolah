package curriculum

import "github.com/google/uuid"

type InitializeCurriculumRequest struct {
	AcademicYearID uuid.UUID `json:"academic_year_id" validate:"required"`
	SchoolID       uuid.UUID `json:"school_id" validate:"required"`
}

type TriggerChapterRequest struct {
	CurriculumDocumentID uuid.UUID `json:"curriculum_document_id" validate:"required"`
	ChapterNumber        int       `json:"chapter_number" validate:"required"`
	Title                string    `json:"title" validate:"required"`
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
