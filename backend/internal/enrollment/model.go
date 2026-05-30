package enrollment

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/student"
	"time"

	"github.com/google/uuid"
)

type Enrollment struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ClassroomID    uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_enrollment" json:"classroom_id"`
	StudentID      uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_enrollment" json:"student_id"`
	EnrollmentDate time.Time `gorm:"type:date;default:CURRENT_DATE" json:"enrollment_date"`

	common.Auditable

	// Relasi
	Student *student.MasterStudent `gorm:"foreignKey:StudentID" json:"student,omitempty"`
}

func (Enrollment) TableName() string { return "trx_enrollment" }
