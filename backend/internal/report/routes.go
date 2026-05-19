package report

import (
	"sim-sekolah/internal/ai"
	"sim-sekolah/internal/classroom"
	"sim-sekolah/internal/enrollment"
	"sim-sekolah/internal/teaching_assignment"
	"sim-sekolah/internal/user"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewReportRepository(db)
	enrollmentRepo := enrollment.NewEnrollmentRepository(db)
	classroomRepo := classroom.NewClassroomRepository(db)
	userRepo := user.NewUserRepository(db)
	teachingAssignmentRepo := teaching_assignment.NewTeachingAssignmentRepository(db)
	aiRepo := ai.NewAIRepository()
	aiSvc := ai.NewAIService(aiRepo)

	svc := NewReportService(repo, enrollmentRepo, classroomRepo, userRepo, teachingAssignmentRepo, aiSvc, db)
	h := NewReportHandler(svc)

	// List & Detail
	router.Get("/kelas/:classroomId/rapor", middleware.Protected(), h.GetReportsByClassroom)
	router.Post("/kelas/:classroomId/rapor/buat", middleware.Protected(), h.GenerateReports)

	report := router.Group("/rapor")
	report.Use(middleware.Protected())

	report.Get("/:id", h.GetReportDetail)
	report.Put("/:id/catatan", h.UpsertReportNotes)
	report.Put("/:id/nilai", h.UpsertReportScore)
	report.Put("/:id/p5", h.UpsertP5)
	report.Put("/:id/pembelajaran-mendalam", h.UpsertDeepLearning)
	report.Put("/:id/ekstrakurikuler", h.UpsertExtracurricular)
	report.Put("/:id/kehadiran", h.UpsertAttendance)
	report.Post("/:id/buat-deskripsi-ai", h.GenerateAIDescription)
	report.Patch("/:id/finalisasi", h.FinalizeReport)
}
