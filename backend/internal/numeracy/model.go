package numeracy

import (
	"time"

	"sim-sekolah/internal/common"
	"sim-sekolah/internal/phase"
	"sim-sekolah/internal/student"

	"github.com/google/uuid"
)

// Numeracy Indicator Types
const (
	NumeracyTypeNumbers      = "NUMBERS"       // Bilangan
	NumeracyTypeOperations   = "OPERATIONS"    // Operasi Hitung
	NumeracyTypeGeometry     = "GEOMETRY"      // Geometri
	NumeracyTypeMeasurement  = "MEASUREMENT"   // Pengukuran
	NumeracyTypeDataAnalysis = "DATA_ANALYSIS" // Analisis Data
)

// NumeracyIndicator represents numeracy learning indicators per phase
type NumeracyIndicator struct {
	ID            uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PhaseID       uuid.UUID `gorm:"type:uuid;not null;index" json:"phase_id"`
	NumeracyType  string    `gorm:"type:varchar(20);not null" json:"numeracy_type"`
	IndicatorCode string    `gorm:"type:varchar(20);unique;not null" json:"indicator_code"`
	IndicatorName string    `gorm:"type:varchar(100);not null" json:"indicator_name"`
	Description   string    `gorm:"type:text;not null" json:"description"`
	GradeLevel    string    `gorm:"type:varchar(10)" json:"grade_level"` // Kelas 1-6
	MinAge        int       `gorm:"type:int" json:"min_age"`
	MaxAge        int       `gorm:"type:int" json:"max_age"`
	Difficulty    string    `gorm:"type:varchar(10)" json:"difficulty"` // LOW, MEDIUM, HIGH
	Examples      string    `gorm:"type:text" json:"examples"`          // JSON array of examples
	IsActive      bool      `gorm:"default:true" json:"is_active"`

	common.Auditable

	Phase *phase.Phase `gorm:"foreignKey:PhaseID" json:"phase,omitempty"`
}

func (NumeracyIndicator) TableName() string {
	return "numeracy_indicators"
}

// NumeracyAssessment represents numeracy assessment for students
type NumeracyAssessment struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID      uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	IndicatorID    uuid.UUID `gorm:"type:uuid;not null;index" json:"indicator_id"`
	AssessmentDate time.Time `gorm:"type:date;not null" json:"assessment_date"`
	AssessmentType string    `gorm:"type:varchar(20);not null" json:"assessment_type"` // DIAGNOSTIC, FORMATIVE, SUMMATIVE
	Score          float64   `gorm:"type:numeric(5,2)" json:"score"`
	MasteryLevel   string    `gorm:"type:varchar(20);not null" json:"mastery_level"` // BELUM, SEDANG, MENGUASAI
	ResponseTime   int       `gorm:"type:int" json:"response_time"`                  // in seconds
	Attempts       int       `gorm:"type:int;default:1" json:"attempts"`
	TeacherID      uuid.UUID `gorm:"type:uuid" json:"teacher_id"`
	Notes          string    `gorm:"type:text" json:"notes"`
	EvidenceFiles  string    `gorm:"type:text" json:"evidence_files"` // JSON array of file paths

	common.Auditable

	Student   *student.Student   `gorm:"foreignKey:StudentID" json:"student,omitempty"`
	Indicator *NumeracyIndicator `gorm:"foreignKey:IndicatorID" json:"indicator,omitempty"`
}

func (NumeracyAssessment) TableName() string {
	return "numeracy_assessments"
}

// NumeracyGrowth tracks student numeracy growth over time
type NumeracyGrowth struct {
	ID                uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID         uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_numeracy_growth_student_period" json:"student_id"`
	Period            string    `gorm:"type:varchar(20);not null;uniqueIndex:idx_numeracy_growth_student_period" json:"period"` // SEMESTER_1, SEMESTER_2
	AcademicYearID    uuid.UUID `gorm:"type:uuid;not null;index" json:"academic_year_id"`
	OverallScore      float64   `gorm:"type:numeric(5,2)" json:"overall_score"`
	NumbersScore      float64   `gorm:"type:numeric(5,2)" json:"numbers_score"`
	OperationsScore   float64   `gorm:"type:numeric(5,2)" json:"operations_score"`
	GeometryScore     float64   `gorm:"type:numeric(5,2)" json:"geometry_score"`
	MeasurementScore  float64   `gorm:"type:numeric(5,2)" json:"measurement_score"`
	DataAnalysisScore float64   `gorm:"type:numeric(5,2)" json:"data_analysis_score"`
	MasteryRate       float64   `gorm:"type:numeric(5,2)" json:"mastery_rate"` // Percentage of indicators mastered
	GrowthRate        float64   `gorm:"type:numeric(5,2)" json:"growth_rate"`  // Growth from previous period
	Percentile        int       `gorm:"type:int" json:"percentile"`            // National percentile
	TeacherID         uuid.UUID `gorm:"type:uuid" json:"teacher_id"`
	Notes             string    `gorm:"type:text" json:"notes"`

	common.Auditable

	Student *student.Student `gorm:"foreignKey:StudentID" json:"student,omitempty"`
}

func (NumeracyGrowth) TableName() string {
	return "numeracy_growth"
}

// NumeracyIntervention represents remedial/enrichment activities for numeracy
type NumeracyIntervention struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID        uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	IndicatorID      uuid.UUID `gorm:"type:uuid;not null;index" json:"indicator_id"`
	InterventionType string    `gorm:"type:varchar(20);not null" json:"intervention_type"` // REMEDIAL, ENRICHMENT
	StartDate        time.Time `gorm:"type:date;not null" json:"start_date"`
	EndDate          time.Time `gorm:"type:date" json:"end_date"`
	Status           string    `gorm:"type:varchar(20);not null" json:"status"` // PLANNED, ONGOING, COMPLETED
	Activities       string    `gorm:"type:text" json:"activities"`             // JSON array of activities
	TeacherID        uuid.UUID `gorm:"type:uuid" json:"teacher_id"`
	Outcome          string    `gorm:"type:text" json:"outcome"`
	Effectiveness    string    `gorm:"type:varchar(10)" json:"effectiveness"` // LOW, MEDIUM, HIGH

	common.Auditable

	Student   *student.Student   `gorm:"foreignKey:StudentID" json:"student,omitempty"`
	Indicator *NumeracyIndicator `gorm:"foreignKey:IndicatorID" json:"indicator,omitempty"`
}

func (NumeracyIntervention) TableName() string {
	return "numeracy_interventions"
}

// GetNumeracyTypeDescription returns Indonesian description of numeracy type
func GetNumeracyTypeDescription(numeracyType string) string {
	descriptions := map[string]string{
		NumeracyTypeNumbers:      "Bilangan",
		NumeracyTypeOperations:   "Operasi Hitung",
		NumeracyTypeGeometry:     "Geometri",
		NumeracyTypeMeasurement:  "Pengukuran",
		NumeracyTypeDataAnalysis: "Analisis Data",
	}
	return descriptions[numeracyType]
}

// GetMasteryLevelDescription returns Indonesian description of mastery level
func GetMasteryLevelDescription(masteryLevel string) string {
	descriptions := map[string]string{
		"BELUM":     "Belum Menguasai",
		"SEDANG":    "Sedang Mengembangkan",
		"MENGUASAI": "Menguasai",
	}
	return descriptions[masteryLevel]
}

// IsValidNumeracyType validates numeracy type
func IsValidNumeracyType(numeracyType string) bool {
	validTypes := map[string]bool{
		NumeracyTypeNumbers:      true,
		NumeracyTypeOperations:   true,
		NumeracyTypeGeometry:     true,
		NumeracyTypeMeasurement:  true,
		NumeracyTypeDataAnalysis: true,
	}
	return validTypes[numeracyType]
}

// IsValidMasteryLevel validates mastery level
func IsValidMasteryLevel(masteryLevel string) bool {
	validLevels := map[string]bool{
		"BELUM":     true,
		"SEDANG":    true,
		"MENGUASAI": true,
	}
	return validLevels[masteryLevel]
}
