package logger

import (
	"context"
	"log/slog"

	"go.opentelemetry.io/otel/trace"
)

// ExtractTraceFields retrieves OTel trace and span IDs from context for logging
func ExtractTraceFields(ctx context.Context) slog.Attr {
	span := trace.SpanFromContext(ctx)
	if !span.SpanContext().IsValid() {
		return slog.Attr{}
	}

	return slog.Group("trace",
		slog.String("trace_id", span.SpanContext().TraceID().String()),
		slog.String("span_id", span.SpanContext().SpanID().String()),
	)
}

// WithContext returns a logger decorated with trace IDs from context
func WithContext(ctx context.Context) *slog.Logger {
	attr := ExtractTraceFields(ctx)
	if attr.Key == "" {
		return Log
	}
	return Log.With(attr)
}
