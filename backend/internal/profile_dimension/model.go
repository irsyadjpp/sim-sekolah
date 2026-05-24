package profile_dimension

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// ProfileDimension represents a dimension of the graduation profile according to Deep Learning framework.
// The 8 dimensions are: Keimanan dan Ketakwaan, Kewargaan, Penalaran Kritis, Kreativitas, Kolaborasi, Kemandirian, Kesehatan, Komunikasi
type ProfileDimension struct {
	ID            uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DimensionCode string    `gorm:"column:dimension_code;uniqueIndex;not null"      json:"dimension_code"`
	DimensionName string    `gorm:"column:dimension_name;not null"                  json:"dimension_name"`
	Description   string    `gorm:"column:description"                              json:"description"`
	IsActive      bool      `gorm:"column:is_active;default:true"                 json:"is_active"`

	common.Auditable
}

func (ProfileDimension) TableName() string {
	return "master_profile_dimension"
}

// Valid dimension codes according to Deep Learning framework
const (
	DimensionCodeKeimanan    = "DIM_KEIMANAN"
	DimensionCodeKewargaan   = "DIM_KEWARGAAN"
	DimensionCodePenalaran   = "DIM_PENALARAN"
	DimensionCodeKreativitas = "DIM_KREATIVITAS"
	DimensionCodeKolaborasi  = "DIM_KOLABORASI"
	DimensionCodeKemandirian = "DIM_KEMANDIRIAN"
	DimensionCodeKesehatan   = "DIM_KESEHATAN"
	DimensionCodeKomunikasi  = "DIM_KOMUNIKASI"
)

// GetStandardDimensions returns the 8 standard profile dimensions according to Deep Learning framework
func GetStandardDimensions() []ProfileDimension {
	return []ProfileDimension{
		{
			DimensionCode: DimensionCodeKeimanan,
			DimensionName: "Keimanan dan Ketakwaan terhadap Tuhan YME",
			Description:   "Individu yang memiliki keyakinan teguh akan keberadaan Tuhan YME dan menghayati serta mengamalkan nilai-nilai spiritual dalam kehidupan sehari-hari.",
			IsActive:      true,
		},
		{
			DimensionCode: DimensionCodeKewargaan,
			DimensionName: "Kewargaan",
			Description:   "Individu yang memiliki rasa cinta tanah air serta menghargai keberagaman budaya, mentaati aturan dan norma sosial dalam kehidupan bermasyarakat, memiliki kepedulian dan tanggung jawab sosial, serta berkomitmen untuk menyelesaikan masalah nyata yang berkaitan dengan keberlanjutan kehidupan, lingkungan, dan harmoni antarbangsa dalam konteks kebhinekaan global.",
			IsActive:      true,
		},
		{
			DimensionCode: DimensionCodePenalaran,
			DimensionName: "Penalaran Kritis",
			Description:   "Individu yang mampu berpikir secara logis, analitis, dan reflektif dalam memahami, mengevaluasi, serta memproses informasi untuk menyelesaikan masalah.",
			IsActive:      true,
		},
		{
			DimensionCode: DimensionCodeKreativitas,
			DimensionName: "Kreativitas",
			Description:   "Individu yang mampu berpikir secara inovatif, fleksibel, dan orisinal dalam mengolah ide atau informasi untuk menciptakan solusi yang unik dan bermanfaat.",
			IsActive:      true,
		},
		{
			DimensionCode: DimensionCodeKolaborasi,
			DimensionName: "Kolaborasi",
			Description:   "Individu yang mampu bekerja sama secara efektif dengan orang lain secara gotong royong untuk mencapai tujuan bersama melalui pembagian peran dan tanggung jawab.",
			IsActive:      true,
		},
		{
			DimensionCode: DimensionCodeKemandirian,
			DimensionName: "Kemandirian",
			Description:   "Individu yang mampu bertanggung jawab atas proses dan hasil belajarnya sendiri dengan menunjukkan kemampuan untuk mengambil inisiatif, mengatasi hambatan, dan menyelesaikan tugas secara tepat tanpa bergantung pada orang lain.",
			IsActive:      true,
		},
		{
			DimensionCode: DimensionCodeKesehatan,
			DimensionName: "Kesehatan",
			Description:   "Individu yang memiliki fisik yang prima, bugar, sehat, dan mampu menjaga keseimbangan kesehatan mental dan fisik untuk mewujudkan kesejahteraan lahir dan batin (well-being).",
			IsActive:      true,
		},
		{
			DimensionCode: DimensionCodeKomunikasi,
			DimensionName: "Komunikasi",
			Description:   "Individu yang memiliki kemampuan komunikasi intrapribadi untuk melakukan refleksi dan antarpribadi untuk menyampaikan ide, gagasan, dan informasi baik lisan maupun tulisan serta berinteraksi secara efektif dalam berbagai situasi.",
			IsActive:      true,
		},
	}
}
