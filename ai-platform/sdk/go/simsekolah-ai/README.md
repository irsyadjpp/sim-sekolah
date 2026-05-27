# SimSekolah AI Platform Go SDK

Go SDK for the AI Platform services, providing a clean interface for Go applications to interact with AI Platform gRPC services.

## Features

- **Type-safe gRPC clients**: Auto-generated from proto definitions
- **Connection management**: Automatic connection pooling and keepalive
- **Circuit breaker**: Built-in circuit breaker pattern for resilience
- **Retry logic**: Automatic retry with configurable backoff
- **Error handling**: Structured error types with proper error codes
- **Configuration**: Environment-based configuration with sensible defaults
- **TLS support**: Secure connections with configurable TLS options

## Installation

```bash
go get github.com/simsekolah/ai-platform-sdk-go
```

## Quick Start

```go
package main

import (
    "context"
    "log"
    
    "github.com/simsekolah/ai-platform-sdk-go"
    "github.com/simsekolah/ai-platform-sdk-go/config"
)

func main() {
    // Load configuration from environment
    cfg := config.ConfigFromEnv()
    
    // Create client
    client, err := simsekolah.NewClient(cfg)
    if err != nil {
        log.Fatalf("Failed to create client: %v", err)
    }
    defer client.Close()
    
    // Use the client
    docConn := client.GetDocumentServiceClient()
    // Use docConn to make gRPC calls to document service
    
    // Health check
    health := client.HealthCheck(context.Background())
    log.Printf("Service health: %v", health)
}
```

## Configuration

Configure the SDK using environment variables:

```bash
# Service URLs
export AI_DOCUMENT_SERVICE_URL=localhost:50051
export AI_EMBEDDING_SERVICE_URL=localhost:50052
export AI_RETRIEVAL_SERVICE_URL=localhost:50053
export AI_GENERATION_SERVICE_URL=localhost:50054
export AI_GUARD_SERVICE_URL=localhost:50055
export AI_AUDIT_SERVICE_URL=localhost:50056
export AI_MODERATION_SERVICE_URL=localhost:50057

# Connection settings
export AI_MAX_CONN_IDLE_TIME=5m
export AI_MAX_CONN_AGE=30m

# TLS
export AI_USE_TLS=false
export AI_INSECURE_SKIP_VERIFY=false

# Retry
export AI_MAX_RETRIES=3
export AI_RETRY_DELAY=1s

# Circuit breaker
export AI_CIRCUIT_BREAKER_ENABLED=true
export AI_CIRCUIT_BREAKER_THRESHOLD=5
export AI_CIRCUIT_BREAKER_TIMEOUT=30s

# Timeouts
export AI_DEFAULT_TIMEOUT=30s

# Authentication
export AI_API_KEY=your-api-key
export AI_JWT_TOKEN=your-jwt-token

# Debug
export AI_DEBUG=false
```

## Usage Examples

### Document Service

```go
import (
    "context"
    pb "github.com/simsekolah/ai-platform-sdk-go/proto/document/v1"
)

func uploadDocument(client *simsekolah.Client) error {
    ctx := context.Background()
    conn := client.GetDocumentServiceClient()
    grpcClient := pb.NewDocumentServiceClient(conn)
    
    resp, err := grpcClient.UploadDocument(ctx, &pb.UploadDocumentRequest{
        Title:   "Test Document",
        Content: "Test content",
        Metadata: map[string]string{
            "author": "Test Author",
        },
    })
    
    if err != nil {
        return err
    }
    
    log.Printf("Document uploaded: %s", resp.DocumentId)
    return nil
}
```

### Error Handling

```go
import (
    "github.com/simsekolah/ai-platform-sdk-go/errors"
)

func handleExample() {
    // Handle specific error types
    if errors.IsConnectionError(err) {
        log.Println("Connection failed, will retry")
    } else if errors.IsTimeoutError(err) {
        log.Println("Request timed out")
    } else if errors.IsAuthError(err) {
        log.Println("Authentication failed")
    } else if errors.IsRetryable(err) {
        log.Println("Error is retryable")
    }
}
```

### Circuit Breaker

```go
import (
    "github.com/simsekolah/ai-platform-sdk-go/circuitbreaker"
)

func circuitBreakerExample() {
    manager := circuitbreaker.NewManager()
    
    config := circuitbreaker.Config{
        Threshold:     5,
        Timeout:       30 * time.Second,
        ResetTimeout:  10 * time.Second,
    }
    
    cb := manager.GetOrCreate("document-service", config)
    
    err := cb.Execute(context.Background(), func() error {
        // Execute the operation
        return callDocumentService()
    })
    
    if err != nil {
        log.Printf("Operation failed: %v", err)
    }
}
```

## Service Clients

The SDK provides access to the following AI Platform services:

- **Document Service**: Document management and processing
- **Embedding Service**: Text embedding generation
- **Retrieval Service**: Semantic search and retrieval
- **Generation Service**: AI text generation
- **Guard Service**: Content moderation and safety checks
- **Audit Service**: Audit logging and tracking
- **Moderation Service**: Content moderation

## Error Handling

The SDK uses structured error types:

```go
type SDKError struct {
    Code       ErrorCode
    Message    string
    StatusCode int
    Details    map[string]interface{}
    Cause      error
}
```

Error codes include:
- Connection errors: `CONNECTION_FAILED`, `TIMEOUT`, `SERVICE_UNAVAILABLE`
- Authentication errors: `UNAUTHORIZED`, `INVALID_TOKEN`, `EXPIRED_TOKEN`
- Validation errors: `INVALID_REQUEST`, `MISSING_PARAMETER`
- Business logic errors: `NOT_FOUND`, `ALREADY_EXISTS`, `CONFLICT`
- Rate limiting: `RATE_LIMITED`
- Internal errors: `INTERNAL_ERROR`, `UNKNOWN_ERROR`

## Development

### Generate Proto Files

```bash
# Install protoc and plugins
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Generate Go code from proto files
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    proto/**/*.proto
```

### Run Tests

```bash
go test ./...
```

### Build

```bash
go build ./...
```

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open a GitHub issue or contact the development team.