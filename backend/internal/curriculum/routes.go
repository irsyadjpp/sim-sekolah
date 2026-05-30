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
	group.Put("/:id/tipe", h.UpdateCurriculumType)

	// Co-curricular activities routes
	kokurikulerGroup := router.Group("/kokurikuler")
	kokurikulerGroup.Use(middleware.Protected())
	kokurikulerGroup.Get("/", h.GetAllKokurikulerActivities)
	kokurikulerGroup.Get("/:id", h.GetKokurikulerActivityByID)
	kokurikulerGroup.Post("/", h.CreateKokurikulerActivity)
	kokurikulerGroup.Put("/:id", h.UpdateKokurikulerActivity)
	kokurikulerGroup.Delete("/:id", h.DeleteKokurikulerActivity)

	// Extra-curricular activities routes
	ekstrakurikulerGroup := router.Group("/ekstrakurikuler")
	ekstrakurikulerGroup.Use(middleware.Protected())
	ekstrakurikulerGroup.Get("/", h.GetAllEkstrakurikulerActivities)
	ekstrakurikulerGroup.Get("/:id", h.GetEkstrakurikulerActivityByID)
	ekstrakurikulerGroup.Post("/", h.CreateEkstrakurikulerActivity)
	ekstrakurikulerGroup.Put("/:id", h.UpdateEkstrakurikulerActivity)
	ekstrakurikulerGroup.Delete("/:id", h.DeleteEkstrakurikulerActivity)

	// Analysis Data Integration routes (FR 4.2.1-4.2.5)
	analysisIntegrationGroup := router.Group("/analysis-integration")
	analysisIntegrationGroup.Use(middleware.Protected())
	analysisIntegrationGroup.Post("/swot", h.IntegrateSWOTData)
	analysisIntegrationGroup.Post("/root-cause", h.IntegrateRootCauseData)
	analysisIntegrationGroup.Post("/fishbone", h.IntegrateFishboneData)
	analysisIntegrationGroup.Post("/student-needs", h.IntegrateStudentNeedsData)
	analysisIntegrationGroup.Post("/generate-ksp", h.GenerateKSPWithAnalysis)
}
