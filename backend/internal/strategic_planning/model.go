package strategic_planning

import (
	"sim-sekolah/internal/common"
	"time"

	"github.com/google/uuid"
)

// RaporPendidikan represents data from Rapor Pendidikan Kemdikbud API
type RaporPendidikan struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID         uuid.UUID `gorm:"type:uuid;not null;index" json:"school_id"`
	Year             string    `gorm:"type:varchar(10);not null" json:"year"`
	Semester         string    `gorm:"type:varchar(10);not null" json:"semester"`
	LiteracyScore    *float64  `gorm:"type:decimal(5,2)" json:"literacy_score"`
	NumeracyScore    *float64  `gorm:"type:decimal(5,2)" json:"numeracy_score"`
	CharacterScore   *float64  `gorm:"type:decimal(5,2)" json:"character_score"`
	RawData          *string   `gorm:"type:jsonb" json:"raw_data"`
	SyncAt           time.Time `gorm:"default:CURRENT_TIMESTAMP" json:"sync_at"`
	SyncStatus       string    `gorm:"type:varchar(50);default:'SUCCESS'" json:"sync_status"`
	SyncErrorMessage *string   `gorm:"type:text" json:"sync_error_message"`

	common.Auditable
}

func (RaporPendidikan) TableName() string {
	return "rapor_pendidikan"
}

// Survey represents digital questionnaires for data collection
type Survey struct {
	ID               uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID         uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	TargetAudience   string     `gorm:"type:varchar(50);not null" json:"target_audience"`
	Title            string     `gorm:"type:varchar(255);not null" json:"title"`
	Description      *string    `gorm:"type:text" json:"description"`
	FormSchema       string     `gorm:"type:jsonb;not null" json:"form_schema"`
	Status           string     `gorm:"type:varchar(50);default:'DRAFT'" json:"status"`
	IsAnonymous      bool       `gorm:"default:false" json:"is_anonymous"`
	AllowMultiple    bool       `gorm:"default:false" json:"allow_multiple_responses"`
	MaxResponses     *int       `json:"max_responses"`
	IsTemplate       bool       `gorm:"default:false" json:"is_template"`
	TemplateCategory *string    `gorm:"type:varchar(100)" json:"template_category"`
	StartDate        *time.Time `json:"start_date"`
	EndDate          *time.Time `json:"end_date"`

	common.Auditable
}

func (Survey) TableName() string {
	return "surveys"
}

// SurveyResponse represents responses to surveys
type SurveyResponse struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SurveyID       uuid.UUID  `gorm:"type:uuid;not null;index" json:"survey_id"`
	RespondentID   *uuid.UUID `gorm:"type:uuid" json:"respondent_id"`
	RespondentName *string    `gorm:"type:varchar(255)" json:"respondent_name"`
	RespondentType *string    `gorm:"type:varchar(50)" json:"respondent_type"`
	AnswersJSON    string     `gorm:"type:jsonb;not null" json:"answers_json"`
	SubmittedAt    time.Time  `gorm:"default:CURRENT_TIMESTAMP" json:"submitted_at"`
	IPAddress      *string    `gorm:"type:varchar(50)" json:"ip_address"`
	UserAgent      *string    `gorm:"type:text" json:"user_agent"`

	common.Auditable
}

func (SurveyResponse) TableName() string {
	return "survey_responses"
}

// FGDSession represents Focus Group Discussion sessions
type FGDSession struct {
	ID                  uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID            uuid.UUID `gorm:"type:uuid;not null;index" json:"school_id"`
	Topic               string    `gorm:"type:varchar(255);not null" json:"topic"`
	Description         *string   `gorm:"type:text" json:"description"`
	SessionType         string    `gorm:"type:varchar(50);default:'VIRTUAL'" json:"session_type"`
	ScheduledDate       time.Time `gorm:"type:timestamp;not null" json:"scheduled_date"`
	DurationMinutes     int       `gorm:"default:60" json:"duration_minutes"`
	ConferencePlatform  *string   `gorm:"type:varchar(50)" json:"conference_platform"`
	ConferenceLink      *string   `gorm:"type:varchar(500)" json:"conference_link"`
	ConferenceMeetingID *string   `gorm:"type:varchar(255)" json:"conference_meeting_id"`
	ConferencePassword  *string   `gorm:"type:varchar(100)" json:"conference_password"`
	NotesContent        *string   `gorm:"type:text" json:"notes_content"`
	NotesFormat         string    `gorm:"type:varchar(20);default:'TEXT'" json:"notes_format"`
	Participants        *string   `gorm:"type:jsonb" json:"participants"`
	MaxParticipants     *int      `json:"max_participants"`
	Status              string    `gorm:"type:varchar(50);default:'SCHEDULED'" json:"status"`
	RecordingURL        *string   `gorm:"type:text" json:"recording_url"`
	IsRecorded          bool      `gorm:"default:false" json:"is_recorded"`
	SentimentSummary    *string   `gorm:"type:text" json:"sentiment_summary"`
	SentimentScore      *float64  `gorm:"type:decimal(3,2)" json:"sentiment_score"`

	common.Auditable
}

func (FGDSession) TableName() string {
	return "fgd_sessions"
}

// FGDParticipant represents participants in FGD sessions
type FGDParticipant struct {
	ID                 uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	FGDSessionID       uuid.UUID  `gorm:"type:uuid;not null;index" json:"fgd_session_id"`
	UserID             *uuid.UUID `gorm:"type:uuid" json:"user_id"`
	ParticipantName    string     `gorm:"type:varchar(255);not null" json:"participant_name"`
	ParticipantRole    string     `gorm:"type:varchar(50)" json:"participant_role"`
	Email              *string    `gorm:"type:varchar(255)" json:"email"`
	IsInvited          bool       `gorm:"default:false" json:"is_invited"`
	IsAttended         bool       `gorm:"default:false" json:"is_attended"`
	JoinedAt           *time.Time `json:"joined_at"`
	LeftAt             *time.Time `json:"left_at"`
	ContributionRating *int       `json:"contribution_rating"`
	Feedback           *string    `gorm:"type:text" json:"feedback"`

	common.Auditable
}

func (FGDParticipant) TableName() string {
	return "fgd_participants"
}

// StudentNeedsEnhanced represents enhanced student profiling
type StudentNeedsEnhanced struct {
	ID                   uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID             uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	StudentContextExtID  *uuid.UUID `gorm:"type:uuid" json:"student_context_ext_id"`
	ProfilDimensi        string     `gorm:"type:varchar(100);not null" json:"profil_dimensi"`
	SurveyResponseID     *uuid.UUID `gorm:"type:uuid" json:"survey_response_id"`
	SurveyID             *uuid.UUID `gorm:"type:uuid" json:"survey_id"`
	CurrentStatus        *string    `gorm:"type:text" json:"current_status"`
	GapAnalysis          *string    `gorm:"type:text" json:"gap_analysis"`
	PriorityLevel        int        `gorm:"default:1" json:"priority_level"`
	ActionPlan           *string    `gorm:"type:text" json:"action_plan"`
	ActionPlanStatus     string     `gorm:"type:varchar(50);default:'NOT_STARTED'" json:"action_plan_status"`
	ActionPlanAssignedTo *uuid.UUID `gorm:"type:uuid" json:"action_plan_assigned_to"`
	ActionPlanDueDate    *time.Time `json:"action_plan_due_date"`
	ProgressPercentage   int        `gorm:"default:0" json:"progress_percentage"`
	LastAssessmentDate   *time.Time `json:"last_assessment_date"`
	NextAssessmentDate   *time.Time `json:"next_assessment_date"`
	Notes                *string    `gorm:"type:text" json:"notes"`
	Tags                 []string   `gorm:"type:varchar(100)[]" json:"tags"`

	common.Auditable
}

func (StudentNeedsEnhanced) TableName() string {
	return "student_needs_enhanced"
}

// StudentNeedsHistory represents history of student needs changes
type StudentNeedsHistory struct {
	ID                     uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentNeedsEnhancedID uuid.UUID  `gorm:"type:uuid;not null;index" json:"student_needs_enhanced_id"`
	PreviousStatus         *string    `gorm:"type:text" json:"previous_status"`
	NewStatus              *string    `gorm:"type:text" json:"new_status"`
	PreviousActionPlan     *string    `gorm:"type:text" json:"previous_action_plan"`
	NewActionPlan          *string    `gorm:"type:text" json:"new_action_plan"`
	AssessmentDate         time.Time  `gorm:"default:CURRENT_TIMESTAMP" json:"assessment_date"`
	AssessorID             *uuid.UUID `gorm:"type:uuid" json:"assessor_id"`
	AssessmentNotes        *string    `gorm:"type:text" json:"assessment_notes"`
	AssessmentMethod       string     `gorm:"type:varchar(50)" json:"assessment_method"`
	PreviousProgress       *int       `json:"previous_progress"`
	NewProgress            *int       `json:"new_progress"`
	ProgressNotes          *string    `gorm:"type:text" json:"progress_notes"`

	common.Auditable
}

func (StudentNeedsHistory) TableName() string {
	return "student_needs_history"
}

// SWOTItem represents individual SWOT analysis items
type SWOTItem struct {
	ID                  uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID            uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	Quadrant            string     `gorm:"type:varchar(1);not null" json:"quadrant"`
	Statement           string     `gorm:"type:text;not null" json:"statement"`
	Description         *string    `gorm:"type:text" json:"description"`
	SourceDataID        *uuid.UUID `gorm:"type:uuid" json:"source_data_id"`
	SourceDataType      *string    `gorm:"type:varchar(50)" json:"source_data_type"`
	SourceTable         *string    `gorm:"type:varchar(100)" json:"source_table"`
	Category            *string    `gorm:"type:varchar(100)" json:"category"`
	Tags                []string   `gorm:"type:varchar(100)[]" json:"tags"`
	Priority            int        `gorm:"default:1" json:"priority"`
	ImpactScore         *int       `json:"impact_score"`
	UrgencyScore        *int       `json:"urgency_score"`
	HasActionItem       bool       `gorm:"default:false" json:"has_action_item"`
	ActionItemID        *uuid.UUID `gorm:"type:uuid" json:"action_item_id"`
	CreatedFromTemplate bool       `gorm:"default:false" json:"created_from_template"`
	TemplateReference   *string    `gorm:"type:varchar(100)" json:"template_reference"`

	common.Auditable
}

func (SWOTItem) TableName() string {
	return "swot_items"
}

// SWOTAnalysisSession represents SWOT analysis sessions
type SWOTAnalysisSession struct {
	ID            uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID      uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	SessionName   string     `gorm:"type:varchar(255);not null" json:"session_name"`
	Description   *string    `gorm:"type:text" json:"description"`
	AnalysisDate  time.Time  `gorm:"default:CURRENT_TIMESTAMP" json:"analysis_date"`
	Participants  *string    `gorm:"type:jsonb" json:"participants"`
	FacilitatorID *uuid.UUID `gorm:"type:uuid" json:"facilitator_id"`
	Status        string     `gorm:"type:varchar(50);default:'DRAFT'" json:"status"`
	SummaryText   *string    `gorm:"type:text" json:"summary_text"`
	KeyInsights   []string   `gorm:"type:text[]" json:"key_insights"`
	IsTemplate    bool       `gorm:"default:false" json:"is_template"`
	TemplateName  *string    `gorm:"type:varchar(255)" json:"template_name"`

	common.Auditable
}

func (SWOTAnalysisSession) TableName() string {
	return "swot_analysis_sessions"
}

// SWOTSessionItem represents junction between sessions and SWOT items
type SWOTSessionItem struct {
	ID            uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SWOTSessionID uuid.UUID `gorm:"type:uuid;not null;index" json:"swot_session_id"`
	SWOTItemID    uuid.UUID `gorm:"type:uuid;not null" json:"swot_item_id"`
	SequenceOrder int       `gorm:"default:0" json:"sequence_order"`
	Quadrant      *string   `gorm:"type:varchar(50)" json:"quadrant"`  // S, W, O, T
	Category      *string   `gorm:"type:varchar(100)" json:"category"` // Custom category
	Notes         *string   `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (SWOTSessionItem) TableName() string {
	return "swot_session_items"
}

// RootCause represents root cause analysis with 5-Whys method
type RootCause struct {
	ID                   uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID             uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	RaporMetricID        *uuid.UUID `gorm:"type:uuid" json:"rapor_metric_id"`
	IdentifiedProblem    string     `gorm:"type:text;not null" json:"identified_problem"`
	ProblemCategory      *string    `gorm:"type:varchar(100)" json:"problem_category"`
	Why1                 *string    `gorm:"type:text" json:"why_1"`
	Why2                 *string    `gorm:"type:text" json:"why_2"`
	Why3                 *string    `gorm:"type:text" json:"why_3"`
	Why4                 *string    `gorm:"type:text" json:"why_4"`
	Why5                 *string    `gorm:"type:text" json:"why_5"`
	RootCause            string     `gorm:"type:text;not null" json:"root_cause"`
	RootCauseCategory    *string    `gorm:"type:varchar(100)" json:"root_cause_category"`
	KegiatanBenahi       string     `gorm:"type:text;not null" json:"kegiatan_benahi"`
	ActionPriority       int        `gorm:"default:1" json:"action_priority"`
	AssignedTo           *uuid.UUID `gorm:"type:uuid" json:"assigned_to"`
	DueDate              *time.Time `json:"due_date"`
	Status               string     `gorm:"type:varchar(50);default:'IDENTIFIED'" json:"status"`
	CompletionPercentage int        `gorm:"default:0" json:"completion_percentage"`
	ActualCompletionDate *time.Time `json:"actual_completion_date"`
	IsValidated          bool       `gorm:"default:false" json:"is_validated"`
	ValidatedBy          *uuid.UUID `gorm:"type:uuid" json:"validated_by"`
	ValidatedAt          *time.Time `json:"validated_at"`
	ValidationNotes      *string    `gorm:"type:text" json:"validation_notes"`
	LinkedSWOTID         *uuid.UUID `gorm:"type:uuid" json:"linked_swot_id"`
	EvidenceURLs         []string   `gorm:"type:text[]" json:"evidence_urls"`
	Notes                *string    `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (RootCause) TableName() string {
	return "root_causes"
}

// RootCauseHistory represents history of root cause changes
type RootCauseHistory struct {
	ID                 uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	RootCauseID        uuid.UUID  `gorm:"type:uuid;not null;index" json:"root_cause_id"`
	PreviousStatus     *string    `gorm:"type:varchar(50)" json:"previous_status"`
	NewStatus          *string    `gorm:"type:varchar(50)" json:"new_status"`
	PreviousKegiatan   *string    `gorm:"type:text" json:"previous_kegiatan_benahi"`
	NewKegiatan        *string    `gorm:"type:text" json:"new_kegiatan_benahi"`
	ValidationDate     *time.Time `json:"validation_date"`
	ValidatorID        *uuid.UUID `gorm:"type:uuid" json:"validator_id"`
	ValidationResult   *string    `gorm:"type:varchar(50)" json:"validation_result"`
	ValidationComments *string    `gorm:"type:text" json:"validation_comments"`

	common.Auditable
}

func (RootCauseHistory) TableName() string {
	return "root_cause_history"
}

// FishboneDiagram represents fishbone (Ishikawa) diagrams
type FishboneDiagram struct {
	ID                uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID          uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	HeadEffect        string     `gorm:"type:text;not null" json:"head_effect"`
	Description       *string    `gorm:"type:text" json:"description"`
	DiagramName       *string    `gorm:"type:varchar(255)" json:"diagram_name"`
	DiagramType       string     `gorm:"type:varchar(50);default:'STANDARD'" json:"diagram_type"`
	BoneCategories    []string   `gorm:"type:varchar(100)[]" json:"bone_categories"`
	Status            string     `gorm:"type:varchar(50);default:'DRAFT'" json:"status"`
	IsTemplate        bool       `gorm:"default:false" json:"is_template"`
	TemplateName      *string    `gorm:"type:varchar(255)" json:"template_name"`
	TotalNodes        int        `gorm:"default:0" json:"total_nodes"`
	LastModifiedAt    *time.Time `json:"last_modified_at"`
	LinkedRootCauseID *uuid.UUID `gorm:"type:uuid" json:"linked_root_cause_id"`
	LinkedSWOTID      *uuid.UUID `gorm:"type:uuid" json:"linked_swot_id"`

	common.Auditable
}

func (FishboneDiagram) TableName() string {
	return "fishbone_diagrams"
}

// FishboneNode represents nodes in fishbone diagrams
type FishboneNode struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DiagramID    uuid.UUID  `gorm:"type:uuid;not null;index" json:"diagram_id"`
	BoneCategory string     `gorm:"type:varchar(100);not null" json:"bone_category"`
	CauseText    string     `gorm:"type:text;not null" json:"cause_text"`
	NodeLevel    int        `gorm:"default:1" json:"node_level"`
	ParentNodeID *uuid.UUID `gorm:"type:uuid" json:"parent_node_id"`
	PositionX    *int       `json:"position_x"`
	PositionY    *int       `json:"position_y"`
	SequenceNo   int        `gorm:"default:0" json:"sequence_no"`
	IsMainBone   bool       `gorm:"default:false" json:"is_main_bone"`
	Color        *string    `gorm:"type:varchar(20)" json:"color"`
	NodeSize     string     `gorm:"type:varchar(20);default:'MEDIUM'" json:"node_size"`
	EvidenceURLs []string   `gorm:"type:text[]" json:"evidence_urls"`
	Notes        *string    `gorm:"type:text" json:"notes"`
	Priority     int        `gorm:"default:1" json:"priority"`

	common.Auditable
}

func (FishboneNode) TableName() string {
	return "fishbone_nodes"
}

// FishboneConnection represents connections between fishbone nodes
type FishboneConnection struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DiagramID      uuid.UUID `gorm:"type:uuid;not null;index" json:"diagram_id"`
	FromNodeID     uuid.UUID `gorm:"type:uuid;not null" json:"from_node_id"`
	ToNodeID       uuid.UUID `gorm:"type:uuid;not null" json:"to_node_id"`
	ConnectionType string    `gorm:"type:varchar(50);default:'DIRECT'" json:"connection_type"`
	LineStyle      string    `gorm:"type:varchar(50);default:'SOLID'" json:"line_style"`
	LineWeight     int       `gorm:"default:2" json:"line_weight"`

	common.Auditable
}

func (FishboneConnection) TableName() string {
	return "fishbone_connections"
}

// KSPAnalysisIntegration represents integration of analysis into KSP documents
type KSPAnalysisIntegration struct {
	ID                   uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID             uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	CurriculumDocumentID uuid.UUID  `gorm:"type:uuid;not null" json:"curriculum_document_id"`
	SWOTAnalysisID       *uuid.UUID `gorm:"type:uuid" json:"swot_analysis_id"`
	RootCauseID          *uuid.UUID `gorm:"type:uuid" json:"root_cause_id"`
	FishboneDiagramID    *uuid.UUID `gorm:"type:uuid" json:"fishbone_diagram_id"`
	StudentNeedsID       *uuid.UUID `gorm:"type:uuid" json:"student_needs_id"`
	RaporPendidikanID    *uuid.UUID `gorm:"type:uuid" json="rapor_pendidikan_id"`
	IntegrationType      string     `gorm:"type:varchar(50);not null" json:"integration_type"`
	SectionInKSP         string     `gorm:"type:text;not null" json:"section_in_ksp"`
	IntegratedContent    *string    `gorm:"type:text" json:"integrated_content"`
	Weight               float64    `gorm:"type:decimal(3,2);default:1.0" json:"weight"`
	InfluenceType        *string    `gorm:"type:varchar(50)" json:"influence_type"`
	IntegrationStatus    string     `gorm:"type:varchar(50);default:'PENDING'" json:"integration_status"`
	ApprovedBy           *uuid.UUID `gorm:"type:uuid" json:"approved_by"`
	ApprovedAt           *time.Time `json:"approved_at"`
	ApprovalNotes        *string    `gorm:"type:text" json:"approval_notes"`
	IsUsedInDocument     bool       `gorm:"default:false" json:"is_used_in_document"`
	UsedInSections       []string   `gorm:"type:text[]" json:"used_in_sections"`
	Notes                *string    `gorm:"type:text" json:"notes"`
	Tags                 []string   `gorm:"type:varchar(100)[]" json:"tags"`

	common.Auditable
}

func (KSPAnalysisIntegration) TableName() string {
	return "ksp_analysis_integration"
}

// KSPAnalysisRecommendation represents recommendations based on analysis
type KSPAnalysisRecommendation struct {
	ID                       uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	KSPAnalysisIntegrationID uuid.UUID  `gorm:"type:uuid;not null;index" json:"ksp_analysis_integration_id"`
	RecommendationType       string     `gorm:"type:varchar(50);not null" json:"recommendation_type"`
	RecommendationText       string     `gorm:"type:text;not null" json:"recommendation_text"`
	Priority                 int        `gorm:"default:1" json:"priority"`
	SuggestedAction          *string    `gorm:"type:text" json:"suggested_action"`
	TargetSectionInKSP       *string    `gorm:"type:text" json:"target_section_in_ksp"`
	Status                   string     `gorm:"type:varchar(50);default:'SUGGESTED'" json:"status"`
	ImplementedAt            *time.Time `json:"implemented_at"`
	ImplementedBy            *uuid.UUID `gorm:"type:uuid" json:"implemented_by"`
	EffectivenessRating      *int       `json:"effectiveness_rating"`
	EffectivenessNotes       *string    `gorm:"type:text" json:"effectiveness_notes"`
	Source                   *string    `gorm:"type:varchar(50)" json:"source"`
	ConfidenceScore          *float64   `gorm:"type:decimal(3,2)" json:"confidence_score"`

	common.Auditable
}

func (KSPAnalysisRecommendation) TableName() string {
	return "ksp_analysis_recommendations"
}

// KSPAnalysisTemplate represents templates for KSP analysis integration
type KSPAnalysisTemplate struct {
	ID                    uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID              *uuid.UUID `gorm:"type:uuid" json:"school_id"`
	TemplateName          string     `gorm:"type:varchar(255);not null" json:"template_name"`
	TemplateDescription   *string    `gorm:"type:text" json:"template_description"`
	TemplateCategory      *string    `gorm:"type:varchar(100)" json:"template_category"`
	IntegrationStructure  string     `gorm:"type:jsonb;not null" json:"integration_structure"`
	DefaultSections       []string   `gorm:"type:text[]" json:"default_sections"`
	RequiredAnalysisTypes []string   `gorm:"type:varchar(50)[]" json:"required_analysis_types"`
	IsPublic              bool       `gorm:"default:false" json:"is_public"`
	IsActive              bool       `gorm:"default:true" json:"is_active"`
	UsageCount            int        `gorm:"default:0" json:"usage_count"`

	common.Auditable
}

func (KSPAnalysisTemplate) TableName() string {
	return "ksp_analysis_templates"
}
