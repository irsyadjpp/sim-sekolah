package subject

// CreateSubjectRequest adalah request body untuk membuat mata pelajaran.
type CreateSubjectRequest struct {
	SubjectCode          string                             `json:"subject_code" validate:"omitempty,max=20" example:"MAT-SD-A"`                        // Kode unik mata pelajaran (e.g. MAT-SD-A)
	SubjectName          string                             `json:"subject_name" validate:"required,max=255" example:"Matematika"`                      // Nama resmi mata pelajaran
	Rational             string                             `json:"rational" validate:"omitempty" example:"Kemampuan numerasi sangat krusial bagi..."`  // Rasionalitas mata pelajaran dalam kurikulum merdeka
	Goals                string                             `json:"goals" validate:"omitempty" example:"Membentuk pola pikir logis dan matematis..."`   // Tujuan pembelajaran mata pelajaran
	Characteristics      string                             `json:"characteristics" validate:"omitempty" example:"Pembelajaran berbasis eksplorasi..."` // Karakteristik umum pengajaran mata pelajaran
	IsActive             *bool                              `json:"is_active" validate:"omitempty" example:"true"`                                      // Status keaktifan mata pelajaran
	Level                string                             `json:"level" validate:"omitempty,max=10" example:"SD"`                                     // Tingkatan sekolah (SD, SMP, SMA)
	Abbreviation         string                             `json:"abbreviation" validate:"omitempty,max=20" example:"MTK"`                             // Singkatan nama mata pelajaran (e.g. MTK, BIN)
	CharacteristicPoints []CreateCharacteristicPointRequest `json:"characteristic_points" validate:"omitempty,dive"`                                    // Elemen / Karakteristik CP yang diampu
}

type CreateCharacteristicPointRequest struct {
	Description string                        `json:"description" validate:"required" example:"Pemahaman konsep bilangan cacah dan pecahan"` // Deskripsi karakteristik CP mata pelajaran
	Elements    []CreateSubjectElementRequest `json:"elements" validate:"omitempty,dive"`                                                    // Daftar elemen sub-kompetensi mata pelajaran
}

type CreateSubjectElementRequest struct {
	ElementName  string `json:"element_name" validate:"required,max=255" example:"Bilangan Cacah"`     // Nama sub-elemen CP (e.g. Bilangan, Geometri, Pengukuran)
	Abbreviation string `json:"abbreviation" validate:"omitempty,max=20" example:"BIL"`                // Singkatan sub-elemen (e.g. BIL, GEO)
	Description  string `json:"description" example:"Mencakup kemampuan mengurutkan, menjumlahkan..."` // Uraian cakupan materi sub-elemen
}

// UpdateSubjectRequest adalah request body untuk memperbarui mata pelajaran.
type UpdateSubjectRequest struct {
	SubjectCode          string                             `json:"subject_code" validate:"omitempty,max=20" example:"MAT-SD-A"`
	SubjectName          string                             `json:"subject_name" validate:"omitempty,max=255" example:"Matematika"`
	Rational             string                             `json:"rational" validate:"omitempty" example:"Kemampuan numerasi sangat krusial bagi..."`
	Goals                string                             `json:"goals" validate:"omitempty" example:"Membentuk pola pikir logis dan matematis..."`
	Characteristics      string                             `json:"characteristics" validate:"omitempty" example:"Pembelajaran berbasis eksplorasi..."`
	IsActive             *bool                              `json:"is_active" validate:"omitempty" example:"true"`
	Level                string                             `json:"level" validate:"omitempty,max=10" example:"SD"`
	Abbreviation         string                             `json:"abbreviation" validate:"omitempty,max=20" example:"MTK"`
	CharacteristicPoints []UpdateCharacteristicPointRequest `json:"characteristic_points" validate:"omitempty,dive"`
}

type UpdateCharacteristicPointRequest struct {
	ID          string                        `json:"id" validate:"omitempty,uuid" example:"a425fa98-4362-4f74-9a33-8dcfbaeecc45"` // UUID Karakteristik CP yang ingin diubah
	Description string                        `json:"description" validate:"required" example:"Pemahaman konsep bilangan cacah dan pecahan"`
	Elements    []UpdateSubjectElementRequest `json:"elements" validate:"omitempty,dive"`
}

type UpdateSubjectElementRequest struct {
	ID           string `json:"id" validate:"omitempty,uuid" example:"cfd0a60c-8f12-4e2c-a217-9ac5a14de76c"` // UUID Elemen CP yang ingin diubah
	ElementName  string `json:"element_name" validate:"required,max=255" example:"Bilangan Cacah"`
	Abbreviation string `json:"abbreviation" validate:"omitempty,max=20" example:"BIL"`
	Description  string `json:"description" example:"Mencakup kemampuan mengurutkan, menjumlahkan..."`
}
