package routes

import (
	"sim-sekolah/internal/academic_year"
	"sim-sekolah/internal/ai"
	"sim-sekolah/internal/assessment"
	"sim-sekolah/internal/auth"
	"sim-sekolah/internal/classroom"
	"sim-sekolah/internal/cp"
	"sim-sekolah/internal/curriculum"
	"sim-sekolah/internal/deep_learning"
	"sim-sekolah/internal/enrollment"
	"sim-sekolah/internal/grade"
	"sim-sekolah/internal/intelligence"
	"sim-sekolah/internal/learning"
	"sim-sekolah/internal/local_context"
	"sim-sekolah/internal/permission"
	"sim-sekolah/internal/phase"
	"sim-sekolah/internal/ppdb"
	"sim-sekolah/internal/profile_dimension"
	"sim-sekolah/internal/promotion"
	"sim-sekolah/internal/report"
	"sim-sekolah/internal/schedule"
	"sim-sekolah/internal/school"
	"sim-sekolah/internal/student"
	"sim-sekolah/internal/subject"
	"sim-sekolah/internal/system"
	"sim-sekolah/internal/teacher"
	"sim-sekolah/internal/teaching_assignment"
	"sim-sekolah/internal/user"

	"github.com/gofiber/fiber/v2"
	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB, rdb *redis.Client) {
	// Auth
	auth.SetupRoutes(api, db, rdb)

	// Kurikulum
	cp.SetupRoutes(api, db)
	phase.SetupRoutes(api, db)
	subject.SetupRoutes(api, db)
	profile_dimension.SetupRoutes(api, db)
	deep_learning.SetupRoutes(api, db)
	curriculum.SetupRoutes(api, db, rdb)

	// Konteks Lokal
	local_context.SetupRoutes(api, db)

	// Institusi & Aktor
	academic_year.SetupRoutes(api, db)
	school.SetupRoutes(api, db)
	grade.SetupRoutes(api, db)
	teacher.SetupRoutes(api, db)
	student.SetupRoutes(api, db)
	promotion.RegisterRoutes(api, promotion.NewPromotionHandler(promotion.NewPromotionService(promotion.NewPromotionRepository(db))))
	intelligence.RegisterRoutes(api, intelligence.NewIntelligenceHandler(intelligence.NewIntelligenceService(intelligence.NewIntelligenceRepository(db))))

	// Admin User Management
	user.SetupRoutes(api, db)
	permission.RegisterRoutes(api, permission.NewPermissionHandler(permission.NewPermissionService(permission.NewPermissionRepository(db))))

	// Rombel & KBM
	classroom.SetupRoutes(api, db)
	enrollment.SetupRoutes(api, db)
	teaching_assignment.SetupRoutes(api, db)
	schedule.SetupRoutes(api, db)

	// Penilaian / Asesmen
	assessment.SetupRoutes(api, db)

	// Rapor
	report.SetupRoutes(api, db)

	// Pembelajaran (Phase 5)
	learning.SetupRoutes(api, db)

	// Integrasi AI
	ai.SetupRoutes(api, db)

	// PPDB
	ppdb.SetupRoutes(api, db)

	// System Dashboard
	system.SetupRoutes(api, db, rdb)
}
