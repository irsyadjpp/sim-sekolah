package tingkat_asesmen

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// AssessmentLevel represents a Deep Learning Assessment Level.
type AssessmentLevel struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	LevelCode   string    `gorm:"column:level_code;uniqueIndex;not null"         json:"level_code"`
	Description string    `gorm:"column:description;not null"                    json:"description"`
	PISALevel   string    `gorm:"column:pisa_level"                              json:"pisa_level"`

	common.Auditable
}

func (AssessmentLevel) TableName() string {
	return "dl_assessment_level"
}
