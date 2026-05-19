package enrollment

import (
	"context"
	"errors"
	"fmt"
	"time"

	"sim-sekolah/internal/classroom"

	"github.com/google/uuid"
)

type EnrollmentService interface {
	GetByClassroom(ctx context.Context, classroomID string) ([]Enrollment, error)
	Enroll(ctx context.Context, classroomID string, req CreateEnrollmentRequest) (*Enrollment, error)
	BulkEnroll(ctx context.Context, classroomID string, req BulkEnrollRequest) ([]Enrollment, []string, error)
	Unenroll(ctx context.Context, classroomID, enrollmentID string) error
}

type enrollmentService struct {
	repo          EnrollmentRepository
	classroomRepo classroom.ClassroomRepository
}

func NewEnrollmentService(repo EnrollmentRepository, classroomRepo classroom.ClassroomRepository) EnrollmentService {
	return &enrollmentService{repo: repo, classroomRepo: classroomRepo}
}

func (s *enrollmentService) GetByClassroom(ctx context.Context, classroomID string) ([]Enrollment, error) {
	return s.repo.GetByClassroom(ctx, classroomID)
}

func (s *enrollmentService) Enroll(ctx context.Context, classroomID string, req CreateEnrollmentRequest) (*Enrollment, error) {
	// 1. Get Classroom to check quota
	class, err := s.classroomRepo.GetByID(ctx, classroomID)
	if err != nil {
		return nil, errors.New("kelas tidak ditemukan")
	}

	// 2. Check Current Enrollment Count
	currentCount, err := s.repo.CountByClassroom(ctx, classroomID)
	if err != nil {
		return nil, err
	}

	if int(currentCount) >= class.MaxQuota {
		return nil, fmt.Errorf("kuota kelas %s sudah penuh (maksimal %d siswa)", class.ClassroomName, class.MaxQuota)
	}

	// 3. Cek duplikasi
	enrolled, err := s.repo.IsEnrolled(ctx, classroomID, req.StudentID)
	if err != nil {
		return nil, err
	}
	if enrolled {
		return nil, errors.New("siswa sudah terdaftar di kelas ini")
	}

	classUUID, _ := uuid.Parse(classroomID)
	studentUUID, _ := uuid.Parse(req.StudentID)

	e := &Enrollment{
		ID:             uuid.New(),
		ClassroomID:    classUUID,
		StudentID:      studentUUID,
		EnrollmentDate: time.Now(),
	}

	if err := s.repo.Create(ctx, e); err != nil {
		return nil, err
	}
	return e, nil
}

// BulkEnroll mendaftarkan banyak siswa sekaligus, melewati yang sudah terdaftar.
func (s *enrollmentService) BulkEnroll(ctx context.Context, classroomID string, req BulkEnrollRequest) ([]Enrollment, []string, error) {
	// 1. Get Classroom to check quota
	class, err := s.classroomRepo.GetByID(ctx, classroomID)
	if err != nil {
		return nil, nil, errors.New("kelas tidak ditemukan")
	}

	var created []Enrollment
	var skipped []string
	classUUID, _ := uuid.Parse(classroomID)

	for _, sid := range req.StudentIDs {
		// 2. Check Current Enrollment Count inside loop for bulk safety (though less efficient than one-time check)
		currentCount, err := s.repo.CountByClassroom(ctx, classroomID)
		if err != nil {
			return nil, nil, err
		}

		if int(currentCount) >= class.MaxQuota {
			return created, skipped, fmt.Errorf("kuota kelas %s sudah penuh, berhenti di sisa siswa", class.ClassroomName)
		}

		enrolled, err := s.repo.IsEnrolled(ctx, classroomID, sid)
		if err != nil {
			return nil, nil, err
		}
		if enrolled {
			skipped = append(skipped, sid)
			continue
		}

		studentUUID, _ := uuid.Parse(sid)
		e := &Enrollment{
			ID:             uuid.New(),
			ClassroomID:    classUUID,
			StudentID:      studentUUID,
			EnrollmentDate: time.Now(),
		}
		if err := s.repo.Create(ctx, e); err != nil {
			return nil, nil, err
		}
		created = append(created, *e)
	}

	return created, skipped, nil
}

func (s *enrollmentService) Unenroll(ctx context.Context, classroomID, enrollmentID string) error {
	e, err := s.repo.GetByID(ctx, enrollmentID)
	if err != nil {
		return errors.New("data enrollment tidak ditemukan")
	}
	// Pastikan enrollment ini memang milik classroom yang benar
	if e.ClassroomID.String() != classroomID {
		return errors.New("enrollment ini bukan milik kelas tersebut")
	}
	return s.repo.Delete(ctx, enrollmentID)
}
