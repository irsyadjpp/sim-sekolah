package play_based_learning

import (
	"github.com/google/uuid"

	"sim-sekolah/internal/common"
)

// Social Interaction Type constants
const (
	SocialInteractionIndividual = "INDIVIDUAL"
	SocialInteractionPair       = "PAIR"
	SocialInteractionGroup      = "GROUP"
	SocialInteractionClass      = "CLASS"
)

// Physical Activity Level constants
const (
	PhysicalActivityLow    = "LOW"
	PhysicalActivityMedium = "MEDIUM"
	PhysicalActivityHigh   = "HIGH"
)

// IsValidSocialInteraction validates social interaction type
func IsValidSocialInteraction(interaction string) bool {
	validInteractions := map[string]bool{
		SocialInteractionIndividual: true,
		SocialInteractionPair:       true,
		SocialInteractionGroup:      true,
		SocialInteractionClass:      true,
	}
	return validInteractions[interaction]
}

// IsValidPhysicalActivity validates physical activity level
func IsValidPhysicalActivity(level string) bool {
	validLevels := map[string]bool{
		PhysicalActivityLow:    true,
		PhysicalActivityMedium: true,
		PhysicalActivityHigh:   true,
	}
	return validLevels[level]
}

// PlayActivityType represents a type of play-based activity for Fase A
type PlayActivityType struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ActivityCode     string    `gorm:"type:varchar(20);uniqueIndex;not null" json:"activity_code"`
	ActivityName     string    `gorm:"type:varchar(100);not null" json:"activity_name"`
	Description      string    `gorm:"type:text;not null" json:"description"`
	LearningOutcomes string    `gorm:"type:text" json:"learning_outcomes"`    // JSON array
	MaterialsNeeded  string    `gorm:"type:text" json:"materials_needed"`     // JSON array
	SuggestedAge     string    `gorm:"type:varchar(20)" json:"suggested_age"` // 6-7, 7-8
	PlayDomain       string    `gorm:"type:varchar(50)" json:"play_domain"`   // PHYSICAL, SOCIAL, COGNITIVE, CREATIVE
	PhaseID          uuid.UUID `gorm:"type:uuid;index" json:"phase_id"`
	IsActive         bool      `gorm:"type:boolean;default:true" json:"is_active"`

	common.Auditable
}

func (PlayActivityType) TableName() string {
	return "master_play_activity_type"
}

// PlayBasedActivity represents a play-based activity in a teaching module
type PlayBasedActivity struct {
	ID                    uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ModuleID              uuid.UUID `gorm:"type:uuid;not null;index" json:"module_id"`
	ActivityTypeID        uuid.UUID `gorm:"type:uuid;not null;index" json:"activity_type_id"`
	ActivityName          string    `gorm:"type:varchar(100);not null" json:"activity_name"`
	DurationMinutes       int       `gorm:"type:int" json:"duration_minutes"`
	SocialInteractionType string    `gorm:"type:varchar(30);not null" json:"social_interaction_type"`
	PhysicalActivityLevel string    `gorm:"type:varchar(20);not null" json:"physical_activity_level"`
	LearningGoals         string    `gorm:"type:text" json:"learning_goals"` // JSON array
	Instructions          string    `gorm:"type:text" json:"instructions"`
	SafetyConsiderations  string    `gorm:"type:text" json:"safety_considerations"`
	AssessmentMethod      string    `gorm:"type:varchar(100)" json:"assessment_method"`

	common.Auditable

	// Relations
	ActivityType PlayActivityType `gorm:"foreignKey:ActivityTypeID" json:"activity_type,omitempty"`
}

func (PlayBasedActivity) TableName() string {
	return "trx_play_based_activity"
}

// PlayObservation represents observation of play-based learning
type PlayObservation struct {
	ID                 uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ActivityID         uuid.UUID `gorm:"type:uuid;not null;index" json:"activity_id"`
	StudentID          uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	EngagementLevel    string    `gorm:"type:varchar(20)" json:"engagement_level"` // HIGH, MEDIUM, LOW
	SocialInteraction  string    `gorm:"type:varchar(50)" json:"social_interaction"`
	SkillsDemonstrated string    `gorm:"type:text" json:"skills_demonstrated"` // JSON array
	ChallengesObserved string    `gorm:"type:text" json:"challenges_observed"`
	TeacherNotes       string    `gorm:"type:text" json:"teacher_notes"`
	ObservationDate    string    `gorm:"type:date" json:"observation_date"`

	common.Auditable
}

func (PlayObservation) TableName() string {
	return "trx_play_observation"
}
