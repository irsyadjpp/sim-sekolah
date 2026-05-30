package teaching_assignment

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/subject"
	"sim-sekolah/internal/teacher"

	"github.com/google/uuid"
)

type TeachingAssignment struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ClassroomID uuid.UUID `gorm:"type:uuid;not null;index" json:"classroom_id"`
	TeacherID   uuid.UUID `gorm:"type:uuid;not null;index" json:"teacher_id"`
	SubjectID   uuid.UUID `gorm:"type:uuid;not null;index" json:"subject_id"`

	common.Auditable

	// Relasi
	Teacher *teacher.MasterTeacher `gorm:"foreignKey:TeacherID" json:"teacher,omitempty"`
	Subject *subject.Subject       `gorm:"foreignKey:SubjectID" json:"subject,omitempty"`
}

func (TeachingAssignment) TableName() string { return "trx_teaching_assignment" }
