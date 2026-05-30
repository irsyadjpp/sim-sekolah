package school

import (
	"context"
	"errors"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type SchoolService interface {
	GetAll(ctx context.Context, pagination common.Pagination, search string) ([]SchoolComplete, int64, error)
	GetByID(ctx context.Context, id string) (*SchoolComplete, error)
	Create(ctx context.Context, req CreateSchoolRequest) (*SchoolComplete, error)
	Update(ctx context.Context, id string, req UpdateSchoolRequest) (*SchoolComplete, error)
	Delete(ctx context.Context, id string) error
}

type schoolService struct {
	repo SchoolRepository
}

// NewSchoolService creates a new SchoolService with an injected SchoolRepository.
func NewSchoolService(repo SchoolRepository) SchoolService {
	return &schoolService{repo: repo}
}

func (s *schoolService) GetAll(ctx context.Context, pagination common.Pagination, search string) ([]SchoolComplete, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset, search)
}

func (s *schoolService) GetByID(ctx context.Context, id string) (*SchoolComplete, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *schoolService) Create(ctx context.Context, req CreateSchoolRequest) (*SchoolComplete, error) {
	schoolComplete := &SchoolComplete{
		MasterSchool: MasterSchool{
			ID:             uuid.New(),
			NPSN:           req.NPSN,
			SchoolName:     req.SchoolName,
			Phone:          req.Phone,
			Email:          req.Email,
			Status:         req.Status,
			OperatingHours: req.OperatingHours,
			BOSStatus:      req.BOSStatus,
		},
		SchoolLocation: SchoolLocation{
			District:    req.District,
			Regency:     req.Regency,
			Province:    req.Province,
			Country:     req.Country,
			Latitude:    req.Latitude,
			Longitude:   req.Longitude,
			FullAddress: req.Address,
			PostalCode:  "",
		},
		SchoolStatistics: SchoolStatistics{
			TotalStudents:   int64(req.TotalStudents),
			MaleStudents:    int64(req.MaleStudents),
			FemaleStudents:  int64(req.FemaleStudents),
			TotalTeachers:   int64(req.TotalTeachers),
			MaleTeachers:    int64(req.MaleTeachers),
			FemaleTeachers:  int64(req.FemaleTeachers),
			TotalStaff:      int64(req.TotalStaff),
			RombelCount:     int64(req.RombelCount),
			StudentRatio:    req.StudentRatio,
			StudentReligion: req.StudentReligion,
		},
		SchoolInfrastructure: SchoolInfrastructure{
			ElectricityCapacity:   int64(req.ElectricityCapacity),
			SignalStatus:          req.SignalStatus,
			WaterSource:           req.WaterSource,
			InternetAccess:        req.InternetAccess,
			ClassroomCount:        int64(req.ClassroomCount),
			ClassroomGoodCount:    int64(req.ClassroomGoodCount),
			ClassroomDamagedCount: int64(req.ClassroomDamagedCount),
			LibraryCount:          int64(req.LibraryCount),
			LabCount:              int64(req.LabCount),
			ToiletStudentCount:    int64(req.ToiletStudentCount),
			ToiletTeacherCount:    int64(req.ToiletTeacherCount),
			InfrastructureSummary: req.InfrastructureSummary,
		},
		SchoolAcademic: SchoolAcademic{
			Curriculum:     req.Curriculum,
			Accreditation:  req.Accreditation,
			EducationForm:  req.EducationForm,
			GraduationData: req.GraduationData,
		},
		SchoolAdministration: SchoolAdministration{
			PrincipalName:  req.PrincipalName,
			OperatorName:   req.OperatorName,
			Vision:         req.Vision,
			VisionMeaning:  req.VisionMeaning,
			Mission:        req.Mission,
			Goal:           req.Goal,
			SyncSystem:     req.SyncSystem,
			SyncCompliance: req.SyncCompliance,
		},
	}

	if err := s.repo.CreateComplete(ctx, schoolComplete); err != nil {
		return nil, err
	}

	// Trigger RAG embedding
	TriggerContextEmbedding(&schoolComplete.MasterSchool)

	return schoolComplete, nil
}

func (s *schoolService) Update(ctx context.Context, id string, req UpdateSchoolRequest) (*SchoolComplete, error) {
	schoolComplete, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("sekolah tidak ditemukan")
	}

	// Update MasterSchool fields
	if req.NPSN != "" {
		schoolComplete.MasterSchool.NPSN = req.NPSN
	}
	if req.SchoolName != "" {
		schoolComplete.MasterSchool.SchoolName = req.SchoolName
	}
	if req.Phone != "" {
		schoolComplete.MasterSchool.Phone = req.Phone
	}
	if req.Email != "" {
		schoolComplete.MasterSchool.Email = req.Email
	}
	if req.Status != "" {
		schoolComplete.MasterSchool.Status = req.Status
	}
	if req.OperatingHours != "" {
		schoolComplete.MasterSchool.OperatingHours = req.OperatingHours
	}
	if req.BOSStatus != "" {
		schoolComplete.MasterSchool.BOSStatus = req.BOSStatus
	}

	// Update SchoolLocation fields
	if req.Address != "" {
		schoolComplete.SchoolLocation.FullAddress = req.Address
	}
	if req.District != "" {
		schoolComplete.SchoolLocation.District = req.District
	}
	if req.Regency != "" {
		schoolComplete.SchoolLocation.Regency = req.Regency
	}
	if req.Province != "" {
		schoolComplete.SchoolLocation.Province = req.Province
	}
	if req.Country != "" {
		schoolComplete.SchoolLocation.Country = req.Country
	}
	if req.Latitude != 0 {
		schoolComplete.SchoolLocation.Latitude = req.Latitude
	}
	if req.Longitude != 0 {
		schoolComplete.SchoolLocation.Longitude = req.Longitude
	}

	// Update SchoolStatistics fields
	if req.TotalStudents != 0 {
		schoolComplete.SchoolStatistics.TotalStudents = int64(req.TotalStudents)
	}
	if req.MaleStudents != 0 {
		schoolComplete.SchoolStatistics.MaleStudents = int64(req.MaleStudents)
	}
	if req.FemaleStudents != 0 {
		schoolComplete.SchoolStatistics.FemaleStudents = int64(req.FemaleStudents)
	}
	if req.TotalTeachers != 0 {
		schoolComplete.SchoolStatistics.TotalTeachers = int64(req.TotalTeachers)
	}
	if req.MaleTeachers != 0 {
		schoolComplete.SchoolStatistics.MaleTeachers = int64(req.MaleTeachers)
	}
	if req.FemaleTeachers != 0 {
		schoolComplete.SchoolStatistics.FemaleTeachers = int64(req.FemaleTeachers)
	}
	if req.TotalStaff != 0 {
		schoolComplete.SchoolStatistics.TotalStaff = int64(req.TotalStaff)
	}
	if req.RombelCount != 0 {
		schoolComplete.SchoolStatistics.RombelCount = int64(req.RombelCount)
	}
	if req.StudentRatio != "" {
		schoolComplete.SchoolStatistics.StudentRatio = req.StudentRatio
	}
	if req.StudentReligion != "" {
		schoolComplete.SchoolStatistics.StudentReligion = req.StudentReligion
	}

	// Update SchoolInfrastructure fields
	if req.ElectricityCapacity != 0 {
		schoolComplete.SchoolInfrastructure.ElectricityCapacity = int64(req.ElectricityCapacity)
	}
	if req.SignalStatus != "" {
		schoolComplete.SchoolInfrastructure.SignalStatus = req.SignalStatus
	}
	if req.WaterSource != "" {
		schoolComplete.SchoolInfrastructure.WaterSource = req.WaterSource
	}
	if req.InternetAccess != "" {
		schoolComplete.SchoolInfrastructure.InternetAccess = req.InternetAccess
	}
	if req.ClassroomCount != 0 {
		schoolComplete.SchoolInfrastructure.ClassroomCount = int64(req.ClassroomCount)
	}
	if req.ClassroomGoodCount != 0 {
		schoolComplete.SchoolInfrastructure.ClassroomGoodCount = int64(req.ClassroomGoodCount)
	}
	if req.ClassroomDamagedCount != 0 {
		schoolComplete.SchoolInfrastructure.ClassroomDamagedCount = int64(req.ClassroomDamagedCount)
	}
	if req.LibraryCount != 0 {
		schoolComplete.SchoolInfrastructure.LibraryCount = int64(req.LibraryCount)
	}
	if req.LabCount != 0 {
		schoolComplete.SchoolInfrastructure.LabCount = int64(req.LabCount)
	}
	if req.ToiletStudentCount != 0 {
		schoolComplete.SchoolInfrastructure.ToiletStudentCount = int64(req.ToiletStudentCount)
	}
	if req.ToiletTeacherCount != 0 {
		schoolComplete.SchoolInfrastructure.ToiletTeacherCount = int64(req.ToiletTeacherCount)
	}
	if req.InfrastructureSummary != "" {
		schoolComplete.SchoolInfrastructure.InfrastructureSummary = req.InfrastructureSummary
	}

	// Update SchoolAcademic fields
	if req.Curriculum != "" {
		schoolComplete.SchoolAcademic.Curriculum = req.Curriculum
	}
	if req.Accreditation != "" {
		schoolComplete.SchoolAcademic.Accreditation = req.Accreditation
	}
	if req.EducationForm != "" {
		schoolComplete.SchoolAcademic.EducationForm = req.EducationForm
	}
	if req.GraduationData != "" {
		schoolComplete.SchoolAcademic.GraduationData = req.GraduationData
	}

	// Update SchoolAdministration fields
	if req.PrincipalName != "" {
		schoolComplete.SchoolAdministration.PrincipalName = req.PrincipalName
	}
	if req.OperatorName != "" {
		schoolComplete.SchoolAdministration.OperatorName = req.OperatorName
	}
	if req.Vision != "" {
		schoolComplete.SchoolAdministration.Vision = req.Vision
	}
	if req.VisionMeaning != "" {
		schoolComplete.SchoolAdministration.VisionMeaning = req.VisionMeaning
	}
	if req.Mission != "" {
		schoolComplete.SchoolAdministration.Mission = req.Mission
	}
	if req.Goal != "" {
		schoolComplete.SchoolAdministration.Goal = req.Goal
	}
	if req.SyncSystem != "" {
		schoolComplete.SchoolAdministration.SyncSystem = req.SyncSystem
	}
	if req.SyncCompliance != "" {
		schoolComplete.SchoolAdministration.SyncCompliance = req.SyncCompliance
	}

	if err := s.repo.UpdateComplete(ctx, schoolComplete); err != nil {
		return nil, err
	}

	// Trigger RAG embedding
	TriggerContextEmbedding(&schoolComplete.MasterSchool)

	return schoolComplete, nil
}

func (s *schoolService) Delete(ctx context.Context, id string) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("sekolah tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}
