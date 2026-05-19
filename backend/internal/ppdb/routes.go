package ppdb

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewPPDBRepository(db)
	svc := NewPPDBService(repo)
	h := NewPPDBHandler(svc)

	group := router.Group("/ppdb")

	// Public routes
	group.Post("/register", h.Register)
	group.Get("/check-status", h.CheckStatus)
	group.Post("/applicants/:id/documents", h.UploadDocument)
	group.Get("/admission-paths", h.GetAdmissionPaths)
	group.Get("/academic-years", h.GetActiveAcademicYears)

	// Admin routes
	admin := group.Group("/admin")
	admin.Use(middleware.Protected())
	admin.Use(auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"))

	admin.Get("/applicants", h.GetApplicants)
	admin.Get("/applicants/:id", h.GetApplicantDetail)
	admin.Post("/applicants/:id/verify", h.VerifyApplicant)
}
