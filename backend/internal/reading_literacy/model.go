package reading_literacy

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// ReadingLevel represents standard reading levels for SD students
type ReadingLevel struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	LevelCode   string    `gorm:"column:level_code;uniqueIndex;not null" json:"level_code"` // LEVEL_0 to LEVEL_6
	LevelName   string    `gorm:"column:level_name;not null" json:"level_name"`
	Description string    `gorm:"column:description;not null" json:"description"`
	PhaseID     uuid.UUID `gorm:"column:phase_id" json:"phase_id"`
	Indicators  string    `gorm:"column:indicators;type:text" json:"indicators"` // JSON array of indicators
	WPMRange    string    `gorm:"column:wpm_range;type:text" json:"wpm_range"`   // Words per minute range
	IsActive    bool      `gorm:"column:is_active;default:true" json:"is_active"`

	common.Auditable
}

func (ReadingLevel) TableName() string {
	return "master_reading_level"
}

// ReadingLiteracyAssessment represents assessment results for reading literacy
type ReadingLiteracyAssessment struct {
	ID                 uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID          uuid.UUID `gorm:"column:student_id;not null" json:"student_id"`
	ReadingLevelID     uuid.UUID `gorm:"column:reading_level_id;not null" json:"reading_level_id"`
	AssessmentDate     string    `gorm:"column:assessment_date;type:date;not null" json:"assessment_date"`
	WordsPerMinute     int       `gorm:"column:words_per_minute" json:"words_per_minute"`
	ComprehensionScore float64   `gorm:"column:comprehension_score;type:decimal(5,2)" json:"comprehension_score"`
	FluencyRating      string    `gorm:"column:fluency_rating" json:"fluency_rating"` // RENDAH, SEDANG, TINGGI
	AccuracyScore      float64   `gorm:"column:accuracy_score;type:decimal(5,2)" json:"accuracy_score"`
	Notes              string    `gorm:"column:notes;type:text" json:"notes"`
	TeacherID          uuid.UUID `gorm:"column:teacher_id" json:"teacher_id"`

	common.Auditable
}

func (ReadingLiteracyAssessment) TableName() string {
	return "trx_reading_literacy_assessment"
}

// Reading Level Codes
const (
	ReadingLevel0 = "LEVEL_0" // Pre-reading
	ReadingLevel1 = "LEVEL_1" // Emergent reader
	ReadingLevel2 = "LEVEL_2" // Beginning reader
	ReadingLevel3 = "LEVEL_3" // Developing reader
	ReadingLevel4 = "LEVEL_4" // Fluent reader
	ReadingLevel5 = "LEVEL_5" // Proficient reader
	ReadingLevel6 = "LEVEL_6" // Advanced reader
)

// Fluency Ratings
const (
	FluencyRendah = "RENDAH"
	FluencySedang = "SEDANG"
	FluencyTinggi = "TINGGI"
)

// GetStandardReadingLevels returns standard reading levels for SD
func GetStandardReadingLevels() []ReadingLevel {
	return []ReadingLevel{
		{
			LevelCode:   ReadingLevel0,
			LevelName:   "Pra-Membaca",
			Description: "Anak belum dapat membaca, hanya mengenali gambar dan simbol sederhana",
			Indicators:  `["Mengenali gambar", "Menunjuk objek dalam gambar", "Memahami cerita yang dibacakan", "Mengenal huruf pertama nama"]`,
			WPMRange:    "0-10",
			IsActive:    true,
		},
		{
			LevelCode:   ReadingLevel1,
			LevelName:   "Pembaca Awal",
			Description: "Anak mulai mengenali huruf dan suku kata sederhana",
			Indicators:  `["Mengenali semua huruf", "Membunyikan suku kata", "Membaca kata sederhana", "Memahami makna kata sederhana"]`,
			WPMRange:    "10-30",
			IsActive:    true,
		},
		{
			LevelCode:   ReadingLevel2,
			LevelName:   "Pembaca Pemula",
			Description: "Anak dapat membaca kalimat sederhana dengan bantuan",
			Indicators:  `["Membaca kalimat sederhana", "Memahami kalimat dibaca", "Mengenal kata bervariasi", "Membaca dengan pengucapan yang cukup jelas"]`,
			WPMRange:    "30-50",
			IsActive:    true,
		},
		{
			LevelCode:   ReadingLevel3,
			LevelName:   "Pembaca Berkembang",
			Description: "Anak dapat membaca teks pendek dengan pemahaman dasar",
			Indicators:  `["Membaca teks pendek", "Memahami ide pokok", "Mengingat detail penting", "Membaca dengan ekspresi sederhana"]`,
			WPMRange:    "50-70",
			IsActive:    true,
		},
		{
			LevelCode:   ReadingLevel4,
			LevelName:   "Pembaca Lancar",
			Description: "Anak dapat membaca dengan lancar dan pemahaman yang baik",
			Indicators:  `["Membaca lancar", "Memahami teks panjang", "Meninferensi makna", "Membaca dengan intonasi yang baik"]`,
			WPMRange:    "70-90",
			IsActive:    true,
		},
		{
			LevelCode:   ReadingLevel5,
			LevelName:   "Pembaca Mahir",
			Description: "Anak dapat membaca berbagai jenis teks dengan pemahaman mendalam",
			Indicators:  `["Membaca berbagai jenis teks", "Menganalisis struktur teks", "Mengkritisi isi teks", "Membaca dengan kecepatan tinggi"]`,
			WPMRange:    "90-110",
			IsActive:    true,
		},
		{
			LevelCode:   ReadingLevel6,
			LevelName:   "Pembaca Lanjut",
			Description: "Anak memiliki kemampuan membaca tingkat lanjut dengan pemahaman kompleks",
			Indicators:  `["Membaca teks kompleks", "Menganalisis implicit meaning", "Menghubungkan teks dengan konteks", "Kecepatan membaca sangat tinggi"]`,
			WPMRange:    "110+",
			IsActive:    true,
		},
	}
}

// IsValidReadingLevel validates reading level code
func IsValidReadingLevel(levelCode string) bool {
	validLevels := map[string]bool{
		ReadingLevel0: true,
		ReadingLevel1: true,
		ReadingLevel2: true,
		ReadingLevel3: true,
		ReadingLevel4: true,
		ReadingLevel5: true,
		ReadingLevel6: true,
	}
	return validLevels[levelCode]
}

// IsValidFluencyRating validates fluency rating
func IsValidFluencyRating(rating string) bool {
	validRatings := map[string]bool{
		FluencyRendah: true,
		FluencySedang: true,
		FluencyTinggi: true,
	}
	return validRatings[rating]
}

// GetReadingLevelDescription returns Indonesian description of reading level
func GetReadingLevelDescription(levelCode string) string {
	descriptions := map[string]string{
		ReadingLevel0: "Pra-Membaca (belum dapat membaca)",
		ReadingLevel1: "Pembaca Awal (mulai mengenali huruf)",
		ReadingLevel2: "Pembaca Pemula (membaca kalimat sederhana)",
		ReadingLevel3: "Pembaca Berkembang (membaca teks pendek)",
		ReadingLevel4: "Pembaca Lancar (membaca lancar)",
		ReadingLevel5: "Pembaca Mahir (membaca berbagai teks)",
		ReadingLevel6: "Pembaca Lanjut (kemampuan kompleks)",
	}
	return descriptions[levelCode]
}

// GetFluencyDescription returns Indonesian description of fluency rating
func GetFluencyDescription(rating string) string {
	descriptions := map[string]string{
		FluencyRendah: "Kelancaran Rendah",
		FluencySedang: "Kelancaran Sedang",
		FluencyTinggi: "Kelancaran Tinggi",
	}
	return descriptions[rating]
}
