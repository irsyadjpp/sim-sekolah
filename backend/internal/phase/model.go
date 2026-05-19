package phase

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// Phase merepresentasikan fase belajar (A, B, C) pada kurikulum.
type Phase struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Code        string    `gorm:"uniqueIndex;column:phase_code" json:"phase_code"`
	Name        string    `gorm:"uniqueIndex;column:phase_name" json:"phase_name"`
	Description string    `gorm:"column:description"            json:"description"`

	common.Auditable
}

func (Phase) TableName() string {
	return "master_phase"
}
