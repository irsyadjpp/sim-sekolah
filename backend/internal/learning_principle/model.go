package learning_principle

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// LearningPrinciple represents the 3 learning principles from Deep Learning framework:
// Berkesadaran (Conscious/Aware), Bermakna (Meaningful), Menggembirakan (Joyful)
type LearningPrinciple struct {
	ID                     uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PrincipleCode          string    `gorm:"column:principle_code;uniqueIndex;not null" json:"principle_code"`
	PrincipleName          string    `gorm:"column:principle_name;not null" json:"principle_name"`
	Description            string    `gorm:"column:description;not null" json:"description"`
	KeyCharacteristics     string    `gorm:"column:key_characteristics;type:text" json:"key_characteristics"`         // JSON array
	ImplementationExamples string    `gorm:"column:implementation_examples;type:text" json:"implementation_examples"` // JSON array
	IsActive               bool      `gorm:"column:is_active;default:true" json:"is_active"`

	common.Auditable
}

func (LearningPrinciple) TableName() string {
	return "master_learning_principle"
}

// Valid principle codes according to Deep Learning framework
const (
	PrincipleCodeBerkesadaran   = "BERKESADARAN"
	PrincipleCodeBermakna       = "BERMAKNA"
	PrincipleCodeMenggembirakan = "MENGENGIRAKAN"
)

// GetStandardPrinciples returns the 3 standard learning principles according to Deep Learning framework
func GetStandardPrinciples() []LearningPrinciple {
	return []LearningPrinciple{
		{
			PrincipleCode:          PrincipleCodeBerkesadaran,
			PrincipleName:          "Berkesadaran",
			Description:            "Pengalaman belajar peserta didik yang diperoleh ketika mereka memiliki kesadaran untuk menjadi pembelajar yang aktif dan mampu meregulasi diri. Peserta didik memahami tujuan pembelajaran, termotivasi secara intrinsik untuk belajar, serta aktif mengembangkan strategi belajar untuk mencapai tujuan.",
			KeyCharacteristics:     `["Kenyamanan peserta didik dalam belajar", "Fokus, konsentrasi, dan perhatian", "Kesadaran terhadap proses berpikir", "Keterbukaan terhadap perspektif baru", "Keingintahuan terhadap pengetahuan dan pengalaman baru"]`,
			ImplementationExamples: `["Siswa menyadari tujuan pembelajaran sebelum memulai", "Siswa mengatur strategi belajar mereka sendiri", "Siswa merefleksikan proses berpikir mereka", "Siswa aktif bertanya dan mencari informasi baru"]`,
			IsActive:               true,
		},
		{
			PrincipleCode:          PrincipleCodeBermakna,
			PrincipleName:          "Bermakna",
			Description:            "Peserta didik dapat merasakan manfaat dan relevansi dari hal-hal yang dipelajari untuk kehidupan. Peserta didik mampu mengkonstruksi pengetahuan baru berdasarkan pengetahuan lama dan menerapkan pengetahuannya dalam kehidupan nyata.",
			KeyCharacteristics:     `["Kontekstual dan/atau relevan dengan kehidupan nyata", "Keterkaitan dengan pengalaman sebelumnya", "Kebermanfaatan pengalaman belajar untuk diterapkan dalam konteks baru", "Keterkaitan dengan bidang ilmu lain", "Pembelajar sepanjang hayat"]`,
			ImplementationExamples: `["Menghubungkan pelajaran dengan pengalaman sehari-hari siswa", "Menunjukkan bagaimana konsep diterapkan dalam kehidupan nyata", "Menggunakan contoh yang dekat dengan kehidupan siswa", "Menghubungkan dengan mata pelajaran lain"]`,
			IsActive:               true,
		},
		{
			PrincipleCode:          PrincipleCodeMenggembirakan,
			PrincipleName:          "Menggembirakan",
			Description:            "Pembelajaran yang menggembirakan merupakan suasana belajar yang positif, menyenangkan, menantang, dan memotivasi. Peserta didik merasa dihargai atas keterlibatan dan kontribusinya pada proses pembelajaran. Peserta didik terhubung secara emosional, sehingga lebih mudah memahami, mengingat, dan menerapkan pengetahuan.",
			KeyCharacteristics:     `["Lingkungan pembelajaran yang interaktif", "Aktivitas pembelajaran yang menarik", "Menginspirasi", "Tantangan yang memotivasi", "Tercapainya keberhasilan belajar (AHA moment)"]`,
			ImplementationExamples: `["Menggunakan permainan dalam pembelajaran", "Memberikan tantangan yang sesuai dengan kemampuan siswa", "Menciptakan suasana kelas yang positif", "Merayakan keberhasilan belajar siswa"]`,
			IsActive:               true,
		},
	}
}
