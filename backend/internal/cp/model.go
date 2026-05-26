package cp

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/phase"
	"sim-sekolah/internal/subject"

	"github.com/google/uuid"
)

// LearningOutcome represents a Capaian Pembelajaran (CP) entry.
type LearningOutcome struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PhaseID     uuid.UUID `gorm:"index" json:"phase_id"`
	SubjectID   uuid.UUID `gorm:"index" json:"subject_id"`
	CPCode      string    `gorm:"uniqueIndex;column:cp_code"                      json:"cp_code"`
	OutcomeText string    `json:"outcome_text"`
	YearSK      string    `gorm:"index;column:year_sk"                            json:"year_sk"` // e.g., 24, 26

	common.Auditable

	// Relations to other modules
	Phase   phase.Phase     `gorm:"foreignKey:PhaseID"   json:"phase,omitempty"`
	Subject subject.Subject `gorm:"foreignKey:SubjectID" json:"subject,omitempty"`

	// Related detail entries
	Details []CPDetail `gorm:"foreignKey:LearningOutcomeID" json:"details,omitempty"`
}

func (LearningOutcome) TableName() string {
	return "cur_learning_outcome"
}

// CPDetail represents an individual detail entry of a LearningOutcome.
type CPDetail struct {
	ID                uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	LearningOutcomeID uuid.UUID `json:"learning_outcome_id"`
	ElementID         uuid.UUID `json:"element_id"`
	SubCode           string    `json:"sub_code"`
	DetailText        string    `json:"detail_text"`
	SequenceNo        int       `gorm:"default:1"                                       json:"sequence_no"`

	common.Auditable

	Element subject.SubjectElement `gorm:"foreignKey:ElementID" json:"element,omitempty"`
}

func (CPDetail) TableName() string {
	return "cur_cp_detail"
}

// LearningObjective (TP) represents a specific objective derived from a CP.
type LearningObjective struct {
	ID                uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	LearningOutcomeID uuid.UUID `gorm:"type:uuid;not null;index" json:"learning_outcome_id"`
	Description       string    `gorm:"type:text;not null" json:"description"`
	Sequence          int       `gorm:"type:integer;default:1;index" json:"sequence"`              // TP sequencing order
	DifficultyLevel   string    `gorm:"type:varchar(20);default:'MEDIUM'" json:"difficulty_level"` // EASY, MEDIUM, HARD
	CognitiveDomain   string    `gorm:"type:varchar(50)" json:"cognitive_domain"`                  // C1, C2, C3, C4, C5, C6 (Bloom's)
	EstimatedHours    float64   `gorm:"type:decimal(5,2);default:1.0" json:"estimated_hours"`      // Time estimation for this objective

	common.Auditable
}

func (LearningObjective) TableName() string {
	return "cur_learning_objective"
}

// Difficulty level constants
const (
	DifficultyLevelEasy   = "EASY"
	DifficultyLevelMedium = "MEDIUM"
	DifficultyLevelHard   = "HARD"
)

// Cognitive domain constants (Bloom's Taxonomy)
const (
	CognitiveDomainC1 = "C1" // Remembering
	CognitiveDomainC2 = "C2" // Understanding
	CognitiveDomainC3 = "C3" // Applying
	CognitiveDomainC4 = "C4" // Analyzing
	CognitiveDomainC5 = "C5" // Evaluating
	CognitiveDomainC6 = "C6" // Creating
)

// GetDifficultyLevelDescription returns Indonesian description for difficulty level
func GetDifficultyLevelDescription(level string) string {
	descriptions := map[string]string{
		DifficultyLevelEasy:   "Mudah",
		DifficultyLevelMedium: "Sedang",
		DifficultyLevelHard:   "Sulit",
	}
	if desc, exists := descriptions[level]; exists {
		return desc
	}
	return level
}

// GetCognitiveDomainDescription returns Indonesian description for cognitive domain
func GetCognitiveDomainDescription(domain string) string {
	descriptions := map[string]string{
		CognitiveDomainC1: "Mengingat (C1)",
		CognitiveDomainC2: "Memahami (C2)",
		CognitiveDomainC3: "Menerapkan (C3)",
		CognitiveDomainC4: "Menganalisis (C4)",
		CognitiveDomainC5: "Mengevaluasi (C5)",
		CognitiveDomainC6: "Mencipta (C6)",
	}
	if desc, exists := descriptions[domain]; exists {
		return desc
	}
	return domain
}
