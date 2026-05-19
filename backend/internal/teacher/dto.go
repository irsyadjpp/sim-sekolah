package teacher

// CreateTeacherRequest is the request body for creating a new teacher record.
type CreateTeacherRequest struct {
	SchoolID string `json:"school_id" validate:"required,uuid" example:"804b75d4-2822-48a7-8eba-3566f038f81f"` // UUID Sekolah tempat guru mengajar

	// Identitas
	FullName    string `json:"full_name" validate:"required,max=255" example:"Budi Santoso, S.Pd"` // Nama lengkap guru beserta gelar akademik
	Gender      string `json:"gender" validate:"omitempty,oneof=L P" example:"L"`                  // Jenis kelamin: 'L' (Laki-laki) atau 'P' (Perempuan)
	BirthPlace  string `json:"birth_place" example:"Makassar"`                                     // Tempat lahir guru
	BirthDate   string `json:"birth_date" example:"1985-05-12"`                                    // Tanggal lahir format YYYY-MM-DD
	NIK         string `json:"nik" validate:"omitempty,max=20" example:"7301021205850001"`         // Nomor Induk Kependudukan (16 digit)
	NUPTK       string `json:"nuptk" validate:"omitempty,max=20" example:"9876543210123456"`       // Nomor Unik Pendidik dan Tenaga Kependidikan (16 digit)
	NIYNIGK     string `json:"niy_nigk" example:"NIY-098765"`                                      // Nomor Induk Yayasan / GTY jika sekolah swasta
	Religion    string `json:"religion" example:"Islam"`                                           // Agama guru
	Nationality string `json:"nationality" example:"WNI"`                                          // Kewarganegaraan (e.g. WNI, WNA)
	PhotoURL    string `json:"photo_url" example:"https://example.com/photos/budi.jpg"`            // URL berkas foto profil guru

	// Kontak & Alamat
	FullAddress string `json:"full_address" example:"Jl. Trans Sulawesi No. 85"`                  // Alamat domisili lengkap (nama jalan, nomor rumah)
	Hamlet      string `json:"hamlet" example:"Dusun Bonerate"`                                   // Nama dusun / lingkungan
	RTRW        string `json:"rt_rw" example:"002/001"`                                           // Rukun Tetangga / Rukun Warga
	Village     string `json:"village" example:"Bonerate"`                                        // Nama desa atau kelurahan
	District    string `json:"district" example:"Pasimarannu"`                                    // Nama kecamatan
	Regency     string `json:"regency" example:"Kepulauan Selayar"`                               // Nama kabupaten atau kota
	Province    string `json:"province" example:"Sulawesi Selatan"`                               // Nama provinsi
	PostalCode  string `json:"postal_code" example:"92854"`                                       // Kode pos alamat domisili
	Phone       string `json:"phone" validate:"omitempty,max=30" example:"081234567890"`          // Nomor telepon seluler aktif
	Email       string `json:"email" validate:"omitempty,email,max=100" example:"budi@sd.sch.id"` // Alamat email resmi aktif

	// Kepegawaian
	NIP                string `json:"nip" validate:"omitempty,max=30" example:"198505122010011003"`                    // NIP (Nomor Induk Pegawai) jika PNS/PPPK
	EmploymentStatus   string `json:"employment_status" validate:"omitempty,oneof=PNS PPPK Honorer GTY" example:"PNS"` // Status kepegawaian aktif
	StartTeachingDate  string `json:"start_teaching_date" example:"2010-01-02"`                                        // Tanggal mulai mengajar pertama kali format YYYY-MM-DD
	AppointmentDecree  string `json:"appointment_decree" example:"800/234/SK-KADIS/2010"`                              // Nomor SK Pengangkatan pertama
	SalarySource       string `json:"salary_source" example:"APBD Kabupaten"`                                          // Sumber gaji utama (APBN, APBD, Yayasan)
	TeachingSubject    string `json:"teaching_subject" example:"Matematika"`                                           // Mata pelajaran utama yang diampu
	AdditionalPosition string `json:"additional_position" example:"Kepala Perpustakaan"`                               // Tugas tambahan di luar mengajar (e.g. Kepala Laboratorium)
	TeachingHours      int    `json:"teaching_hours" example:"24"`                                                     // Total jam mengajar tatap muka per minggu
	IsActive           *bool  `json:"is_active" example:"true"`                                                        // Status keaktifan guru di sekolah

	// Pendidikan
	LastEducation     string `json:"last_education" example:"S1"`                           // Tingkatan pendidikan terakhir (e.g. S1, S2)
	Major             string `json:"major" example:"Pendidikan Matematika"`                 // Jurusan pendidikan terakhir
	UniversityName    string `json:"university_name" example:"Universitas Negeri Makassar"` // Nama perguruan tinggi kelulusan
	GraduationYear    int    `json:"graduation_year" example:"2008"`                        // Tahun kelulusan kuliah
	IsCertified       *bool  `json:"is_certified" example:"true"`                           // Status sertifikasi pendidik
	CertificateNumber string `json:"certificate_number" example:"10234/CERT/2012"`          // Nomor sertifikasi pendidik jika tersertifikasi

	// Narasi AI
	TeachingPreference string `json:"teaching_preference" example:"Sangat sabar dan menyukai pembelajaran berbasis gamifikasi"` // Preferensi gaya mengajar untuk analisis AI
}

// UpdateTeacherRequest is the request body for updating an existing teacher record.
type UpdateTeacherRequest struct {
	// Identitas
	FullName    string `json:"full_name" example:"Budi Santoso, S.Pd, M.Pd"`            // Nama lengkap beserta gelar akademik terbaru
	Gender      string `json:"gender" validate:"omitempty,oneof=L P" example:"L"`       // Jenis kelamin
	BirthPlace  string `json:"birth_place" example:"Makassar"`                          // Tempat lahir
	BirthDate   string `json:"birth_date" example:"1985-05-12"`                         // Tanggal lahir YYYY-MM-DD
	NIK         string `json:"nik" example:"7301021205850001"`                          // Nomor Induk Kependudukan
	NUPTK       string `json:"nuptk" example:"9876543210123456"`                        // Nomor NUPTK (16 digit)
	NIYNIGK     string `json:"niy_nigk" example:"NIY-098765"`                           // Nomor NIY/NIGK
	Religion    string `json:"religion" example:"Islam"`                                // Agama
	Nationality string `json:"nationality" example:"WNI"`                               // Kewarganegaraan
	PhotoURL    string `json:"photo_url" example:"https://example.com/photos/budi.jpg"` // Foto profil URL

	// Kontak & Alamat
	FullAddress string `json:"full_address" example:"Jl. Trans Sulawesi No. 85"`
	Hamlet      string `json:"hamlet" example:"Dusun Bonerate"`
	RTRW        string `json:"rt_rw" example:"002/001"`
	Village     string `json:"village" example:"Bonerate"`
	District    string `json:"district" example:"Pasimarannu"`
	Regency     string `json:"regency" example:"Kepulauan Selayar"`
	Province    string `json:"province" example:"Sulawesi Selatan"`
	PostalCode  string `json:"postal_code" example:"92854"`
	Phone       string `json:"phone" example:"081234567890"`
	Email       string `json:"email" validate:"omitempty,email" example:"budi@sd.sch.id"`

	// Kepegawaian
	NIP                string `json:"nip" example:"198505122010011003"`
	EmploymentStatus   string `json:"employment_status" validate:"omitempty,oneof=PNS PPPK Honorer GTY" example:"PNS"`
	StartTeachingDate  string `json:"start_teaching_date" example:"2010-01-02"`
	AppointmentDecree  string `json:"appointment_decree" example:"800/234/SK-KADIS/2010"`
	SalarySource       string `json:"salary_source" example:"APBD Kabupaten"`
	TeachingSubject    string `json:"teaching_subject" example:"Matematika"`
	AdditionalPosition string `json:"additional_position" example:"Kepala Perpustakaan"`
	TeachingHours      int    `json:"teaching_hours" example:"24"`
	IsActive           *bool  `json:"is_active" example:"true"`

	// Pendidikan
	LastEducation     string `json:"last_education" example:"S1"`
	Major             string `json:"major" example:"Pendidikan Matematika"`
	UniversityName    string `json:"university_name" example:"Universitas Negeri Makassar"`
	GraduationYear    int    `json:"graduation_year" example:"2008"`
	IsCertified       *bool  `json:"is_certified" example:"true"`
	CertificateNumber string `json:"certificate_number" example:"10234/CERT/2012"`

	// Narasi AI
	TeachingPreference string `json:"teaching_preference" example:"Sangat sabar dan menyukai pembelajaran berbasis gamifikasi"`
}
