package student

// CreateStudentRequest is the request body for creating a new student record.
type CreateStudentRequest struct {
	SchoolID string `json:"school_id" validate:"required,uuid" example:"804b75d4-2822-48a7-8eba-3566f038f81f"` // UUID Sekolah tempat siswa terdaftar

	// Identitas
	FullName    string `json:"full_name" validate:"required,max=255" example:"Rian Hidayat"` // Nama lengkap siswa sesuai akta lahir
	NIS         string `json:"nis" validate:"omitempty,max=20" example:"202601001"`          // Nomor Induk Siswa lokal sekolah
	NISN        string `json:"nisn" validate:"omitempty,max=20" example:"0151234567"`        // Nomor Induk Siswa Nasional (10 digit)
	Gender      string `json:"gender" validate:"omitempty,oneof=L P" example:"L"`            // Jenis kelamin: 'L' (Laki-laki) atau 'P' (Perempuan)
	BirthPlace  string `json:"birth_place" example:"Kepulauan Selayar"`                      // Tempat lahir siswa
	BirthDate   string `json:"birth_date" example:"2015-08-20"`                              // Tanggal lahir format YYYY-MM-DD
	Religion    string `json:"religion" example:"Islam"`                                     // Agama siswa
	Nationality string `json:"nationality" example:"WNI"`                                    // Kewarganegaraan
	ChildOrder  int    `json:"child_order" example:"2"`                                      // Anak ke-berapa dalam keluarga
	Siblings    int    `json:"siblings" example:"3"`                                         // Jumlah saudara kandung
	PhotoURL    string `json:"photo_url" example:"https://example.com/photos/rian.jpg"`      // URL berkas foto profil siswa

	// Kependudukan
	NIK              string `json:"nik" example:"7301022008150002"`                // Nomor Induk Kependudukan (16 digit)
	FamilyCardNumber string `json:"family_card_number" example:"7301021208100003"` // Nomor Kartu Keluarga (KK)
	BirthCertificate string `json:"birth_certificate" example:"1204/DISDUK/2015"`  // Nomor registrasi Akta Kelahiran
	KIPNumber        string `json:"kip_number" example:"KIP-88776655"`             // Nomor Kartu Indonesia Pintar (jika ada)

	// Alamat
	FullAddress string `json:"full_address" example:"Jl. Bonerate Raya No. 4"` // Alamat lengkap rumah
	RTRW        string `json:"rt_rw" example:"001/002"`                        // RT/RW domisili
	Village     string `json:"village" example:"Bonerate"`                     // Kelurahan / Desa
	District    string `json:"district" example:"Pasimarannu"`                 // Kecamatan
	Regency     string `json:"regency" example:"Kepulauan Selayar"`            // Kabupaten / Kota
	Province    string `json:"province" example:"Sulawesi Selatan"`            // Provinsi
	PostalCode  string `json:"postal_code" example:"92854"`                    // Kode Pos
	Coordinates string `json:"coordinates" example:"-7.3912,121.1293"`         // Titik koordinat peta (Latitude, Longitude)

	// Data Sekolah
	EnrollmentYear int    `json:"enrollment_year" example:"2026"`                // Tahun ajaran pendaftaran siswa
	Curriculum     string `json:"curriculum" example:"Kurikulum Merdeka"`        // Jenis kurikulum yang diikuti
	StudentStatus  string `json:"student_status" example:"AKTIF"`                // Status keaktifan (e.g. AKTIF, LULUS, MUTASI)
	EntryPath      string `json:"entry_path" example:"SPMB REGULER"`             // Jalur masuk sekolah (e.g. ZONASI, REGULER)
	PreviousSchool string `json:"previous_school" example:"TK Pembina Bonerate"` // Nama asal sekolah tingkat sebelumnya
	ExamNumber     string `json:"exam_number" example:"U-99887766"`              // Nomor ujian sekolah sebelumnya

	// Kesehatan
	BloodType      string  `json:"blood_type" example:"O"`                                      // Golongan darah: A, B, AB, O
	Height         float64 `json:"height" example:"125.5"`                                      // Tinggi badan dalam centimeter (cm)
	Weight         float64 `json:"weight" example:"28.4"`                                       // Berat badan dalam kilogram (kg)
	MedicalHistory string  `json:"medical_history" example:"Tidak ada riwayat penyakit kronis"` // Riwayat penyakit bawaan atau kronis
	Disability     string  `json:"disability" example:"TIDAK ADA"`                              // Kategori disabilitas jika berkebutuhan khusus
}

// UpdateStudentRequest is the request body for updating an existing student record.
type UpdateStudentRequest struct {
	FullName    string `json:"full_name" example:"Rian Hidayat"`
	NIS         string `json:"nis" example:"202601001"`
	NISN        string `json:"nisn" example:"0151234567"`
	Gender      string `json:"gender" validate:"omitempty,oneof=L P" example:"L"`
	BirthPlace  string `json:"birth_place" example:"Kepulauan Selayar"`
	BirthDate   string `json:"birth_date" example:"2015-08-20"`
	Religion    string `json:"religion" example:"Islam"`
	Nationality string `json:"nationality" example:"WNI"`
	ChildOrder  int    `json:"child_order" example:"2"`
	Siblings    int    `json:"siblings" example:"3"`
	PhotoURL    string `json:"photo_url" example:"https://example.com/photos/rian.jpg"`

	NIK              string `json:"nik" example:"7301022008150002"`
	FamilyCardNumber string `json:"family_card_number" example:"7301021208100003"`
	BirthCertificate string `json:"birth_certificate" example:"1204/DISDUK/2015"`
	KIPNumber        string `json:"kip_number" example:"KIP-88776655"`

	FullAddress string `json:"full_address" example:"Jl. Bonerate Raya No. 4"`
	RTRW        string `json:"rt_rw" example:"001/002"`
	Village     string `json:"village" example:"Bonerate"`
	District    string `json:"district" example:"Pasimarannu"`
	Regency     string `json:"regency" example:"Kepulauan Selayar"`
	Province    string `json:"province" example:"Sulawesi Selatan"`
	PostalCode  string `json:"postal_code" example:"92854"`
	Coordinates string `json:"coordinates" example:"-7.3912,121.1293"`

	EnrollmentYear int    `json:"enrollment_year" example:"2026"`
	Curriculum     string `json:"curriculum" example:"Kurikulum Merdeka"`
	StudentStatus  string `json:"student_status" example:"AKTIF"`
	EntryPath      string `json:"entry_path" example:"SPMB REGULER"`
	PreviousSchool string `json:"previous_school" example:"TK Pembina Bonerate"`
	ExamNumber     string `json:"exam_number" example:"U-99887766"`

	BloodType      string  `json:"blood_type" example:"O"`
	Height         float64 `json:"height" example:"125.5"`
	Weight         float64 `json:"weight" example:"28.4"`
	MedicalHistory string  `json:"medical_history" example:"Tidak ada riwayat penyakit kronis"`
	Disability     string  `json:"disability" example:"TIDAK ADA"`
}

// UpsertParentRequest is the request body for adding or updating a student's parent/guardian.
type UpsertParentRequest struct {
	ParentType string `json:"parent_type" validate:"required,oneof=FATHER MOTHER GUARDIAN" example:"FATHER"` // Kategori wali: 'FATHER' (Ayah), 'MOTHER' (Ibu), atau 'GUARDIAN' (Wali)
	FullName   string `json:"full_name" validate:"required" example:"Ahmad Basri"`                           // Nama lengkap orang tua / wali sesuai identitas resmi
	NIK        string `json:"nik" example:"7301021208750001"`                                                // Nomor Induk Kependudukan orang tua (16 digit)
	Education  string `json:"education" example:"S1"`                                                        // Tingkat pendidikan terakhir (e.g. SD, SMP, SMA, S1, S2)
	Occupation string `json:"occupation" example:"Wiraswasta"`                                               // Pekerjaan utama orang tua
	Income     int64  `json:"income" example:"4500000"`                                                      // Penghasilan bulanan dalam Rupiah (e.g. 4500000)
	Phone      string `json:"phone" example:"081398765432"`                                                  // Nomor telepon seluler aktif orang tua
}
