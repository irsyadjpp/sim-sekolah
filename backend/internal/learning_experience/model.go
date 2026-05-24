package learning_experience

import (
	"time"

	"github.com/google/uuid"

	"sim-sekolah/internal/common"
)

// Learning Experience Phases (3 Tahap)
const (
	ExperienceCodeMemahami     = "MEMAHAMI"    // Understanding
	ExperienceCodeMengaplikasi = "MENAPLIKASI" // Applying
	ExperienceCodeMerefleksi   = "MEREFEKSI"   // Reflecting
)

// GetExperienceDescription returns Indonesian description of experience phase
func GetExperienceDescription(experienceCode string) string {
	descriptions := map[string]string{
		ExperienceCodeMemahami:     "Memahami (Understanding)",
		ExperienceCodeMengaplikasi: "Mengaplikasi (Applying)",
		ExperienceCodeMerefleksi:   "Merefleksi (Reflecting)",
	}
	return descriptions[experienceCode]
}

// IsValidExperienceCode validates experience code
func IsValidExperienceCode(experienceCode string) bool {
	validCodes := map[string]bool{
		ExperienceCodeMemahami:     true,
		ExperienceCodeMengaplikasi: true,
		ExperienceCodeMerefleksi:   true,
	}
	return validCodes[experienceCode]
}

// LearningExperience represents the 3 phases of learning experience
type LearningExperience struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ExperienceCode string    `gorm:"type:varchar(10);uniqueIndex;not null" json:"experience_code"` // MEMAHAMI, MENAPLIKASI, MEREFLEKSI
	ExperienceName string    `gorm:"type:varchar(50);not null" json:"experience_name"`
	Description    string    `gorm:"type:text;not null" json:"description"`
	SequenceOrder  int       `gorm:"type:int;not null" json:"sequence_order"` // 1, 2, 3
	KeyIndicators  string    `gorm:"type:text" json:"key_indicators"`         // JSON array of indicators
	IsActive       bool      `gorm:"type:boolean;default:true" json:"is_active"`

	common.Auditable
}

func (LearningExperience) TableName() string {
	return "master_learning_experience"
}

// ActivityExperienceMapping links teaching module activities to experience phases
type ActivityExperienceMapping struct {
	ActivityID   uuid.UUID `gorm:"type:uuid;primaryKey" json:"activity_id"`
	ExperienceID uuid.UUID `gorm:"type:uuid;primaryKey" json:"experience_id"`
	CreatedAt    time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"created_at"`
}

func (ActivityExperienceMapping) TableName() string {
	return "trx_activity_experience_mapping"
}

// StudentExperienceProgression tracks student progression through experience phases
type StudentExperienceProgression struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID      uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	SubjectID      uuid.UUID `gorm:"type:uuid;not null;index" json:"subject_id"`
	ExperienceID   uuid.UUID `gorm:"type:uuid;not null;index" json:"experience_id"`
	MasteryLevel   float64   `gorm:"type:numeric(3,2);default:0" json:"mastery_level"` // 0.00 to 1.00
	LastAssessedAt time.Time `gorm:"type:timestamptz" json:"last_assessed_at"`
	Notes          string    `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (StudentExperienceProgression) TableName() string {
	return "trx_student_experience_progression"
}
