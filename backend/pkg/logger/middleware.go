package logger

import (
	"log/slog"
	"time"

	"github.com/gofiber/fiber/v2"
)

func Middleware() fiber.Handler {
	return func(c *fiber.Ctx) error {
		start := time.Now()

		// Continue stack
		err := c.Next()

		latency := time.Since(start)

		// Use WithContext to extract OTel trace IDs if present
		l := WithContext(c.UserContext())

		// Log structured request data following enterprise standards
		l.Info("http_request",
			slog.Group("http",
				slog.String("method", c.Method()),
				slog.String("path", c.Path()),
				slog.Int("status_code", c.Response().StatusCode()),
				slog.Int64("latency_ms", latency.Milliseconds()),
				slog.String("client_ip", c.IP()),
				slog.String("user_agent", c.Get("User-Agent")),
			),
			slog.Group("trace",
				slog.String("request_id", c.Get("X-Request-ID")),
			),
		)

		return err
	}
}
