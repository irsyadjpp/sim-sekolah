package intelligence

import (
	"sim-sekolah/internal/auth"

	"github.com/gofiber/fiber/v2"
)

func RegisterRoutes(router fiber.Router, h *IntelligenceHandler) {
	group := router.Group("/kecerdasan-sistem", auth.Protected())

	group.Get("/murid/:student_id/360", h.GetStudent360)
	group.Put("/murid/:student_id/profil-eksternal", h.UpsertProfileExt)
	group.Post("/anekdot", h.CreateAnecdotal)
	group.Get("/tag-observasi", h.GetObservationTags)

	group.Post("/instrumen-penilaian", h.CreateInstrument)
	group.Post("/instrumen-penilaian/:instrument_id/hasil", h.SubmitResults)
	group.Get("/instrumen-penilaian/:instrument_id/hasil", h.GetResults)

	group.Get("/peringatan", h.GetAlerts)
	group.Put("/peringatan/:alert_id/intervensi", h.UpdateAlert)
	group.Post("/peringatan/pemicu-cron", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN"), h.TriggerCron)
}
