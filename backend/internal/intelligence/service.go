package intelligence

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type IntelligenceService interface {
	GetStudent360Profile(ctx context.Context, studentID string) (*Student360ProfileResponse, error)
	UpsertProfileExt(ctx context.Context, studentID string, req UpsertProfileExtRequest) error
	CreateAnecdotal(ctx context.Context, req CreateAnecdotalRequest, teacherID string) (*AnecdotalObservation, error)
	GetObservationTags(ctx context.Context) ([]ObservationTag, error)

	CreateInstrument(ctx context.Context, req CreateInstrumentRequest) (*AssessmentInstrument, error)
	SubmitResultsBatch(ctx context.Context, instrumentID string, req SubmitResultsBatchRequest) error
	GetResultsByInstrument(ctx context.Context, instrumentID string) ([]StudentAssessmentResult, error)

	GetAlertsByClassroom(ctx context.Context, classroomID string) ([]EarlyWarningAlert, error)
	UpdateAlert(ctx context.Context, alertID string, req EarlyWarningInterventionRequest) error

	CalculateEarlyWarningAlerts(ctx context.Context) error
}

type intelligenceService struct {
	repo IntelligenceRepository
}

func NewIntelligenceService(repo IntelligenceRepository) IntelligenceService {
	return &intelligenceService{repo: repo}
}

func (s *intelligenceService) GetStudent360Profile(ctx context.Context, studentID string) (*Student360ProfileResponse, error) {
	studentUUID, err := uuid.Parse(studentID)
	if err != nil {
		return nil, errors.New("invalid student ID")
	}

	// 1. Ambil Profile Ext
	ext, err := s.repo.GetProfileExt(ctx, studentUUID)
	if err != nil {
		return nil, err
	}

	// 2. Ambil Jurnal Anekdotal
	anecdotals, err := s.repo.GetAnecdotalsByStudent(ctx, studentUUID)
	if err != nil {
		return nil, err
	}

	// 3. Kalkulasi Tag Cloud
	tagCloud := make(map[string]int)
	for _, obs := range anecdotals {
		for _, tag := range obs.Tags {
			tagCloud[tag.TagName]++
		}
	}

	// 4. Ambil Progress Akademik (TP Progress)
	academicProgress, err := s.repo.GetAcademicProgressByStudent(ctx, studentUUID)
	if err != nil {
		return nil, err
	}

	// 5. Ambil EWS Alerts
	alerts, err := s.repo.GetAlertsByStudent(ctx, studentUUID)
	if err != nil {
		return nil, err
	}

	// 6. Fetch basic student info from master_student
	var studentBasic struct {
		FullName string
		NIS      string
		NISN     string
	}
	repoImpl, ok := s.repo.(*intelligenceRepository)
	if ok {
		err = repoImpl.db.WithContext(ctx).Table("master_student").
			Select("full_name, nis, nisn").
			Where("id = ?", studentUUID).
			Scan(&studentBasic).Error
		if err != nil {
			return nil, errors.New("student basic info not found")
		}
	}

	return &Student360ProfileResponse{
		StudentID:          studentID,
		FullName:           studentBasic.FullName,
		NIS:                studentBasic.NIS,
		NISN:               studentBasic.NISN,
		ProfileExt:         ext,
		Anecdotals:         anecdotals,
		TagCloud:           tagCloud,
		AcademicProgress:   academicProgress,
		EarlyWarningAlerts: alerts,
	}, nil
}

func (s *intelligenceService) UpsertProfileExt(ctx context.Context, studentID string, req UpsertProfileExtRequest) error {
	studentUUID, err := uuid.Parse(studentID)
	if err != nil {
		return errors.New("invalid student ID")
	}

	ext := &StudentProfileExt{
		StudentID:         studentUUID,
		LearningStyle:     req.LearningStyle,
		DominantInterests: req.DominantInterests,
		SpecialNeedsNotes: req.SpecialNeedsNotes,
		BaselineLiteracy:  req.BaselineLiteracy,
		BaselineNumeracy:  req.BaselineNumeracy,
		UpdatedAt:         time.Now(),
	}

	return s.repo.UpsertProfileExt(ctx, ext)
}

func (s *intelligenceService) CreateAnecdotal(ctx context.Context, req CreateAnecdotalRequest, teacherID string) (*AnecdotalObservation, error) {
	studentUUID, err := uuid.Parse(req.StudentID)
	if err != nil {
		return nil, errors.New("invalid student ID")
	}

	teacherUUID, err := uuid.Parse(teacherID)
	if err != nil {
		return nil, errors.New("invalid teacher ID")
	}

	obs := &AnecdotalObservation{
		ID:              uuid.New(),
		StudentID:       studentUUID,
		TeacherID:       teacherUUID,
		ObservationDate: time.Now(),
		ContextActivity: req.ContextActivity,
		Notes:           req.Notes,
		CreatedAt:       time.Now(),
	}

	err = s.repo.CreateAnecdotal(ctx, obs, req.TagIDs)
	if err != nil {
		return nil, err
	}

	// Fetch fully loaded anecdotal observation to return (preloaded with tags)
	anecdotals, err := s.repo.GetAnecdotalsByStudent(ctx, studentUUID)
	if err == nil && len(anecdotals) > 0 {
		for _, a := range anecdotals {
			if a.ID == obs.ID {
				return &a, nil
			}
		}
	}

	return obs, nil
}

func (s *intelligenceService) GetObservationTags(ctx context.Context) ([]ObservationTag, error) {
	return s.repo.GetObservationTags(ctx)
}

func (s *intelligenceService) CreateInstrument(ctx context.Context, req CreateInstrumentRequest) (*AssessmentInstrument, error) {
	objectiveUUID, err := uuid.Parse(req.LearningObjectiveID)
	if err != nil {
		return nil, errors.New("invalid learning objective ID")
	}

	var moduleUUID *uuid.UUID
	if req.TeachingModuleID != "" {
		u, err := uuid.Parse(req.TeachingModuleID)
		if err != nil {
			return nil, errors.New("invalid teaching module ID")
		}
		moduleUUID = &u
	}

	inst := &AssessmentInstrument{
		ID:                  uuid.New(),
		TeachingModuleID:    moduleUUID,
		LearningObjectiveID: objectiveUUID,
		Title:               req.Title,
		AssessmentType:      req.AssessmentType,
		ScoringMethod:       req.ScoringMethod,
		CreatedAt:           time.Now(),
	}

	err = s.repo.CreateInstrument(ctx, inst)
	if err != nil {
		return nil, err
	}
	return inst, nil
}

func (s *intelligenceService) SubmitResultsBatch(ctx context.Context, instrumentID string, req SubmitResultsBatchRequest) error {
	instUUID, err := uuid.Parse(instrumentID)
	if err != nil {
		return errors.New("invalid instrument ID")
	}

	inst, err := s.repo.GetInstrumentByID(ctx, instUUID)
	if err != nil {
		return errors.New("assessment instrument not found")
	}

	var results []StudentAssessmentResult
	for _, item := range req.Results {
		studentUUID, err := uuid.Parse(item.StudentID)
		if err != nil {
			return errors.New("invalid student ID in batch: " + item.StudentID)
		}

		res := StudentAssessmentResult{
			ID:                uuid.New(),
			InstrumentID:      instUUID,
			StudentID:         studentUUID,
			RubricAchievement: item.RubricAchievement,
			NarrativeFeedback: item.NarrativeFeedback,
			AssessedAt:        time.Now(),
		}

		if inst.ScoringMethod == "NUMERIC" {
			if item.NumericScore == nil {
				return fmt.Errorf("numeric_score is required for numeric scoring method for student %s", item.StudentID)
			}
			res.NumericScore = item.NumericScore
		}

		results = append(results, res)
	}

	return s.repo.SubmitResultsBatch(ctx, results)
}

func (s *intelligenceService) GetResultsByInstrument(ctx context.Context, instrumentID string) ([]StudentAssessmentResult, error) {
	instUUID, err := uuid.Parse(instrumentID)
	if err != nil {
		return nil, errors.New("invalid instrument ID")
	}
	return s.repo.GetResultsByInstrument(ctx, instUUID)
}

func (s *intelligenceService) GetAlertsByClassroom(ctx context.Context, classroomID string) ([]EarlyWarningAlert, error) {
	classUUID, err := uuid.Parse(classroomID)
	if err != nil {
		return nil, errors.New("invalid classroom ID")
	}
	return s.repo.GetAlertsByClassroom(ctx, classUUID)
}

func (s *intelligenceService) UpdateAlert(ctx context.Context, alertID string, req EarlyWarningInterventionRequest) error {
	alertUUID, err := uuid.Parse(alertID)
	if err != nil {
		return errors.New("invalid alert ID")
	}

	var resolvedAt *time.Time
	if req.Status == "RESOLVED" {
		t := time.Now()
		resolvedAt = &t
	}

	return s.repo.UpdateAlert(ctx, alertUUID, req.Status, req.InterventionNotes, resolvedAt)
}

func (s *intelligenceService) CalculateEarlyWarningAlerts(ctx context.Context) error {
	repoImpl, ok := s.repo.(*intelligenceRepository)
	if !ok {
		return errors.New("cannot cast repository to intelligenceRepository")
	}

	// 1. Dapatkan daftar semua rombel (classroom) yang aktif
	type Classroom struct {
		ID uuid.UUID
	}
	var classrooms []Classroom
	err := repoImpl.db.WithContext(ctx).Table("master_classroom").Select("id").Find(&classrooms).Error
	if err != nil {
		return err
	}

	for _, class := range classrooms {
		// 2. Ambil semua murid di rombel tersebut
		type StudentEnrollment struct {
			StudentID uuid.UUID `gorm:"column:student_id"`
		}
		var enrollments []StudentEnrollment
		err = repoImpl.db.WithContext(ctx).
			Table("trx_enrollment").
			Select("student_id").
			Where("classroom_id = ?", class.ID).
			Find(&enrollments).Error
		if err != nil {
			continue
		}

		for _, enr := range enrollments {
			// A. DETEKSI ABSENSI (ATTENDANCE_DROP): alpa (A) >= 3 kali dalam 7 hari terakhir
			var attendanceDropCount int64
			err = repoImpl.db.WithContext(ctx).
				Table("trx_daily_attendance").
				Where("student_id = ? AND status = 'A' AND date >= ?", enr.StudentID, time.Now().AddDate(0, 0, -7)).
				Count(&attendanceDropCount).Error

			if err == nil && attendanceDropCount >= 3 {
				exists, _ := s.repo.CheckAlertExists(ctx, enr.StudentID, "ATTENDANCE_DROP")
				if !exists {
					alert := &EarlyWarningAlert{
						ID:            uuid.New(),
						StudentID:     enr.StudentID,
						ClassroomID:   class.ID,
						AlertType:     "ATTENDANCE_DROP",
						SeverityLevel: "HIGH",
						TriggerReason: fmt.Sprintf("Siswa terdeteksi alpa sebanyak %d kali dalam 7 hari terakhir.", attendanceDropCount),
						Status:        "OPEN",
						DetectedAt:    time.Now(),
					}
					_ = s.repo.CreateAlert(ctx, alert)
				}
			}

			// B. DETEKSI LITERASI/BEHAVIOR (LITERACY_DELAY / BEHAVIORAL_CONCERN):
			// tag sentiment 'NEEDS_HELP' >= 2 kali dalam 7 hari terakhir
			type TagCount struct {
				TagID    string
				Category string
				Count    int
			}
			var tagsNeedHelp []TagCount
			err = repoImpl.db.WithContext(ctx).Raw(`
				SELECT t.id as tag_id, t.category as category, count(*) as count
				FROM trx_anecdotal_observation o
				JOIN trx_observation_tag_mapping m ON o.id = m.observation_id
				JOIN sys_observation_tags t ON m.tag_id = t.id
				WHERE o.student_id = ? AND t.sentiment = 'NEEDS_HELP' AND o.observation_date >= ?
				GROUP BY t.id, t.category
			`, enr.StudentID, time.Now().AddDate(0, 0, -7)).Scan(&tagsNeedHelp).Error

			if err == nil {
				for _, tc := range tagsNeedHelp {
					if tc.Count >= 2 {
						alertType := "BEHAVIORAL_CONCERN"
						severity := "MEDIUM"
						if tc.TagID == "HAB_READING_DELAY" || tc.Category == "Habits" {
							alertType = "LITERACY_DELAY"
							severity = "HIGH"
						}

						exists, _ := s.repo.CheckAlertExists(ctx, enr.StudentID, alertType)
						if !exists {
							alert := &EarlyWarningAlert{
								ID:            uuid.New(),
								StudentID:     enr.StudentID,
								ClassroomID:   class.ID,
								AlertType:     alertType,
								SeverityLevel: severity,
								TriggerReason: fmt.Sprintf("Tercatat tag perilaku negatif '%s' sebanyak %d kali dalam seminggu terakhir.", tc.TagID, tc.Count),
								Status:        "OPEN",
								DetectedAt:    time.Now(),
							}
							_ = s.repo.CreateAlert(ctx, alert)
						}
					}
				}
			}
		}
	}

	return nil
}
