package differentiated_instruction

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewDIRepository(db)
	service := NewDIService(repo)
	handler := NewDIHandler(service)

	registerDIRoutes(group, handler)
}

func registerDIRoutes(router fiber.Router, handler *DIHandler) {
	// DI Strategy routes
	strategies := router.Group("/differentiated-instruction/strategies")
	{
		strategies.Post("", handler.CreateDIStrategy)
		strategies.Get("", handler.GetAllDIStrategies)
		strategies.Get("/active", handler.GetActiveDIStrategies)
		strategies.Get("/target-group/:targetGroup", handler.GetDIStrategiesByTargetGroup)
		strategies.Get("/:id", handler.GetDIStrategyByID)
		strategies.Put("/:id", handler.UpdateDIStrategy)
		strategies.Delete("/:id", handler.DeleteDIStrategy)
	}

	// Module Differentiation routes
	modules := router.Group("/teaching-modules/:moduleId")
	{
		modules.Post("/differentiation", handler.CreateModuleDifferentiation)
		modules.Get("/differentiation/summary", handler.GetModuleDISummary)
		modules.Get("/differentiation", handler.GetDifferentiationsByModuleID)
		modules.Delete("/differentiation", handler.DeleteDifferentiationsByModuleID)
	}

	// Module Differentiation individual routes
	differentiation := router.Group("/differentiated-instruction/differentiations")
	{
		differentiation.Get("/:id", handler.GetModuleDifferentiationByID)
		differentiation.Put("/:id", handler.UpdateModuleDifferentiation)
		differentiation.Delete("/:id", handler.DeleteModuleDifferentiation)
	}

	// Student DI Need routes
	students := router.Group("/students/:studentId")
	{
		students.Get("/differentiation-needs", handler.GetDINeedsByStudentID)
		students.Get("/differentiation-needs/active", handler.GetActiveDINeedsByStudentID)
		students.Get("/differentiation-needs/summary", handler.GetStudentDINeedSummary)
		students.Get("/subjects/:subjectId/differentiation-needs", handler.GetDINeedsByStudentAndSubject)
		students.Post("/differentiation-needs", handler.CreateStudentDINeed)
	}

	// Student DI Need individual routes
	diNeeds := router.Group("/differentiated-instruction/student-needs")
	{
		diNeeds.Get("/:id", handler.GetStudentDINeedByID)
		diNeeds.Put("/:id", handler.UpdateStudentDINeed)
		diNeeds.Delete("/:id", handler.DeleteStudentDINeed)
	}
}
