package teaching_assignment

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewTeachingAssignmentRepository(db)
	svc := NewTeachingAssignmentService(repo)
	h := NewTeachingAssignmentHandler(svc)

	group := router.Group("/kelas/:classroomId/tugas-mengajar")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAssignments)
	group.Post("/", h.CreateAssignment)
	group.Put("/:id", h.UpdateAssignment)
	group.Delete("/:id", h.DeleteAssignment)
}
