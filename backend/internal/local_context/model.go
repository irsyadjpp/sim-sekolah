package local_context

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// LocalContextCategory merepresentasikan kategori konteks lokal.
type LocalContextCategory struct {
	ID           uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	CategoryCode string    `gorm:"unique;column:category_code"                      json:"category_code"`
	CategoryName string    `gorm:"column:category_name"                             json:"category_name"`
	Description  string    `gorm:"column:description"                               json:"description"`

	common.Auditable
}

func (LocalContextCategory) TableName() string {
	return "master_local_context_category"
}

// LocalContext merepresentasikan data konteks lokal spesifik.
type LocalContext struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID    *uuid.UUID `gorm:"column:school_id"                                json:"school_id"`
	CategoryID  uuid.UUID  `gorm:"column:category_id"                               json:"category_id"`
	Title       string     `gorm:"column:title"                                     json:"title"`
	Description string     `gorm:"column:description"                               json:"description"`
	Location    string     `gorm:"column:location"                                  json:"location"`
	ScopeType   string     `gorm:"column:scope_type"                                json:"scope_type"` // SCHOOL, VILLAGE, CLASS, STUDENT
	IsActive    bool       `gorm:"default:true"                                     json:"is_active"`

	common.Auditable

	// Relations
	Category LocalContextCategory `gorm:"foreignKey:CategoryID" json:"category,omitempty"`
}

func (LocalContext) TableName() string {
	return "master_local_context"
}
