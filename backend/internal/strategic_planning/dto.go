package strategic_planning

import (
	"time"

	"github.com/google/uuid"
)

// Rapor Pendidikan DTOs
type CreateRaporPendidikanRequest struct {
	SchoolID       string   `json:"school_id" validate:"required,uuid"`
	Year           string   `json:"year" validate:"required,max=10"`
	Semester       string   `json:"semester" validate:"required,max=10"`
	LiteracyScore  *float64 `json:"literacy_score" validate:"omitempty,min=0,max=100"`
	NumeracyScore  *float64 `json:"numeracy_score" validate:"omitempty,min=0,max=100"`
	CharacterScore *float64 `json:"character_score" validate:"omitempty,min=0,max=100"`
	RawData        *string  `json:"raw_data"`
}

type UpdateRaporPendidikanRequest struct {
	Year             string   `json:"year" validate:"omitempty,max=10"`
	Semester         string   `json:"semester" validate:"omitempty,max=10"`
	LiteracyScore    *float64 `json:"literacy_score" validate:"omitempty,min=0,max=100"`
	NumeracyScore    *float64 `json:"numeracy_score" validate:"omitempty,min=0,max=100"`
	CharacterScore   *float64 `json:"character_score" validate:"omitempty,min=0,max=100"`
	RawData          *string  `json:"raw_data"`
	SyncStatus       string   `json:"sync_status" validate:"omitempty,oneof=SUCCESS FAILED PENDING"`
	SyncErrorMessage *string  `json:"sync_error_message"`
}

type SyncRaporPendidikanRequest struct {
	SchoolID string `json:"school_id" validate:"required,uuid"`
	Year     string `json:"year" validate:"required,max=10"`
	Semester string `json:"semester" validate:"required,max=10"`
}

// Survey DTOs
type CreateSurveyRequest struct {
	SchoolID         string     `json:"school_id" validate:"required,uuid"`
	TargetAudience   string     `json:"target_audience" validate:"required,oneof=murid ortu mitra guru staff"`
	Title            string     `json:"title" validate:"required,max=255"`
	Description      *string    `json:"description"`
	FormSchema       string     `json:"form_schema" validate:"required"`
	IsAnonymous      bool       `json:"is_anonymous"`
	AllowMultiple    bool       `json:"allow_multiple_responses"`
	MaxResponses     *int       `json:"max_responses" validate:"omitempty,min=1"`
	IsTemplate       bool       `json:"is_template"`
	TemplateCategory *string    `json:"template_category" validate:"omitempty,max=100"`
	StartDate        *time.Time `json:"start_date"`
	EndDate          *time.Time `json:"end_date"`
}

type UpdateSurveyRequest struct {
	TargetAudience   string     `json:"target_audience" validate:"omitempty,oneof=murid ortu mitra guru staff"`
	Title            *string    `json:"title" validate:"omitempty,max=255"`
	Description      *string    `json:"description"`
	FormSchema       *string    `json:"form_schema" validate:"omitempty"`
	Status           *string    `json:"status" validate:"omitempty,oneof=DRAFT ACTIVE CLOSED ARCHIVED"`
	IsAnonymous      *bool      `json:"is_anonymous"`
	AllowMultiple    *bool      `json:"allow_multiple_responses"`
	MaxResponses     *int       `json:"max_responses" validate:"omitempty,min=1"`
	IsTemplate       *bool      `json:"is_template"`
	TemplateCategory *string    `json:"template_category" validate:"omitempty,max=100"`
	StartDate        *time.Time `json:"start_date"`
	EndDate          *time.Time `json:"end_date"`
}

type CreateSurveyResponseRequest struct {
	SurveyID       string  `json:"survey_id" validate:"required,uuid"`
	RespondentID   *string `json:"respondent_id" validate:"omitempty,uuid"`
	RespondentName *string `json:"respondent_name" validate:"omitempty,max=255"`
	RespondentType *string `json:"respondent_type" validate:"omitempty,max=50"`
	AnswersJSON    string  `json:"answers_json" validate:"required"`
	IPAddress      *string `json:"ip_address" validate:"omitempty,max=50"`
	UserAgent      *string `json:"user_agent"`
}

type SurveyAnalyticsResponse struct {
	TotalResponses        int                    `json:"total_responses"`
	CompletionRate        float64                `json:"completion_rate"`
	AverageTimeToComplete int                    `json:"average_time_to_complete_minutes"`
	ResponsesByDate       map[string]int         `json:"responses_by_date"`
	ResponseData          map[string]interface{} `json:"response_data"`
}

// FGD Session DTOs
type CreateFGDSessionRequest struct {
	SchoolID            string    `json:"school_id" validate:"required,uuid"`
	Topic               string    `json:"topic" validate:"required,max=255"`
	Description         *string   `json:"description"`
	SessionType         string    `json:"session_type" validate:"omitempty,oneof=VIRTUAL HYBRID OFFLINE"`
	ScheduledDate       time.Time `json:"scheduled_date" validate:"required"`
	DurationMinutes     int       `json:"duration_minutes" validate:"omitempty,min=15,max=480"`
	ConferencePlatform  *string   `json:"conference_platform" validate:"omitempty,max=50"`
	ConferenceLink      *string   `json:"conference_link" validate:"omitempty,max=500"`
	ConferenceMeetingID *string   `json:"conference_meeting_id" validate:"omitempty,max=255"`
	ConferencePassword  *string   `json:"conference_password" validate:"omitempty,max=100"`
	MaxParticipants     *int      `json:"max_participants" validate:"omitempty,min=1"`
	IsRecorded          bool      `json:"is_recorded"`
}

type UpdateFGDSessionRequest struct {
	Topic               *string    `json:"topic" validate:"omitempty,max=255"`
	Description         *string    `json:"description"`
	SessionType         *string    `json:"session_type" validate:"omitempty,oneof=VIRTUAL HYBRID OFFLINE"`
	ScheduledDate       *time.Time `json:"scheduled_date"`
	DurationMinutes     *int       `json:"duration_minutes" validate:"omitempty,min=15,max=480"`
	ConferencePlatform  *string    `json:"conference_platform" validate:"omitempty,max=50"`
	ConferenceLink      *string    `json:"conference_link" validate:"omitempty,max=500"`
	ConferenceMeetingID *string    `json:"conference_meeting_id" validate:"omitempty,max=255"`
	ConferencePassword  *string    `json:"conference_password" validate:"omitempty,max=100"`
	NotesContent        *string    `json:"notes_content"`
	NotesFormat         *string    `json:"notes_format" validate:"omitempty,oneof=TEXT MARKDOWN HTML"`
	MaxParticipants     *int       `json:"max_participants" validate:"omitempty,min=1"`
	Status              *string    `json:"status" validate:"omitempty,oneof=SCHEDULED IN_PROGRESS COMPLETED CANCELLED"`
	RecordingURL        *string    `json:"recording_url"`
	IsRecorded          *bool      `json:"is_recorded"`
	SentimentSummary    *string    `json:"sentiment_summary"`
	SentimentScore      *float64   `json:"sentiment_score" validate:"omitempty,min=-1,max=1"`
}

type AddFGDParticipantRequest struct {
	FGDSessionID    string  `json:"fgd_session_id" validate:"required,uuid"`
	UserID          *string `json:"user_id" validate:"omitempty,uuid"`
	ParticipantName string  `json:"participant_name" validate:"required,max=255"`
	ParticipantRole string  `json:"participant_role" validate:"required,max=50"`
	Email           *string `json:"email" validate:"omitempty,email,max=255"`
	IsInvited       bool    `json:"is_invited"`
}

type UpdateFGDParticipantRequest struct {
	ParticipantName    *string    `json:"participant_name" validate:"omitempty,max=255"`
	ParticipantRole    *string    `json:"participant_role" validate:"omitempty,max=50"`
	Email              *string    `json:"email" validate:"omitempty,email,max=255"`
	IsInvited          *bool      `json:"is_invited"`
	IsAttended         *bool      `json:"is_attended"`
	JoinedAt           *time.Time `json:"joined_at"`
	LeftAt             *time.Time `json:"left_at"`
	ContributionRating *int       `json:"contribution_rating" validate:"omitempty,min=1,max=5"`
	Feedback           *string    `json:"feedback"`
}

// Student Needs Enhanced DTOs
type CreateStudentNeedsEnhancedRequest struct {
	SchoolID             string     `json:"school_id" validate:"required,uuid"`
	StudentContextExtID  *string    `json:"student_context_ext_id" validate:"omitempty,uuid"`
	ProfilDimensi        string     `json:"profil_dimensi" validate:"required,max=100"`
	SurveyResponseID     *string    `json:"survey_response_id" validate:"omitempty,uuid"`
	SurveyID             *string    `json:"survey_id" validate:"omitempty,uuid"`
	CurrentStatus        *string    `json:"current_status"`
	GapAnalysis          *string    `json:"gap_analysis"`
	PriorityLevel        int        `json:"priority_level" validate:"omitempty,min=1,max=5"`
	ActionPlan           *string    `json:"action_plan"`
	ActionPlanAssignedTo *string    `json:"action_plan_assigned_to" validate:"omitempty,uuid"`
	ActionPlanDueDate    *time.Time `json:"action_plan_due_date"`
	ProgressPercentage   int        `json:"progress_percentage" validate:"omitempty,min=0,max=100"`
	LastAssessmentDate   *time.Time `json:"last_assessment_date"`
	NextAssessmentDate   *time.Time `json:"next_assessment_date"`
	Notes                *string    `json:"notes"`
	Tags                 []string   `json:"tags" validate:"omitempty,dive,max=100"`
}

type UpdateStudentNeedsEnhancedRequest struct {
	StudentContextExtID  *string    `json:"student_context_ext_id" validate:"omitempty,uuid"`
	ProfilDimensi        *string    `json:"profil_dimensi" validate:"omitempty,max=100"`
	SurveyResponseID     *string    `json:"survey_response_id" validate:"omitempty,uuid"`
	SurveyID             *string    `json:"survey_id" validate:"omitempty,uuid"`
	CurrentStatus        *string    `json:"current_status"`
	GapAnalysis          *string    `json:"gap_analysis"`
	PriorityLevel        *int       `json:"priority_level" validate:"omitempty,min=1,max=5"`
	ActionPlan           *string    `json:"action_plan"`
	ActionPlanStatus     *string    `json:"action_plan_status" validate:"omitempty,oneof=NOT_STARTED IN_PROGRESS ON_HOLD COMPLETED CANCELLED"`
	ActionPlanAssignedTo *string    `json:"action_plan_assigned_to" validate:"omitempty,uuid"`
	ActionPlanDueDate    *time.Time `json:"action_plan_due_date"`
	ProgressPercentage   *int       `json:"progress_percentage" validate:"omitempty,min=0,max=100"`
	LastAssessmentDate   *time.Time `json:"last_assessment_date"`
	NextAssessmentDate   *time.Time `json:"next_assessment_date"`
	Notes                *string    `json:"notes"`
	Tags                 []string   `json:"tags" validate:"omitempty,dive,max=100"`
}

// SWOT Item DTOs
type CreateSWOTItemRequest struct {
	SchoolID     string  `json:"school_id" validate:"required,uuid"`
	Quadrant     string  `json:"quadrant" validate:"required,oneof=S W O T"`
	Statement    string  `json:"statement" validate:"required"`
	SourceDataID *string `json:"source_data_id" validate:"omitempty,uuid"`
	SourceType   *string `json:"source_type" validate:"omitempty,max=50"`
	Priority     int     `json:"priority" validate:"omitempty,min=1,max=5"`
}

type UpdateSWOTItemRequest struct {
	Quadrant     *string `json:"quadrant" validate:"omitempty,oneof=S W O T"`
	Statement    *string `json:"statement" validate:"omitempty"`
	SourceDataID *string `json:"source_data_id" validate:"omitempty,uuid"`
	SourceType   *string `json:"source_type" validate:"omitempty,max=50"`
	Priority     *int    `json:"priority" validate:"omitempty,min=1,max=5"`
}

type CreateSWOTAnalysisSessionRequest struct {
	SchoolID      string  `json:"school_id" validate:"required,uuid"`
	SessionName   string  `json:"session_name" validate:"required,max=255"`
	Description   *string `json:"description"`
	AnalysisScope *string `json:"analysis_scope"`
	Participants  *string `json:"participants"`
	IsTemplate    bool    `json:"is_template"`
	TemplateID    *string `json:"template_id" validate:"omitempty,uuid"`
}

type UpdateSWOTAnalysisSessionRequest struct {
	SessionName   *string `json:"session_name" validate:"omitempty,max=255"`
	Description   *string `json:"description"`
	AnalysisScope *string `json:"analysis_scope"`
	Participants  *string `json:"participants"`
	Status        *string `json:"status" validate:"omitempty,oneof=DRAFT IN_PROGRESS COMPLETED ARCHIVED"`
}

type AddSWOTSessionItemRequest struct {
	SessionID string `json:"session_id" validate:"required,uuid"`
	ItemID    string `json:"item_id" validate:"required,uuid"`
}

// Root Cause DTOs
type CreateRootCauseRequest struct {
	SchoolID          string     `json:"school_id" validate:"required,uuid"`
	RaporMetricID     *string    `json:"rapor_metric_id" validate:"omitempty,uuid"`
	IdentifiedProblem string     `json:"identified_problem" validate:"required"`
	Why1              *string    `json:"why_1"`
	Why2              *string    `json:"why_2"`
	Why3              *string    `json:"why_3"`
	Why4              *string    `json:"why_4"`
	Why5              *string    `json:"why_5"`
	RootCause         *string    `json:"root_cause"`
	KegiatanBenahi    *string    `json:"kegiatan_benahi"`
	AssignedTo        *string    `json:"assigned_to" validate:"omitempty,uuid"`
	DueDate           *time.Time `json:"due_date"`
}

type UpdateRootCauseRequest struct {
	RaporMetricID     *string    `json:"rapor_metric_id" validate:"omitempty,uuid"`
	IdentifiedProblem *string    `json:"identified_problem" validate:"omitempty"`
	Why1              *string    `json:"why_1"`
	Why2              *string    `json:"why_2"`
	Why3              *string    `json:"why_3"`
	Why4              *string    `json:"why_4"`
	Why5              *string    `json:"why_5"`
	RootCause         *string    `json:"root_cause"`
	KegiatanBenahi    *string    `json:"kegiatan_benahi"`
	Status            *string    `json:"status" validate:"omitempty,oneof=IDENTIFIED IN_PROGRESS RESOLVED CANCELLED"`
	AssignedTo        *string    `json:"assigned_to" validate:"omitempty,uuid"`
	DueDate           *time.Time `json:"due_date"`
}

type ValidateRootCauseRequest struct {
	ValidatorID string `json:"validator_id" validate:"required,uuid"`
	Notes       string `json:"notes" validate:"required"`
}

// Fishbone Diagram DTOs
type CreateFishboneDiagramRequest struct {
	SchoolID    string  `json:"school_id" validate:"required,uuid"`
	HeadEffect  string  `json:"head_effect" validate:"required"`
	Description *string `json:"description"`
}

type UpdateFishboneDiagramRequest struct {
	HeadEffect  *string `json:"head_effect" validate:"omitempty"`
	Description *string `json:"description"`
}

type CreateFishboneNodeRequest struct {
	DiagramID    string  `json:"diagram_id" validate:"required,uuid"`
	BoneCategory string  `json:"bone_category" validate:"required,oneof=Manusia Metode Material Fasilitas Lingkungan Uang"`
	ParentNodeID *string `json:"parent_node_id" validate:"omitempty,uuid"`
	CauseText    string  `json:"cause_text" validate:"required"`
	PositionX    *int    `json:"position_x"`
	PositionY    *int    `json:"position_y"`
	SequenceNo   int     `json:"sequence_no" validate:"omitempty,min=0"`
}

type UpdateFishboneNodeRequest struct {
	BoneCategory *string `json:"bone_category" validate:"omitempty,oneof=Manusia Metode Material Fasilitas Lingkungan Uang"`
	ParentNodeID *string `json:"parent_node_id" validate:"omitempty,uuid"`
	CauseText    *string `json:"cause_text" validate:"omitempty"`
	PositionX    *int    `json:"position_x"`
	PositionY    *int    `json:"position_y"`
	SequenceNo   *int    `json:"sequence_no" validate:"omitempty,min=0"`
}

type CreateFishboneConnectionRequest struct {
	DiagramID      string `json:"diagram_id" validate:"required,uuid"`
	FromNodeID     string `json:"from_node_id" validate:"required,uuid"`
	ToNodeID       string `json:"to_node_id" validate:"required,uuid"`
	ConnectionType string `json:"connection_type" validate:"required,oneof=CAUSAL CONTRIBUTION RELATIONSHIP"`
}

// KSP Analysis Integration DTOs
type CreateKSPAnalysisIntegrationRequest struct {
	DocumentID      string     `json:"document_id" validate:"required,uuid"`
	SchoolID        string     `json:"school_id" validate:"required,uuid"`
	IntegrationType string     `json:"integration_type" validate:"required,oneof=SWOT ROOT_CAUSE FISHBONE STUDENT_NEEDS SURVEY"`
	AnalysisData    string     `json:"analysis_data" validate:"required"`
	TemplateID      *string    `json:"template_id" validate:"omitempty,uuid"`
	IntegrationDate *time.Time `json:"integration_date"`
}

type UpdateKSPAnalysisIntegrationRequest struct {
	AnalysisData    *string `json:"analysis_data" validate:"omitempty"`
	IntegrationType *string `json:"integration_type" validate:"omitempty,oneof=SWOT ROOT_CAUSE FISHBONE STUDENT_NEEDS SURVEY"`
	Status          *string `json:"status" validate:"omitempty,oneof=PENDING APPROVED REJECTED REVISION_REQUIRED"`
	Notes           *string `json:"notes"`
}

type ApproveKSPAnalysisIntegrationRequest struct {
	ApproverID string `json:"approver_id" validate:"required,uuid"`
	Notes      string `json:"notes" validate:"required"`
}

type CreateKSPAnalysisRecommendationRequest struct {
	IntegrationID  string  `json:"integration_id" validate:"required,uuid"`
	Recommendation string  `json:"recommendation" validate:"required"`
	Priority       int     `json:"priority" validate:"omitempty,min=1,max=5"`
	Category       *string `json:"category" validate:"omitempty,max=100"`
}

type UpdateKSPAnalysisRecommendationRequest struct {
	Recommendation *string    `json:"recommendation" validate:"omitempty"`
	Priority       *int       `json:"priority" validate:"omitempty,min=1,max=5"`
	Category       *string    `json:"category" validate:"omitempty,max=100"`
	Status         *string    `json:"status" validate:"omitempty,oneof=PENDING IN_PROGRESS COMPLETED DEFERRED"`
	AssignedTo     *string    `json:"assigned_to" validate:"omitempty,uuid"`
	DueDate        *time.Time `json:"due_date"`
}

type CreateKSPAnalysisTemplateRequest struct {
	TemplateName        string  `json:"template_name" validate:"required,max=255"`
	TemplateCategory    string  `json:"template_category" validate:"required,max=100"`
	TemplateDescription *string `json:"template_description"`
	TemplateStructure   string  `json:"template_structure" validate:"required"`
	IsPublic            bool    `json:"is_public"`
	SchoolID            *string `json:"school_id" validate:"omitempty,uuid"`
}

type UpdateKSPAnalysisTemplateRequest struct {
	TemplateName        *string `json:"template_name" validate:"omitempty,max=255"`
	TemplateCategory    *string `json:"template_category" validate:"omitempty,max=100"`
	TemplateDescription *string `json:"template_description"`
	TemplateStructure   *string `json:"template_structure" validate:"omitempty"`
	IsPublic            *bool   `json:"is_public"`
	IsActive            *bool   `json:"is_active"`
}

// FASE 4: Integration DTOs

// Local Context Integration (FR 2.1)
type LocalContextAnalysisResponse struct {
	SchoolID        string                   `json:"school_id"`
	LocalContexts   []*LocalContextItem      `json:"local_contexts"`
	SWOTIntegration *LocalContextSWOTMapping `json:"swot_integration"`
	LastUpdated     time.Time                `json:"last_updated"`
}

type LocalContextItem struct {
	ID          string `json:"id"`
	Category    string `json:"category"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Location    string `json:"location"`
	ScopeType   string `json:"scope_type"`
	IsActive    bool   `json:"is_active"`
}

type LocalContextSWOTMapping struct {
	Strengths     []*LocalContextItem `json:"strengths"`
	Weaknesses    []*LocalContextItem `json:"weaknesses"`
	Opportunities []*LocalContextItem `json:"opportunities"`
	Threats       []*LocalContextItem `json:"threats"`
}

type LearningPotentialAnalysisResponse struct {
	SchoolID              string                   `json:"school_id"`
	OverallPotentialScore float64                  `json:"overall_potential_score"`
	CategoryScores        []*LearningCategoryScore `json:"category_scores"`
	Recommendations       []string                 `json:"recommendations"`
	AnalysisDate          time.Time                `json:"analysis_date"`
}

type LearningCategoryScore struct {
	Category    string  `json:"category"`
	Score       float64 `json:"score"`
	Potential   string  `json:"potential"` // HIGH, MEDIUM, LOW
	Utilization float64 `json:"utilization"`
	Gap         float64 `json:"gap"`
}

type EnhancedCategoryResponse struct {
	CategoryCode    string   `json:"category_code"`
	CategoryName    string   `json:"category_name"`
	Description     string   `json:"description"`
	StrategicTags   []string `json:"strategic_tags"`
	PriorityLevel   int      `json:"priority_level"`
	IntegrationType string   `json:"integration_type"`
}

// Student Context Analytics (FR 2.2)
type SurveyAnalyticsAggregatedResponse struct {
	SurveyID           string                 `json:"survey_id"`
	SchoolID           string                 `json:"school_id"`
	TotalResponses     int                    `json:"total_responses"`
	ResponseRate       float64                `json:"response_rate"`
	AggregatedAnswers  map[string]interface{} `json:"aggregated_answers"`
	StatisticalSummary *StatisticalSummary    `json:"statistical_summary"`
	TrendAnalysis      *TrendAnalysis         `json:"trend_analysis"`
	LastUpdated        time.Time              `json:"last_updated"`
}

type StatisticalSummary struct {
	Mean        map[string]float64            `json:"mean"`
	Median      map[string]float64            `json:"median"`
	Mode        map[string]string             `json:"mode"`
	StdDev      map[string]float64            `json:"std_dev"`
	Min         map[string]float64            `json:"min"`
	Max         map[string]float64            `json:"max"`
	Percentiles map[string]map[string]float64 `json:"percentiles"`
}

type TrendAnalysis struct {
	Period    string              `json:"period"`
	TrendData []TrendDataPoint    `json:"trend_data"`
	Insights  []string            `json:"insights"`
	Forecast  []ForecastDataPoint `json:"forecast"`
}

type TrendDataPoint struct {
	Date   string                 `json:"date"`
	Values map[string]interface{} `json:"values"`
}

type ForecastDataPoint struct {
	Date       string                 `json:"date"`
	Predicted  map[string]interface{} `json:"predicted"`
	Confidence map[string]float64     `json:"confidence"`
}

type StudentProfileAnalysisResponse struct {
	SchoolID            string                 `json:"school_id"`
	ProfileDimension    string                 `json:"profile_dimension"`
	TotalStudents       int                    `json:"total_students"`
	ProfileDistribution []*ProfileDistribution `json:"profile_distribution"`
	RiskFactors         []*RiskFactor          `json:"risk_factors"`
	Recommendations     []string               `json:"recommendations"`
	AnalysisDate        time.Time              `json:"analysis_date"`
}

type ProfileDistribution struct {
	ProfileLevel    string   `json:"profile_level"`
	Count           int      `json:"count"`
	Percentage      float64  `json:"percentage"`
	Characteristics []string `json:"characteristics"`
}

type RiskFactor struct {
	Factor        string  `json:"factor"`
	Severity      string  `json:"severity"` // HIGH, MEDIUM, LOW
	AffectedCount int     `json:"affected_count"`
	Percentage    float64 `json:"percentage"`
	Mitigation    string  `json:"mitigation"`
}

type StatisticalAnalysisResponse struct {
	SchoolID     string                 `json:"school_id"`
	AnalysisType string                 `json:"analysis_type"`
	Results      map[string]interface{} `json:"results"`
	Metadata     *AnalysisMetadata      `json:"metadata"`
	GeneratedAt  time.Time              `json:"generated_at"`
}

type AnalysisMetadata struct {
	DataPeriod      string    `json:"data_period"`
	Source          string    `json:"source"`
	ConfidenceLevel float64   `json:"confidence_level"`
	SampleSize      int       `json:"sample_size"`
	LastUpdated     time.Time `json:"last_updated"`
}

type ActionPlanRecommendationResponse struct {
	ID               string    `json:"id"`
	SchoolID         string    `json:"school_id"`
	ProfileDimension string    `json:"profile_dimension"`
	Priority         int       `json:"priority"`
	Action           string    `json:"action"`
	ExpectedOutcome  string    `json:"expected_outcome"`
	Timeline         string    `json:"timeline"`
	Resources        []string  `json:"resources"`
	Responsible      string    `json:"responsible"`
	SuccessCriteria  string    `json:"success_criteria"`
	CreatedAt        time.Time `json:"created_at"`
}

// School Data Integration (FR 2.3)
type SchoolDataAnalysisResponse struct {
	SchoolID           string                  `json:"school_id"`
	SchoolName         string                  `json:"school_name"`
	InfrastructureData *InfrastructureAnalysis `json:"infrastructure_data"`
	HumanResourcesData *HRAnalysis             `json:"human_resources_data"`
	AcademicData       *AcademicAnalysis       `json:"academic_data"`
	SWOTMapping        *SchoolSWOTMapping      `json:"swot_mapping"`
	AnalysisDate       time.Time               `json:"analysis_date"`
}

type InfrastructureAnalysis struct {
	ClassroomCondition   *ConditionAnalysis `json:"classroom_condition"`
	FacilityAvailability *FacilityAnalysis  `json:"facility_availability"`
	MaintenanceNeeds     []*MaintenanceNeed `json:"maintenance_needs"`
	DigitalReadiness     float64            `json:"digital_readiness"`
}

type ConditionAnalysis struct {
	Total    int     `json:"total"`
	Good     int     `json:"good"`
	Damaged  int     `json:"damaged"`
	GoodRate float64 `json:"good_rate"`
	Priority string  `json:"priority"`
}

type FacilityAnalysis struct {
	Library          *FacilityStatus `json:"library"`
	Toilets          *FacilityStatus `json:"toilets"`
	Labs             *FacilityStatus `json:"labs"`
	SportsFacilities *FacilityStatus `json:"sports_facilities"`
	Administrative   *FacilityStatus `json:"administrative"`
}

type FacilityStatus struct {
	Available   bool    `json:"available"`
	Count       int     `json:"count"`
	Condition   string  `json:"condition"`
	Utilization float64 `json:"utilization"`
	Adequacy    string  `json:"adequacy"`
}

type MaintenanceNeed struct {
	Item          string  `json:"item"`
	CurrentState  string  `json:"current_state"`
	RequiredState string  `json:"required_state"`
	Priority      int     `json:"priority"`
	EstimatedCost float64 `json:"estimated_cost"`
	Timeline      string  `json:"timeline"`
	Impact        string  `json:"impact"`
}

type HRAnalysis struct {
	TeacherData     *TeacherAnalysis         `json:"teacher_data"`
	StaffData       *StaffAnalysis           `json:"staff_data"`
	ProfessionalDev *ProfessionalDevAnalysis `json:"professional_development"`
	Workload        *WorkloadAnalysis        `json:"workload"`
}

type TeacherAnalysis struct {
	Total         int     `json:"total"`
	PNS           int     `json:"pns"`
	Honor         int     `json:"honor"`
	CertifiedRate float64 `json:"certified_rate"`
	QualifiedRate float64 `json:"qualified_rate"`
	StudentRatio  float64 `json:"student_ratio"`
	Adequacy      string  `json:"adequacy"`
}

type StaffAnalysis struct {
	Total        int    `json:"total"`
	AdminCount   int    `json:"admin_count"`
	SupportCount int    `json:"support_count"`
	Adequacy     string `json:"adequacy"`
}

type ProfessionalDevAnalysis struct {
	TrainingParticipation float64  `json:"training_participation"`
	CertificationRate     float64  `json:"certification_rate"`
	SkillGaps             []string `json:"skill_gaps"`
	Recommendations       []string `json:"recommendations"`
}

type WorkloadAnalysis struct {
	AverageHoursPerWeek  float64            `json:"average_hours_per_week"`
	WorkloadDistribution map[string]float64 `json:"workload_distribution"`
	BurnoutRisk          string             `json:"burnout_risk"`
}

type AcademicAnalysis struct {
	StudentPerformance  *PerformanceAnalysis `json:"student_performance"`
	GraduationRate      float64              `json:"graduation_rate"`
	DropoutRate         float64              `json:"dropout_rate"`
	TransitionRate      float64              `json:"transition_rate"`
	CurriculumAlignment *CurriculumAnalysis  `json:"curriculum_alignment"`
}

type PerformanceAnalysis struct {
	AverageScore     float64            `json:"average_score"`
	SubjectBreakdown map[string]float64 `json:"subject_breakdown"`
	Trend            string             `json:"trend"`
	ImprovementAreas []string           `json:"improvement_areas"`
}

type CurriculumAnalysis struct {
	AlignmentScore  float64  `json:"alignment_score"`
	GapAreas        []string `json:"gap_areas"`
	StrengthAreas   []string `json:"strength_areas"`
	Recommendations []string `json:"recommendations"`
}

type SchoolSWOTMapping struct {
	Strengths     []*SchoolSWOTItem `json:"strengths"`
	Weaknesses    []*SchoolSWOTItem `json:"weaknesses"`
	Opportunities []*SchoolSWOTItem `json:"opportunities"`
	Threats       []*SchoolSWOTItem `json:"threats"`
}

type SchoolSWOTItem struct {
	Category    string `json:"category"`
	Description string `json:"description"`
	Impact      string `json:"impact"`
	Priority    int    `json:"priority"`
	DataSource  string `json:"data_source"`
}

type DigitalReadinessResponse struct {
	SchoolID              string           `json:"school_id"`
	OverallReadinessScore float64          `json:"overall_readiness_score"`
	ReadinessLevel        string           `json:"readiness_level"` // EMERGING, DEVELOPING, PROFICIENT, ADVANCED
	AssessmentAreas       []*ReadinessArea `json:"assessment_areas"`
	CodingReadiness       *CodingReadiness `json:"coding_readiness"`
	AIReadiness           *AIReadiness     `json:"ai_readiness"`
	Recommendations       []string         `json:"recommendations"`
	AssessmentDate        time.Time        `json:"assessment_date"`
}

type ReadinessArea struct {
	Area            string   `json:"area"`
	Score           float64  `json:"score"`
	Level           string   `json:"level"`
	Gaps            []string `json:"gaps"`
	Strengths       []string `json:"strengths"`
	Recommendations []string `json:"recommendations"`
}

type CodingReadiness struct {
	Score                 float64  `json:"score"`
	Level                 string   `json:"level"`
	TeacherCapacity       float64  `json:"teacher_capacity"`
	Infrastructure        float64  `json:"infrastructure"`
	CurriculumIntegration float64  `json:"curriculum_integration"`
	Recommendations       []string `json:"recommendations"`
}

type AIReadiness struct {
	Score             float64  `json:"score"`
	Level             string   `json:"level"`
	TeacherAwareness  float64  `json:"teacher_awareness"`
	Infrastructure    float64  `json:"infrastructure"`
	EthicalGuidelines float64  `json:"ethical_guidelines"`
	Recommendations   []string `json:"recommendations"`
}

type SarprasPriorityResponse struct {
	ItemName          string   `json:"item_name"`
	CurrentCondition  string   `json:"current_condition"`
	RequiredCondition string   `json:"required_condition"`
	PriorityScore     float64  `json:"priority_score"`
	PriorityLevel     string   `json:"priority_level"` // CRITICAL, HIGH, MEDIUM, LOW
	EstimatedCost     float64  `json:"estimated_cost"`
	Timeline          string   `json:"timeline"`
	Impact            string   `json:"impact"`
	Urgency           string   `json:"urgency"`
	Dependencies      []string `json:"dependencies"`
	Recommendation    string   `json:"recommendation"`
}

// FASE 5: Analysis Tool Enhancements

// SWOT Builder Enhancements (FR 3.1)

type SWOTAnalyticsResponse struct {
	SessionID  string `json:"session_id"`
	TotalItems struct {
		Strengths     int `json:"strengths"`
		Weaknesses    int `json:"weaknesses"`
		Opportunities int `json:"opportunities"`
		Threats       int `json:"threats"`
	} `json:"total_items"`
	DataMappingCount struct {
		Strengths     int `json:"strengths"`
		Weaknesses    int `json:"weaknesses"`
		Opportunities int `json:"opportunities"`
		Threats       int `json:"threats"`
	} `json:"data_mapping_count"`
	CategoryBreakdown []struct {
		Category string `json:"category"`
		Count    int    `json:"count"`
	} `json:"category_breakdown"`
	DataSourceBreakdown []struct {
		SourceType string `json:"source_type"`
		Count      int    `json:"count"`
	} `json:"data_source_breakdown"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type SWOTDataMappingRequest struct {
	ItemID      string  `json:"item_id" binding:"required"`
	SourceType  string  `json:"source_type" binding:"required"` // RAPOR, SURVEY, SARPRAS, SCHOOL_DATA
	SourceID    string  `json:"source_id" binding:"required"`
	SourceField string  `json:"source_field" binding:"required"`
	Confidence  float64 `json:"confidence"` // 0-1
	Notes       string  `json:"notes"`
}

type DataSourceTypeResponse struct {
	SourceType string `json:"source_type"`
	SourceName string `json:"source_name"`
	Available  bool   `json:"available"`
	Count      int    `json:"count"`
}

// Root Cause Analyzer Enhancements (FR 3.2)

type FiveWhysRequest struct {
	RootCauseID string `json:"root_cause_id" binding:"required"`
	Problem     string `json:"problem" binding:"required"`
	MaxDepth    int    `json:"max_depth"` // Default 5
	Context     string `json:"context"`
}

type FiveWhysResponse struct {
	RootCauseID  string         `json:"root_cause_id"`
	Problem      string         `json:"problem"`
	AnalysisTree []FiveWhysNode `json:"analysis_tree"`
	Conclusion   string         `json:"conclusion"`
	Confidence   float64        `json:"confidence"`
	CreatedAt    time.Time      `json:"created_at"`
}

type FiveWhysNode struct {
	Level    int            `json:"level"`
	Question string         `json:"question"`
	Answer   string         `json:"answer"`
	Evidence []string       `json:"evidence"`
	Children []FiveWhysNode `json:"children"`
}

type RaporMetricLinkRequest struct {
	RootCauseID string  `json:"root_cause_id" binding:"required"`
	MetricID    string  `json:"metric_id" binding:"required"`
	LinkType    string  `json:"link_type"` // CAUSE, EFFECT, CORRELATION
	Confidence  float64 `json:"confidence"`
	Notes       string  `json:"notes"`
}

type RootCauseSuggestionResponse struct {
	SuggestionID string   `json:"suggestion_id"`
	RootCauseID  string   `json:"root_cause_id"`
	Title        string   `json:"title"`
	Description  string   `json:"description"`
	Evidence     []string `json:"evidence"`
	Priority     string   `json:"priority"`
	Source       string   `json:"source"`
	Relevance    float64  `json:"relevance"`
}

// Fishbone Diagram Enhancements (FR 3.3)

type FishboneAnalyticsResponse struct {
	DiagramID     string `json:"diagram_id"`
	TotalNodes    int    `json:"total_nodes"`
	TotalEdges    int    `json:"total_edges"`
	CategoryStats []struct {
		Category  string `json:"category"`
		NodeCount int    `json:"node_count"`
	} `json:"category_stats"`
	DepthAnalysis []struct {
		Depth int `json:"depth"`
		Count int `json:"count"`
	} `json:"depth_analysis"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type FishboneValidationResponse struct {
	DiagramID   string   `json:"diagram_id"`
	IsValid     bool     `json:"is_valid"`
	Issues      []string `json:"issues"`
	Warnings    []string `json:"warnings"`
	Suggestions []string `json:"suggestions"`
}

type FishboneCategoryResponse struct {
	CategoryID   string `json:"category_id"`
	CategoryName string `json:"category_name"`
	Description  string `json:"description"`
	Icon         string `json:"icon"`
	Color        string `json:"color"`
	IsPreset     bool   `json:"is_preset"`
}

// Fishbone Template DTOs

type CreateFishboneTemplateRequest struct {
	TemplateName        string               `json:"template_name" binding:"required"`
	TemplateCategory    string               `json:"template_category"`
	TemplateDescription string               `json:"template_description"`
	HeadEffect          string               `json:"head_effect" binding:"required"`
	PresetNodes         []PresetFishboneNode `json:"preset_nodes"`
	IsPublic            bool                 `json:"is_public"`
}

type PresetFishboneNode struct {
	CauseText    string  `json:"cause_text" binding:"required"`
	BoneCategory string  `json:"bone_category" binding:"required"`
	PositionX    float64 `json:"position_x"`
	PositionY    float64 `json:"position_y"`
	SequenceNo   int     `json:"sequence_no"`
}

type UpdateFishboneTemplateRequest struct {
	TemplateName        *string               `json:"template_name"`
	TemplateCategory    *string               `json:"template_category"`
	TemplateDescription *string               `json:"template_description"`
	HeadEffect          *string               `json:"head_effect"`
	PresetNodes         *[]PresetFishboneNode `json:"preset_nodes"`
	IsPublic            *bool                 `json:"is_public"`
	IsActive            *bool                 `json:"is_active"`
}

type FishboneTemplateResponse struct {
	ID                  string               `json:"id"`
	TemplateName        string               `json:"template_name"`
	TemplateCategory    string               `json:"template_category"`
	TemplateDescription string               `json:"template_description"`
	HeadEffect          string               `json:"head_effect"`
	PresetNodes         []PresetFishboneNode `json:"preset_nodes"`
	IsPublic            bool                 `json:"is_public"`
	IsActive            bool                 `json:"is_active"`
	UsageCount          int                  `json:"usage_count"`
	CreatedBy           string               `json:"created_by"`
	CreatedAt           time.Time            `json:"created_at"`
	UpdatedAt           time.Time            `json:"updated_at"`
}

type FishboneTemplate struct {
	ID                  uuid.UUID
	TemplateName        string
	TemplateCategory    string
	TemplateDescription string
	HeadEffect          string
	PresetNodes         []PresetFishboneNode
	IsPublic            bool
	IsActive            bool
	UsageCount          int
	CreatedBy           uuid.UUID
	CreatedAt           time.Time
	UpdatedAt           time.Time
}

// FASE 6: KSP Enhanced Generation DTOs

type KSPAnalysisIntegrationRequest struct {
	CurriculumDocumentID   string                 `json:"curriculum_document_id" binding:"required"`
	SchoolID               string                 `json:"school_id" binding:"required"`
	IntegrationType        string                 `json:"integration_type" binding:"required"` // SWOT, ROOT_CAUSE, FISHBONE, STUDENT_NEEDS, COMPREHENSIVE
	AnalysisData           map[string]interface{} `json:"analysis_data"`
	SelectedDataPoints     []DataPointSelection   `json:"selected_data_points"`
	CustomSections         []CustomSection        `json:"custom_sections"`
	IncludeCharts          bool                   `json:"include_charts"`
	IncludeRecommendations bool                   `json:"include_recommendations"`
}

type DataPointSelection struct {
	DataType string `json:"data_type" binding:"required"` // SWOT, ROOT_CAUSE, FISHBONE, STUDENT_NEEDS
	DataID   string `json:"data_id" binding:"required"`
	Section  string `json:"section"` // ANALISIS, PEMECAHAN MASALAH, RENCANA TINDAKAN
	Priority int    `json:"priority"`
	Notes    string `json:"notes"`
}

type CustomSection struct {
	SectionTitle string `json:"section_title" binding:"required"`
	SectionOrder int    `json:"section_order"`
	Content      string `json:"content"`
	IncludeInTOC bool   `json:"include_in_toc"`
}

type DocumentCompilationRequest struct {
	IntegrationID   string                 `json:"integration_id" binding:"required"`
	Format          string                 `json:"format" binding:"required"` // PDF, DOCX
	IncludeTOC      bool                   `json:"include_toc"`
	IncludeCharts   bool                   `json:"include_charts"`
	IncludeAppendix bool                   `json:"include_appendix"`
	CustomStyling   map[string]interface{} `json:"custom_styling"`
}

type DocumentCompilationResponse struct {
	DocumentID        string `json:"document_id"`
	DocumentURL       string `json:"document_url"`
	Format            string `json:"format"`
	PageCount         int    `json:"page_count"`
	FileSize          int64  `json:"file_size"`
	CompilationStatus string `json:"compilation_status"`
	GeneratedAt       string `json:"generated_at"`
	ExpiresAt         string `json:"expires_at"`
}

type AnalysisDataSnapshot struct {
	IntegrationID    string                  `json:"integration_id"`
	SWOTData         *map[string]interface{} `json:"swot_data"`
	RootCauseData    *map[string]interface{} `json:"root_cause_data"`
	FishboneData     *map[string]interface{} `json:"fishbone_data"`
	StudentNeedsData *map[string]interface{} `json:"student_needs_data"`
	SurveyData       *map[string]interface{} `json:"survey_data"`
	RaporData        *map[string]interface{} `json:"rapor_data"`
	CapturedAt       string                  `json:"captured_at"`
}

// Chart Generation DTOs (FR 4.1.3)

type ChartConfig struct {
	ChartType  string                 `json:"chart_type" binding:"required"` // BAR, PIE, LINE, SCATTER, RADAR
	Title      string                 `json:"title"`
	Data       map[string]interface{} `json:"data" binding:"required"`
	Width      int                    `json:"width"`
	Height     int                    `json:"height"`
	Colors     []string               `json:"colors"`
	Labels     []string               `json:"labels"`
	ShowLegend bool                   `json:"show_legend"`
	ChartStyle map[string]interface{} `json:"chart_style"`
}

type ChartGenerationRequest struct {
	IntegrationID string        `json:"integration_id" binding:"required"`
	ChartConfigs  []ChartConfig `json:"chart_configs" binding:"required"`
	Format        string        `json:"format"` // PNG, SVG, PDF
}

type ChartGenerationResponse struct {
	ChartID     string `json:"chart_id"`
	ChartURL    string `json:"chart_url"`
	ChartType   string `json:"chart_type"`
	GeneratedAt string `json:"generated_at"`
}

type SWOTChartData struct {
	Strengths         int `json:"strengths"`
	Weaknesses        int `json:"weaknesses"`
	Opportunities     int `json:"opportunities"`
	Threats           int `json:"threats"`
	CategoryBreakdown []struct {
		Category string `json:"category"`
		Count    int    `json:"count"`
	} `json:"category_breakdown"`
}

type RootCauseChartData struct {
	TotalRootCauses    int            `json:"total_root_causes"`
	Resolved           int            `json:"resolved"`
	InProgress         int            `json:"in_progress"`
	Pending            int            `json:"pending"`
	StatusDistribution map[string]int `json:"status_distribution"`
}

type FishboneChartData struct {
	TotalDiagrams        int            `json:"total_diagrams"`
	TotalNodes           int            `json:"total_nodes"`
	CategoryDistribution map[string]int `json:"category_distribution"`
	DepthAnalysis        []struct {
		Depth int `json:"depth"`
		Count int `json:"count"`
	} `json:"depth_analysis"`
}

type StudentNeedsChartData struct {
	TotalProfiles       int            `json:"total_profiles"`
	CriticalNeeds       int            `json:"critical_needs"`
	PriorityAreas       []string       `json:"priority_areas"`
	ProfileDistribution map[string]int `json:"profile_distribution"`
}

// AI Platform Integration DTOs (FR 4.1.4)

type AIContentGenerationRequest struct {
	IntegrationID string                 `json:"integration_id" binding:"required"`
	ContentType   string                 `json:"content_type" binding:"required"` // EXECUTIVE_SUMMARY, ANALYSIS_SECTION, RECOMMENDATION, ACTION_PLAN
	Context       map[string]interface{} `json:"context"`
	Tone          string                 `json:"tone"` // FORMAL, SEMI_FORMAL, CASUAL
	Language      string                 `json:"language"`
	MaxLength     int                    `json:"max_length"`
}

type AIContentGenerationResponse struct {
	GeneratedContent string  `json:"generated_content"`
	ContentID        string  `json:"content_id"`
	Confidence       float64 `json:"confidence"`
	WordCount        int     `json:"word_count"`
	TokensUsed       int     `json:"tokens_used"`
	GeneratedAt      string  `json:"generated_at"`
}

type AIRecommendationRequest struct {
	AnalysisData       map[string]interface{} `json:"analysis_data" binding:"required"`
	RecommendationType string                 `json:"recommendation_type" binding:"required"` // SWOT_ACTION, ROOT_CAUSE_SOLUTION, GENERAL
	TargetAudience     string                 `json:"target_audience"`
	Priority           string                 `json:"priority"`
	Context            string                 `json:"context"`
}

type AIRecommendationResponse struct {
	Recommendations []string `json:"recommendations"`
	Confidence      float64  `json:"confidence"`
	Sources         []string `json:"sources"`
	GeneratedAt     string   `json:"generated_at"`
}

type AIIntegrationConfig struct {
	APIEndpoint  string  `json:"api_endpoint"`
	APIKey       string  `json:"api_key"`
	ModelVersion string  `json:"model_version"`
	MaxTokens    int     `json:"max_tokens"`
	Temperature  float64 `json:"temperature"`
	Timeout      int     `json:"timeout"`
	Enabled      bool    `json:"enabled"`
}

// Version History DTOs (FR 4.1.5)

type AnalysisVersionHistory struct {
	ID            string                 `json:"id"`
	AnalysisType  string                 `json:"analysis_type"` // SWOT, ROOT_CAUSE, FISHBONE, STUDENT_NEEDS
	AnalysisID    string                 `json:"analysis_id"`
	Version       int                    `json:"version"`
	Changes       map[string]interface{} `json:"changes"`
	ChangeType    string                 `json:"change_type"` // CREATE, UPDATE, DELETE
	ChangeSummary string                 `json:"change_summary"`
	ChangedBy     string                 `json:"changed_by"`
	ChangedAt     string                 `json:"changed_at"`
	PreviousData  map[string]interface{} `json:"previous_data,omitempty"`
	NewData       map[string]interface{} `json:"new_data,omitempty"`
}

type AnalysisVersionHistoryRequest struct {
	AnalysisType  string                 `json:"analysis_type" binding:"required"`
	AnalysisID    string                 `json:"analysis_id" binding:"required"`
	Changes       map[string]interface{} `json:"changes"`
	ChangeType    string                 `json:"change_type" binding:"required"`
	ChangeSummary string                 `json:"change_summary" binding:"required"`
	PreviousData  map[string]interface{} `json:"previous_data,omitempty"`
	NewData       map[string]interface{} `json:"new_data,omitempty"`
}

type VersionHistoryResponse struct {
	ID            string                 `json:"id"`
	AnalysisType  string                 `json:"analysis_type"`
	AnalysisID    string                 `json:"analysis_id"`
	Version       int                    `json:"version"`
	Changes       map[string]interface{} `json:"changes"`
	ChangeType    string                 `json:"change_type"`
	ChangeSummary string                 `json:"change_summary"`
	ChangedBy     string                 `json:"changed_by"`
	ChangedAt     string                 `json:"changed_at"`
	PreviousData  map[string]interface{} `json:"previous_data,omitempty"`
	NewData       map[string]interface{} `json:"new_data,omitempty"`
}

type AnalysisVersionComparison struct {
	Version1    AnalysisVersionHistory `json:"version_1"`
	Version2    AnalysisVersionHistory `json:"version_2"`
	Differences []string               `json:"differences"`
	Summary     string                 `json:"summary"`
}

type VersionRestoreRequest struct {
	AnalysisID string `json:"analysis_id" binding:"required"`
	Version    int    `json:"version" binding:"required"`
	Reason     string `json:"reason" binding:"required"`
}

// Extended Review and Approval Workflow DTOs (FR 4.1.13)

type ApprovalWorkflowStep struct {
	ID           string `json:"id"`
	StepName     string `json:"step_name"`
	Order        int    `json:"order"`
	Required     bool   `json:"required"`
	ApproverRole string `json:"approver_role"`
	Description  string `json:"description"`
}

type ApprovalWorkflow struct {
	ID           string                 `json:"id"`
	WorkflowName string                 `json:"workflow_name"`
	WorkflowType string                 `json:"workflow_type"` // KSP_GENERATION, ANALYSIS_REVIEW, DOCUMENT_APPROVAL
	Steps        []ApprovalWorkflowStep `json:"steps"`
	IsActive     bool                   `json:"is_active"`
	SchoolID     string                 `json:"school_id,omitempty"`
	CreatedBy    string                 `json:"created_by"`
	CreatedAt    string                 `json:"created_at"`
	UpdatedAt    string                 `json:"updated_at"`
}

type ApprovalWorkflowRequest struct {
	WorkflowName string                 `json:"workflow_name" binding:"required"`
	WorkflowType string                 `json:"workflow_type" binding:"required"`
	Steps        []ApprovalWorkflowStep `json:"steps" binding:"required"`
	SchoolID     string                 `json:"school_id,omitempty"`
}

type ApprovalRequest struct {
	DocumentID       string `json:"document_id" binding:"required"`
	WorkflowID       string `json:"workflow_id" binding:"required"`
	StepID           string `json:"step_id" binding:"required"`
	Action           string `json:"action" binding:"required"` // APPROVE, REJECT, REQUEST_CHANGES
	Comments         string `json:"comments"`
	RequestedChanges string `json:"requested_changes,omitempty"`
}

type ApprovalResponse struct {
	ID               string `json:"id"`
	DocumentID       string `json:"document_id"`
	WorkflowID       string `json:"workflow_id"`
	StepID           string `json:"step_id"`
	Action           string `json:"action"`
	ApproverID       string `json:"approver_id"`
	Comments         string `json:"comments"`
	RequestedChanges string `json:"requested_changes,omitempty"`
	ApprovedAt       string `json:"approved_at"`
}

type DocumentApprovalStatus struct {
	DocumentID      string             `json:"document_id"`
	CurrentStep     string             `json:"current_step"`
	CurrentStepName string             `json:"current_step_name"`
	OverallStatus   string             `json:"overall_status"` // PENDING, IN_PROGRESS, APPROVED, REJECTED
	CompletedSteps  []string           `json:"completed_steps"`
	PendingSteps    []string           `json:"pending_steps"`
	ApprovalHistory []ApprovalResponse `json:"approval_history"`
	StartedAt       string             `json:"started_at"`
	CompletedAt     string             `json:"completed_at,omitempty"`
}

type WorkflowStepAssignment struct {
	ID          string `json:"id"`
	WorkflowID  string `json:"workflow_id"`
	StepID      string `json:"step_id"`
	DocumentID  string `json:"document_id"`
	AssignedTo  string `json:"assigned_to"`
	AssignedBy  string `json:"assigned_by"`
	AssignedAt  string `json:"assigned_at"`
	Status      string `json:"status"` // PENDING, COMPLETED, SKIPPED
	CompletedAt string `json:"completed_at,omitempty"`
}

type ApprovalNotification struct {
	ID          string `json:"id"`
	RecipientID string `json:"recipient_id"`
	DocumentID  string `json:"document_id"`
	WorkflowID  string `json:"workflow_id"`
	StepID      string `json:"step_id"`
	Message     string `json:"message"`
	Type        string `json:"type"` // APPROVAL_REQUIRED, APPROVED, REJECTED, CHANGES_REQUESTED
	SentAt      string `json:"sent_at"`
	ReadAt      string `json:"read_at,omitempty"`
}
