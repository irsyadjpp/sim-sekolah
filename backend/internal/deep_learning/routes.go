package deep_learning

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/deep_learning/elemen_desain"
	"sim-sekolah/internal/deep_learning/tahapan_kognitif"
	"sim-sekolah/internal/deep_learning/tingkat_asesmen"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/deep-learning")
	group.Use(middleware.Protected())

	// Design Element
	edRepo := elemen_desain.NewRepository(db)
	group.Get("/design-element", func(c *fiber.Ctx) error {
		data, err := edRepo.GetAll()
		if err != nil {
			return common.Error(c, 500, "Failed to fetch design elements", err.Error())
		}
		return common.Success(c, "Design elements retrieved successfully", data)
	})

	// Cognitive Stage
	tkRepo := tahapan_kognitif.NewRepository(db)
	group.Get("/cognitive-stage", func(c *fiber.Ctx) error {
		data, err := tkRepo.GetAll()
		if err != nil {
			return common.Error(c, 500, "Failed to fetch cognitive stages", err.Error())
		}
		return common.Success(c, "Cognitive stages retrieved successfully", data)
	})

	// Assessment Level
	taRepo := tingkat_asesmen.NewRepository(db)
	group.Get("/assessment-level", func(c *fiber.Ctx) error {
		data, err := taRepo.GetAll()
		if err != nil {
			return common.Error(c, 500, "Failed to fetch assessment levels", err.Error())
		}
		return common.Success(c, "Assessment levels retrieved successfully", data)
	})
}
