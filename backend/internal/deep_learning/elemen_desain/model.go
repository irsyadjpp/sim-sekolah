package elemen_desain

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// DesignElement represents a Deep Learning Design Element.
type DesignElement struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Name        string    `gorm:"column:design_element_name;uniqueIndex;not null"  json:"design_element_name"`
	Description string    `gorm:"column:description"                              json:"description"`
	IsActive    bool      `gorm:"column:is_active;default:true"                  json:"is_active"`

	common.Auditable
}

func (DesignElement) TableName() string {
	return "dl_design_element"
}
