package intelligence

import (
	"sim-sekolah/internal/auth"

	"github.com/gofiber/fiber/v2"
)

func RegisterRoutes(router fiber.Router, h *IntelligenceHandler) {
	group := router.Group("/intelligence", auth.Protected())

	group.Get("/students/:student_id/360", h.GetStudent360)
	group.Put("/students/:student_id/profile-ext", h.UpsertProfileExt)
	group.Post("/anecdotal", h.CreateAnecdotal)
	group.Get("/observation-tags", h.GetObservationTags)

	group.Post("/assessment-instruments", h.CreateInstrument)
	group.Post("/assessment-instruments/:instrument_id/results", h.SubmitResults)
	group.Get("/assessment-instruments/:instrument_id/results", h.GetResults)

	group.Get("/alerts", h.GetAlerts)
	group.Put("/alerts/:alert_id/intervene", h.UpdateAlert)
	group.Post("/alerts/trigger-cron", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN"), h.TriggerCron)
}
