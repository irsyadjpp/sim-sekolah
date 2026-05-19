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
	GetAll(ctx context.Context, pagination common.Pagination, search string) ([]Teacher, int64, error)
	GetByID(ctx context.Context, id string) (*Teacher, error)
	GetBySchoolID(ctx context.Context, schoolID string) ([]Teacher, error)
	Create(ctx context.Context, req CreateTeacherRequest) (*Teacher, error)
	Update(ctx context.Context, id string, req UpdateTeacherRequest) (*Teacher, error)
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

func (s *teacherService) GetAll(ctx context.Context, pagination common.Pagination, search string) ([]Teacher, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset, search)
}

func (s *teacherService) GetByID(ctx context.Context, id string) (*Teacher, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *teacherService) GetBySchoolID(ctx context.Context, schoolID string) ([]Teacher, error) {
	return s.repo.GetBySchoolID(ctx, schoolID)
}

func (s *teacherService) Create(ctx context.Context, req CreateTeacherRequest) (*Teacher, error) {
	schoolUUID, _ := uuid.Parse(req.SchoolID)

	teacher := &Teacher{
		ID:                 uuid.New(),
		SchoolID:           schoolUUID,
		FullName:           req.FullName,
		Gender:             req.Gender,
		BirthPlace:         req.BirthPlace,
		NIK:                req.NIK,
		NUPTK:              req.NUPTK,
		NIYNIGK:            req.NIYNIGK,
		Religion:           req.Religion,
		Nationality:        coalesce(req.Nationality, "WNI"),
		PhotoURL:           req.PhotoURL,
		FullAddress:        req.FullAddress,
		Hamlet:             req.Hamlet,
		RTRW:               req.RTRW,
		Village:            req.Village,
		District:           req.District,
		Regency:            req.Regency,
		Province:           req.Province,
		PostalCode:         req.PostalCode,
		Phone:              req.Phone,
		Email:              req.Email,
		NIP:                req.NIP,
		EmploymentStatus:   req.EmploymentStatus,
		AppointmentDecree:  req.AppointmentDecree,
		SalarySource:       req.SalarySource,
		TeachingSubject:    req.TeachingSubject,
		AdditionalPosition: req.AdditionalPosition,
		TeachingHours:      req.TeachingHours,
		IsActive:           true,
		LastEducation:      req.LastEducation,
		Major:              req.Major,
		UniversityName:     req.UniversityName,
		GraduationYear:     req.GraduationYear,
		CertificateNumber:  req.CertificateNumber,
		TeachingPreference: req.TeachingPreference,
	}

	// Parse boolean pointer fields
	if req.IsActive != nil {
		teacher.IsActive = *req.IsActive
	}
	if req.IsCertified != nil {
		teacher.IsCertified = *req.IsCertified
	}

	// Parse dates
	if req.BirthDate != "" {
		t, err := time.Parse("2006-01-02", req.BirthDate)
		if err != nil {
			return nil, errors.New("format tanggal lahir tidak valid, gunakan YYYY-MM-DD")
		}
		teacher.BirthDate = &t
	}
	if req.StartTeachingDate != "" {
		t, err := time.Parse("2006-01-02", req.StartTeachingDate)
		if err != nil {
			return nil, errors.New("format TMT mengajar tidak valid, gunakan YYYY-MM-DD")
		}
		teacher.StartTeachingDate = &t
	}

	// Simpan data guru
	if err := s.repo.Create(ctx, teacher); err != nil {
		return nil, err
	}

	// ============================================================
	// AUTO-CREATE USER ACCOUNT untuk Guru
	// ============================================================
	if err := s.createUserAccount(ctx, teacher); err != nil {
		logger.Warn(fmt.Sprintf("Gagal membuat akun user untuk guru %s", teacher.FullName), err)
	}

	return teacher, nil
}

// createUserAccount membuat akun User secara otomatis saat data Guru dibuat
func (s *teacherService) createUserAccount(ctx context.Context, teacher *Teacher) error {
	// Generate username dari NIP atau prefix email
	username := ""
	if teacher.NIP != "" {
		username = teacher.NIP
	} else if teacher.Email != "" {
		parts := strings.Split(teacher.Email, "@")
		username = parts[0]
	} else {
		// Fallback: gunakan ID guru
		username = "guru_" + teacher.ID.String()[:8]
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

	// Buat user baru
	teacherID := teacher.ID
	user := &auth.User{
		ID:           uuid.New(),
		TeacherID:    &teacherID,
		FullName:     teacher.FullName,
		Username:     username,
		Email:        teacher.Email,
		PasswordHash: string(hash),
		IsEnabled:    true,
		Roles:        []auth.Role{guruRole},
	}

	return s.db.WithContext(ctx).Create(user).Error
}

func (s *teacherService) Update(ctx context.Context, id string, req UpdateTeacherRequest) (*Teacher, error) {
	teacher, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("guru tidak ditemukan")
	}

	// Update semua field yang dikirim
	if req.FullName != "" {
		teacher.FullName = req.FullName
	}
	if req.Gender != "" {
		teacher.Gender = req.Gender
	}
	if req.BirthPlace != "" {
		teacher.BirthPlace = req.BirthPlace
	}
	if req.BirthDate != "" {
		t, err := time.Parse("2006-01-02", req.BirthDate)
		if err != nil {
			return nil, errors.New("format tanggal lahir tidak valid")
		}
		teacher.BirthDate = &t
	}
	if req.NIK != "" {
		teacher.NIK = req.NIK
	}
	if req.NUPTK != "" {
		teacher.NUPTK = req.NUPTK
	}
	if req.NIYNIGK != "" {
		teacher.NIYNIGK = req.NIYNIGK
	}
	if req.Religion != "" {
		teacher.Religion = req.Religion
	}
	if req.Nationality != "" {
		teacher.Nationality = req.Nationality
	}
	if req.PhotoURL != "" {
		teacher.PhotoURL = req.PhotoURL
	}
	if req.FullAddress != "" {
		teacher.FullAddress = req.FullAddress
	}
	if req.Hamlet != "" {
		teacher.Hamlet = req.Hamlet
	}
	if req.RTRW != "" {
		teacher.RTRW = req.RTRW
	}
	if req.Village != "" {
		teacher.Village = req.Village
	}
	if req.District != "" {
		teacher.District = req.District
	}
	if req.Regency != "" {
		teacher.Regency = req.Regency
	}
	if req.Province != "" {
		teacher.Province = req.Province
	}
	if req.PostalCode != "" {
		teacher.PostalCode = req.PostalCode
	}
	if req.Phone != "" {
		teacher.Phone = req.Phone
	}
	if req.Email != "" {
		teacher.Email = req.Email
	}
	if req.NIP != "" {
		teacher.NIP = req.NIP
	}
	if req.EmploymentStatus != "" {
		teacher.EmploymentStatus = req.EmploymentStatus
	}
	if req.StartTeachingDate != "" {
		t, _ := time.Parse("2006-01-02", req.StartTeachingDate)
		teacher.StartTeachingDate = &t
	}
	if req.AppointmentDecree != "" {
		teacher.AppointmentDecree = req.AppointmentDecree
	}
	if req.SalarySource != "" {
		teacher.SalarySource = req.SalarySource
	}
	if req.TeachingSubject != "" {
		teacher.TeachingSubject = req.TeachingSubject
	}
	if req.AdditionalPosition != "" {
		teacher.AdditionalPosition = req.AdditionalPosition
	}
	if req.TeachingHours > 0 {
		teacher.TeachingHours = req.TeachingHours
	}
	if req.IsActive != nil {
		teacher.IsActive = *req.IsActive
	}
	if req.LastEducation != "" {
		teacher.LastEducation = req.LastEducation
	}
	if req.Major != "" {
		teacher.Major = req.Major
	}
	if req.UniversityName != "" {
		teacher.UniversityName = req.UniversityName
	}
	if req.GraduationYear > 0 {
		teacher.GraduationYear = req.GraduationYear
	}
	if req.IsCertified != nil {
		teacher.IsCertified = *req.IsCertified
	}
	if req.CertificateNumber != "" {
		teacher.CertificateNumber = req.CertificateNumber
	}
	teacher.TeachingPreference = req.TeachingPreference

	if err := s.repo.Update(ctx, teacher); err != nil {
		return nil, err
	}
	return teacher, nil
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
