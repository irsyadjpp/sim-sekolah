package routes

import (
	"sim-sekolah/internal/academic_year"
	"sim-sekolah/internal/ai"
	"sim-sekolah/internal/assessment"
	"sim-sekolah/internal/auth"
	"sim-sekolah/internal/character_intervention"
	"sim-sekolah/internal/classroom"
	"sim-sekolah/internal/cp"
	"sim-sekolah/internal/curriculum"
	"sim-sekolah/internal/deep_learning"
	"sim-sekolah/internal/differentiated_instruction"
	"sim-sekolah/internal/enrollment"
	"sim-sekolah/internal/foundational_skills"
	"sim-sekolah/internal/grade"
	"sim-sekolah/internal/individual_learning_plan"
	"sim-sekolah/internal/intelligence"
	"sim-sekolah/internal/learning"
	"sim-sekolah/internal/learning_experience"
	"sim-sekolah/internal/learning_principle"
	"sim-sekolah/internal/local_context"
	"sim-sekolah/internal/olah_aspect"
	"sim-sekolah/internal/parent_partnership"
	"sim-sekolah/internal/peer_assessment"
	"sim-sekolah/internal/permission"
	"sim-sekolah/internal/phase"
	"sim-sekolah/internal/play_based_learning"
	"sim-sekolah/internal/profile_dimension"
	"sim-sekolah/internal/promotion"
	"sim-sekolah/internal/reading_literacy"
	"sim-sekolah/internal/report"
	"sim-sekolah/internal/schedule"
	"sim-sekolah/internal/school"
	"sim-sekolah/internal/spmb"
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
	olah_aspect.SetupRoutes(api, db)
	learning_principle.SetupRoutes(api, db)
	learning_experience.SetupRoutes(api, db)
	foundational_skills.SetupRoutes(api, db)
	reading_literacy.SetupRoutes(api, db)

	// Phase 3 - Deep Learning Enhancements
	individual_learning_plan.SetupRoutes(api, db)
	differentiated_instruction.SetupRoutes(api, db)
	play_based_learning.SetupRoutes(api, db)

	// Phase 4 - Optimization
	parent_partnership.SetupRoutes(api, db)
	character_intervention.SetupRoutes(api, db)
	peer_assessment.SetupRoutes(api, db)

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

	// SPMB
	spmb.SetupRoutes(api, db)

	// System Dashboard
	system.SetupRoutes(api, db, rdb)
}
