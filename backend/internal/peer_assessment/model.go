package peer_assessment

import (
	"time"

	"github.com/lib/pq"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// Assessment Type Constants
const (
	AssessmentTypeSelf  = "SELF"
	AssessmentTypePeer  = "PEER"
	AssessmentTypeGroup = "GROUP"
)

// Phase Constants
const (
	PhaseFaseA = "FASE_A"
	PhaseFaseB = "FASE_B"
	PhaseFaseC = "FASE_C"
)

// Assessment Focus Constants
const (
	AssessmentFocusCollaboration    = "COLLABORATION"
	AssessmentFocusCommunication    = "COMMUNICATION"
	AssessmentFocusCreativity       = "CREATIVITY"
	AssessmentFocusCriticalThinking = "CRITICAL_THINKING"
	AssessmentFocusParticipation    = "PARTICIPATION"
)

// Confidence Level Constants
const (
	ConfidenceLevelLow    = "LOW"
	ConfidenceLevelMedium = "MEDIUM"
	ConfidenceLevelHigh   = "HIGH"
)

// Review Status Constants
const (
	ReviewStatusPending  = "PENDING"
	ReviewStatusApproved = "APPROVED"
	ReviewStatusRejected = "REJECTED"
)

// Rating Constants
const (
	RatingPoor      = "POOR"
	RatingFair      = "FAIR"
	RatingGood      = "GOOD"
	RatingExcellent = "EXCELLENT"
)

// Participation Rating Constants
const (
	ParticipationRatingLow    = "LOW"
	ParticipationRatingMedium = "MEDIUM"
	ParticipationRatingHigh   = "HIGH"
)

// Role Constants
const (
	RoleLeader      = "LEADER"
	RoleContributor = "CONTRIBUTOR"
	RoleSupporter   = "SUPPORTER"
	RoleObserver    = "OBSERVER"
)

// PeerAssessmentTemplate represents simplified rubrics for SD
type PeerAssessmentTemplate struct {
	ID              uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TemplateName    string     `gorm:"type:varchar(100);not null" json:"template_name"`
	AssessmentType  string     `gorm:"type:varchar(20);not null" json:"assessment_type"`
	SubjectID       *uuid.UUID `gorm:"type:uuid" json:"subject_id"`
	Phase           string     `gorm:"type:varchar(20);not null" json:"phase"`
	AssessmentFocus string     `gorm:"type:varchar(50);not null" json:"assessment_focus"`
	Description     string     `gorm:"type:text;not null" json:"description"`
	Criteria        string     `gorm:"type:jsonb;not null" json:"criteria"`     // Simplified criteria structure suitable for SD
	RatingScale     string     `gorm:"type:jsonb;not null" json:"rating_scale"` // Simple rating scales (emojis, stars, etc.)
	Instructions    string     `gorm:"type:text" json:"instructions"`
	IsActive        bool       `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (PeerAssessmentTemplate) TableName() string {
	return "master_peer_assessment_template"
}

// SelfAssessment represents student self-assessments
type SelfAssessment struct {
	ID              uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID       uuid.UUID  `gorm:"type:uuid;not null" json:"student_id"`
	TemplateID      uuid.UUID  `gorm:"type:uuid;not null" json:"template_id"`
	TeacherID       *uuid.UUID `gorm:"type:uuid" json:"teacher_id"`
	AssessmentDate  time.Time  `gorm:"type:date;not null;default:CURRENT_DATE" json:"assessment_date"`
	Context         string     `gorm:"type:varchar(100)" json:"context"`     // Which activity/project this is for
	Responses       string     `gorm:"type:jsonb;not null" json:"responses"` // Student's self-assessment responses
	SelfReflection  string     `gorm:"type:text" json:"self_reflection"`
	GoalsSet        []string   `gorm:"type:jsonb" json:"goals_set"`
	ConfidenceLevel string     `gorm:"type:varchar(20)" json:"confidence_level"`
	TeacherFeedback string     `gorm:"type:text" json:"teacher_feedback"`

	common.Auditable
}

func (SelfAssessment) TableName() string {
	return "trx_self_assessment"
}

// PeerAssessment represents peer-to-peer assessments
type PeerAssessment struct {
	ID                   uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	AssessorStudentID    uuid.UUID  `gorm:"type:uuid;not null" json:"assessor_student_id"`
	AssessedStudentID    uuid.UUID  `gorm:"type:uuid;not null" json:"assessed_student_id"`
	TemplateID           uuid.UUID  `gorm:"type:uuid;not null" json:"template_id"`
	TeacherID            *uuid.UUID `gorm:"type:uuid" json:"teacher_id"`
	AssessmentDate       time.Time  `gorm:"type:date;not null;default:CURRENT_DATE" json:"assessment_date"`
	Context              string     `gorm:"type:varchar(100)" json:"context"`     // Which activity/project this is for
	Responses            string     `gorm:"type:jsonb;not null" json:"responses"` // Peer's assessment responses
	PositiveFeedback     string     `gorm:"type:text" json:"positive_feedback"`
	ConstructiveFeedback string     `gorm:"type:text" json:"constructive_feedback"`
	Suggestions          []string   `gorm:"type:jsonb" json:"suggestions"`
	RelationshipContext  string     `gorm:"type:varchar(50)" json:"relationship_context"` // GROUP_MEMBER, CLASSMATE, PROJECT_PARTNER
	TeacherReviewStatus  string     `gorm:"type:varchar(20);default:PENDING" json:"teacher_review_status"`
	TeacherNotes         string     `gorm:"type:text" json:"teacher_notes"`

	common.Auditable
}

func (PeerAssessment) TableName() string {
	return "trx_peer_assessment"
}

// GroupAssessment represents group assessments for collaborative work
type GroupAssessment struct {
	ID                      uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	GroupID                 uuid.UUID  `gorm:"type:uuid;not null" json:"group_id"`
	GroupName               string     `gorm:"type:varchar(100);not null" json:"group_name"`
	TemplateID              uuid.UUID  `gorm:"type:uuid;not null" json:"template_id"`
	TeacherID               *uuid.UUID `gorm:"type:uuid" json:"teacher_id"`
	AssessmentDate          time.Time  `gorm:"type:date;not null;default:CURRENT_DATE" json:"assessment_date"`
	Context                 string     `gorm:"type:varchar(100)" json:"context"` // Which project/activity
	ProjectDescription      string     `gorm:"type:text" json:"project_description"`
	GroupResponses          string     `gorm:"type:jsonb;not null" json:"group_responses"` // Group-level assessment responses
	IndividualContributions string     `gorm:"type:jsonb" json:"individual_contributions"` // Individual contribution tracking
	CollaborationRating     string     `gorm:"type:varchar(20)" json:"collaboration_rating"`
	GroupGoals              []string   `gorm:"type:jsonb" json:"group_goals"`
	GroupReflection         string     `gorm:"type:text" json:"group_reflection"`
	TeacherFeedback         string     `gorm:"type:text" json:"teacher_feedback"`

	common.Auditable
}

func (GroupAssessment) TableName() string {
	return "trx_group_assessment"
}

// GroupAssessmentMember represents individual member contributions in group assessments
type GroupAssessmentMember struct {
	ID                     uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	GroupAssessmentID      uuid.UUID      `gorm:"type:uuid;not null" json:"group_assessment_id"`
	StudentID              uuid.UUID      `gorm:"type:uuid;not null" json:"student_id"`
	Role                   string         `gorm:"type:varchar(50)" json:"role"`
	ParticipationRating    string         `gorm:"type:varchar(20)" json:"participation_rating"`
	PeerFeedbackReceived   pq.StringArray `gorm:"type:jsonb" json:"peer_feedback_received"`
	SelfContributionRating string         `gorm:"type:varchar(20)" json:"self_contribution_rating"`
	ContributionNotes      string         `gorm:"type:text" json:"contribution_notes"`

	common.Auditable
}

func (GroupAssessmentMember) TableName() string {
	return "trx_group_assessment_member"
}

// PeerAssessmentGuideline represents age-appropriate peer assessment guidelines for SD
type PeerAssessmentGuideline struct {
	ID                uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Phase             string         `gorm:"type:varchar(20);not null" json:"phase"`
	GuidelineCategory string         `gorm:"type:varchar(50);not null" json:"guideline_category"` // GIVING_FEEDBACK, RECEIVING_FEEDBACK, SELF_REFLECTION
	Title             string         `gorm:"type:varchar(100);not null" json:"title"`
	Content           string         `gorm:"type:text;not null" json:"content"`
	Examples          pq.StringArray `json:"examples"`
	Dos               pq.StringArray `json:"dos"`
	Donts             pq.StringArray `json:"donts"`
	DisplayOrder      int            `gorm:"default:0" json:"display_order"`
	IsActive          bool           `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (PeerAssessmentGuideline) TableName() string {
	return "master_peer_assessment_guideline"
}
