package character_intervention

import (
	"time"

	"github.com/lib/pq"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// Character Dimension Constants
const (
	CharacterDimensionBerakhlak        = "BERAKHLAK"
	CharacterDimensionBerkebhineasan   = "BERKEBHINEASAN"
	CharacterDimensionBernilaiSantun   = "BERNILAI_SANTUN"
	CharacterDimensionMandiri          = "MANDIRI"
	CharacterDimensionBertanggungJawab = "BERTANGGUNG_JAWAB"
	CharacterDimensionGotongRoyong     = "GOTONG_ROYONG"
)

// Target Age Group Constants
const (
	TargetAgeGroupFaseA = "FASE_A"
	TargetAgeGroupFaseB = "FASE_B"
	TargetAgeGroupFaseC = "FASE_C"
)

// Intervention Type Constants
const (
	InterventionTypePositiveReinforcement = "POSITIVE_REINFORCEMENT"
	InterventionTypeBehaviorModification  = "BEHAVIOR_MODIFICATION"
	InterventionTypeMentoring             = "MENTORING"
	InterventionTypeGroupActivity         = "GROUP_ACTIVITY"
	InterventionTypeCounseling            = "COUNSELING"
)

// Assignment Status Constants
const (
	AssignmentStatusPlanned   = "PLANNED"
	AssignmentStatusActive    = "ACTIVE"
	AssignmentStatusPaused    = "PAUSED"
	AssignmentStatusCompleted = "COMPLETED"
	AssignmentStatusCancelled = "CANCELLED"
)

// Priority Level Constants
const (
	PriorityLevelLow    = "LOW"
	PriorityLevelMedium = "MEDIUM"
	PriorityLevelHigh   = "HIGH"
	PriorityLevelUrgent = "URGENT"
)

// Progress Rating Constants
const (
	ProgressRatingNoProgress  = "NO_PROGRESS"
	ProgressRatingMinimal     = "MINIMAL"
	ProgressRatingModerate    = "MODERATE"
	ProgressRatingSignificant = "SIGNIFICANT"
	ProgressRatingExcellent   = "EXCELLENT"
)

// Achievement Level Constants
const (
	AchievementLevelEmerging   = "EMERGING"
	AchievementLevelDeveloping = "DEVELOPING"
	AchievementLevelProficient = "PROFICIENT"
	AchievementLevelExemplary  = "EXEMPLARY"
)

// Celebration Method Constants
const (
	CelebrationMethodVerbalPraise       = "VERBAL_PRAISE"
	CelebrationMethodCertificate        = "CERTIFICATE"
	CelebrationMethodClassRecognition   = "CLASS_RECOGNITION"
	CelebrationMethodParentNotification = "PARENT_NOTIFICATION"
)

// Recommendation Source Constants
const (
	RecommendationSourceP5Assessment       = "P5_ASSESSMENT"
	RecommendationSourceTeacherObservation = "TEACHER_OBSERVATION"
	RecommendationSourceParentFeedback     = "PARENT_FEEDBACK"
	RecommendationSourcePeerFeedback       = "PEER_FEEDBACK"
)

// CharacterIntervention represents master intervention strategies
type CharacterIntervention struct {
	ID                 uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	InterventionName   string         `gorm:"type:varchar(100);not null" json:"intervention_name"`
	CharacterDimension string         `gorm:"type:varchar(50);not null" json:"character_dimension"`
	TargetAgeGroup     string         `gorm:"type:varchar(20)" json:"target_age_group"`
	InterventionType   string         `gorm:"type:varchar(50);not null" json:"intervention_type"`
	Description        string         `gorm:"type:text;not null" json:"description"`
	Strategies         pq.StringArray `gorm:"type:jsonb" json:"strategies"`
	Resources          pq.StringArray `gorm:"type:jsonb" json:"resources"`
	DurationWeeks      int            `gorm:"default:4" json:"duration_weeks"`
	SuccessCriteria    pq.StringArray `gorm:"type:jsonb" json:"success_criteria"`
	IsActive           bool           `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (CharacterIntervention) TableName() string {
	return "master_character_intervention"
}

// StudentCharacterIntervention represents student-specific intervention assignments
type StudentCharacterIntervention struct {
	ID                   uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID            uuid.UUID      `gorm:"type:uuid;not null" json:"student_id"`
	InterventionID       uuid.UUID      `gorm:"type:uuid;not null" json:"intervention_id"`
	TeacherID            uuid.UUID      `gorm:"type:uuid;not null" json:"teacher_id"`
	AssignmentDate       time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"assignment_date"`
	TargetStartDate      time.Time      `gorm:"type:date;not null" json:"target_start_date"`
	TargetEndDate        time.Time      `gorm:"type:date;not null" json:"target_end_date"`
	CurrentStatus        string         `gorm:"type:varchar(20);default:ACTIVE" json:"current_status"`
	PriorityLevel        string         `gorm:"type:varchar(20);default:MEDIUM" json:"priority_level"`
	BaselineAssessment   string         `gorm:"type:text" json:"baseline_assessment"`
	CustomizedStrategies pq.StringArray `gorm:"type:jsonb" json:"customized_strategies"`
	Notes                string         `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (StudentCharacterIntervention) TableName() string {
	return "trx_student_character_intervention"
}

// CharacterInterventionProgress tracks intervention progress
type CharacterInterventionProgress struct {
	ID                   uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	AssignmentID         uuid.UUID      `gorm:"type:uuid;not null" json:"assignment_id"`
	ObservationDate      time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"observation_date"`
	ObserverID           uuid.UUID      `gorm:"type:uuid;not null" json:"observer_id"`
	ProgressRating       string         `gorm:"type:varchar(20)" json:"progress_rating"`
	BehavioralIndicators pq.StringArray `gorm:"type:jsonb" json:"behavioral_indicators"`
	SpecificAchievements pq.StringArray `gorm:"type:jsonb" json:"specific_achievements"`
	Challenges           pq.StringArray `gorm:"type:jsonb" json:"challenges"`
	SupportProvided      string         `gorm:"type:text" json:"support_provided"`
	NextSteps            pq.StringArray `gorm:"type:jsonb" json:"next_steps"`
	Notes                string         `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (CharacterInterventionProgress) TableName() string {
	return "trx_character_intervention_progress"
}

// InterventionRecommendation represents recommendation engine results
type InterventionRecommendation struct {
	ID                          uuid.UUID   `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID                   uuid.UUID   `gorm:"type:uuid;not null" json:"student_id"`
	P5AssessmentID              *uuid.UUID  `gorm:"type:uuid" json:"p5_assessment_id"`
	RecommendedInterventions    []uuid.UUID `gorm:"type:uuid[]" json:"recommended_interventions"`
	RecommendationDate          time.Time   `gorm:"type:date;not null;default:CURRENT_DATE" json:"recommendation_date"`
	RecommendationSource        string      `gorm:"type:varchar(50);not null" json:"recommendation_source"`
	ConfidenceScore             *float64    `gorm:"type:numeric(3,2)" json:"confidence_score"`
	Rationale                   string      `gorm:"type:text" json:"rationale"`
	PriorityRanking             []int       `gorm:"type:int[]" json:"priority_ranking"`
	ImplementationTimelineWeeks int         `gorm:"default:4" json:"implementation_timeline_weeks"`
	AdditionalNotes             string      `gorm:"type:text" json:"additional_notes"`
	IsAccepted                  *bool       `gorm:"type:boolean" json:"is_accepted"`
	AcceptedBy                  *uuid.UUID  `gorm:"type:uuid" json:"accepted_by"`
	AcceptedDate                *time.Time  `gorm:"type:timestamp" json:"accepted_date"`

	common.Auditable
}

func (InterventionRecommendation) TableName() string {
	return "trx_intervention_recommendation"
}

// CharacterMilestone tracks character development milestones
type CharacterMilestone struct {
	ID                   uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID            uuid.UUID      `gorm:"type:uuid;not null" json:"student_id"`
	CharacterDimension   string         `gorm:"type:varchar(50);not null" json:"character_dimension"`
	MilestoneDescription string         `gorm:"type:text;not null" json:"milestone_description"`
	MilestoneDate        time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"milestone_date"`
	AchievementLevel     string         `gorm:"type:varchar(20);not null" json:"achievement_level"`
	Evidence             pq.StringArray `gorm:"type:jsonb" json:"evidence"`
	ObserverID           uuid.UUID      `gorm:"type:uuid;not null" json:"observer_id"`
	CelebrationMethod    string         `gorm:"type:varchar(50)" json:"celebration_method"`
	Notes                string         `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (CharacterMilestone) TableName() string {
	return "trx_character_milestone"
}
