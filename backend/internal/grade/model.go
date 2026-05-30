package grade

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type Grade struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PhaseID    uuid.UUID `gorm:"type:uuid;not null" json:"phase_id"`
	GradeLevel int       `gorm:"type:smallint;not null" json:"grade_level"`
	GradeName  string    `gorm:"type:varchar(20);not null" json:"grade_name"`

	common.Auditable
}

func (Grade) TableName() string {
	return "master_grade"
}
