package classroom

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewClassroomRepository(db)
	svc := NewClassroomService(repo)
	h := NewClassroomHandler(svc)

	group := router.Group("/kelas")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAllClassrooms)
	group.Get("/:id", h.GetClassroomByID)
	group.Post("/", h.CreateClassroom)
	group.Put("/:id", h.UpdateClassroom)
	group.Delete("/:id", h.DeleteClassroom)
}
