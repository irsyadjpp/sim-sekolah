package foundational_skills

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// FoundationalSkillStandard represents standards for literacy and numerasi assessment
type FoundationalSkillStandard struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SkillType   string    `gorm:"column:skill_type;not null" json:"skill_type"` // LITERASI, NUMERASI
	SkillCode   string    `gorm:"column:skill_code;uniqueIndex;not null" json:"skill_code"`
	SkillName   string    `gorm:"column:skill_name;not null" json:"skill_name"`
	Description string    `gorm:"column:description;not null" json:"description"`
	PhaseID     uuid.UUID `gorm:"column:phase_id" json:"phase_id"`
	Indicators  string    `gorm:"column:indicators;type:text" json:"indicators"` // JSON array of indicators
	IsActive    bool      `gorm:"column:is_active;default:true" json:"is_active"`

	common.Auditable
}

func (FoundationalSkillStandard) TableName() string {
	return "master_foundational_skill_standard"
}

// FoundationalSkillAssessment represents assessment results for foundational skills
type FoundationalSkillAssessment struct {
	ID              uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID       uuid.UUID `gorm:"column:student_id;not null" json:"student_id"`
	SkillStandardID uuid.UUID `gorm:"column:skill_standard_id;not null" json:"skill_standard_id"`
	AssessmentDate  string    `gorm:"column:assessment_date;type:date;not null" json:"assessment_date"`
	MasteryLevel    string    `gorm:"column:mastery_level;not null" json:"mastery_level"` // BELUM, SEDANG, MENGUASAI
	Score           float64   `gorm:"column:score;type:decimal(5,2)" json:"score"`
	Notes           string    `gorm:"column:notes;type:text" json:"notes"`
	TeacherID       uuid.UUID `gorm:"column:teacher_id" json:"teacher_id"`

	common.Auditable
}

func (FoundationalSkillAssessment) TableName() string {
	return "trx_foundational_skill_assessment"
}

// Skill Types
const (
	SkillTypeLiterasi = "LITERASI"
	SkillTypeNumerasi = "NUMERASI"
)

// Mastery Levels
const (
	MasteryLevelBelum     = "BELUM"
	MasteryLevelSedang    = "SEDANG"
	MasteryLevelMenguasai = "MENGUASAI"
)

// GetStandardFoundationalSkillStandards returns the standard foundational skills for SD
func GetStandardFoundationalSkillStandards() []FoundationalSkillStandard {
	return []FoundationalSkillStandard{
		// Literasi Standards (Fase A focused)
		{
			SkillType:   SkillTypeLiterasi,
			SkillCode:   "LIT-FONEMIK",
			SkillName:   "Kesadaran Fonemik",
			Description: "Kemampuan mengidentifikasi dan memanipulasi suara dalam kata-kata",
			Indicators:  `["Mengidentifikasi suku kata awal", "Mengidentifikasi suku kata akhir", "Menggabungkan suara menjadi kata", "Membunyikan kata sederhana"]`,
			IsActive:    true,
		},
		{
			SkillType:   SkillTypeLiterasi,
			SkillCode:   "LIT-HURUF",
			SkillName:   "Pengenalan Huruf",
			Description: "Kemampuan mengenali dan menulis huruf abjad",
			Indicators:  `["Mengenali huruf abjad", "Menulis huruf dengan benar", "Membedakan huruf besar dan kecil", "Menyusun huruf menjadi kata sederhana"]`,
			IsActive:    true,
		},
		{
			SkillType:   SkillTypeLiterasi,
			SkillCode:   "LIT-KATA",
			SkillName:   "Pengenalan Kata",
			Description: "Kemampuan membaca dan memahami kata sederhana",
			Indicators:  `["Membaca kata sederhana", "Memahami makna kata", "Menggunakan kata dalam kalimat", "Mengidentifikasi kata dalam teks"]`,
			IsActive:    true,
		},
		// Numerasi Standards (Fase A focused)
		{
			SkillType:   SkillTypeNumerasi,
			SkillCode:   "NUM-KONSEP",
			SkillName:   "Konsep Bilangan",
			Description: "Pemahaman dasar tentang bilangan dan kuantitas",
			Indicators:  `["Menghitung objek konkret", "Mengenali simbol angka", "Membandingkan kuantitas", "Menyusun urutan bilangan"]`,
			IsActive:    true,
		},
		{
			SkillType:   SkillTypeNumerasi,
			SkillCode:   "NUM-OPERASI",
			SkillName:   "Operasi Dasar",
			Description: "Kemampuan melakukan operasi matematika dasar",
			Indicators:  `["Penjumlahan sederhana", "Pengurangan sederhana", "Memecahkan masalah dengan operasi dasar", "Menggunakan manipulatif untuk operasi"]`,
			IsActive:    true,
		},
		{
			SkillType:   SkillTypeNumerasi,
			SkillCode:   "NUM-POLA",
			SkillName:   "Pola dan Hubungan",
			Description: "Kemampuan mengenali dan melanjutkan pola",
			Indicators:  `["Mengenali pola berulang", "Melanjutkan pola sederhana", "Membuat pola sendiri", "Memahami hubungan sebab-akibat"]`,
			IsActive:    true,
		},
	}
}

// IsValidSkillType validates skill type
func IsValidSkillType(skillType string) bool {
	validTypes := map[string]bool{
		SkillTypeLiterasi: true,
		SkillTypeNumerasi: true,
	}
	return validTypes[skillType]
}

// IsValidMasteryLevel validates mastery level
func IsValidMasteryLevel(level string) bool {
	validLevels := map[string]bool{
		MasteryLevelBelum:     true,
		MasteryLevelSedang:    true,
		MasteryLevelMenguasai: true,
	}
	return validLevels[level]
}

// GetMasteryLevelDescription returns Indonesian description of mastery level
func GetMasteryLevelDescription(level string) string {
	descriptions := map[string]string{
		MasteryLevelBelum:     "Belum Menguasai",
		MasteryLevelSedang:    "Sedang Berkembang",
		MasteryLevelMenguasai: "Menguasai",
	}
	return descriptions[level]
}
