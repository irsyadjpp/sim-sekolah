package enrollment

import (
	"sim-sekolah/internal/classroom"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewEnrollmentRepository(db)
	classRepo := classroom.NewClassroomRepository(db)
	svc := NewEnrollmentService(repo, classRepo)
	h := NewEnrollmentHandler(svc)

	group := router.Group("/kelas/:classroomId/anggota")
	group.Use(middleware.Protected())

	group.Get("/", h.GetEnrollments)
	group.Post("/", h.EnrollStudent)
	group.Post("/massal", h.BulkEnroll)
	group.Delete("/:enrollmentId", h.UnenrollStudent)
}
