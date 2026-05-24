package elemen_desain

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// DesignElement represents a Deep Learning Design Element.
// Each element belongs to one of the 4 framework categories:
// Praktik Pedagogis, Kemitraan Pembelajaran, Lingkungan Pembelajaran, Pemanfaatan Digital
type DesignElement struct {
	ID                   uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Name                 string    `gorm:"column:design_element_name;uniqueIndex;not null"  json:"design_element_name"`
	Description          string    `gorm:"column:description"                              json:"description"`
	FrameworkElementType string    `gorm:"column:framework_element_type"                json:"framework_element_type"` // PRAKTIK_PEDAGOGIS, KEMITRAAN_PEMBELAJARAN, LINGKUNGAN_PEMBELAJARAN, PEMANFAATAN_DIGITAL
	IsActive             bool      `gorm:"column:is_active;default:true"                  json:"is_active"`

	common.Auditable
}

func (DesignElement) TableName() string {
	return "dl_design_element"
}

// Framework Element Types according to Deep Learning 4 Elements of Learning Design
const (
	FrameworkElementPraktikPedagogis       = "PRAKTIK_PEDAGOGIS"
	FrameworkElementKemitraanPembelajaran  = "KEMITRAAN_PEMBELAJARAN"
	FrameworkElementLingkunganPembelajaran = "LINGKUNGAN_PEMBELAJARAN"
	FrameworkElementPemanfaatanDigital     = "PEMANFAATAN_DIGITAL"
)

// GetStandardFrameworkElements returns the 4 standard framework categories and their elements
// according to Deep Learning framework
func GetStandardFrameworkElements() []DesignElement {
	return []DesignElement{
		// Praktik Pedagogis (Pedagogical Practices)
		{
			Name:                 "Differentiated Instruction",
			Description:          "Pendekatan pembelajaran yang disesuaikan dengan kebutuhan, kemampuan, dan minat peserta didik",
			FrameworkElementType: FrameworkElementPraktikPedagogis,
			IsActive:             true,
		},
		{
			Name:                 "Formative Assessment",
			Description:          "Penilaian yang dilakukan secara berkelanjutan selama proses pembelajaran untuk memberikan umpan balik",
			FrameworkElementType: FrameworkElementPraktikPedagogis,
			IsActive:             true,
		},
		{
			Name:                 "Scaffolding",
			Description:          "Dukungan sementara yang diberikan kepada peserta didik untuk membantu mereka mencapai tujuan pembelajaran",
			FrameworkElementType: FrameworkElementPraktikPedagogis,
			IsActive:             true,
		},
		{
			Name:                 "Inquiry-Based Learning",
			Description:          "Pembelajaran berbasis penyelidikan di mana peserta didik mengajukan pertanyaan dan mengeksplorasi topik",
			FrameworkElementType: FrameworkElementPraktikPedagogis,
			IsActive:             true,
		},
		// Kemitraan Pembelajaran (Learning Partnerships)
		{
			Name:                 "Kemitraan Guru-Siswa",
			Description:          "Kolaborasi aktif antara guru dan siswa dalam proses pembelajaran",
			FrameworkElementType: FrameworkElementKemitraanPembelajaran,
			IsActive:             true,
		},
		{
			Name:                 "Kemitraan Siswa-Siswa",
			Description:          "Kerja sama dan kolaborasi antar siswa untuk mencapai tujuan bersama",
			FrameworkElementType: FrameworkElementKemitraanPembelajaran,
			IsActive:             true,
		},
		{
			Name:                 "Kemitraan Sekolah-Komunitas",
			Description:          "Keterlibatan komunitas dan orang tua dalam pembelajaran",
			FrameworkElementType: FrameworkElementKemitraanPembelajaran,
			IsActive:             true,
		},
		{
			Name:                 "Kemitraan Sekolah-Expert",
			Description:          "Kerja sama dengan pakar atau expert luar untuk mendukung pembelajaran",
			FrameworkElementType: FrameworkElementKemitraanPembelajaran,
			IsActive:             true,
		},
		// Lingkungan Pembelajaran (Learning Environment)
		{
			Name:                 "Lingkungan Kelas yang Kondusif",
			Description:          "Pengaturan ruang kelas yang mendukung pembelajaran",
			FrameworkElementType: FrameworkElementLingkunganPembelajaran,
			IsActive:             true,
		},
		{
			Name:                 "Lingkungan Sosial yang Positif",
			Description:          "Budaya kelas yang saling menghargai dan mendukung",
			FrameworkElementType: FrameworkElementLingkunganPembelajaran,
			IsActive:             true,
		},
		{
			Name:                 "Lingkungan Fisik yang Aman",
			Description:          "Ruang fisik yang aman, nyaman, dan mendukung pembelajaran",
			FrameworkElementType: FrameworkElementLingkunganPembelajaran,
			IsActive:             true,
		},
		{
			Name:                 "Lingkungan Digital yang Terintegrasi",
			Description:          "Integrasi teknologi dalam lingkungan pembelajaran secara seamless",
			FrameworkElementType: FrameworkElementLingkunganPembelajaran,
			IsActive:             true,
		},
		// Pemanfaatan Digital (Digital Utilization)
		{
			Name:                 "Pemanfaatan Media Digital",
			Description:          "Penggunaan teknologi digital dalam pembelajaran",
			FrameworkElementType: FrameworkElementPemanfaatanDigital,
			IsActive:             true,
		},
		{
			Name:                 "Pemanfaatan Platform Pembelajaran",
			Description:          "Penggunaan LMS dan platform edukasi",
			FrameworkElementType: FrameworkElementPemanfaatanDigital,
			IsActive:             true,
		},
		{
			Name:                 "Digital Collaboration Tools",
			Description:          "Alat kolaborasi digital untuk kerja sama siswa",
			FrameworkElementType: FrameworkElementPemanfaatanDigital,
			IsActive:             true,
		},
		{
			Name:                 "Digital Assessment Tools",
			Description:          "Alat asesmen digital untuk evaluasi pembelajaran",
			FrameworkElementType: FrameworkElementPemanfaatanDigital,
			IsActive:             true,
		},
	}
}

// IsValidFrameworkElementType checks if the given framework element type is valid
func IsValidFrameworkElementType(frameworkType string) bool {
	validTypes := map[string]bool{
		FrameworkElementPraktikPedagogis:       true,
		FrameworkElementKemitraanPembelajaran:  true,
		FrameworkElementLingkunganPembelajaran: true,
		FrameworkElementPemanfaatanDigital:     true,
	}
	return validTypes[frameworkType]
}

// GetFrameworkElementDescription returns the Indonesian description of a framework type
func GetFrameworkElementDescription(frameworkType string) string {
	descriptions := map[string]string{
		FrameworkElementPraktikPedagogis:       "Praktik Pedagogis (Pedagogical Practices)",
		FrameworkElementKemitraanPembelajaran:  "Kemitraan Pembelajaran (Learning Partnerships)",
		FrameworkElementLingkunganPembelajaran: "Lingkungan Pembelajaran (Learning Environment)",
		FrameworkElementPemanfaatanDigital:     "Pemanfaatan Digital (Digital Utilization)",
	}
	return descriptions[frameworkType]
}
