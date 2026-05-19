package report

import (
	"context"
	"errors"
	"fmt"

	"sim-sekolah/internal/ai"
	"sim-sekolah/internal/assessment"
	"sim-sekolah/internal/classroom"
	"sim-sekolah/internal/enrollment"
	"sim-sekolah/internal/teaching_assignment"
	"sim-sekolah/internal/user"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type ReportService interface {
	GenerateReportsForClassroom(ctx context.Context, classroomID string, semester string) error
	GetByClassroom(ctx context.Context, classroomID, semester string) ([]Report, error)
	GetByID(ctx context.Context, id string) (*Report, error)

	UpsertNotes(ctx context.Context, id string, req UpsertReportNotesRequest) error
	UpsertScore(ctx context.Context, id string, req UpsertReportScoreRequest) error
	UpsertP5(ctx context.Context, id string, req UpsertReportP5Request) error
	UpsertDeepLearning(ctx context.Context, id string, req UpsertReportDeepLearningRequest) error
	UpsertExtracurricular(ctx context.Context, id string, req UpsertReportExtracurricularRequest) error
	UpsertAttendance(ctx context.Context, id string, req UpsertReportAttendanceRequest) error

	FinalizeReport(ctx context.Context, id string) error
	GenerateReportNarrativeAI(ctx context.Context, id string) error
}

type reportService struct {
	repo                   ReportRepository
	enrollmentRepo         enrollment.EnrollmentRepository
	classroomRepo          classroom.ClassroomRepository
	userRepo               user.UserRepository
	teachingAssignmentRepo teaching_assignment.TeachingAssignmentRepository
	aiService              ai.AIService
	db                     *gorm.DB // For raw aggregation queries
}

func NewReportService(
	repo ReportRepository,
	enrollmentRepo enrollment.EnrollmentRepository,
	classroomRepo classroom.ClassroomRepository,
	userRepo user.UserRepository,
	teachingAssignmentRepo teaching_assignment.TeachingAssignmentRepository,
	aiService ai.AIService,
	db *gorm.DB,
) ReportService {
	return &reportService{
		repo:                   repo,
		enrollmentRepo:         enrollmentRepo,
		classroomRepo:          classroomRepo,
		userRepo:               userRepo,
		teachingAssignmentRepo: teachingAssignmentRepo,
		aiService:              aiService,
		db:                     db,
	}
}

// GenerateReportsForClassroom otomatis membuat draft rapor untuk semua siswa yang terdaftar di kelas.
func (s *reportService) GenerateReportsForClassroom(ctx context.Context, classroomID string, semester string) error {
	if err := s.checkHomeroomOrAdmin(ctx, classroomID); err != nil {
		return err
	}

	enrollments, err := s.enrollmentRepo.GetByClassroom(ctx, classroomID)
	if err != nil {
		return errors.New("gagal mengambil data siswa di kelas ini")
	}

	classUUID, _ := uuid.Parse(classroomID)

	for _, e := range enrollments {
		report := &Report{
			ID:          uuid.New(),
			ClassroomID: classUUID,
			StudentID:   e.StudentID,
			Semester:    semester,
		}
		// Insert. Jika sudah ada, DoNothing (di-handle repo)
		_ = s.repo.Create(ctx, report)
	}

	return nil
}

func (s *reportService) GetByClassroom(ctx context.Context, classroomID, semester string) ([]Report, error) {
	// Semua role (Guru, Admin) bisa melihat list rapor
	return s.repo.GetByClassroomAndSemester(ctx, classroomID, semester)
}

func (s *reportService) GetByID(ctx context.Context, id string) (*Report, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *reportService) UpsertNotes(ctx context.Context, id string, req UpsertReportNotesRequest) error {
	rep, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("rapor tidak ditemukan")
	}
	if rep.IsFinalized {
		return errors.New("rapor sudah difinalisasi, tidak bisa diubah")
	}
	if err := s.checkHomeroomOrAdmin(ctx, rep.ClassroomID.String()); err != nil {
		return err
	}

	rep.HomeroomNotes = req.HomeroomNotes
	rep.StudentReflection = req.StudentReflection
	return s.repo.Update(ctx, rep)
}

func (s *reportService) UpsertScore(ctx context.Context, id string, req UpsertReportScoreRequest) error {
	rep, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("rapor tidak ditemukan")
	}
	if rep.IsFinalized {
		return errors.New("rapor sudah difinalisasi")
	}

	// Validasi: Apakah guru ini mengajar mapel ini di kelas ini?
	if err := s.checkSubjectTeacherOrAdmin(ctx, rep.ClassroomID.String(), req.SubjectID); err != nil {
		return err
	}

	repUUID, _ := uuid.Parse(id)
	subUUID, _ := uuid.Parse(req.SubjectID)

	score := &ReportScore{
		ID:                         uuid.New(), // Akan di-ignore jika OnConflict update
		ReportID:                   repUUID,
		SubjectID:                  subUUID,
		FinalScore:                 req.FinalScore,
		CompetencyAchieved:         req.CompetencyAchieved,
		CompetencyNeedsImprovement: req.CompetencyNeedsImprovement,
	}

	return s.repo.UpsertScore(ctx, score)
}

func (s *reportService) UpsertP5(ctx context.Context, id string, req UpsertReportP5Request) error {
	rep, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("rapor tidak ditemukan")
	}
	if rep.IsFinalized {
		return errors.New("rapor sudah difinalisasi")
	}
	if err := s.checkHomeroomOrAdmin(ctx, rep.ClassroomID.String()); err != nil {
		return err
	}

	repUUID, _ := uuid.Parse(id)
	p5 := &ReportP5{
		ID:          uuid.New(),
		ReportID:    repUUID,
		Theme:       req.Theme,
		Description: req.Description,
		Predicate:   req.Predicate,
	}
	return s.repo.UpsertP5(ctx, p5)
}

func (s *reportService) UpsertDeepLearning(ctx context.Context, id string, req UpsertReportDeepLearningRequest) error {
	rep, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("rapor tidak ditemukan")
	}
	if rep.IsFinalized {
		return errors.New("rapor sudah difinalisasi")
	}
	if err := s.checkHomeroomOrAdmin(ctx, rep.ClassroomID.String()); err != nil {
		return err
	}

	repUUID, _ := uuid.Parse(id)
	dl := &ReportDeepLearning{
		ID:               uuid.New(),
		ReportID:         repUUID,
		Aspect:           req.Aspect,
		ObservationNotes: req.ObservationNotes,
	}
	return s.repo.UpsertDeepLearning(ctx, dl)
}

func (s *reportService) UpsertExtracurricular(ctx context.Context, id string, req UpsertReportExtracurricularRequest) error {
	rep, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("rapor tidak ditemukan")
	}
	if rep.IsFinalized {
		return errors.New("rapor sudah difinalisasi")
	}
	if err := s.checkHomeroomOrAdmin(ctx, rep.ClassroomID.String()); err != nil {
		return err
	}

	repUUID, _ := uuid.Parse(id)
	ext := &ReportExtracurricular{
		ID:           uuid.New(),
		ReportID:     repUUID,
		ActivityName: req.ActivityName,
		Predicate:    req.Predicate,
		Description:  req.Description,
	}
	return s.repo.UpsertExtracurricular(ctx, ext)
}

func (s *reportService) UpsertAttendance(ctx context.Context, id string, req UpsertReportAttendanceRequest) error {
	rep, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("rapor tidak ditemukan")
	}
	if rep.IsFinalized {
		return errors.New("rapor sudah difinalisasi")
	}
	if err := s.checkHomeroomOrAdmin(ctx, rep.ClassroomID.String()); err != nil {
		return err
	}

	repUUID, _ := uuid.Parse(id)
	att := &ReportAttendance{
		ID:         uuid.New(),
		ReportID:   repUUID,
		Sick:       req.Sick,
		Permission: req.Permission,
		Unexcused:  req.Unexcused,
	}
	return s.repo.UpsertAttendance(ctx, att)
}

func (s *reportService) FinalizeReport(ctx context.Context, id string) error {
	rep, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("rapor tidak ditemukan")
	}
	if err := s.checkHomeroomOrAdmin(ctx, rep.ClassroomID.String()); err != nil {
		return err
	}

	// Gatekeeper 1: Cek apakah ada mapel yang belum ada nilainya
	assignments, _ := s.teachingAssignmentRepo.GetByClassroom(ctx, rep.ClassroomID.String())
	if len(rep.Scores) < len(assignments) {
		return errors.New("finalisasi ditolak: masih ada mata pelajaran yang belum memiliki nilai")
	}

	// Gatekeeper 2: Cek data absensi
	var att assessment.Attendance
	if err := s.db.Where("student_id = ? AND classroom_id = ? AND semester = ?", rep.StudentID, rep.ClassroomID, rep.Semester).First(&att).Error; err != nil {
		return errors.New("finalisasi ditolak: data absensi belum diisi lengkap untuk siswa ini")
	}

	rep.IsFinalized = true
	rep.Status = "FINAL"
	return s.repo.Update(ctx, rep)
}

func (s *reportService) GenerateReportNarrativeAI(ctx context.Context, id string) error {
	rep, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("rapor tidak ditemukan")
	}

	// 1. Agregasi skor Akademik (HOTS/LOTS)
	type ScoreAggr struct {
		Tingkat  string
		AvgScore float64
	}
	var acadResults []ScoreAggr
	s.db.Raw(`
		SELECT b.tingkat, AVG(n.score) as avg_score
		FROM trx_academic_score n
		JOIN trx_question_bank b ON n.question_id = b.id
		WHERE n.student_id = ? AND n.assessment_type = 'SUMATIF'
		GROUP BY b.tingkat
	`, rep.StudentID).Scan(&acadResults)

	lotsScore := 0.0
	hotsScore := 0.0
	for _, res := range acadResults {
		if res.Tingkat == "LOTS" {
			lotsScore = res.AvgScore
		}
		if res.Tingkat == "HOTS" {
			hotsScore = res.AvgScore
		}
	}

	// 2. Agregasi data Karakter (P5)
	var p5Scores []assessment.AssessmentP5
	s.db.Where("student_id = ?", rep.StudentID).Find(&p5Scores)
	p5Summary := ""
	for _, p := range p5Scores {
		p5Summary += fmt.Sprintf("- Dimensi P5: %s, Capaian: %s\n", p.DimensionID, p.Capaian)
	}

	// 3. Generate Akademik
	acadPrompt := fmt.Sprintf(`
		Tulis deskripsi capaian akademik (max 2 paragraf) untuk siswa bernama %s.
		- Pemahaman Dasar (LOTS): %.2f
		- Penalaran Kritis (HOTS): %.2f
		Instruksi: Apresiasi LOTS, beri dorongan untuk HOTS jika rendah. Jangan gunakan istilah teknis.
	`, rep.Student.FullName, lotsScore, hotsScore)

	acadNarrative, _ := s.aiService.GenerateNarrative(ctx, ai.GenerateNarrativeRequest{
		GenerationType: "RAPOR_AKADEMIK",
		StudentName:    rep.Student.FullName,
		ContextData:    acadPrompt,
	})

	// 4. Generate Karakter
	charPrompt := fmt.Sprintf(`
		Tulis deskripsi perkembangan karakter P5 (max 1 paragraf) untuk siswa bernama %s.
		Data Capaian:
		%s
		Instruksi: Gunakan bahasa yang suportif dan ceritakan bagaimana siswa menunjukkan karakter tersebut dalam projek sekolah.
	`, rep.Student.FullName, p5Summary)

	charNarrative, _ := s.aiService.GenerateNarrative(ctx, ai.GenerateNarrativeRequest{
		GenerationType: "RAPOR_KARAKTER",
		StudentName:    rep.Student.FullName,
		ContextData:    charPrompt,
	})

	rep.AcademicNarrativeAI = acadNarrative
	rep.CharacterNarrativeAI = charNarrative
	return s.repo.Update(ctx, rep)
}

// --- HELPER BOLA ---

func (s *reportService) checkHomeroomOrAdmin(ctx context.Context, classroomID string) error {
	rolesStr, ok := ctx.Value("roles").([]string)
	if !ok {
		return errors.New("unauthorized")
	}

	for _, r := range rolesStr {
		if r == "SUPER_ADMIN" || r == "ADMIN_SEKOLAH" || r == "ADMIN" {
			return nil
		}
	}

	userIDStr := ctx.Value("user_id").(string)
	teacherIDStr, _ := s.userRepo.GetTeacherID(ctx, userIDStr)

	classData, err := s.classroomRepo.GetByID(ctx, classroomID)
	if err != nil || classData.HomeroomTeacherID == nil || classData.HomeroomTeacherID.String() != teacherIDStr {
		return errors.New("forbidden: hanya wali kelas atau admin yang berhak")
	}

	return nil
}

func (s *reportService) checkSubjectTeacherOrAdmin(ctx context.Context, classroomID, subjectID string) error {
	rolesStr, ok := ctx.Value("roles").([]string)
	if !ok {
		return errors.New("unauthorized")
	}

	for _, r := range rolesStr {
		if r == "SUPER_ADMIN" || r == "ADMIN_SEKOLAH" || r == "ADMIN" {
			return nil
		}
	}

	userIDStr := ctx.Value("user_id").(string)
	teacherIDStr, _ := s.userRepo.GetTeacherID(ctx, userIDStr)

	// Cek di teaching_assignments
	isAssigned, err := s.teachingAssignmentRepo.IsTeacherAssigned(ctx, classroomID, subjectID, teacherIDStr)
	if err != nil || !isAssigned {
		return errors.New("forbidden: anda tidak mengajar mata pelajaran ini di kelas ini")
	}

	return nil
}
