package spmb

import (
	"context"
	"fmt"
	"time"

	"sim-sekolah/internal/student"
	"sim-sekolah/pkg/cache"

	"gorm.io/gorm"
)

type SPMBRepository interface {
	GetAdmissionPaths(ctx context.Context) ([]AdmissionPath, error)
	GetApplicants(ctx context.Context, limit, offset int, status string) ([]Applicant, int64, error)
	GetApplicantByID(ctx context.Context, id string) (*Applicant, error)
	GetApplicantByNIK(ctx context.Context, nik string) (*Applicant, error)

	CreateApplication(ctx context.Context, app *Applicant, parents *ApplicantParent) error
	UpdateApplicationStatus(ctx context.Context, log *VerificationLog) error
	AcceptApplicant(ctx context.Context, app *Applicant, log *VerificationLog, student *student.Student, parents []student.StudentParent) error
	GetYearlyStudentCount(ctx context.Context, year int) (int64, error)
	GetDefaultSchoolID(ctx context.Context) (string, error)

	SaveDocument(ctx context.Context, doc *ApplicantDocument) error
	GetActiveAcademicYears(ctx context.Context) ([]SPMBAcademicYear, error)
}

type spmbRepository struct {
	db *gorm.DB
}

func NewSPMBRepository(db *gorm.DB) SPMBRepository {
	return &spmbRepository{db: db}
}

func (r *spmbRepository) GetAdmissionPaths(ctx context.Context) ([]AdmissionPath, error) {
	cacheKey := "spmb:admission_paths:active"
	var paths []AdmissionPath

	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, cacheKey, &paths); err == nil {
			return paths, nil
		}
	}

	err := r.db.WithContext(ctx).Where("is_active = ?", true).Find(&paths).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, cacheKey, paths, 24*time.Hour)
	}
	return paths, err
}

func (r *spmbRepository) GetApplicants(ctx context.Context, limit, offset int, status string) ([]Applicant, int64, error) {
	var apps []Applicant
	var total int64

	query := r.db.WithContext(ctx).Model(&Applicant{})
	if status != "" {
		query = query.Where("status = ?", status)
	}

	query.Count(&total)

	orderClause := `
		CASE 
			WHEN trx_spmb_admission_path.name = 'Domisili' THEN 
				CASE WHEN trx_spmb_applicant.birth_date <= (date_trunc('year', CURRENT_DATE) + interval '6 months' - interval '7 years') THEN 0 ELSE 1 END
			ELSE 0
		END ASC,
		CASE 
			WHEN trx_spmb_admission_path.name = 'Domisili' THEN trx_spmb_applicant.distance_to_school_km 
			ELSE 0 
		END ASC,
		trx_spmb_applicant.created_at DESC
	`

	err := query.Joins("LEFT JOIN trx_spmb_admission_path ON trx_spmb_admission_path.id = trx_spmb_applicant.admission_path_id").
		Preload("AdmissionPath").
		Preload("SchoolYear").
		Order(orderClause).
		Limit(limit).Offset(offset).Find(&apps).Error

	return apps, total, err
}

func (r *spmbRepository) GetApplicantByID(ctx context.Context, id string) (*Applicant, error) {
	var app Applicant
	err := r.db.WithContext(ctx).
		Preload("AdmissionPath").
		Preload("SchoolYear").
		Preload("Parents").
		Preload("Documents").
		First(&app, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &app, nil
}

func (r *spmbRepository) GetApplicantByNIK(ctx context.Context, nik string) (*Applicant, error) {
	var app Applicant
	err := r.db.WithContext(ctx).First(&app, "nik = ?", nik).Error
	if err != nil {
		return nil, err
	}
	return &app, nil
}

func (r *spmbRepository) CreateApplication(ctx context.Context, app *Applicant, parents *ApplicantParent) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		// Generate registration number (Tahun + Seq)
		var count int64
		tx.Model(&Applicant{}).Where("EXTRACT(YEAR FROM created_at) = ?", time.Now().Year()).Count(&count)
		app.RegistrationNo = fmt.Sprintf("SPMB-%d-%04d", time.Now().Year(), count+1)

		if err := tx.Create(app).Error; err != nil {
			return err
		}

		parents.ApplicantID = app.ID
		if err := tx.Create(parents).Error; err != nil {
			return err
		}
		return nil
	})
}

func (r *spmbRepository) UpdateApplicationStatus(ctx context.Context, log *VerificationLog) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if err := tx.Model(&Applicant{}).Where("id = ?", log.ApplicantID).Update("status", log.StatusChangedTo).Error; err != nil {
			return err
		}
		return tx.Create(log).Error
	})
}

func (r *spmbRepository) AcceptApplicant(ctx context.Context, app *Applicant, log *VerificationLog, studentObj *student.Student, parents []student.StudentParent) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		// Update Status Pendaftar
		if err := tx.Model(app).Update("status", "Accepted").Error; err != nil {
			return err
		}

		// Simpan Log Verifikasi
		if err := tx.Create(log).Error; err != nil {
			return err
		}

		// Simpan Data Siswa
		if err := tx.Create(studentObj).Error; err != nil {
			return err
		}

		// Simpan Data Orang Tua Siswa
		for i := range parents {
			parents[i].StudentID = studentObj.ID
			if err := tx.Create(&parents[i]).Error; err != nil {
				return err
			}
		}

		return nil
	})
}

func (r *spmbRepository) GetYearlyStudentCount(ctx context.Context, year int) (int64, error) {
	var count int64
	err := r.db.WithContext(ctx).Table("students").Where("EXTRACT(YEAR FROM created_at) = ?", year).Count(&count).Error
	return count, err
}

func (r *spmbRepository) GetDefaultSchoolID(ctx context.Context) (string, error) {
	var schoolID string
	err := r.db.WithContext(ctx).Table("schools").Select("id").Limit(1).Scan(&schoolID).Error
	return schoolID, err
}

func (r *spmbRepository) SaveDocument(ctx context.Context, doc *ApplicantDocument) error {
	// Upsert dokumen (timpa jika dokumen dengan tipe yang sama diupload ulang)
	var existing ApplicantDocument
	err := r.db.WithContext(ctx).Where("applicant_id = ? AND document_type = ?", doc.ApplicantID, doc.DocumentType).First(&existing).Error
	if err == nil {
		doc.ID = existing.ID
		return r.db.WithContext(ctx).Save(doc).Error
	}
	return r.db.WithContext(ctx).Create(doc).Error
}

func (r *spmbRepository) GetActiveAcademicYears(ctx context.Context) ([]SPMBAcademicYear, error) {
	cacheKey := "spmb:academic_years:active"
	var years []SPMBAcademicYear

	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, cacheKey, &years); err == nil {
			return years, nil
		}
	}

	err := r.db.WithContext(ctx).Where("is_active = ?", true).Find(&years).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, cacheKey, years, 24*time.Hour)
	}
	return years, err
}
