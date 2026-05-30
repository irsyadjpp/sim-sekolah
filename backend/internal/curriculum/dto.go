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

// Analysis Data Integration DTOs (FR 4.2.1-4.2.4)

type SWOTDataForKSP struct {
	SessionID     string     `json:"session_id"`
	SessionName   string     `json:"session_name"`
	Strengths     []SWOTItem `json:"strengths"`
	Weaknesses    []SWOTItem `json:"weaknesses"`
	Opportunities []SWOTItem `json:"opportunities"`
	Threats       []SWOTItem `json:"threats"`
	AnalysisDate  string     `json:"analysis_date"`
}

type SWOTItem struct {
	ID          string `json:"id"`
	Description string `json:"description"`
	Quadrant    string `json:"quadrant"`
	Priority    string `json:"priority"`
}

type RootCauseDataForKSP struct {
	RootCauseID      string          `json:"root_cause_id"`
	ProblemStatement string          `json:"problem_statement"`
	RootCauses       []RootCauseItem `json:"root_causes"`
	FiveWhysAnalysis []FiveWhysStep  `json:"five_whys_analysis"`
	Solutions        []SolutionItem  `json:"solutions"`
	AnalysisDate     string          `json:"analysis_date"`
}

type RootCauseItem struct {
	ID          string `json:"id"`
	Cause       string `json:"cause"`
	Category    string `json:"category"`
	ImpactLevel string `json:"impact_level"`
}

type FiveWhysStep struct {
	StepNumber int    `json:"step_number"`
	Question   string `json:"question"`
	Answer     string `json:"answer"`
}

type SolutionItem struct {
	ID          string `json:"id"`
	Description string `json:"description"`
	Status      string `json:"status"`
	Deadline    string `json:"deadline"`
}

type FishboneDataForKSP struct {
	DiagramID        string             `json:"diagram_id"`
	DiagramName      string             `json:"diagram_name"`
	ProblemStatement string             `json:"problem_statement"`
	Categories       []FishboneCategory `json:"categories"`
	AnalysisDate     string             `json:"analysis_date"`
}

type FishboneCategory struct {
	CategoryName string         `json:"category_name"`
	Nodes        []FishboneNode `json:"nodes"`
}

type FishboneNode struct {
	ID         string `json:"id"`
	Text       string `json:"text"`
	CauseLevel int    `json:"cause_level"`
}

type StudentNeedsDataForKSP struct {
	ProfileID            string            `json:"profile_id"`
	ProfileName          string            `json:"profile_name"`
	ProfileDimension     string            `json:"profile_dimension"`
	Needs                []StudentNeedItem `json:"needs"`
	PriorityDistribution map[string]int    `json:"priority_distribution"`
	AnalysisDate         string            `json:"analysis_date"`
}

type StudentNeedItem struct {
	ID          string `json:"id"`
	Need        string `json:"need"`
	Category    string `json:"category"`
	Priority    string `json:"priority"`
	ImpactLevel string `json:"impact_level"`
}

type AnalysisDataIntegrationRequest struct {
	CurriculumDocumentID  string                 `json:"curriculum_document_id" binding:"required"`
	IncludeSWOT           bool                   `json:"include_swot"`
	IncludeRootCause      bool                   `json:"include_root_cause"`
	IncludeFishbone       bool                   `json:"include_fishbone"`
	IncludeStudentNeeds   bool                   `json:"include_student_needs"`
	SWOTSessionID         string                 `json:"swot_session_id,omitempty"`
	RootCauseID           string                 `json:"root_cause_id,omitempty"`
	FishboneDiagramID     string                 `json:"fishbone_diagram_id,omitempty"`
	StudentNeedsProfileID string                 `json:"student_needs_profile_id,omitempty"`
	Customizations        map[string]interface{} `json:"customizations,omitempty"`
}

type AnalysisDataIntegrationResponse struct {
	CurriculumDocumentID string              `json:"curriculum_document_id"`
	IntegrationID        string              `json:"integration_id"`
	AnalysisData         AnalysisDataSummary `json:"analysis_data"`
	GeneratedContent     GeneratedContent    `json:"generated_content"`
	Status               string              `json:"status"`
	Message              string              `json:"message"`
}

type AnalysisDataSummary struct {
	SWOTData         *SWOTDataForKSP         `json:"swot_data,omitempty"`
	RootCauseData    *RootCauseDataForKSP    `json:"root_cause_data,omitempty"`
	FishboneData     *FishboneDataForKSP     `json:"fishbone_data,omitempty"`
	StudentNeedsData *StudentNeedsDataForKSP `json:"student_needs_data,omitempty"`
}

type GeneratedContent struct {
	ExecutiveSummary string            `json:"executive_summary"`
	AnalysisSection  string            `json:"analysis_section"`
	Recommendations  []string          `json:"recommendations"`
	ActionPlan       string            `json:"action_plan"`
	Charts           map[string]string `json:"charts"`
}

type KSPExportWithAnalysisRequest struct {
	CurriculumDocumentID  string                 `json:"curriculum_document_id" binding:"required"`
	Format                string                 `json:"format" binding:"required,oneof=PDF WORD"` // PDF or WORD
	IncludeAnalysisData   bool                   `json:"include_analysis_data"`
	AnalysisIntegrationID string                 `json:"analysis_integration_id,omitempty"`
	Customizations        map[string]interface{} `json:"customizations,omitempty"`
}

type KSPExportWithAnalysisResponse struct {
	ExportID    string `json:"export_id"`
	DocumentURL string `json:"document_url"`
	Format      string `json:"format"`
	FileSize    int64  `json:"file_size"`
	GeneratedAt string `json:"generated_at"`
	ExpiresAt   string `json:"expires_at"`
}
