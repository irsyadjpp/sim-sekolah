package assessment

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewAssessmentRepository(db)
	svc := NewAssessmentService(repo)
	h := NewAssessmentHandler(svc)

	// Assessment endpoints
	router.Get("/tugas-mengajar/:assignmentId/penilaian", middleware.Protected(), h.GetAssessments)
	router.Post("/tugas-mengajar/:assignmentId/penilaian", middleware.Protected(), h.CreateAssessment)

	assessment := router.Group("/penilaian")
	assessment.Use(middleware.Protected())

	assessment.Get("/:id", h.GetAssessmentByID)
	assessment.Put("/:id", h.UpdateAssessment)
	assessment.Delete("/:id", h.DeleteAssessment)

	// Scores
	assessment.Get("/:id/nilai", h.GetScores)
	assessment.Post("/:id/nilai", h.UpsertScores)

	// Daily Attendance endpoints
	router.Get("/kelas/:classroomId/kehadiran", middleware.Protected(), h.GetAttendances)
	router.Post("/kelas/:classroomId/kehadiran", middleware.Protected(), h.UpsertAttendances)
}
