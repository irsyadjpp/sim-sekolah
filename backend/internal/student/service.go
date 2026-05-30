package student

import (
	"context"
	"errors"
	"time"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type StudentService interface {
	GetAll(ctx context.Context, pagination common.Pagination, search string) ([]StudentComplete, int64, error)
	GetByID(ctx context.Context, id string) (*StudentComplete, error)
	GetBySchoolID(ctx context.Context, schoolID string) ([]StudentComplete, error)
	Create(ctx context.Context, req CreateStudentRequest) (*StudentComplete, error)
	Update(ctx context.Context, id string, req UpdateStudentRequest) (*StudentComplete, error)
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

func (s *studentService) GetAll(ctx context.Context, pagination common.Pagination, search string) ([]StudentComplete, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset, search)
}

func (s *studentService) GetByID(ctx context.Context, id string) (*StudentComplete, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *studentService) GetBySchoolID(ctx context.Context, schoolID string) ([]StudentComplete, error) {
	return s.repo.GetBySchoolID(ctx, schoolID)
}

func (s *studentService) Create(ctx context.Context, req CreateStudentRequest) (*StudentComplete, error) {
	schoolUUID, _ := uuid.Parse(req.SchoolID)

	studentComplete := &StudentComplete{
		MasterStudent: MasterStudent{
			ID:          uuid.New(),
			NIK:         req.NIK, // NIK di MasterStudent sebagai data identitas
			SchoolID:    schoolUUID,
			FullName:    req.FullName,
			Gender:      req.Gender,
			BirthPlace:  req.BirthPlace,
			Religion:    req.Religion,
			Nationality: coalesce(req.Nationality, "WNI"),
			PhotoURL:    req.PhotoURL,
		},
		StudentContact: StudentContact{
			FullAddress: req.FullAddress,
			RTRW:        req.RTRW,
			Village:     req.Village,
			District:    req.District,
			Regency:     req.Regency,
			Province:    req.Province,
			PostalCode:  req.PostalCode,
			Coordinates: req.Coordinates,
		},
		StudentFamily: StudentFamily{
			ChildOrder:       req.ChildOrder,
			Siblings:         req.Siblings,
			FamilyCardNumber: req.FamilyCardNumber,
			BirthCertificate: req.BirthCertificate,
			KIPNumber:        req.KIPNumber,
		},
		StudentEnrollment: StudentEnrollment{
			NIS:            req.NIS,
			NISN:           req.NISN,
			EnrollmentYear: req.EnrollmentYear,
			Curriculum:     req.Curriculum,
			StudentStatus:  StudentStatus(coalesce(req.StudentStatus, "active")),
			EntryPath:      req.EntryPath,
			PreviousSchool: req.PreviousSchool,
			ExamNumber:     req.ExamNumber,
		},
		StudentHealth: StudentHealth{
			BloodType:      req.BloodType,
			Height:         req.Height,
			Weight:         req.Weight,
			MedicalHistory: req.MedicalHistory,
			Disability:     req.Disability,
		},
	}

	if req.BirthDate != "" {
		t, err := time.Parse("2006-01-02", req.BirthDate)
		if err != nil {
			return nil, errors.New("format tanggal lahir tidak valid, gunakan YYYY-MM-DD")
		}
		studentComplete.MasterStudent.BirthDate = &t
	}

	if err := s.repo.CreateComplete(ctx, studentComplete); err != nil {
		return nil, err
	}
	return studentComplete, nil
}

func (s *studentService) Update(ctx context.Context, id string, req UpdateStudentRequest) (*StudentComplete, error) {
	studentComplete, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("siswa tidak ditemukan")
	}

	// Update MasterStudent fields
	if req.NIK != "" {
		studentComplete.MasterStudent.NIK = req.NIK // NIK di MasterStudent
	}
	if req.FullName != "" {
		studentComplete.MasterStudent.FullName = req.FullName
	}
	if req.NIS != "" {
		studentComplete.StudentEnrollment.NIS = req.NIS
	}
	if req.NISN != "" {
		studentComplete.StudentEnrollment.NISN = req.NISN
	}
	if req.Gender != "" {
		studentComplete.MasterStudent.Gender = req.Gender
	}
	if req.BirthPlace != "" {
		studentComplete.MasterStudent.BirthPlace = req.BirthPlace
	}
	if req.BirthDate != "" {
		t, err := time.Parse("2006-01-02", req.BirthDate)
		if err != nil {
			return nil, errors.New("format tanggal lahir tidak valid")
		}
		studentComplete.MasterStudent.BirthDate = &t
	}
	if req.Religion != "" {
		studentComplete.MasterStudent.Religion = req.Religion
	}
	if req.Nationality != "" {
		studentComplete.MasterStudent.Nationality = req.Nationality
	}
	if req.ChildOrder > 0 {
		studentComplete.StudentFamily.ChildOrder = req.ChildOrder
	}
	if req.Siblings > 0 {
		studentComplete.StudentFamily.Siblings = req.Siblings
	}
	if req.PhotoURL != "" {
		studentComplete.MasterStudent.PhotoURL = req.PhotoURL
	}

	// Update StudentContact fields
	if req.FullAddress != "" {
		studentComplete.StudentContact.FullAddress = req.FullAddress
	}
	if req.RTRW != "" {
		studentComplete.StudentContact.RTRW = req.RTRW
	}
	if req.Village != "" {
		studentComplete.StudentContact.Village = req.Village
	}
	if req.District != "" {
		studentComplete.StudentContact.District = req.District
	}
	if req.Regency != "" {
		studentComplete.StudentContact.Regency = req.Regency
	}
	if req.Province != "" {
		studentComplete.StudentContact.Province = req.Province
	}
	if req.PostalCode != "" {
		studentComplete.StudentContact.PostalCode = req.PostalCode
	}
	if req.Coordinates != "" {
		studentComplete.StudentContact.Coordinates = req.Coordinates
	}

	// Update StudentFamily fields
	if req.FamilyCardNumber != "" {
		studentComplete.StudentFamily.FamilyCardNumber = req.FamilyCardNumber
	}
	if req.BirthCertificate != "" {
		studentComplete.StudentFamily.BirthCertificate = req.BirthCertificate
	}
	if req.KIPNumber != "" {
		studentComplete.StudentFamily.KIPNumber = req.KIPNumber
	}

	// Update StudentEnrollment fields
	if req.EnrollmentYear > 0 {
		studentComplete.StudentEnrollment.EnrollmentYear = req.EnrollmentYear
	}
	if req.Curriculum != "" {
		studentComplete.StudentEnrollment.Curriculum = req.Curriculum
	}
	if req.StudentStatus != "" {
		studentComplete.StudentEnrollment.StudentStatus = StudentStatus(req.StudentStatus)
	}
	if req.EntryPath != "" {
		studentComplete.StudentEnrollment.EntryPath = req.EntryPath
	}
	if req.PreviousSchool != "" {
		studentComplete.StudentEnrollment.PreviousSchool = req.PreviousSchool
	}
	if req.ExamNumber != "" {
		studentComplete.StudentEnrollment.ExamNumber = req.ExamNumber
	}

	// Update StudentHealth fields
	if req.BloodType != "" {
		studentComplete.StudentHealth.BloodType = req.BloodType
	}
	if req.Height > 0 {
		studentComplete.StudentHealth.Height = req.Height
	}
	if req.Weight > 0 {
		studentComplete.StudentHealth.Weight = req.Weight
	}
	studentComplete.StudentHealth.MedicalHistory = req.MedicalHistory
	studentComplete.StudentHealth.Disability = req.Disability

	if err := s.repo.UpdateComplete(ctx, studentComplete); err != nil {
		return nil, err
	}
	return studentComplete, nil
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
