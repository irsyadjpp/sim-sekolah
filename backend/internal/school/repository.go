package school

import (
	"context"

	"gorm.io/gorm"
)

type SchoolRepository interface {
	GetAll(ctx context.Context, limit, offset int, search string) ([]SchoolComplete, int64, error)
	GetByID(ctx context.Context, id string) (*SchoolComplete, error)
	CreateComplete(ctx context.Context, data *SchoolComplete) error
	UpdateComplete(ctx context.Context, data *SchoolComplete) error
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

func (r *schoolRepository) GetAll(ctx context.Context, limit, offset int, search string) ([]SchoolComplete, int64, error) {
	var schools []SchoolComplete
	var total int64

	query := r.db.WithContext(ctx).Model(&MasterSchool{})
	if search != "" {
		like := "%" + search + "%"
		query = query.Where("school_name ILIKE ? OR npsn ILIKE ?", like, like)
	}

	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("school_name ASC").Find(&schools).Error
	return schools, total, err
}

func (r *schoolRepository) GetByID(ctx context.Context, id string) (*SchoolComplete, error) {
	var s SchoolComplete
	if err := r.db.WithContext(ctx).First(&s.MasterSchool, "id = ?", id).Error; err != nil {
		return nil, err
	}

	// Load related data
	r.db.WithContext(ctx).First(&s.SchoolLocation, "school_id = ?", id)
	r.db.WithContext(ctx).First(&s.SchoolStatistics, "school_id = ?", id)
	r.db.WithContext(ctx).First(&s.SchoolInfrastructure, "school_id = ?", id)
	r.db.WithContext(ctx).First(&s.SchoolAcademic, "school_id = ?", id)
	r.db.WithContext(ctx).First(&s.SchoolAdministration, "school_id = ?", id)

	return &s, nil
}

func (r *schoolRepository) CreateComplete(ctx context.Context, data *SchoolComplete) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if err := tx.Create(&data.MasterSchool).Error; err != nil {
			return err
		}

		data.SchoolLocation.SchoolID = data.MasterSchool.ID
		if err := tx.Create(&data.SchoolLocation).Error; err != nil {
			return err
		}

		data.SchoolStatistics.SchoolID = data.MasterSchool.ID
		if err := tx.Create(&data.SchoolStatistics).Error; err != nil {
			return err
		}

		data.SchoolInfrastructure.SchoolID = data.MasterSchool.ID
		if err := tx.Create(&data.SchoolInfrastructure).Error; err != nil {
			return err
		}

		data.SchoolAcademic.SchoolID = data.MasterSchool.ID
		if err := tx.Create(&data.SchoolAcademic).Error; err != nil {
			return err
		}

		data.SchoolAdministration.SchoolID = data.MasterSchool.ID
		if err := tx.Create(&data.SchoolAdministration).Error; err != nil {
			return err
		}

		return nil
	})
}

func (r *schoolRepository) UpdateComplete(ctx context.Context, data *SchoolComplete) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if err := tx.Save(&data.MasterSchool).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.SchoolLocation).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.SchoolStatistics).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.SchoolInfrastructure).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.SchoolAcademic).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.SchoolAdministration).Error; err != nil {
			return err
		}

		return nil
	})
}

func (r *schoolRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		// Delete related records first
		tx.Where("school_id = ?", id).Delete(&SchoolLocation{})
		tx.Where("school_id = ?", id).Delete(&SchoolStatistics{})
		tx.Where("school_id = ?", id).Delete(&SchoolInfrastructure{})
		tx.Where("school_id = ?", id).Delete(&SchoolAcademic{})
		tx.Where("school_id = ?", id).Delete(&SchoolAdministration{})

		// Delete main record
		return tx.Delete(&MasterSchool{}, "id = ?", id).Error
	})
}

func (r *schoolRepository) Seed(ctx context.Context) error {
	schoolComplete := SchoolComplete{
		MasterSchool: MasterSchool{
			NPSN:           "40304877",
			SchoolName:     "UPT SDI Bonerate No 85 Kepulauan Selayar",
			Phone:          "",
			Email:          "",
			Status:         "Negeri",
			OperatingHours: "Pagi / 6 Hari Kerja",
			BOSStatus:      "Penerima BOS",
		},
		SchoolLocation: SchoolLocation{
			District:    "Pasimarannu",
			Regency:     "Kabupaten Kepulauan Selayar",
			Province:    "Sulawesi Selatan",
			Country:     "Indonesia",
			Latitude:    -7.3458,
			Longitude:   121.1456,
			FullAddress: "Jalan Majapahit No. 312, Desa Bonerate, Kec. Pasimarannu, Kab. Kepulauan Selayar, Prov. Sulawesi Selatan",
			PostalCode:  "",
		},
		SchoolStatistics: SchoolStatistics{
			TotalStudents:   251,
			MaleStudents:    130,
			FemaleStudents:  121,
			TotalTeachers:   20,
			MaleTeachers:    6,
			FemaleTeachers:  14,
			TotalStaff:      4,
			RombelCount:     12,
			StudentRatio:    "Rata-rata 21 Siswa per Rombel",
			StudentReligion: "Islam (100%)",
		},
		SchoolInfrastructure: SchoolInfrastructure{
			ElectricityCapacity:   1300,
			SignalStatus:          "4G Spotty",
			WaterSource:           "Sumur/Pompa",
			InternetAccess:        "Telkomsel",
			ClassroomCount:        12,
			ClassroomGoodCount:    8,
			ClassroomDamagedCount: 4,
			LibraryCount:          0,
			LabCount:              0,
			ToiletStudentCount:    3,
			ToiletTeacherCount:    1,
			InfrastructureSummary: "12 Ruang Kelas (Tersedia & Digunakan Penuh, 8 Baik, 4 Rusak Ringan), Sanitasi (Siswa: 3, Guru: 1)",
		},
		SchoolAcademic: SchoolAcademic{
			Curriculum:     "Kurikulum Merdeka",
			Accreditation:  "B",
			EducationForm:  "Sekolah Dasar (SD)",
			GraduationData: "52 Siswa Kelas VI siap lulus pada TA 2025/2026",
		},
		SchoolAdministration: SchoolAdministration{
			PrincipalName:  "Zamrah",
			OperatorName:   "Nurhaeni",
			Vision:         "Terwujudnya Generasi yang Berakhlak Mulia, Cerdas, Tangguh, dan Berwawasan Lingkungan Bahari Berlandaskan Profil Pelajar Pancasila.",
			VisionMeaning:  "Berakhlak Mulia: Mengakar pada kuatnya nilai-nilai agama Islam dan tradisi luhur masyarakat Bonerate.\nCerdas: Komitmen sekolah untuk terus meningkatkan literasi dan numerasi meski berada di wilayah kepulauan yang terluar.\nTangguh: Menggambarkan daya juang (resiliensi) siswa yang terbiasa menghadapi tantangan alam dan keterbatasan infrastruktur.\nBerwawasan Lingkungan Bahari: Kesadaran bahwa siswa hidup di ekosistem pesisir/kepulauan, sehingga mereka harus mencintai dan mampu menjaga potensi laut serta alam sekitarnya.",
			Mission:        "1. Pembentukan Karakter dan Nilai Agama: Menanamkan keimanan dan ketakwaan melalui pembiasaan ibadah rutin (salat dhuha/dhuhur berjamaah) dan mengintegrasikan kearifan lokal.\n2. Peningkatan Kualitas Pembelajaran: Menyelenggarakan PAIKEM yang berpusat pada siswa dan mengoptimalkan fasilitas untuk literasi/numerasi agar mampu bersaing.\n3. Pengembangan Ketangguhan: Melatih kedisiplinan dan kemandirian melalui Pramuka dan ekskul, serta membekali life skills relevan.\n4. Penanaman Wawasan Bahari: Mengintegrasikan pelestarian ekosistem pesisir ke dalam Mapel/Projek P5 dan membiasakan aksi peduli pesisir.\n5. Sinergi Masyarakat: Membangun kemitraan kuat antara sekolah, orang tua, tokoh masyarakat, dan pemerintah desa Bonerate.",
			Goal:           "Rumusan visi dan misi ini dirancang agar lulusan UPT SDI Bonerate No. 85 tidak hanya memiliki nilai akademik yang baik, tetapi juga memiliki mental yang pantang menyerah, bangga akan identitas mereka sebagai masyarakat kepulauan Selayar, serta siap beradaptasi dengan kemajuan zaman tanpa meninggalkan nilai-nilai luhur budaya pesisir.",
			SyncSystem:     "Dapodikdasmen (Data Pokok Pendidikan Dasar dan Menengah)",
			SyncCompliance: "Aktif melakukan pengiriman data",
		},
	}

	var existing MasterSchool
	if err := r.db.Where("npsn = ?", "40304877").First(&existing).Error; err != nil {
		r.db.Create(&schoolComplete.MasterSchool)
	} else {
		schoolComplete.MasterSchool.ID = existing.ID
		r.db.Save(&schoolComplete.MasterSchool)
	}

	// Create/update related records
	schoolComplete.SchoolLocation.SchoolID = schoolComplete.MasterSchool.ID
	schoolComplete.SchoolStatistics.SchoolID = schoolComplete.MasterSchool.ID
	schoolComplete.SchoolInfrastructure.SchoolID = schoolComplete.MasterSchool.ID
	schoolComplete.SchoolAcademic.SchoolID = schoolComplete.MasterSchool.ID
	schoolComplete.SchoolAdministration.SchoolID = schoolComplete.MasterSchool.ID

	r.db.Save(&schoolComplete.SchoolLocation)
	r.db.Save(&schoolComplete.SchoolStatistics)
	r.db.Save(&schoolComplete.SchoolInfrastructure)
	r.db.Save(&schoolComplete.SchoolAcademic)
	r.db.Save(&schoolComplete.SchoolAdministration)

	return nil
}
