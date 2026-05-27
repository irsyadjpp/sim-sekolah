package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"sim-sekolah/internal/ai/grpc/pb/visionservice"
)

// VisionServiceClient is a convenience wrapper around the generated
// visionservice.VisionServiceClient that manages its own connection.
type VisionServiceClient struct {
	conn *grpc.ClientConn
	visionservice.VisionServiceClient
}

// NewVisionServiceClient creates a new Vision Service gRPC client.
// The caller must call Close() when done.
func NewVisionServiceClient(address string) (*VisionServiceClient, error) {
	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to vision service: %w", err)
	}

	return &VisionServiceClient{
		conn:                conn,
		VisionServiceClient: visionservice.NewVisionServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *VisionServiceClient) Close() error {
	return c.conn.Close()
}
