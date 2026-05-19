package school

import (
	"context"

	"github.com/lib/pq"
	"gorm.io/gorm"
)

type SchoolRepository interface {
	GetAll(ctx context.Context, limit, offset int, search string) ([]School, int64, error)
	GetByID(ctx context.Context, id string) (*School, error)
	Create(ctx context.Context, data *School) error
	Update(ctx context.Context, data *School) error
	Delete(ctx context.Context, id string) error
	Seed(ctx context.Context) error
}

type schoolRepository struct {
	db *gorm.DB
}

// NewSchoolRepository creates a new SchoolRepository with an injected *gorm.DB.
func NewSchoolRepository(db *gorm.DB) SchoolRepository {
	return &schoolRepository{db: db}
}

func (r *schoolRepository) GetAll(ctx context.Context, limit, offset int, search string) ([]School, int64, error) {
	var schools []School
	var total int64

	query := r.db.WithContext(ctx).Model(&School{})
	if search != "" {
		like := "%" + search + "%"
		query = query.Where("school_name ILIKE ? OR npsn ILIKE ?", like, like)
	}

	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("school_name ASC").Find(&schools).Error
	return schools, total, err
}

func (r *schoolRepository) GetByID(ctx context.Context, id string) (*School, error) {
	var s School
	if err := r.db.WithContext(ctx).First(&s, "id = ?", id).Error; err != nil {
		return nil, err
	}
	return &s, nil
}

func (r *schoolRepository) Create(ctx context.Context, data *School) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *schoolRepository) Update(ctx context.Context, data *School) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *schoolRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&School{}, "id = ?", id).Error
}

func (r *schoolRepository) Seed(ctx context.Context) error {
	school := School{
		NPSN:                  "40304877",
		SchoolName:            "UPT SDI Bonerate No 85 Kepulauan Selayar",
		Address:               "Jalan Majapahit No. 312, Desa Bonerate, Kec. Pasimarannu, Kab. Kepulauan Selayar, Prov. Sulawesi Selatan",
		District:              "Pasimarannu",
		Regency:               "Kabupaten Kepulauan Selayar",
		Province:              "Sulawesi Selatan",
		Country:               "Indonesia",
		Status:                "Negeri",
		Accreditation:         "B",
		PrincipalName:         "Zamrah",
		OperatorName:          "Nurhaeni",
		OperatingHours:        "Pagi / 6 Hari Kerja",
		Latitude:              -7.3458,
		Longitude:             121.1456,
		TotalStudents:         251,
		MaleStudents:          130,
		FemaleStudents:        121,
		TotalTeachers:         20,
		MaleTeachers:          6,
		FemaleTeachers:        14,
		TotalStaff:            4,
		EducationForm:         "Sekolah Dasar (SD)",
		Curriculum:            "Kurikulum Merdeka",
		ElectricityCapacity:   1300,
		SignalStatus:          "4G Spotty",
		InternetAccess:        "Telkomsel",
		WaterSource:           "Sumur/Pompa",
		BOSStatus:             "Penerima BOS",
		InfrastructureSummary: "12 Ruang Kelas (Tersedia & Digunakan Penuh, 8 Baik, 4 Rusak Ringan), Sanitasi (Siswa: 3, Guru: 1)",
		GraduationData:        "52 Siswa Kelas VI siap lulus pada TA 2025/2026",
		TeacherPnsCount:       14,
		TeacherHonorCount:     6,
		TeacherCertifiedCount: "±60% - 80%",
		TeacherQualifiedCount: "90%",
		ClassroomCount:        12,
		ClassroomGoodCount:    8,
		ClassroomDamagedCount: 4,
		LibraryCount:          0,
		LabCount:              0,
		ToiletStudentCount:    3,
		ToiletTeacherCount:    1,
		StudentReligion:       "Islam (100%)",
		StudentRatio:          "Rata-rata 21 Siswa per Rombel",
		RombelCount:           12,
		SyncSystem:            "Dapodikdasmen (Data Pokok Pendidikan Dasar dan Menengah)",
		SyncCompliance:        "Aktif melakukan pengiriman data",
		Vision:                "Terwujudnya Generasi yang Berakhlak Mulia, Cerdas, Tangguh, dan Berwawasan Lingkungan Bahari Berlandaskan Profil Pelajar Pancasila.",
		VisionMeaning: `Berakhlak Mulia: Mengakar pada kuatnya nilai-nilai agama Islam dan tradisi luhur masyarakat Bonerate.
Cerdas: Komitmen sekolah untuk terus meningkatkan literasi dan numerasi meski berada di wilayah kepulauan yang terluar.
Tangguh: Menggambarkan daya juang (resiliensi) siswa yang terbiasa menghadapi tantangan alam dan keterbatasan infrastruktur.
Berwawasan Lingkungan Bahari: Kesadaran bahwa siswa hidup di ekosistem pesisir/kepulauan, sehingga mereka harus mencintai dan mampu menjaga potensi laut serta alam sekitarnya.`,
		Mission: `1. Pembentukan Karakter dan Nilai Agama: Menanamkan keimanan dan ketakwaan melalui pembiasaan ibadah rutin (salat dhuha/dhuhur berjamaah) dan mengintegrasikan kearifan lokal.
2. Peningkatan Kualitas Pembelajaran: Menyelenggarakan PAIKEM yang berpusat pada siswa dan mengoptimalkan fasilitas untuk literasi/numerasi agar mampu bersaing.
3. Pengembangan Ketangguhan: Melatih kedisiplinan dan kemandirian melalui Pramuka dan ekskul, serta membekali life skills relevan.
4. Penanaman Wawasan Bahari: Mengintegrasikan pelestarian ekosistem pesisir ke dalam Mapel/Projek P5 dan membiasakan aksi peduli pesisir.
5. Sinergi Masyarakat: Membangun kemitraan kuat antara sekolah, orang tua, tokoh masyarakat, dan pemerintah desa Bonerate.`,
		Goal: "Rumusan visi dan misi ini dirancang agar lulusan UPT SDI Bonerate No. 85 tidak hanya memiliki nilai akademik yang baik, tetapi juga memiliki mental yang pantang menyerah, bangga akan identitas mereka sebagai masyarakat kepulauan Selayar, serta siap beradaptasi dengan kemajuan zaman tanpa meninggalkan nilai-nilai luhur budaya pesisir.",
	}

	var existing School
	if err := r.db.Where("npsn = ?", "40304877").First(&existing).Error; err != nil {
		r.db.Create(&school)
	} else {
		school.ID = existing.ID
		r.db.Save(&school)
	}

	// Seed Local Context
	localCulturalHeritage := "Tradisi Adu Kuda Jantan (hiburan rakyat Pasimarannu), ritual Mandi Syafar (tolak bala bersama di laut), perayaan Maulid Nabi dengan hiasan telur (maudu), serta upacara adat Ambasa (syukuran sebelum musim melaut atau panen emping laut)."
	localUMKMPotential := "Kelompok pengrajin kopra rumahan, pengeringan ikan asin tradisional di pesisir, industri pembuatan shuttlecock lokal (lini SNAR), dan penyedia penginapan rumah (homestay) kemitraan pariwisata bahari."

	localContext := SchoolLocalContext{
		SchoolID:                 school.ID,
		LocalDominantOccupations: "Mayoritas utama adalah nelayan tangkap (tradisional dan modern), petani kelapa/kopra, buruh angkut pelabuhan di Dermaga Bonerate, pengrajin perahu kayu, dan sebagian kecil pelaku UMKM perdagangan antar-pulau.",
		LocalIncomeLevel:         "Pedesaan kepulauan terluar berbasis agraris-maritim dengan tingkat pendapatan musiman (sangat bergantung pada fluktuasi harga kopra dunia dan musim angin laut).",
		LocalLanguageNuance:      "Bahasa Bonerate (dialek khas perpaduan unsur Bajo dan Bugis-Makassar) serta Bahasa Indonesia sebagai bahasa pengantar formal. Kosakata lokal seperti 'mabar' digunakan khusus untuk 'fun games' dalam interaksi komunitas.",
		LocalGeographicType:      "Kawasan pulau terluar (Kepulauan sub-cluster Selayar bagian selatan), didominasi pesisir pantai berpasir putih, ekosistem karang atol (dekat kawasan Taka Bonerate), serta perbukitan rendah di Desa Majapahit.",
		LocalNaturalResources:    "Kelapa kering (kopra), ikan sunu, ikan kerapu, ikan cakalang, lobster, rumput laut, dan kerajinan anyaman sabut kelapa.",
		LocalEnvironmentalIssues: "Abrasi pantai di pesisir Desa Lamantu (Pantai Bangke), penumpukan sampah plastik musiman akibat arus laut global di sepanjang pantai Bonerate, serta keterbatasan air bersih siap minum saat musim kemarau panjang.",
		LocalCulturalHeritage:    &localCulturalHeritage,
		LocalUMKMPotential:       &localUMKMPotential,
	}

	var existingLocal SchoolLocalContext
	if err := r.db.Where("school_id = ?", school.ID).First(&existingLocal).Error; err != nil {
		r.db.Create(&localContext)
	} else {
		localContext.ID = existingLocal.ID
		r.db.Save(&localContext)
	}

	// Seed School Context Ext
	schoolExternalPartners := "Puskesmas Pasimarannu, Pemerintah Desa Bonerate, Komunitas Nelayan Lokal, Yayasan Membangun Kultur Negeri (Yayasan Kultur Juara Indonesia) untuk potensi olahraga/badminton."

	schoolExt := SchoolContextExt{
		SchoolID:                school.ID,
		SchoolVisionCore:        "Berakhlak Mulia, Cerdas, Tangguh, dan Berwawasan Lingkungan Bahari.",
		SchoolDistinctiveValues: "Satuan pendidikan inti kepulauan yang mengintegrasikan kesadaran ekologi pesisir ke dalam Kurikulum Merdeka (Project P5) guna membentuk resiliensi (daya juang) murid terhadap tantangan geografis terluar.",
		SchoolLocationSetting:   "Berada di poros Jalan Majapahit No. 312, Desa Bonerate. Berdekatan dengan pusat aktivitas maritim dermaga transit utama, pemukiman komunal padat pantai, dan area komoditas kelapa.",
		SchoolFacilitiesList: pq.StringArray{
			"Memiliki 12 Ruang Kelas (8 Baik, 4 Rusak Ringan)",
			"Tidak memiliki ruang laboratorium komputer fisik terpisah",
			"Tidak memiliki ruang perpustakaan fisik terpisah",
			"Pembelajaran berbasis IT dijalankan secara hibrida menggunakan perangkat pribadi guru/gawai komunal",
			"Ruang perpustakaan dioptimalkan melalui pojok baca kelas",
		},
		SchoolDigitalAdoptionLevel:    "LOW",
		SchoolTeacherProfileMatrix:    "Memiliki 20 Guru dan 4 Tendik (Total 24 PTK). Rasio guru terhadap rombel sangat ideal (1.67) dan rasio guru terhadap murid sangat intensif (1:12.55). Pendidik didominasi oleh perpaduan guru senior yang kaya pemahaman kultural lokal dan guru muda yang adaptif terhadap implementasi Kurikulum Merdeka.",
		SchoolExternalPartners:        &schoolExternalPartners,
		SchoolParentalInvolvementType: "AKTIF_KOLABORATIF",
	}

	var existingExt SchoolContextExt
	if err := r.db.Where("school_id = ?", school.ID).First(&existingExt).Error; err != nil {
		r.db.Create(&schoolExt)
	} else {
		schoolExt.ID = existingExt.ID
		r.db.Save(&schoolExt)
	}

	return nil
}
