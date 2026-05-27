package simsekolah

import (
	"context"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

// Client is the main SDK client for the AI Platform
type Client struct {
	conn *grpc.ClientConn
}

// Config holds the configuration for the SDK client
type Config struct {
	GatewayServiceAddr string
	Timeout            time.Duration
}

// NewClient creates a new AI Platform SDK client
func NewClient(cfg Config) (*Client, error) {
	ctx, cancel := context.WithTimeout(context.Background(), cfg.Timeout)
	defer cancel()

	conn, err := grpc.DialContext(ctx,
		cfg.GatewayServiceAddr,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithBlock(),
	)
	if err != nil {
		return nil, err
	}

	return &Client{
		conn: conn,
	}, nil
}

// Close closes the gRPC connection
func (c *Client) Close() error {
	return c.conn.Close()
}

// HealthCheck checks the health of the AI Platform
func (c *Client) HealthCheck(ctx context.Context) error {
	// Implementation would call health check endpoint
	return nil
}
