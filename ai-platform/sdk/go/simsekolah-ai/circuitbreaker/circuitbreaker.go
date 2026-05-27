package circuitbreaker

import (
	"context"
	"errors"
	"sync"
	"time"
)

// State represents the state of the circuit breaker
type State int

const (
	StateClosed State = iota
	StateOpen
	StateHalfOpen
)

func (s State) String() string {
	switch s {
	case StateClosed:
		return "CLOSED"
	case StateOpen:
		return "OPEN"
	case StateHalfOpen:
		return "HALF_OPEN"
	default:
		return "UNKNOWN"
	}
}

// Config holds circuit breaker configuration
type Config struct {
	Threshold     int           // Number of failures before opening
	Timeout       time.Duration // How long to stay open before trying half-open
	ResetTimeout  time.Duration // How long to stay in half-open
	ReadyToTrip   func(counts Counts) bool
	OnStateChange func(name string, from State, to State)
}

// Counts holds circuit breaker counters
type Counts struct {
	Requests             uint32
	TotalSuccesses       uint32
	TotalFailures        uint32
	ConsecutiveSuccesses uint32
	ConsecutiveFailures  uint32
}

// CircuitBreaker implements the circuit breaker pattern
type CircuitBreaker struct {
	name          string
	config        Config
	state         State
	mu            sync.RWMutex
	counts        Counts
	expiry        time.Time
	lastStateTime time.Time
}

// NewCircuitBreaker creates a new circuit breaker
func NewCircuitBreaker(name string, config Config) *CircuitBreaker {
	if config.ReadyToTrip == nil {
		config.ReadyToTrip = func(counts Counts) bool {
			return counts.ConsecutiveFailures >= uint32(config.Threshold)
		}
	}
	
	return &CircuitBreaker{
		name:   name,
		config: config,
		state:  StateClosed,
	}
}

// Execute runs the given function if the circuit breaker is closed or half-open
func (cb *CircuitBreaker) Execute(ctx context.Context, fn func() error) error {
	// Check if circuit breaker allows execution
	if !cb.allowRequest() {
		return errors.New("circuit breaker is open")
	}
	
	// Execute the function
	err := fn()
	
	// Record the result
	cb.recordResult(err)
	
	return err
}

// allowRequest determines if a request should be allowed
func (cb *CircuitBreaker) allowRequest() bool {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	
	now := time.Now()
	
	switch cb.state {
	case StateClosed:
		return true
	
	case StateOpen:
		// Check if timeout has elapsed
		if now.After(cb.expiry) {
			cb.mu.RUnlock()
			cb.mu.Lock()
			defer cb.mu.Unlock()
			
			// Double check after acquiring write lock
			if cb.state == StateOpen && now.After(cb.expiry) {
				cb.setState(StateHalfOpen, now)
			}
			return cb.state == StateHalfOpen
		}
		return false
	
	case StateHalfOpen:
		return true
	
	default:
		return false
	}
}

// recordResult records the result of a request
func (cb *CircuitBreaker) recordResult(err error) {
	cb.mu.Lock()
	defer cb.mu.Unlock()
	
	cb.counts.Requests++
	
	if err == nil {
		cb.onSuccess()
	} else {
		cb.onFailure()
	}
}

// onSuccess handles successful request
func (cb *CircuitBreaker) onSuccess() {
	cb.counts.TotalSuccesses++
	cb.counts.ConsecutiveSuccesses++
	cb.counts.ConsecutiveFailures = 0
	
	// If in half-open state, close the circuit
	if cb.state == StateHalfOpen {
		cb.setState(StateClosed, time.Now())
	}
}

// onFailure handles failed request
func (cb *CircuitBreaker) onFailure() {
	cb.counts.TotalFailures++
	cb.counts.ConsecutiveFailures++
	cb.counts.ConsecutiveSuccesses = 0
	
	// Check if we should trip the circuit
	if cb.config.ReadyToTrip(cb.counts) {
		cb.setState(StateOpen, time.Now().Add(cb.config.Timeout))
	}
}

// setState changes the circuit breaker state
func (cb *CircuitBreaker) setState(state State, now time.Time) {
	if cb.state == state {
		return
	}
	
	prevState := cb.state
	cb.state = state
	cb.lastStateTime = now
	
	// Update expiry based on new state
	switch state {
	case StateOpen:
		cb.expiry = now.Add(cb.config.Timeout)
	case StateHalfOpen:
		cb.expiry = now.Add(cb.config.ResetTimeout)
	}
	
	// Call state change callback if configured
	if cb.config.OnStateChange != nil {
		cb.config.OnStateChange(cb.name, prevState, state)
	}
}

// State returns the current state of the circuit breaker
func (cb *CircuitBreaker) State() State {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	return cb.state
}

// Counts returns the current counts
func (cb *CircuitBreaker) Counts() Counts {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	return cb.counts
}

// Reset resets the circuit breaker to closed state
func (cb *CircuitBreaker) Reset() {
	cb.mu.Lock()
	defer cb.mu.Unlock()
	
	cb.counts = Counts{}
	cb.setState(StateClosed, time.Now())
}

// Manager manages multiple circuit breakers
type Manager struct {
	breakers map[string]*CircuitBreaker
	mu       sync.RWMutex
}

// NewManager creates a new circuit breaker manager
func NewManager() *Manager {
	return &Manager{
		breakers: make(map[string]*CircuitBreaker),
	}
}

// GetOrCreate gets or creates a circuit breaker for the given name
func (m *Manager) GetOrCreate(name string, config Config) *CircuitBreaker {
	m.mu.RLock()
	if cb, exists := m.breakers[name]; exists {
		m.mu.RUnlock()
		return cb
	}
	m.mu.RUnlock()
	
	m.mu.Lock()
	defer m.mu.Unlock()
	
	// Double check after acquiring write lock
	if cb, exists := m.breakers[name]; exists {
		return cb
	}
	
	cb := NewCircuitBreaker(name, config)
	m.breakers[name] = cb
	return cb
}

// Get gets a circuit breaker by name
func (m *Manager) Get(name string) (*CircuitBreaker, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()
	cb, exists := m.breakers[name]
	return cb, exists
}

// ResetAll resets all circuit breakers
func (m *Manager) ResetAll() {
	m.mu.Lock()
	defer m.mu.Unlock()
	
	for _, cb := range m.breakers {
		cb.Reset()
	}
}

// GetAllStates returns the state of all circuit breakers
func (m *Manager) GetAllStates() map[string]State {
	m.mu.RLock()
	defer m.mu.RUnlock()
	
	states := make(map[string]State)
	for name, cb := range m.breakers {
		states[name] = cb.State()
	}
	return states
}