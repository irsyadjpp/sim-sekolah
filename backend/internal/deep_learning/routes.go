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
	group := api.Group("/pembelajaran-mendalam")
	group.Use(middleware.Protected())

	// Design Element
	edRepo := elemen_desain.NewRepository(db)
	group.Get("/elemen-desain", func(c *fiber.Ctx) error {
		data, err := edRepo.GetAll()
		if err != nil {
			return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil elemen desain", err)
		}
		return common.Success(c, "Elemen desain berhasil diambil", data)
	})

	// Cognitive Stage
	tkRepo := tahapan_kognitif.NewRepository(db)
	group.Get("/tahapan-kognitif", func(c *fiber.Ctx) error {
		data, err := tkRepo.GetAll()
		if err != nil {
			return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil tahapan kognitif", err)
		}
		return common.Success(c, "Tahapan kognitif berhasil diambil", data)
	})

	// Assessment Level
	taRepo := tingkat_asesmen.NewRepository(db)
	group.Get("/tingkat-asesmen", func(c *fiber.Ctx) error {
		data, err := taRepo.GetAll()
		if err != nil {
			return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil tingkat asesmen", err)
		}
		return common.Success(c, "Tingkat asesmen berhasil diambil", data)
	})
}
