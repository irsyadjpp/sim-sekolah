package spmb

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"mime/multipart"
	"path/filepath"
	"time"

	"sim-sekolah/config"
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/student"

	"github.com/aws/aws-sdk-go-v2/aws"
	awsconfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/google/uuid"
)

type SPMBService interface {
	Register(ctx context.Context, req RegisterSPMBRequest) (*Applicant, error)
	GetApplicants(ctx context.Context, pagination common.Pagination, status string) ([]Applicant, int64, error)
	GetApplicantByID(ctx context.Context, id string) (*Applicant, error)
	CheckStatusByNIK(ctx context.Context, nik string) (*Applicant, error)

	UploadDocument(ctx context.Context, applicantID string, docType string, fileHeader *multipart.FileHeader) error
	VerifyApplication(ctx context.Context, id string, req VerifySPMBRequest) error
	GetAdmissionPaths(ctx context.Context) ([]AdmissionPath, error)
	GetActiveAcademicYears(ctx context.Context) ([]SPMBAcademicYear, error)
}

type spmbService struct {
	repo SPMBRepository
}

func NewSPMBService(repo SPMBRepository) SPMBService {
	return &spmbService{repo: repo}
}

func (s *spmbService) Register(ctx context.Context, req RegisterSPMBRequest) (*Applicant, error) {
	// 1. Cek apakah NIK sudah pernah mendaftar
	if existing, err := s.repo.GetApplicantByNIK(ctx, req.NIK); err == nil && existing != nil {
		return nil, errors.New("nik sudah terdaftar di sistem SPMB")
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

	// Permendikdasmen No. 3 2025: Age validation on July 1st of current year
	targetYear := time.Now().Year()
	targetDate := time.Date(targetYear, 7, 1, 0, 0, 0, 0, time.UTC)
	years := targetDate.Year() - birthDate.Year()
	months := int(targetDate.Month()) - int(birthDate.Month())
	days := targetDate.Day() - birthDate.Day()
	totalMonths := years*12 + months
	if days < 0 {
		totalMonths--
	}
	if totalMonths < 66 { // 5.5 years = 66 months
		return nil, errors.New("usia calon murid kurang dari 5 tahun 6 bulan pada 1 Juli tahun berjalan")
	}

	var cardIssueDate *time.Time
	if req.FamilyCardIssueDate != "" {
		parsed, err := time.Parse("2006-01-02", req.FamilyCardIssueDate)
		if err != nil {
			return nil, errors.New("format tanggal terbit KK tidak valid (harus YYYY-MM-DD)")
		}
		cardIssueDate = &parsed
	}

	// Validate KK for Domisili path
	paths, err := s.repo.GetAdmissionPaths(ctx)
	if err == nil {
		var isDomisili bool
		for _, p := range paths {
			if p.ID == pathUUID && p.Name == "Domisili" {
				isDomisili = true
				break
			}
		}
		if isDomisili {
			if cardIssueDate == nil {
				return nil, errors.New("tanggal terbit KK wajib diisi untuk Jalur Domisili")
			}
			oneYearAgo := time.Now().AddDate(-1, 0, 0)
			if cardIssueDate.After(oneYearAgo) {
				return nil, errors.New("tanggal terbit Kartu Keluarga harus minimal 1 tahun sebelum tanggal pendaftaran")
			}
		}
	}

	app := &Applicant{
		ID:                  uuid.New(),
		SchoolYearID:        syUUID,
		AdmissionPathID:     pathUUID,
		FullName:            req.FullName,
		NIK:                 req.NIK,
		NISN:                req.NISN,
		BirthPlace:          req.BirthPlace,
		BirthDate:           birthDate,
		Gender:              req.Gender,
		Religion:            req.Religion,
		FamilyCardIssueDate: cardIssueDate,
		Address:             req.Address,
		Village:             req.Village,
		District:            req.District,
		Regency:             req.Regency,
		Province:            req.Province,
		PostalCode:          req.PostalCode,
		DistanceToSchoolKm:  req.DistanceToSchoolKm,
		Status:              "Submitted",
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

func (s *spmbService) GetApplicants(ctx context.Context, pagination common.Pagination, status string) ([]Applicant, int64, error) {
	return s.repo.GetApplicants(ctx, pagination.Limit, pagination.Offset, status)
}

func (s *spmbService) GetApplicantByID(ctx context.Context, id string) (*Applicant, error) {
	return s.repo.GetApplicantByID(ctx, id)
}

func (s *spmbService) CheckStatusByNIK(ctx context.Context, nik string) (*Applicant, error) {
	return s.repo.GetApplicantByNIK(ctx, nik)
}

func (s *spmbService) UploadDocument(ctx context.Context, applicantID string, docType string, fileHeader *multipart.FileHeader) error {
	// Buka file
	file, err := fileHeader.Open()
	if err != nil {
		return err
	}
	defer file.Close()

	// 1. Upload ke SeaweedFS (via S3 API)
	cfg, err := awsconfig.LoadDefaultConfig(ctx,
		awsconfig.WithEndpointResolverWithOptions(aws.EndpointResolverWithOptionsFunc(
			func(service, region string, options ...interface{}) (aws.Endpoint, error) {
				return aws.Endpoint{
					URL:               config.Cfg.Storage.SeaweedFSS3Endpoint,
					SigningRegion:     config.Cfg.Storage.SeaweedFSRegion,
					HostnameImmutable: true,
				}, nil
			},
		)),
		awsconfig.WithCredentialsProvider(aws.CredentialsProviderFunc(
			func(ctx context.Context) (aws.Credentials, error) {
				return aws.Credentials{
					AccessKeyID:     config.Cfg.Storage.SeaweedFSAccessKey,
					SecretAccessKey: config.Cfg.Storage.SeaweedFSSecretKey,
				}, nil
			},
		)),
	)
	if err != nil {
		return errors.New("gagal konfigurasi AWS SDK")
	}

	s3Client := s3.NewFromConfig(cfg)

	// Baca file ke buffer
	buf := new(bytes.Buffer)
	_, err = io.Copy(buf, file)
	if err != nil {
		return err
	}

	// Penamaan file yang unik
	filename := fmt.Sprintf("%s_%s%s", applicantID, docType, filepath.Ext(fileHeader.Filename))
	objectKey := fmt.Sprintf("spmb/documents/%s", filename)

	// Upload ke S3
	_, err = s3Client.PutObject(ctx, &s3.PutObjectInput{
		Bucket: aws.String(config.Cfg.Storage.SeaweedFSBucket),
		Key:    aws.String(objectKey),
		Body:   bytes.NewReader(buf.Bytes()),
	})
	if err != nil {
		return fmt.Errorf("gagal upload ke storage server: %w", err)
	}

	// 2. Simpan path ke DB
	filePath := fmt.Sprintf("s3://%s/%s", config.Cfg.Storage.SeaweedFSBucket, objectKey)

	appUUID, _ := uuid.Parse(applicantID)
	doc := &ApplicantDocument{
		ID:           uuid.New(),
		ApplicantID:  appUUID,
		DocumentType: docType,
		FilePath:     filePath,
	}

	return s.repo.SaveDocument(ctx, doc)
}

func (s *spmbService) VerifyApplication(ctx context.Context, id string, req VerifySPMBRequest) error {
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

		newStudent := &student.StudentComplete{
			MasterStudent: student.MasterStudent{
				ID:         uuid.New(),
				NIK:        app.NIK, // NIK di MasterStudent sebagai data identitas
				SchoolID:   schoolUUID,
				FullName:   app.FullName,
				Gender:     app.Gender,
				BirthPlace: app.BirthPlace,
				BirthDate:  &app.BirthDate,
				Religion:   app.Religion,
			},
			StudentContact: student.StudentContact{
				FullAddress: app.Address,
				Village:     app.Village,
				District:    app.District,
				Regency:     app.Regency,
				Province:    app.Province,
				PostalCode:  app.PostalCode,
			},
			StudentFamily: student.StudentFamily{
				ChildOrder: 1,
				Siblings:   0,
			},
			StudentEnrollment: student.StudentEnrollment{
				NIS:           newNIS,
				NISN:          app.NISN,
				EntryPath:     "SPMB", // Set default entry path
				StudentStatus: student.StatusActive,
			},
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

func (s *spmbService) GetAdmissionPaths(ctx context.Context) ([]AdmissionPath, error) {
	return s.repo.GetAdmissionPaths(ctx)
}

func (s *spmbService) GetActiveAcademicYears(ctx context.Context) ([]SPMBAcademicYear, error) {
	return s.repo.GetActiveAcademicYears(ctx)
}
