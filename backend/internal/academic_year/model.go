package academic_year

import (
	"time"

	"github.com/google/uuid"
)

type AcademicYear struct {
	ID        uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	YearName  string    `gorm:"type:varchar(20);not null" json:"year_name"`
	Semester  string    `gorm:"type:varchar(10);not null" json:"semester"` // Ganjil / Genap
	IsActive  bool      `gorm:"type:boolean;default:false;index:idx_single_active_year,unique,where:is_active = true" json:"is_active"`
	CreatedAt time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
}

func (AcademicYear) TableName() string {
	return "master_academic_year"
}
