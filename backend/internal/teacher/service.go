package teacher

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"time"

	"sim-sekolah/internal/auth"
	"sim-sekolah/internal/common"
	"sim-sekolah/pkg/logger"

	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

type TeacherService interface {
	GetAll(ctx context.Context, pagination common.Pagination, search string) ([]TeacherComplete, int64, error)
	GetByID(ctx context.Context, id string) (*TeacherComplete, error)
	GetBySchoolID(ctx context.Context, schoolID string) ([]TeacherComplete, error)
	Create(ctx context.Context, req CreateTeacherRequest) (*TeacherComplete, error)
	Update(ctx context.Context, id string, req UpdateTeacherRequest) (*TeacherComplete, error)
	Delete(ctx context.Context, id string) error
}

type teacherService struct {
	repo TeacherRepository
	db   *gorm.DB // needed for cross-module operations (e.g. auto-create user)
}

// NewTeacherService creates a new TeacherService with an injected TeacherRepository and db.
func NewTeacherService(repo TeacherRepository, db *gorm.DB) TeacherService {
	return &teacherService{repo: repo, db: db}
}

func (s *teacherService) GetAll(ctx context.Context, pagination common.Pagination, search string) ([]TeacherComplete, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset, search)
}

func (s *teacherService) GetByID(ctx context.Context, id string) (*TeacherComplete, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *teacherService) GetBySchoolID(ctx context.Context, schoolID string) ([]TeacherComplete, error) {
	return s.repo.GetBySchoolID(ctx, schoolID)
}

func (s *teacherService) Create(ctx context.Context, req CreateTeacherRequest) (*TeacherComplete, error) {
	schoolUUID, _ := uuid.Parse(req.SchoolID)

	teacherComplete := &TeacherComplete{
		MasterTeacher: MasterTeacher{
			ID:          uuid.New(),
			SchoolID:    schoolUUID,
			FullName:    req.FullName,
			Gender:      req.Gender,
			BirthPlace:  req.BirthPlace,
			NIK:         req.NIK,
			NUPTK:       req.NUPTK,
			NIYNIGK:     req.NIYNIGK,
			Religion:    req.Religion,
			Nationality: coalesce(req.Nationality, "WNI"),
			PhotoURL:    req.PhotoURL,
		},
		TeacherContact: TeacherContact{
			FullAddress: req.FullAddress,
			Hamlet:      req.Hamlet,
			RTRW:        req.RTRW,
			Village:     req.Village,
			District:    req.District,
			Regency:     req.Regency,
			Province:    req.Province,
			PostalCode:  req.PostalCode,
			Phone:       req.Phone,
			Email:       req.Email,
		},
		TeacherEmployment: TeacherEmployment{
			NIP:                req.NIP, // NIP di TeacherEmployment sebagai data employment
			EmploymentStatus:   req.EmploymentStatus,
			AppointmentDecree:  req.AppointmentDecree,
			SalarySource:       req.SalarySource,
			TeachingSubject:    req.TeachingSubject,
			AdditionalPosition: req.AdditionalPosition,
			TeachingHours:      req.TeachingHours,
			IsActive:           true, // Default true untuk teacher baru
		},
		TeacherEducation: TeacherEducation{
			LastEducation:  req.LastEducation,
			Major:          req.Major,
			UniversityName: req.UniversityName,
			GraduationYear: req.GraduationYear,
		},
		TeacherCertification: TeacherCertification{
			IsCertified:       req.IsCertified != nil && *req.IsCertified,
			CertificateNumber: req.CertificateNumber,
		},
		TeacherPreference: TeacherPreference{
			TeachingPreference: req.TeachingPreference,
		},
	}

	// Parse dates
	if req.BirthDate != "" {
		t, err := time.Parse("2006-01-02", req.BirthDate)
		if err != nil {
			return nil, errors.New("format tanggal lahir tidak valid, gunakan YYYY-MM-DD")
		}
		teacherComplete.MasterTeacher.BirthDate = &t
	}
	if req.StartTeachingDate != "" {
		t, err := time.Parse("2006-01-02", req.StartTeachingDate)
		if err != nil {
			return nil, errors.New("format TMT mengajar tidak valid, gunakan YYYY-MM-DD")
		}
		teacherComplete.TeacherEmployment.StartTeachingDate = &t
	}

	// Simpan data guru
	if err := s.repo.CreateComplete(ctx, teacherComplete); err != nil {
		return nil, err
	}

	// ============================================================
	// AUTO-CREATE USER ACCOUNT untuk Guru
	// ============================================================
	if err := s.createUserAccount(ctx, &teacherComplete.MasterTeacher); err != nil {
		logger.Warn(fmt.Sprintf("Gagal membuat akun user untuk guru %s", teacherComplete.MasterTeacher.FullName), err)
	}

	return teacherComplete, nil
}

// createUserAccount membuat akun User secara otomatis saat data Guru dibuat
func (s *teacherService) createUserAccount(ctx context.Context, teacher *MasterTeacher) error {
	// Generate username dari NIP atau prefix email
	username := ""
	// Need to get employment data for NIP
	var employment TeacherEmployment
	if err := s.db.Where("teacher_id = ?", teacher.ID).First(&employment).Error; err == nil && employment.NIP != "" {
		username = employment.NIP
	} else {
		// Get contact data for email
		var contact TeacherContact
		if err := s.db.Where("teacher_id = ?", teacher.ID).First(&contact).Error; err == nil && contact.Email != "" {
			parts := strings.Split(contact.Email, "@")
			username = parts[0]
		} else {
			// Fallback: gunakan ID guru
			username = "guru_" + teacher.ID.String()[:8]
		}
	}

	// Cek apakah username sudah ada
	var existingCount int64
	s.db.Model(&auth.User{}).Where("username = ?", username).Count(&existingCount)
	if existingCount > 0 {
		username = username + "_" + teacher.ID.String()[:6]
	}

	// Hash default password
	defaultPassword := "GantiPassword123!"
	hash, err := bcrypt.GenerateFromPassword([]byte(defaultPassword), bcrypt.DefaultCost)
	if err != nil {
		return err
	}

	// Cari role GURU
	var guruRole auth.Role
	if err := s.db.Where("role_name = ?", "GURU").First(&guruRole).Error; err != nil {
		return fmt.Errorf("role GURU tidak ditemukan: %w", err)
	}

	// Get contact data for email
	var contact TeacherContact
	s.db.Where("teacher_id = ?", teacher.ID).First(&contact)

	// Buat user baru
	teacherID := teacher.ID
	user := &auth.User{
		ID:           uuid.New(),
		TeacherID:    &teacherID,
		FullName:     teacher.FullName,
		Username:     username,
		Email:        contact.Email,
		PasswordHash: string(hash),
		IsEnabled:    true,
		Roles:        []auth.Role{guruRole},
	}

	return s.db.WithContext(ctx).Create(user).Error
}

func (s *teacherService) Update(ctx context.Context, id string, req UpdateTeacherRequest) (*TeacherComplete, error) {
	teacherComplete, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("guru tidak ditemukan")
	}

	// Update MasterTeacher fields
	if req.FullName != "" {
		teacherComplete.MasterTeacher.FullName = req.FullName
	}
	if req.Gender != "" {
		teacherComplete.MasterTeacher.Gender = req.Gender
	}
	if req.BirthPlace != "" {
		teacherComplete.MasterTeacher.BirthPlace = req.BirthPlace
	}
	if req.BirthDate != "" {
		t, err := time.Parse("2006-01-02", req.BirthDate)
		if err != nil {
			return nil, errors.New("format tanggal lahir tidak valid")
		}
		teacherComplete.MasterTeacher.BirthDate = &t
	}
	if req.NIK != "" {
		teacherComplete.MasterTeacher.NIK = req.NIK
	}
	if req.NUPTK != "" {
		teacherComplete.MasterTeacher.NUPTK = req.NUPTK
	}
	if req.NIYNIGK != "" {
		teacherComplete.MasterTeacher.NIYNIGK = req.NIYNIGK
	}
	if req.Religion != "" {
		teacherComplete.MasterTeacher.Religion = req.Religion
	}
	if req.Nationality != "" {
		teacherComplete.MasterTeacher.Nationality = req.Nationality
	}
	if req.PhotoURL != "" {
		teacherComplete.MasterTeacher.PhotoURL = req.PhotoURL
	}

	// Update TeacherContact fields
	if req.FullAddress != "" {
		teacherComplete.TeacherContact.FullAddress = req.FullAddress
	}
	if req.Hamlet != "" {
		teacherComplete.TeacherContact.Hamlet = req.Hamlet
	}
	if req.RTRW != "" {
		teacherComplete.TeacherContact.RTRW = req.RTRW
	}
	if req.Village != "" {
		teacherComplete.TeacherContact.Village = req.Village
	}
	if req.District != "" {
		teacherComplete.TeacherContact.District = req.District
	}
	if req.Regency != "" {
		teacherComplete.TeacherContact.Regency = req.Regency
	}
	if req.Province != "" {
		teacherComplete.TeacherContact.Province = req.Province
	}
	if req.PostalCode != "" {
		teacherComplete.TeacherContact.PostalCode = req.PostalCode
	}
	if req.Phone != "" {
		teacherComplete.TeacherContact.Phone = req.Phone
	}
	if req.Email != "" {
		teacherComplete.TeacherContact.Email = req.Email
	}

	// Update TeacherEmployment fields
	if req.NIP != "" {
		teacherComplete.TeacherEmployment.NIP = req.NIP
	}
	if req.EmploymentStatus != "" {
		teacherComplete.TeacherEmployment.EmploymentStatus = req.EmploymentStatus
	}
	if req.StartTeachingDate != "" {
		t, _ := time.Parse("2006-01-02", req.StartTeachingDate)
		teacherComplete.TeacherEmployment.StartTeachingDate = &t
	}
	if req.AppointmentDecree != "" {
		teacherComplete.TeacherEmployment.AppointmentDecree = req.AppointmentDecree
	}
	if req.SalarySource != "" {
		teacherComplete.TeacherEmployment.SalarySource = req.SalarySource
	}
	if req.TeachingSubject != "" {
		teacherComplete.TeacherEmployment.TeachingSubject = req.TeachingSubject
	}
	if req.AdditionalPosition != "" {
		teacherComplete.TeacherEmployment.AdditionalPosition = req.AdditionalPosition
	}
	if req.TeachingHours > 0 {
		teacherComplete.TeacherEmployment.TeachingHours = req.TeachingHours
	}

	// Update TeacherEducation fields
	if req.LastEducation != "" {
		teacherComplete.TeacherEducation.LastEducation = req.LastEducation
	}
	if req.Major != "" {
		teacherComplete.TeacherEducation.Major = req.Major
	}
	if req.UniversityName != "" {
		teacherComplete.TeacherEducation.UniversityName = req.UniversityName
	}
	if req.GraduationYear > 0 {
		teacherComplete.TeacherEducation.GraduationYear = req.GraduationYear
	}

	// Update TeacherCertification fields
	if req.IsCertified != nil {
		teacherComplete.TeacherCertification.IsCertified = *req.IsCertified
	}
	if req.CertificateNumber != "" {
		teacherComplete.TeacherCertification.CertificateNumber = req.CertificateNumber
	}

	// Update TeacherPreference fields
	teacherComplete.TeacherPreference.TeachingPreference = req.TeachingPreference

	if err := s.repo.UpdateComplete(ctx, teacherComplete); err != nil {
		return nil, err
	}
	return teacherComplete, nil
}

func (s *teacherService) Delete(ctx context.Context, id string) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("guru tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}

// coalesce mengembalikan nilai pertama yang tidak kosong
func coalesce(val, fallback string) string {
	if val != "" {
		return val
	}
	return fallback
}
