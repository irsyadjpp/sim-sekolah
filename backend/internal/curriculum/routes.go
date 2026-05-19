package curriculum

import (
	"sim-sekolah/internal/academic_year"
	"sim-sekolah/internal/system"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB, rdb *redis.Client) {
	repo := NewCurriculumRepository(db)
	ayRepo := academic_year.NewAcademicYearRepository(db)
	queueSvc := system.NewQueueService(rdb, db)

	svc := NewCurriculumService(repo, ayRepo, queueSvc)
	h := NewCurriculumHandler(svc)

	group := router.Group("/curriculum-documents")
	group.Use(middleware.Protected())

	group.Post("/", h.InitializeDocument)
	group.Get("/", h.GetDocuments)
	group.Get("/:id", h.GetDocumentByID)
	group.Get("/readiness", h.CheckReadiness)
	group.Post("/chapters/trigger", h.TriggerChapterFormulation)
	group.Get("/:id/chapters/:chapter_number", h.GetChapter)
	group.Put("/chapters/:chapter_id", h.UpdateChapterContent)
	group.Post("/:id/finalize", h.FinalizeDocument)
	group.Get("/:id/export", h.ExportDocument)
}
