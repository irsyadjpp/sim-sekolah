package logger

import (
	"context"
	"log/slog"
	"os"
	"runtime"
	"sim-sekolah/config"

	"go.opentelemetry.io/contrib/bridges/otelslog"
	"go.opentelemetry.io/otel/log/global"
)

var Log *slog.Logger

func InitLogger() {
	env := config.Cfg.App.Env
	if env == "" {
		env = os.Getenv("APP_ENV")
	}

	var handler slog.Handler

	if env == "production" {
		// Format JSON for production (ELK/Loki/Datadog compatible)
		handler = slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
			Level:     slog.LevelInfo,
			AddSource: true, // Automatically adds "caller" (file & line)
		})
	} else {
		// Format Text Pretty for development terminal
		handler = slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
			Level:     slog.LevelDebug,
			AddSource: true,
		})
	}

	// 2. OpenTelemetry Handler (Optional)
	// If you want to use otelslog bridge, you can wrap the handler
	// but for standard enterprise setups, reading from Stdout is preferred.
	_ = otelslog.NewHandler(config.Cfg.App.Name, otelslog.WithLoggerProvider(global.GetLoggerProvider()))

	// Set logger global with "service" field
	logger := slog.New(handler).With(
		slog.String("service", config.Cfg.App.Name),
		slog.String("environment", env),
	)

	// Also wrap with OTel if possible, but slog doesn't have a built-in Tee handler.
	// For now, let's prioritize the JSON Stdout as it's the primary requirement.
	// Most log aggregators read from Stdout.

	Log = logger
	slog.SetDefault(Log)
}

// Helpers for structured logging that match the user's requested signature
func Info(msg string, args ...any) {
	slog.Info(msg, args...)
}

func InfoWithContext(ctx context.Context, msg string, args ...any) {
	WithContext(ctx).Info(msg, args...)
}

func Error(msg string, err error, args ...any) {
	if err != nil {
		args = append(args, slog.Group("error",
			slog.String("message", err.Error()),
			slog.String("stack_trace", getStackTrace()),
		))
	}
	slog.Error(msg, args...)
}

func ErrorWithContext(ctx context.Context, msg string, err error, args ...any) {
	if err != nil {
		args = append(args, slog.Group("error",
			slog.String("message", err.Error()),
			slog.String("stack_trace", getStackTrace()),
		))
	}
	WithContext(ctx).Error(msg, args...)
}

func Fatal(msg string, err error, args ...any) {
	if err != nil {
		args = append(args, slog.Group("error",
			slog.String("message", err.Error()),
			slog.String("stack_trace", getStackTrace()),
		))
	}
	slog.Error(msg, args...)
	os.Exit(1)
}

func Warn(msg string, err error, args ...any) {
	if err != nil {
		args = append(args, slog.Group("error", slog.String("message", err.Error())))
	}
	slog.Warn(msg, args...)
}

func Debug(msg string, args ...any) {
	slog.Debug(msg, args...)
}

func getStackTrace() string {
	buf := make([]byte, 2048)
	n := runtime.Stack(buf, false)
	return string(buf[:n])
}
