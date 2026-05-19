package ppdb

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"path/filepath"
	"time"

	"sim-sekolah/config"
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/student"

	"github.com/google/uuid"
)

type PPDBService interface {
	Register(ctx context.Context, req RegisterPPDBRequest) (*Applicant, error)
	GetApplicants(ctx context.Context, pagination common.Pagination, status string) ([]Applicant, int64, error)
	GetApplicantByID(ctx context.Context, id string) (*Applicant, error)
	CheckStatusByNIK(ctx context.Context, nik string) (*Applicant, error)

	UploadDocument(ctx context.Context, applicantID string, docType string, fileHeader *multipart.FileHeader) error
	VerifyApplication(ctx context.Context, id string, req VerifyPPDBRequest) error
	GetAdmissionPaths(ctx context.Context) ([]AdmissionPath, error)
	GetActiveAcademicYears(ctx context.Context) ([]PPDBAcademicYear, error)
}

type ppdbService struct {
	repo PPDBRepository
}

func NewPPDBService(repo PPDBRepository) PPDBService {
	return &ppdbService{repo: repo}
}

func (s *ppdbService) Register(ctx context.Context, req RegisterPPDBRequest) (*Applicant, error) {
	// 1. Cek apakah NIK sudah pernah mendaftar
	if existing, err := s.repo.GetApplicantByNIK(ctx, req.NIK); err == nil && existing != nil {
		return nil, errors.New("nik sudah terdaftar di sistem PPDB")
	}

	syUUID, err := uuid.Parse(req.SchoolYearID)
	if err != nil {
		return nil, errors.New("invalid school_year_id")
	}

	pathUUID, err := uuid.Parse(req.AdmissionPathID)
	if err != nil {
		return nil, errors.New("invalid admission_path_id")
	}

	birthDate, err := time.Parse("2006-01-02", req.BirthDate)
	if err != nil {
		return nil, errors.New("invalid birth_date format")
	}

	app := &Applicant{
		ID:                 uuid.New(),
		SchoolYearID:       syUUID,
		AdmissionPathID:    pathUUID,
		FullName:           req.FullName,
		NIK:                req.NIK,
		NISN:               req.NISN,
		BirthPlace:         req.BirthPlace,
		BirthDate:          birthDate,
		Gender:             req.Gender,
		Religion:           req.Religion,
		Address:            req.Address,
		Village:            req.Village,
		District:           req.District,
		Regency:            req.Regency,
		Province:           req.Province,
		PostalCode:         req.PostalCode,
		DistanceToSchoolKm: req.DistanceToSchoolKm,
		Status:             "Submitted",
	}

	parents := &ApplicantParent{
		ID:               uuid.New(),
		FatherName:       req.FatherName,
		FatherNIK:        req.FatherNIK,
		FatherOccupation: req.FatherOccupation,
		MotherName:       req.MotherName,
		MotherNIK:        req.MotherNIK,
		MotherOccupation: req.MotherOccupation,
		PhoneNumber:      req.PhoneNumber,
	}

	if err := s.repo.CreateApplication(ctx, app, parents); err != nil {
		return nil, err
	}

	return app, nil
}

func (s *ppdbService) GetApplicants(ctx context.Context, pagination common.Pagination, status string) ([]Applicant, int64, error) {
	return s.repo.GetApplicants(ctx, pagination.Limit, pagination.Offset, status)
}

func (s *ppdbService) GetApplicantByID(ctx context.Context, id string) (*Applicant, error) {
	return s.repo.GetApplicantByID(ctx, id)
}

func (s *ppdbService) CheckStatusByNIK(ctx context.Context, nik string) (*Applicant, error) {
	return s.repo.GetApplicantByNIK(ctx, nik)
}

func (s *ppdbService) UploadDocument(ctx context.Context, applicantID string, docType string, fileHeader *multipart.FileHeader) error {
	// Buka file
	file, err := fileHeader.Open()
	if err != nil {
		return err
	}
	defer file.Close()

	// 1. Upload ke RustFS
	rustfsURL := config.Cfg.Storage.RustFSURL

	// Siapkan multipart form untuk RustFS
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	// Penamaan file yang unik
	filename := fmt.Sprintf("%s_%s%s", applicantID, docType, filepath.Ext(fileHeader.Filename))

	part, err := writer.CreateFormFile("file", filename)
	if err != nil {
		return err
	}

	_, err = io.Copy(part, file)
	if err != nil {
		return err
	}

	writer.Close()

	uploadReq, err := http.NewRequestWithContext(ctx, "POST", rustfsURL+"/upload", body)
	if err != nil {
		return err
	}
	uploadReq.Header.Set("Content-Type", writer.FormDataContentType())

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(uploadReq)
	if err != nil {
		return errors.New("gagal terhubung ke storage server (RustFS)")
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
		return fmt.Errorf("gagal upload ke storage server, status: %d", resp.StatusCode)
	}

	// 2. Simpan path ke DB
	filePath := fmt.Sprintf("%s/download/%s", rustfsURL, filename)

	appUUID, _ := uuid.Parse(applicantID)
	doc := &ApplicantDocument{
		ID:           uuid.New(),
		ApplicantID:  appUUID,
		DocumentType: docType,
		FilePath:     filePath,
	}

	return s.repo.SaveDocument(ctx, doc)
}

func (s *ppdbService) VerifyApplication(ctx context.Context, id string, req VerifyPPDBRequest) error {
	app, err := s.repo.GetApplicantByID(ctx, id)
	if err != nil {
		return errors.New("pendaftar tidak ditemukan")
	}

	if app.Status == "Accepted" || app.Status == "Rejected" {
		return errors.New("pendaftar sudah diproses final (Accepted/Rejected)")
	}

	userIDStr, ok := ctx.Value("user_id").(string)
	if !ok {
		return errors.New("unauthorized")
	}
	userUUID, _ := uuid.Parse(userIDStr)

	log := &VerificationLog{
		ID:              uuid.New(),
		ApplicantID:     app.ID,
		VerifiedBy:      userUUID,
		StatusChangedTo: req.Status,
		Notes:           req.Notes,
	}

	if req.Status == "Accepted" {
		// --- LOGIKA TERIMA SISWA & TRANSFER KE TABEL AKTIF ---

		// Auto Generate NIS (Tahun + Seq)
		count, _ := s.repo.GetYearlyStudentCount(ctx, time.Now().Year())
		newNIS := fmt.Sprintf("%d%03d", time.Now().Year(), count+1)

		// Fetch default school ID
		schoolID, _ := s.repo.GetDefaultSchoolID(ctx)
		schoolUUID, _ := uuid.Parse(schoolID)

		newStudent := &student.Student{
			ID:            uuid.New(),
			SchoolID:      schoolUUID,
			FullName:      app.FullName,
			NIK:           app.NIK,
			NISN:          app.NISN,
			NIS:           newNIS,
			Gender:        app.Gender,
			BirthPlace:    app.BirthPlace,
			BirthDate:     &app.BirthDate,
			Religion:      app.Religion,
			FullAddress:   app.Address,
			Village:       app.Village,
			District:      app.District,
			Regency:       app.Regency,
			Province:      app.Province,
			PostalCode:    app.PostalCode,
			EntryPath:     "PPDB", // Set default entry path
			StudentStatus: student.StatusActive,
		}

		// PPDB Parent to Student Parents
		var parents []student.StudentParent
		if app.Parents != nil {
			if app.Parents.FatherName != "" {
				parents = append(parents, student.StudentParent{
					ID:         uuid.New(),
					ParentType: "FATHER",
					FullName:   app.Parents.FatherName,
					NIK:        app.Parents.FatherNIK,
					Occupation: app.Parents.FatherOccupation,
					Phone:      app.Parents.PhoneNumber,
				})
			}
			if app.Parents.MotherName != "" {
				parents = append(parents, student.StudentParent{
					ID:         uuid.New(),
					ParentType: "MOTHER",
					FullName:   app.Parents.MotherName,
					NIK:        app.Parents.MotherNIK,
					Occupation: app.Parents.MotherOccupation,
					Phone:      app.Parents.PhoneNumber,
				})
			}
		}

		return s.repo.AcceptApplicant(ctx, app, log, newStudent, parents)
	}

	// Jika Verified atau Rejected biasa
	return s.repo.UpdateApplicationStatus(ctx, log)
}

func (s *ppdbService) GetAdmissionPaths(ctx context.Context) ([]AdmissionPath, error) {
	return s.repo.GetAdmissionPaths(ctx)
}

func (s *ppdbService) GetActiveAcademicYears(ctx context.Context) ([]PPDBAcademicYear, error) {
	return s.repo.GetActiveAcademicYears(ctx)
}
