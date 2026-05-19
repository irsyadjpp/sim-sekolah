package logger

import (
	"context"
	"log/slog"
)

// Audit logs immutable business events for compliance and security tracking
func Audit(ctx context.Context, action string, actor string, target string, args ...any) {
	domainArgs := []any{
		slog.String("type", "audit"),
		slog.String("action", action),
		slog.String("actor", actor),
		slog.String("target", target),
	}

	if impersonatorID, ok := ctx.Value("impersonator_id").(string); ok && impersonatorID != "" {
		domainArgs = append(domainArgs, slog.String("impersonator_id", impersonatorID))
	}

	domainArgs = append(domainArgs, args...)

	// Correlate with trace if available and group under domain
	WithContext(ctx).Info("audit_event", slog.Group("domain", domainArgs...))
}
