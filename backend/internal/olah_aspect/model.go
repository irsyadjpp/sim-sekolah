package olah_aspect

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// OlahAspect represents the 4 learning aspects from Deep Learning framework:
// Olah Pikir (Mind/Cognitive), Olah Hati (Heart/Spiritual),
// Olah Rasa (Feeling/Aesthetic), Olah Raga (Body/Physical)
type OlahAspect struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	AspectCode string    `gorm:"column:aspect_code;uniqueIndex;not null" json:"aspect_code"`
	AspectName string    `gorm:"column:aspect_name;not null" json:"aspect_name"`
	Definition string    `gorm:"column:definition;not null" json:"definition"`
	Indicators string    `gorm:"column:indicators;type:text" json:"indicators"` // JSON array of indicators
	IsActive   bool      `gorm:"column:is_active;default:true" json:"is_active"`

	common.Auditable
}

func (OlahAspect) TableName() string {
	return "master_olah_aspect"
}

// Valid aspect codes according to Deep Learning framework
const (
	AspectCodeOlahPikir = "OLAH_PIKIR"
	AspectCodeOlahHati  = "OLAH_HATI"
	AspectCodeOlahRasa  = "OLAH_RASA"
	AspectCodeOlahRaga  = "OLAH_RAGA"
)

// GetStandardAspects returns the 4 standard olah aspects according to Deep Learning framework
func GetStandardAspects() []OlahAspect {
	return []OlahAspect{
		{
			AspectCode: AspectCodeOlahPikir,
			AspectName: "Olah Pikir",
			Definition: "Merupakan proses pendidikan yang berfokus pada pengasahan akal budi dan kemampuan kognitif, seperti kemampuan untuk memahami, menganalisa, dan memecahkan masalah",
			Indicators: `["Kemampuan memahami konsep", "Kemampuan menganalisis informasi", "Kemampuan memecahkan masalah", "Kemampuan berpikir logis", "Kemampuan berpikir kritis"]`,
			IsActive:   true,
		},
		{
			AspectCode: AspectCodeOlahHati,
			AspectName: "Olah Hati",
			Definition: "Adalah proses pendidikan untuk mengasah kepekaan batin, membentuk budi pekerti, serta menanamkan nilai-nilai moral dan spiritual",
			Indicators: `["Kepekaan batin", "Budi pekerti luhur", "Nilai moral dan spiritual", "Karakter religius", "Empati moral"]`,
			IsActive:   true,
		},
		{
			AspectCode: AspectCodeOlahRasa,
			AspectName: "Olah Rasa",
			Definition: "Sebagai proses pendidikan yang bertujuan untuk mengembangkan kepekaan estetika, empati, dan kemampuan menghargai keindahan serta hubungan antarmanusia",
			Indicators: `["Kepekaan estetika", "Empati terhadap orang lain", "Penghargaan keindahan", "Hubungan antarmanusia positif", "Ekspresi artistik"]`,
			IsActive:   true,
		},
		{
			AspectCode: AspectCodeOlahRaga,
			AspectName: "Olah Raga",
			Definition: "Merupakan bagian dari pendidikan yang bertujuan untuk menjaga dan meningkatkan kesehatan fisik, kekuatan tubuh, serta membentuk karakter melalui kegiatan jasmani",
			Indicators: `["Kesehatan fisik", "Kekuatan tubuh", "Karakter melalui kegiatan jasmani", "Koordinasi motorik", "Kebugaran jasmani"]`,
			IsActive:   true,
		},
	}
}
