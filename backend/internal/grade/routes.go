package grade

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewGradeRepository(db)
	svc := NewGradeService(repo)
	h := NewGradeHandler(svc)

	group := router.Group("/tingkat-kelas")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAllGrades)
	group.Get("/:id", h.GetGradeByID)
	group.Get("/fase/:phaseId", h.GetGradesByPhase)
	group.Post("/", h.CreateGrade)
	group.Put("/:id", h.UpdateGrade)
	group.Delete("/:id", h.DeleteGrade)
}
