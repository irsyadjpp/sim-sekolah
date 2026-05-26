package cp

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/internal/phase"
	"sim-sekolah/internal/subject"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// SetupRoutes wires CP dependencies and registers routes.
func SetupRoutes(api fiber.Router, db *gorm.DB) {
	cpRepo := NewCPRepository(db)
	detailRepo := NewCPDetailRepository(db)
	subRepo := subject.NewSubjectRepository(db)
	phaseRepo := phase.NewPhaseRepository(db)
	elemRepo := subject.NewSubjectElementRepository(db)
	tpRepo := NewLearningObjectiveRepository(db)
	svc := NewCPService(cpRepo, detailRepo, tpRepo, subRepo, phaseRepo, elemRepo)
	h := NewCPHandler(svc)

	group := api.Group("/capaian-pembelajaran")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAll)
	group.Get("/:id", h.GetByID)

	group.Post("/", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.Create)
	group.Put("/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.Update)
	group.Delete("/:id", auth.RoleMiddleware("SUPER_ADMIN"), h.Delete)

	// Nested Details
	group.Get("/:cpId/detail", h.GetAllDetails)
	group.Post("/:cpId/detail", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.CreateDetail)
	group.Put("/:cpId/detail/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.UpdateDetail)
	group.Delete("/:cpId/detail/:id", auth.RoleMiddleware("SUPER_ADMIN"), h.DeleteDetail)

	// TP (Tujuan Pembelajaran)
	group.Get("/:cpId/tujuan-pembelajaran", h.GetAllObjectives)
	group.Get("/:cpId/tujuan-pembelajaran/:id", h.GetObjectiveByID)
	group.Post("/:cpId/tujuan-pembelajaran", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.CreateObjective)
	group.Put("/:cpId/tujuan-pembelajaran/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.UpdateObjective)
	group.Delete("/:cpId/tujuan-pembelajaran/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.DeleteObjective)
}
