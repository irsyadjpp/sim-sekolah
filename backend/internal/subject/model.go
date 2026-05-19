package subject

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// Subject merepresentasikan mata pelajaran.
type Subject struct {
	ID              uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SubjectCode     string    `gorm:"type:varchar(20);uniqueIndex;not null"           json:"subject_code"`
	SubjectName     string    `gorm:"type:varchar(255);uniqueIndex;not null"          json:"subject_name"`
	Rational        string    `json:"rational"`
	Goals           string    `json:"goals"`
	Characteristics string    `json:"characteristics"`
	IsActive        bool      `gorm:"default:true"                                    json:"is_active"`
	Level           string    `gorm:"column:level"                                    json:"level"`        // e.g., SD, SMP, SMA
	Abbreviation    string    `gorm:"column:abbreviation"                             json:"abbreviation"` // e.g., MTK, PAI

	common.Auditable

	Elements             []SubjectElement      `gorm:"foreignKey:SubjectID" json:"elements,omitempty"`
	CharacteristicPoints []CharacteristicPoint `gorm:"foreignKey:SubjectID" json:"characteristic_points,omitempty"`
}

func (Subject) TableName() string {
	return "master_subject"
}

// CharacteristicPoint merepresentasikan poin karakteristik mata pelajaran.
type CharacteristicPoint struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SubjectID   uuid.UUID `gorm:"type:uuid;index"                                json:"subject_id"`
	Description string    `gorm:"column:description"                             json:"description"`

	Elements []SubjectElement `gorm:"foreignKey:PointID" json:"elements,omitempty"`

	common.Auditable
}

func (CharacteristicPoint) TableName() string {
	return "master_subject_characteristic"
}

// SubjectElement merepresentasikan elemen dari mata pelajaran.
type SubjectElement struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SubjectID    uuid.UUID  `gorm:"type:uuid;index"                                json:"subject_id"`
	PointID      *uuid.UUID `gorm:"type:uuid;index"                                json:"point_id"`
	ElementName  string     `gorm:"column:element_name"                            json:"element_name"`
	Abbreviation string     `gorm:"column:abbreviation"                            json:"abbreviation"`
	ElementCode  string     `gorm:"column:element_code"                            json:"element_code"`
	Description  string     `gorm:"column:description"                             json:"description"`

	common.Auditable
}

func (SubjectElement) TableName() string {
	return "master_subject_element"
}
