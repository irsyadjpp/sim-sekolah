// Package simsekolah provides Go SDK for AI Platform services
package simsekolah

import (
	"context"
	"crypto/tls"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/keepalive"
)

// Config holds configuration for AI Platform SDK clients
type Config struct {
	// Services configuration
	DocumentServiceURL string
	EmbeddingServiceURL string
	RetrievalServiceURL string
	GenerationServiceURL string
	GuardServiceURL string
	AuditServiceURL string
	ModerationServiceURL string

	// Connection settings
	MaxConnIdleTime time.Duration
	MaxConnAge time.Duration
	KeepAliveParams keepalive.ClientParameters
	
	// TLS settings
	UseTLS bool
	TLSConfig *tls.Config
	InsecureSkipVerify bool
	
	// Retry settings
	MaxRetries int
	RetryDelay time.Duration
	
	// Circuit breaker settings
	CircuitBreakerEnabled bool
	CircuitBreakerThreshold int
	CircuitBreakerTimeout time.Duration
	
	// Timeout settings
	DefaultTimeout time.Duration
	ConnectTimeout time.Dialer
	
	// Authentication
	APIKey string
	JWTToken string
	
	// Debugging
	Debug bool
}

// DefaultConfig returns default configuration for SDK
func DefaultConfig() *Config {
	return &Config{
		DocumentServiceURL:    "localhost:50051",
		EmbeddingServiceURL:   "localhost:50052",
		RetrievalServiceURL:   "localhost:50053",
		GenerationServiceURL:  "localhost:50054",
		GuardServiceURL:       "localhost:50055",
		AuditServiceURL:       "localhost:50056",
		ModerationServiceURL:  "localhost:50057",
		
		MaxConnIdleTime:      5 * time.Minute,
		MaxConnAge:           30 * time.Minute,
		KeepAliveParams: keepalive.ClientParameters{
			Time:                10 * time.Second,
			Timeout:             3 * time.Second,
			PermitWithoutStream: true,
		},
		
		UseTLS:               false,
		InsecureSkipVerify:   false,
		
		MaxRetries:           3,
		RetryDelay:           1 * time.Second,
		
		CircuitBreakerEnabled: true,
		CircuitBreakerThreshold: 5,
		CircuitBreakerTimeout: 30 * time.Second,
		
		DefaultTimeout:       30 * time.Second,
		
		Debug:               false,
	}
}

// Client is the main SDK client for AI Platform services
type Client struct {
	config *Config
	
	// gRPC connections
	documentConn    *grpc.ClientConn
	embeddingConn   *grpc.ClientConn
	retrievalConn   *grpc.ClientConn
	generationConn  *grpc.ClientConn
	guardConn       *grpc.ClientConn
	auditConn       *grpc.ClientConn
	moderationConn  *grpc.ClientConn
	
	// Service clients (would be generated from proto files)
	// These are placeholders - actual clients would be proto-generated
}

// NewClient creates a new AI Platform SDK client
func NewClient(config *Config) (*Client, error) {
	if config == nil {
		config = DefaultConfig()
	}
	
	client := &Client{
		config: config,
	}
	
	// Initialize connections
	if err := client.initConnections(); err != nil {
		return nil, err
	}
	
	return client, nil
}

// initConnections initializes gRPC connections to all services
func (c *Client) initConnections() error {
	var err error
	
	// Create dial options based on configuration
	dialOpts := c.getDialOptions()
	
	// Document Service
	if c.documentConn, err = grpc.NewClient(c.config.DocumentServiceURL, dialOpts...); err != nil {
		return err
	}
	
	// Embedding Service
	if c.embeddingConn, err = grpc.NewClient(c.config.EmbeddingServiceURL, dialOpts...); err != nil {
		return err
	}
	
	// Retrieval Service
	if c.retrievalConn, err = grpc.NewClient(c.config.RetrievalServiceURL, dialOpts...); err != nil {
		return err
	}
	
	// Generation Service
	if c.generationConn, err = grpc.NewClient(c.config.GenerationServiceURL, dialOpts...); err != nil {
		return err
	}
	
	// Guard Service
	if c.guardConn, err = grpc.NewClient(c.config.GuardServiceURL, dialOpts...); err != nil {
		return err
	}
	
	// Audit Service
	if c.auditConn, err = grpc.NewClient(c.config.AuditServiceURL, dialOpts...); err != nil {
		return err
	}
	
	// Moderation Service
	if c.moderationConn, err = grpc.NewClient(c.config.ModerationServiceURL, dialOpts...); err != nil {
		return err
	}
	
	return nil
}

// getDialOptions returns gRPC dial options based on configuration
func (c *Client) getDialOptions() []grpc.DialOption {
	opts := []grpc.DialOption{}
	
	// Transport credentials
	if c.config.UseTLS {
		creds := credentials.NewTLS(c.config.TLSConfig)
		if c.config.InsecureSkipVerify {
			creds = credentials.NewTLS(&tls.Config{InsecureSkipVerify: true})
		}
		opts = append(opts, grpc.WithTransportCredentials(creds))
	} else {
		opts = append(opts, grpc.WithTransportCredentials(insecure.NewCredentials()))
	}
	
	// Keepalive
	opts = append(opts, grpc.WithKeepaliveParams(c.config.KeepAliveParams))
	
	// Connection parameters
	opts = append(opts, 
		grpc.WithDefaultCallOptions(
			grpc.MaxCallRecvMsgSize(4*1024*1024), // 4MB
			grpc.MaxCallSendMsgSize(4*1024*1024), // 4MB
		),
	)
	
	// Connection timeout
	if c.config.ConnectTimeout != nil {
		opts = append(opts, grpc.WithConnectParams(connect.Params{
			MinConnectTimeout: 5 * time.Second,
		}))
	}
	
	// Block by default
	opts = append(opts, grpc.WithBlock())
	
	return opts
}

// Close closes all gRPC connections
func (c *Client) Close() error {
	var errors []error
	
	if c.documentConn != nil {
		if err := c.documentConn.Close(); err != nil {
			errors = append(errors, err)
		}
	}
	
	if c.embeddingConn != nil {
		if err := c.embeddingConn.Close(); err != nil {
			errors = append(errors, err)
		}
	}
	
	if c.retrievalConn != nil {
		if err := c.retrievalConn.Close(); err != nil {
			errors = append(errors, err)
		}
	}
	
	if c.generationConn != nil {
		if err := c.generationConn.Close(); err != nil {
			errors = append(errors, err)
		}
	}
	
	if c.guardConn != nil {
		if err := c.guardConn.Close(); err != nil {
			errors = append(errors, err)
		}
	}
	
	if c.auditConn != nil {
		if err := c.auditConn.Close(); err != nil {
			errors = append(errors, err)
		}
	}
	
	if c.moderationConn != nil {
		if err := c.moderationConn.Close(); err != nil {
			errors = append(errors, err)
		}
	}
	
	if len(errors) > 0 {
		return errors[0]
	}
	
	return nil
}

// GetDocumentServiceClient returns a client for the Document Service
func (c *Client) GetDocumentServiceClient() *grpc.ClientConn {
	return c.documentConn
}

// GetEmbeddingServiceClient returns a client for the Embedding Service
func (c *Client) GetEmbeddingServiceClient() *grpc.ClientConn {
	return c.embeddingConn
}

// GetRetrievalServiceClient returns a client for the Retrieval Service
func (c *Client) GetRetrievalServiceClient() *grpc.ClientConn {
	return c.retrievalConn
}

// GetGenerationServiceClient returns a client for the Generation Service
func (c *Client) GetGenerationServiceClient() *grpc.ClientConn {
	return c.generationConn
}

// GetGuardServiceClient returns a client for the Guard Service
func (c *Client) GetGuardServiceClient() *grpc.ClientConn {
	return c.guardConn
}

// GetAuditServiceClient returns a client for the Audit Service
func (c *Client) GetAuditServiceClient() *grpc.ClientConn {
	return c.auditConn
}

// GetModerationServiceClient returns a client for the Moderation Service
func (c *Client) GetModerationServiceClient() *grpc.ClientConn {
	return c.moderationConn
}

// HealthCheck performs a health check on all services
func (c *Client) HealthCheck(ctx context.Context) map[string]bool {
	results := make(map[string]bool)
	
	// Check each service connection
	results["document"] = c.documentConn.GetState() == grpc.Ready
	results["embedding"] = c.embeddingConn.GetState() == grpc.Ready
	results["retrieval"] = c.retrievalConn.GetState() == grpc.Ready
	results["generation"] = c.generationConn.GetState() == grpc.Ready
	results["guard"] = c.guardConn.GetState() == grpc.Ready
	results["audit"] = c.auditConn.GetState() == grpc.Ready
	results["moderation"] = c.moderationConn.GetState() == grpc.Ready
	
	return results
}