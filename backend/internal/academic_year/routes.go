package academic_year

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewAcademicYearRepository(db)
	svc := NewAcademicYearService(repo)
	h := NewAcademicYearHandler(svc)

	group := router.Group("/tahun-ajaran")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAllAcademicYears)
	group.Get("/:id", h.GetAcademicYearByID)
	group.Post("/", h.CreateAcademicYear)
	group.Put("/:id", h.UpdateAcademicYear)
	group.Delete("/:id", h.DeleteAcademicYear)
	group.Patch("/:id/aktifkan", h.SetActiveAcademicYear)
}
