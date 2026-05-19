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

	group := router.Group("/dokumen-kurikulum")
	group.Use(middleware.Protected())

	group.Post("/", h.InitializeDocument)
	group.Get("/", h.GetDocuments)
	group.Get("/:id", h.GetDocumentByID)
	group.Get("/kesiapan", h.CheckReadiness)
	group.Post("/bab/pemicu", h.TriggerChapterFormulation)
	group.Get("/:id/bab/:chapter_number", h.GetChapter)
	group.Put("/bab/:chapter_id", h.UpdateChapterContent)
	group.Post("/:id/finalisasi", h.FinalizeDocument)
	group.Get("/:id/ekspor", h.ExportDocument)
}
