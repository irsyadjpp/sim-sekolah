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
	LearningOutcomeID uuid.UUID `gorm:"type:uuid;not null" json:"learning_outcome_id"`
	Description       string    `gorm:"type:text;not null" json:"description"`

	common.Auditable
}

func (LearningObjective) TableName() string {
	return "cur_learning_objective"
}
