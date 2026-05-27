# gRPC Client Migration Guide

This guide explains how to migrate from hand-written gRPC client wrappers to the new AI Platform Go SDK.

## Overview

The backend currently uses hand-written gRPC client wrappers. These should be migrated to use the new AI Platform Go SDK which provides:

- Centralized connection management
- Circuit breaker pattern for resilience
- Consistent error handling
- Environment-based configuration
- Automatic retry logic
- Health check capabilities

## Migration Steps

### Before (Hand-written wrapper)

```go
package grpc

import (
	"context"
	"fmt"
	"time"
	
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	
	"sim-sekolah/internal/ai/grpc/pb/embeddingservice"
)

type EmbeddingServiceClient struct {
	conn *grpc.ClientConn
	embeddingservice.EmbeddingServiceClient
}

func NewEmbeddingServiceClient(address string) (*EmbeddingServiceClient, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	conn, err := grpc.DialContext(ctx, address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithBlock(),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to embedding service: %w", err)
	}
	
	return &EmbeddingServiceClient{
		conn:                   conn,
		EmbeddingServiceClient: embeddingservice.NewEmbeddingServiceClient(conn),
	}, nil
}

func (c *EmbeddingServiceClient) Close() error {
	return c.conn.Close()
}
```

### After (Using SDK)

```go
package grpc

import (
	"context"
	"fmt"
	"time"
	
	"github.com/simsekolah/ai-platform-sdk-go"
	"github.com/simsekolah/ai-platform-sdk-go/config"
	
	"sim-sekolah/internal/ai/grpc/pb/embeddingservice"
)

type EmbeddingServiceClient struct {
	sdkClient     *simsekolah.Client
	grpcClient    embeddingservice.EmbeddingServiceClient
	circuitBreaker *simsekolah.CircuitBreaker
}

func NewEmbeddingServiceClient() (*EmbeddingServiceClient, error) {
	// Load configuration from environment
	cfg := config.ConfigFromEnv()
	
	// Create SDK client
	sdkClient, err := simsekolah.NewClient(cfg)
	if err != nil {
		return nil, fmt.Errorf("failed to create SDK client: %w", err)
	}
	
	// Get gRPC connection
	conn := sdkClient.GetEmbeddingServiceClient()
	
	// Create circuit breaker
	cb := simsekolah.NewCircuitBreaker("embedding-service", simsekolah.Config{
		Threshold:     cfg.CircuitBreakerThreshold,
		Timeout:       cfg.CircuitBreakerTimeout,
		ResetTimeout:  10 * time.Second,
	})
	
	return &EmbeddingServiceClient{
		sdkClient:     sdkClient,
		grpcClient:    embeddingservice.NewEmbeddingServiceClient(conn),
		circuitBreaker: cb,
	}, nil
}

func (c *EmbeddingServiceClient) CreateEmbedding(ctx context.Context, req *embeddingservice.CreateEmbeddingRequest) (*embeddingservice.CreateEmbeddingResponse, error) {
	var response *embeddingservice.CreateEmbeddingResponse
	var err error
	
	// Execute with circuit breaker
	err = c.circuitBreaker.Execute(ctx, func() error {
		var innerErr error
		response, innerErr = c.grpcClient.CreateEmbedding(ctx, req)
		return innerErr
	})
	
	if err != nil {
		return nil, fmt.Errorf("embedding service call failed: %w", err)
	}
	
	return response, nil
}

func (c *EmbeddingServiceClient) Close() error {
	return c.sdkClient.Close()
}

func (c *EmbeddingServiceClient) HealthCheck(ctx context.Context) error {
	health := c.sdkClient.HealthCheck(ctx)
	if !health["embedding"] {
		return fmt.Errorf("embedding service is unhealthy")
	}
	return nil
}
```

## Key Changes

### 1. Configuration
- **Before**: Hardcoded connection parameters passed to constructor
- **After**: Environment-based configuration using `config.ConfigFromEnv()`

### 2. Connection Management
- **Before**: Each client creates its own gRPC connection
- **After**: SDK manages all connections centrally with connection pooling

### 3. Error Handling
- **Before**: Basic error handling
- **After**: Circuit breaker pattern with automatic failover

### 4. Health Checks
- **Before**: No built-in health checks
- **After**: Centralized health check functionality

### 5. Resilience
- **Before**: No retry logic or circuit breaking
- **After**: Built-in retry, timeout, and circuit breaker

## Environment Variables

Configure services using environment variables:

```bash
# Service URLs
export AI_EMBEDDING_SERVICE_URL=localhost:50052
export AI_RETRIEVAL_SERVICE_URL=localhost:50053
export AI_GENERATION_SERVICE_URL=localhost:50054

# Circuit breaker settings
export AI_CIRCUIT_BREAKER_ENABLED=true
export AI_CIRCUIT_BREAKER_THRESHOLD=5
export AI_CIRCUIT_BREAKER_TIMEOUT=30s

# Retry settings
export AI_MAX_RETRIES=3
export AI_RETRY_DELAY=1s
```

## Migration Checklist

For each service client:

- [ ] Replace connection logic with SDK client creation
- [ ] Add circuit breaker wrapper to all service calls
- [ ] Update error handling to use SDK error types
- [ ] Add health check method
- [ ] Update Close() method to use SDK Close()
- [ ] Remove hardcoded connection parameters
- [ ] Update tests to use new client structure
- [ ] Update documentation

## Service-Specific Examples

### Generation Service

```go
type GenerationServiceClient struct {
	sdkClient     *simsekolah.Client
	grpcClient    generationservice.GenerationServiceClient
	circuitBreaker *simsekolah.CircuitBreaker
}

func NewGenerationServiceClient() (*GenerationServiceClient, error) {
	cfg := config.ConfigFromEnv()
	sdkClient, err := simsekolah.NewClient(cfg)
	if err != nil {
		return nil, err
	}
	
	conn := sdkClient.GetGenerationServiceClient()
	cb := simsekolah.NewCircuitBreaker("generation-service", simsekolah.Config{
		Threshold:     cfg.CircuitBreakerThreshold,
		Timeout:       cfg.CircuitBreakerTimeout,
		ResetTimeout:  10 * time.Second,
	})
	
	return &GenerationServiceClient{
		sdkClient:     sdkClient,
		grpcClient:    generationservice.NewGenerationServiceClient(conn),
		circuitBreaker: cb,
	}, nil
}
```

### Document Service

```go
type DocumentServiceClient struct {
	sdkClient     *simsekolah.Client
	grpcClient    documentservice.DocumentServiceClient
	circuitBreaker *simsekolah.CircuitBreaker
}

func NewDocumentServiceClient() (*DocumentServiceClient, error) {
	cfg := config.ConfigFromEnv()
	sdkClient, err := simsekolah.NewClient(cfg)
	if err != nil {
		return nil, err
	}
	
	conn := sdkClient.GetDocumentServiceClient()
	cb := simsekolah.NewCircuitBreaker("document-service", simsekolah.Config{
		Threshold:     cfg.CircuitBreakerThreshold,
		Timeout:       cfg.CircuitBreakerTimeout,
		ResetTimeout:  10 * time.Second,
	})
	
	return &DocumentServiceClient{
		sdkClient:     sdkClient,
		grpcClient:    documentservice.NewDocumentServiceClient(conn),
		circuitBreaker: cb,
	}, nil
}
```

## Testing

Update tests to use the new SDK-based clients:

```go
func TestEmbeddingServiceClient(t *testing.T) {
	// Set test environment variables
	os.Setenv("AI_EMBEDDING_SERVICE_URL", "localhost:50052")
	os.Setenv("AI_CIRCUIT_BREAKER_ENABLED", "false")
	
	client, err := NewEmbeddingServiceClient()
	require.NoError(t, err)
	defer client.Close()
	
	// Test functionality
	ctx := context.Background()
	resp, err := client.CreateEmbedding(ctx, &embeddingservice.CreateEmbeddingRequest{
		Text: "test text",
		Model: "bge-m3",
	})
	
	require.NoError(t, err)
	assert.NotNil(t, resp)
}
```

## Benefits of Migration

1. **Consistency**: All services use the same connection management
2. **Resilience**: Built-in circuit breaker and retry logic
3. **Maintainability**: Centralized configuration and error handling
4. **Observability**: Better monitoring and health checks
5. **Security**: Consistent TLS and authentication handling
6. **Performance**: Connection pooling and keepalive management

## Rollback Plan

If issues arise during migration:

1. Keep old client files as backup
2. Use feature flags to switch between old and new implementations
3. Monitor error rates and performance metrics
4. Gradual rollout with canary deployments
5. Quick rollback by switching feature flags

## Support

For migration issues, contact the platform team or check the SDK documentation at `sdk/go/simsekolah-ai/README.md`.