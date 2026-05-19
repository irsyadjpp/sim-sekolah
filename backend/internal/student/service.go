package student

import (
	"context"
	"errors"
	"time"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type StudentService interface {
	GetAll(ctx context.Context, pagination common.Pagination, search string) ([]Student, int64, error)
	GetByID(ctx context.Context, id string) (*Student, error)
	GetBySchoolID(ctx context.Context, schoolID string) ([]Student, error)
	Create(ctx context.Context, req CreateStudentRequest) (*Student, error)
	Update(ctx context.Context, id string, req UpdateStudentRequest) (*Student, error)
	Delete(ctx context.Context, id string) error
	UpsertParent(ctx context.Context, studentID string, req UpsertParentRequest) (*StudentParent, error)
	DeleteParent(ctx context.Context, studentID, parentID string) error
}

type studentService struct {
	repo StudentRepository
}

// NewStudentService creates a new StudentService with an injected StudentRepository.
func NewStudentService(repo StudentRepository) StudentService {
	return &studentService{repo: repo}
}

func (s *studentService) GetAll(ctx context.Context, pagination common.Pagination, search string) ([]Student, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset, search)
}

func (s *studentService) GetByID(ctx context.Context, id string) (*Student, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *studentService) GetBySchoolID(ctx context.Context, schoolID string) ([]Student, error) {
	return s.repo.GetBySchoolID(ctx, schoolID)
}

func (s *studentService) Create(ctx context.Context, req CreateStudentRequest) (*Student, error) {
	schoolUUID, _ := uuid.Parse(req.SchoolID)

	student := &Student{
		ID:               uuid.New(),
		SchoolID:         schoolUUID,
		FullName:         req.FullName,
		NIS:              req.NIS,
		NISN:             req.NISN,
		Gender:           req.Gender,
		BirthPlace:       req.BirthPlace,
		Religion:         req.Religion,
		Nationality:      coalesce(req.Nationality, "WNI"),
		ChildOrder:       req.ChildOrder,
		Siblings:         req.Siblings,
		PhotoURL:         req.PhotoURL,
		NIK:              req.NIK,
		FamilyCardNumber: req.FamilyCardNumber,
		BirthCertificate: req.BirthCertificate,
		KIPNumber:        req.KIPNumber,
		FullAddress:      req.FullAddress,
		RTRW:             req.RTRW,
		Village:          req.Village,
		District:         req.District,
		Regency:          req.Regency,
		Province:         req.Province,
		PostalCode:       req.PostalCode,
		Coordinates:      req.Coordinates,
		EnrollmentYear:   req.EnrollmentYear,
		Curriculum:       req.Curriculum,
		StudentStatus:    StudentStatus(coalesce(req.StudentStatus, "active")),
		EntryPath:        req.EntryPath,
		PreviousSchool:   req.PreviousSchool,
		ExamNumber:       req.ExamNumber,
		BloodType:        req.BloodType,
		Height:           req.Height,
		Weight:           req.Weight,
		MedicalHistory:   req.MedicalHistory,
		Disability:       req.Disability,
	}

	if req.BirthDate != "" {
		t, err := time.Parse("2006-01-02", req.BirthDate)
		if err != nil {
			return nil, errors.New("format tanggal lahir tidak valid, gunakan YYYY-MM-DD")
		}
		student.BirthDate = &t
	}

	if err := s.repo.Create(ctx, student); err != nil {
		return nil, err
	}
	return student, nil
}

func (s *studentService) Update(ctx context.Context, id string, req UpdateStudentRequest) (*Student, error) {
	student, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("siswa tidak ditemukan")
	}

	if req.FullName != "" {
		student.FullName = req.FullName
	}
	if req.NIS != "" {
		student.NIS = req.NIS
	}
	if req.NISN != "" {
		student.NISN = req.NISN
	}
	if req.Gender != "" {
		student.Gender = req.Gender
	}
	if req.BirthPlace != "" {
		student.BirthPlace = req.BirthPlace
	}
	if req.BirthDate != "" {
		t, err := time.Parse("2006-01-02", req.BirthDate)
		if err != nil {
			return nil, errors.New("format tanggal lahir tidak valid")
		}
		student.BirthDate = &t
	}
	if req.Religion != "" {
		student.Religion = req.Religion
	}
	if req.Nationality != "" {
		student.Nationality = req.Nationality
	}
	if req.ChildOrder > 0 {
		student.ChildOrder = req.ChildOrder
	}
	if req.PhotoURL != "" {
		student.PhotoURL = req.PhotoURL
	}
	if req.NIK != "" {
		student.NIK = req.NIK
	}
	if req.FamilyCardNumber != "" {
		student.FamilyCardNumber = req.FamilyCardNumber
	}
	if req.BirthCertificate != "" {
		student.BirthCertificate = req.BirthCertificate
	}
	if req.KIPNumber != "" {
		student.KIPNumber = req.KIPNumber
	}
	if req.FullAddress != "" {
		student.FullAddress = req.FullAddress
	}
	if req.RTRW != "" {
		student.RTRW = req.RTRW
	}
	if req.Village != "" {
		student.Village = req.Village
	}
	if req.District != "" {
		student.District = req.District
	}
	if req.Regency != "" {
		student.Regency = req.Regency
	}
	if req.Province != "" {
		student.Province = req.Province
	}
	if req.PostalCode != "" {
		student.PostalCode = req.PostalCode
	}
	if req.Coordinates != "" {
		student.Coordinates = req.Coordinates
	}
	if req.EnrollmentYear > 0 {
		student.EnrollmentYear = req.EnrollmentYear
	}
	if req.Curriculum != "" {
		student.Curriculum = req.Curriculum
	}
	if req.StudentStatus != "" {
		student.StudentStatus = StudentStatus(req.StudentStatus)
	}
	if req.EntryPath != "" {
		student.EntryPath = req.EntryPath
	}
	if req.PreviousSchool != "" {
		student.PreviousSchool = req.PreviousSchool
	}
	if req.ExamNumber != "" {
		student.ExamNumber = req.ExamNumber
	}
	if req.BloodType != "" {
		student.BloodType = req.BloodType
	}
	if req.Height > 0 {
		student.Height = req.Height
	}
	if req.Weight > 0 {
		student.Weight = req.Weight
	}
	student.MedicalHistory = req.MedicalHistory
	student.Disability = req.Disability

	if err := s.repo.Update(ctx, student); err != nil {
		return nil, err
	}
	return student, nil
}

func (s *studentService) Delete(ctx context.Context, id string) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("siswa tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}

// UpsertParent menambah atau memperbarui data orang tua berdasarkan parent_type
func (s *studentService) UpsertParent(ctx context.Context, studentID string, req UpsertParentRequest) (*StudentParent, error) {
	if _, err := s.repo.GetByID(ctx, studentID); err != nil {
		return nil, errors.New("siswa tidak ditemukan")
	}
	return s.repo.UpsertParent(ctx, studentID, req)
}

func (s *studentService) DeleteParent(ctx context.Context, studentID, parentID string) error {
	return s.repo.DeleteParent(ctx, studentID, parentID)
}

func coalesce(val, fallback string) string {
	if val != "" {
		return val
	}
	return fallback
}
