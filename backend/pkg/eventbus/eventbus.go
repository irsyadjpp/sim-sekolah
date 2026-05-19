package eventbus

import (
	"context"
	"sync"
)

// Event merepresentasikan payload data yang dipublikasikan ke event bus
type Event struct {
	Type string
	Data interface{}
}

// Handler merepresentasikan callback function yang menangani event tertentu
type Handler func(ctx context.Context, event Event) error

// EventBus bertugas mengelola langganan (subscription) dan publikasi event secara thread-safe
type EventBus struct {
	mu       sync.RWMutex
	handlers map[string][]Handler
}

// DefaultBus adalah instance global EventBus bawaan aplikasi
var DefaultBus = New()

// New membuat instance EventBus baru yang kosong
func New() *EventBus {
	return &EventBus{
		handlers: make(map[string][]Handler),
	}
}

// Subscribe mendaftarkan handler baru untuk tipe event tertentu
func (eb *EventBus) Subscribe(eventType string, handler Handler) {
	eb.mu.Lock()
	defer eb.mu.Unlock()
	eb.handlers[eventType] = append(eb.handlers[eventType], handler)
}

// Publish memancarkan event ke seluruh handler yang terdaftar secara asinkron di background goroutine
func (eb *EventBus) Publish(ctx context.Context, event Event) {
	eb.mu.RLock()
	handlers, exists := eb.handlers[event.Type]
	eb.mu.RUnlock()

	if !exists {
		return
	}

	for _, handler := range handlers {
		go func(h Handler) {
			_ = h(ctx, event)
		}(handler)
	}
}
