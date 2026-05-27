package config

import (
	"os"
	"strconv"
	"time"
)

// ConfigFromEnv creates configuration from environment variables
func ConfigFromEnv() *Config {
	return &Config{
		DocumentServiceURL:    getEnv("AI_DOCUMENT_SERVICE_URL", "localhost:50051"),
		EmbeddingServiceURL:   getEnv("AI_EMBEDDING_SERVICE_URL", "localhost:50052"),
		RetrievalServiceURL:   getEnv("AI_RETRIEVAL_SERVICE_URL", "localhost:50053"),
		GenerationServiceURL:  getEnv("AI_GENERATION_SERVICE_URL", "localhost:50054"),
		GuardServiceURL:       getEnv("AI_GUARD_SERVICE_URL", "localhost:50055"),
		AuditServiceURL:       getEnv("AI_AUDIT_SERVICE_URL", "localhost:50056"),
		ModerationServiceURL:  getEnv("AI_MODERATION_SERVICE_URL", "localhost:50057"),
		
		MaxConnIdleTime:       getDuration("AI_MAX_CONN_IDLE_TIME", 5*time.Minute),
		MaxConnAge:            getDuration("AI_MAX_CONN_AGE", 30*time.Minute),
		
		UseTLS:                getBool("AI_USE_TLS", false),
		InsecureSkipVerify:    getBool("AI_INSECURE_SKIP_VERIFY", false),
		
		MaxRetries:            getInt("AI_MAX_RETRIES", 3),
		RetryDelay:            getDuration("AI_RETRY_DELAY", 1*time.Second),
		
		CircuitBreakerEnabled: getBool("AI_CIRCUIT_BREAKER_ENABLED", true),
		CircuitBreakerThreshold: getInt("AI_CIRCUIT_BREAKER_THRESHOLD", 5),
		CircuitBreakerTimeout: getDuration("AI_CIRCUIT_BREAKER_TIMEOUT", 30*time.Second),
		
		DefaultTimeout:        getDuration("AI_DEFAULT_TIMEOUT", 30*time.Second),
		
		APIKey:               getEnv("AI_API_KEY", ""),
		JWTToken:              getEnv("AI_JWT_TOKEN", ""),
		
		Debug:                 getBool("AI_DEBUG", false),
	}
}

// Config represents the SDK configuration
type Config struct {
	// Services configuration
	DocumentServiceURL    string
	EmbeddingServiceURL   string
	RetrievalServiceURL   string
	GenerationServiceURL  string
	GuardServiceURL       string
	AuditServiceURL       string
	ModerationServiceURL  string
	
	// Connection settings
	MaxConnIdleTime       time.Duration
	MaxConnAge            time.Duration
	
	// TLS settings
	UseTLS                bool
	InsecureSkipVerify    bool
	
	// Retry settings
	MaxRetries            int
	RetryDelay            time.Duration
	
	// Circuit breaker settings
	CircuitBreakerEnabled bool
	CircuitBreakerThreshold int
	CircuitBreakerTimeout time.Duration
	
	// Timeout settings
	DefaultTimeout        time.Duration
	
	// Authentication
	APIKey                string
	JWTToken              string
	
	// Debugging
	Debug                 bool
}

// Helper functions
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func getBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if boolValue, err := strconv.ParseBool(value); err == nil {
			return boolValue
		}
	}
	return defaultValue
}

func getDuration(key string, defaultValue time.Duration) time.Duration {
	if value := os.Getenv(key); value != "" {
		if duration, err := time.ParseDuration(value); err == nil {
			return duration
		}
	}
	return defaultValue
}