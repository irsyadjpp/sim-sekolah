package classroom

import (
	"time"

	"sim-sekolah/internal/academic_year"
	"sim-sekolah/internal/grade"
	"sim-sekolah/internal/school"
	"sim-sekolah/internal/student"
	"sim-sekolah/internal/teacher"

	"github.com/google/uuid"
)

type Classroom struct {
	ID                   uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID             uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	AcademicYearID       uuid.UUID  `gorm:"type:uuid;not null;uniqueIndex:idx_active_homeroom" json:"academic_year_id"`
	GradeID              uuid.UUID  `gorm:"type:uuid;not null;index" json:"grade_id"`
	PhaseID              uuid.UUID  `gorm:"type:uuid;not null;index" json:"phase_id"`
	ClassroomName        string     `gorm:"type:varchar(50);not null" json:"classroom_name"`
	HomeroomTeacherID    *uuid.UUID `gorm:"type:uuid;uniqueIndex:idx_active_homeroom" json:"homeroom_teacher_id"`
	MaxQuota             int        `gorm:"type:smallint;default:28" json:"max_quota"`
	ClassCharacteristics string     `gorm:"type:text" json:"class_characteristics"` // Narasi kebutuhan belajar
	CreatedAt            time.Time  `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`

	// Relasi
	School       *school.School              `gorm:"foreignKey:SchoolID" json:"school,omitempty"`
	AcademicYear *academic_year.AcademicYear `gorm:"foreignKey:AcademicYearID" json:"academic_year,omitempty"`
	Grade        *grade.Grade                `gorm:"foreignKey:GradeID" json:"grade,omitempty"`
	Homeroom     *teacher.Teacher            `gorm:"foreignKey:HomeroomTeacherID" json:"homeroom_teacher,omitempty"`
	Students     []student.Student           `gorm:"many2many:trx_enrollment;" json:"students,omitempty"`
}

func (Classroom) TableName() string { return "master_classroom" }
