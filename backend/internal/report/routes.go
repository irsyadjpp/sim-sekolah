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
	router.Get("/classrooms/:classroomId/reports", middleware.Protected(), h.GetReportsByClassroom)
	router.Post("/classrooms/:classroomId/reports/generate", middleware.Protected(), h.GenerateReports)

	report := router.Group("/reports")
	report.Use(middleware.Protected())

	report.Get("/:id", h.GetReportDetail)
	report.Put("/:id/notes", h.UpsertReportNotes)
	report.Put("/:id/scores", h.UpsertReportScore)
	report.Put("/:id/p5", h.UpsertP5)
	report.Put("/:id/deep-learning", h.UpsertDeepLearning)
	report.Put("/:id/extracurricular", h.UpsertExtracurricular)
	report.Put("/:id/attendance", h.UpsertAttendance)
	report.Post("/:id/generate-ai-description", h.GenerateAIDescription)
	report.Patch("/:id/finalize", h.FinalizeReport)
}
