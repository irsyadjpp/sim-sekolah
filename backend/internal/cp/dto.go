package cp

// CreateCPRequest is the request body for creating a Learning Outcome (Capaian Pembelajaran).
type CreateCPRequest struct {
	PhaseID     string                  `json:"phase_id" validate:"required,uuid" example:"a425fa98-4362-4f74-9a33-8dcfbaeecc45"`   // UUID Fase kelas (e.g. Fase A, Fase B, Fase C untuk SD)
	SubjectID   string                  `json:"subject_id" validate:"required,uuid" example:"c5d2f366-3ff2-422c-807a-44c618bef84f"` // UUID Mata Pelajaran pengampu CP
	CPCode      string                  `json:"cp_code" validate:"omitempty,max=50" example:"CP-MAT-FA"`                            // Kode unik dokumen CP (e.g. CP-MAT-FA)
	OutcomeText string                  `json:"outcome_text" validate:"omitempty" example:"Peserta didik mampu memahami konsep..."` // Uraian deskripsi komprehensif Capaian Pembelajaran Fase
	YearSK      string                  `json:"year_sk" validate:"required,max=10" example:"2024"`                                  // Tahun berlakunya SK Kemendikbudristek untuk CP ini
	Details     []CreateCPDetailRequest `json:"details" validate:"omitempty,dive"`                                                  // Daftar rincian CP per sub-elemen kompetensi
}

// UpdateCPRequest is the request body for updating a Learning Outcome.
type UpdateCPRequest struct {
	PhaseID     string                  `json:"phase_id" validate:"omitempty,uuid" example:"a425fa98-4362-4f74-9a33-8dcfbaeecc45"`
	SubjectID   string                  `json:"subject_id" validate:"omitempty,uuid" example:"c5d2f366-3ff2-422c-807a-44c618bef84f"`
	CPCode      string                  `json:"cp_code" validate:"omitempty,max=50" example:"CP-MAT-FA"`
	OutcomeText string                  `json:"outcome_text" validate:"omitempty" example:"Peserta didik mampu memahami konsep..."`
	YearSK      string                  `json:"year_sk" validate:"omitempty,max=10" example:"2024"`
	Details     []CreateCPDetailRequest `json:"details" validate:"omitempty,dive"`
}

// CreateCPDetailRequest is the request body for creating a Learning Outcome detail entry.
type CreateCPDetailRequest struct {
	ElementID  string `json:"element_id" validate:"required,uuid" example:"7e83162c-cbeb-4cd6-b027-2239a1ca481c"` // UUID Elemen CP dari mata pelajaran terkait
	SubCode    string `json:"sub_code" validate:"omitempty" example:"CP.MAT.FA.01"`                               // Kode sub-kompetensi CP (e.g. CP.MAT.FA.01)
	DetailText string `json:"detail_text" validate:"required" example:"Pada akhir fase A, peserta didik..."`      // Deskripsi target capaian sub-kompetensi
	SequenceNo int    `json:"sequence_no" validate:"required,min=1" example:"1"`                                  // Nomor urut alur pembelajaran (sequence)
}

// UpdateCPDetailRequest is the request body for updating a Learning Outcome detail entry.
type UpdateCPDetailRequest struct {
	ElementID  string `json:"element_id" validate:"omitempty,uuid" example:"7e83162c-cbeb-4cd6-b027-2239a1ca481c"`
	SubCode    string `json:"sub_code" validate:"omitempty" example:"CP.MAT.FA.01"`
	DetailText string `json:"detail_text" validate:"omitempty" example:"Pada akhir fase A, peserta didik..."`
	SequenceNo int    `json:"sequence_no" validate:"omitempty,min=1" example:"1"`
}

type CreateTPRequest struct {
	Description string `json:"description" validate:"required" example:"Peserta didik mampu menjumlahkan dua bilangan cacah hingga 20"` // Deskripsi Tujuan Pembelajaran (TP) yang diturunkan dari CP
}
