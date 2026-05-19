package profile_dimension

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// ProfileDimension represents a dimension of the graduation profile (Pancasila).
type ProfileDimension struct {
	ID            uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DimensionCode string    `gorm:"column:dimension_code;uniqueIndex;not null"      json:"dimension_code"`
	DimensionName string    `gorm:"column:dimension_name;not null"                  json:"dimension_name"`
	Description   string    `gorm:"column:description"                              json:"description"`
	IsActive      bool      `gorm:"column:is_active;default:true"                 json:"is_active"`

	common.Auditable
}

func (ProfileDimension) TableName() string {
	return "master_profile_dimension"
}
