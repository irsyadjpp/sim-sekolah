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
	router.Get("/teaching-assignments/:assignmentId/assessments", middleware.Protected(), h.GetAssessments)
	router.Post("/teaching-assignments/:assignmentId/assessments", middleware.Protected(), h.CreateAssessment)

	assessment := router.Group("/assessments")
	assessment.Use(middleware.Protected())

	assessment.Get("/:id", h.GetAssessmentByID)
	assessment.Put("/:id", h.UpdateAssessment)
	assessment.Delete("/:id", h.DeleteAssessment)

	// Scores
	assessment.Get("/:id/scores", h.GetScores)
	assessment.Post("/:id/scores", h.UpsertScores)

	// Daily Attendance endpoints
	router.Get("/classrooms/:classroomId/attendances", middleware.Protected(), h.GetAttendances)
	router.Post("/classrooms/:classroomId/attendances", middleware.Protected(), h.UpsertAttendances)
}
