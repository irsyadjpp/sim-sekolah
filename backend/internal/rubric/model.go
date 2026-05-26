package rubric

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/subject"

	"github.com/google/uuid"
)

// Rubric represents a comprehensive assessment rubric template
type Rubric struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Title          string     `gorm:"type:varchar(200);not null" json:"title"`
	Description    string     `gorm:"type:text" json:"description"`
	SubjectID      *uuid.UUID `gorm:"type:uuid;index" json:"subject_id"`
	AssessmentType string     `gorm:"type:varchar(50);not null;index" json:"assessment_type"` // PROJECT, PRESENTATION, WRITTEN_WORK, PRACTICAL, BEHAVIORAL
	GradeLevel     string     `gorm:"type:varchar(50);index" json:"grade_level"`              // 1-6 for SD, or specific grade levels
	MaxScore       float64    `gorm:"type:decimal(5,2);default:100" json:"max_score"`
	IsTemplate     bool       `gorm:"default:true" json:"is_template"` // Can be used as template for other rubrics
	IsActive       bool       `gorm:"default:true" json:"is_active"`

	common.Auditable

	Subject  *subject.Subject `gorm:"foreignKey:SubjectID" json:"subject,omitempty"`
	Criteria []RubricCriteria `gorm:"foreignKey:RubricID" json:"criteria,omitempty"`
	Levels   []RubricLevel    `gorm:"foreignKey:RubricID" json:"levels,omitempty"`
}

func (Rubric) TableName() string {
	return "master_rubric"
}

// RubricCriteria represents individual assessment criteria within a rubric
type RubricCriteria struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	RubricID    uuid.UUID `gorm:"type:uuid;not null;index" json:"rubric_id"`
	Title       string    `gorm:"type:varchar(200);not null" json:"title"`
	Description string    `gorm:"type:text" json:"description"`
	Weight      float64   `gorm:"type:decimal(5,2);default:1.0" json:"weight"` // Weight for this criteria in total score
	Sequence    int       `gorm:"type:integer;default:1" json:"sequence"`      // Order in rubric
	IsRequired  bool      `gorm:"default:true" json:"is_required"`

	common.Auditable

	Rubric *Rubric               `gorm:"foreignKey:RubricID" json:"rubric,omitempty"`
	Levels []RubricCriteriaLevel `gorm:"foreignKey:CriteriaID" json:"levels,omitempty"`
}

func (RubricCriteria) TableName() string {
	return "master_rubric_criteria"
}

// RubricLevel represents scoring levels (e.g., 1-4, or MB-SB-BSH-SAB)
type RubricLevel struct {
	ID            uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	RubricID      uuid.UUID `gorm:"type:uuid;not null;index" json:"rubric_id"`
	LevelCode     string    `gorm:"type:varchar(20);not null" json:"level_code"`         // 1, 2, 3, 4 or MB, SB, BSH, SAB
	LevelName     string    `gorm:"type:varchar(100);not null" json:"level_name"`        // "Mulai Berkembang", "Sedang Berkembang", etc.
	PointValue    float64   `gorm:"type:decimal(5,2);not null" json:"point_value"`       // Numeric value for this level
	MinPercentage float64   `gorm:"type:decimal(5,2);default:0" json:"min_percentage"`   // Minimum percentage for this level
	MaxPercentage float64   `gorm:"type:decimal(5,2);default:100" json:"max_percentage"` // Maximum percentage for this level
	Sequence      int       `gorm:"type:integer;default:1" json:"sequence"`
	Color         string    `gorm:"type:varchar(20)" json:"color"` // Optional color coding (e.g., #FF0000 for low levels)

	common.Auditable

	Rubric *Rubric `gorm:"foreignKey:RubricID" json:"rubric,omitempty"`
}

func (RubricLevel) TableName() string {
	return "master_rubric_level"
}

// RubricCriteriaLevel represents specific descriptions for each criteria at each level
type RubricCriteriaLevel struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	CriteriaID  uuid.UUID `gorm:"type:uuid;not null;index" json:"criteria_id"`
	LevelID     uuid.UUID `gorm:"type:uuid;not null;index" json:"level_id"`
	Description string    `gorm:"type:text;not null" json:"description"` // What this criteria looks like at this level
	Examples    string    `gorm:"type:text" json:"examples"`             // Optional examples for this criteria at this level

	common.Auditable

	Criteria *RubricCriteria `gorm:"foreignKey:CriteriaID" json:"criteria,omitempty"`
	Level    *RubricLevel    `gorm:"foreignKey:LevelID" json:"level,omitempty"`
}

func (RubricCriteriaLevel) TableName() string {
	return "master_rubric_criteria_level"
}

// Assessment type constants
const (
	AssessmentTypeProject      = "PROJECT"
	AssessmentTypePresentation = "PRESENTATION"
	AssessmentTypeWrittenWork  = "WRITTEN_WORK"
	AssessmentTypePractical    = "PRACTICAL"
	AssessmentTypeBehavioral   = "BEHAVIORAL"
	AssessmentTypeOral         = "ORAL"
	AssessmentTypeObservation  = "OBSERVATION"
)

// Grade level constants for SD
const (
	GradeLevel1 = "1"
	GradeLevel2 = "2"
	GradeLevel3 = "3"
	GradeLevel4 = "4"
	GradeLevel5 = "5"
	GradeLevel6 = "6"
	GradeLower  = "LOWER" // 1-3
	GradeUpper  = "UPPER" // 4-6
	GradeAll    = "ALL"   // All grades
)

// Common rubric level codes for Indonesian education
const (
	LevelCodeMB  = "MB"  // Mulai Berkembang
	LevelCodeSB  = "SB"  // Sedang Berkembang
	LevelCodeBSH = "BSH" // Berkembang Sesuai Harapan
	LevelCodeSAB = "SAB" // Sangat Berkembang

	LevelCode1 = "1"
	LevelCode2 = "2"
	LevelCode3 = "3"
	LevelCode4 = "4"
)

// GetAssessmentTypeDescription returns Indonesian description for assessment type
func GetAssessmentTypeDescription(assessmentType string) string {
	descriptions := map[string]string{
		AssessmentTypeProject:      "Proyek",
		AssessmentTypePresentation: "Presentasi",
		AssessmentTypeWrittenWork:  "Karya Tulis",
		AssessmentTypePractical:    "Praktik",
		AssessmentTypeBehavioral:   "Perilaku",
		AssessmentTypeOral:         "Lisan",
		AssessmentTypeObservation:  "Observasi",
	}
	if desc, exists := descriptions[assessmentType]; exists {
		return desc
	}
	return assessmentType
}

// GetLevelCodeDescription returns Indonesian description for level code
func GetLevelCodeDescription(levelCode string) string {
	descriptions := map[string]string{
		LevelCodeMB:  "Mulai Berkembang",
		LevelCodeSB:  "Sedang Berkembang",
		LevelCodeBSH: "Berkembang Sesuai Harapan",
		LevelCodeSAB: "Sangat Berkembang",
	}
	if desc, exists := descriptions[levelCode]; exists {
		return desc
	}
	return levelCode
}
