package tahapan_kognitif

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// CognitiveStage represents a Deep Learning Cognitive Stage.
type CognitiveStage struct {
	ID    uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Order int       `gorm:"column:stage_order;not null"                     json:"stage_order"`
	Name  string    `gorm:"column:stage_name;uniqueIndex;not null"          json:"stage_name"`
	KKO   string    `gorm:"column:operational_verbs"                        json:"operational_verbs"`

	common.Auditable
}

func (CognitiveStage) TableName() string {
	return "dl_cognitive_stage"
}
