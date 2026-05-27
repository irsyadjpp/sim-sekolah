package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"sim-sekolah/internal/ai/grpc/pb/generationservice"
)

// GenerationServiceClient is a convenience wrapper around the generated
// generationservice.GenerationServiceClient that manages its own connection.
type GenerationServiceClient struct {
	conn *grpc.ClientConn
	generationservice.GenerationServiceClient
}

// NewGenerationServiceClient creates a new Generation Service gRPC client.
// The caller must call Close() when done.
func NewGenerationServiceClient(address string) (*GenerationServiceClient, error) {
	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to generation service: %w", err)
	}

	return &GenerationServiceClient{
		conn:                    conn,
		GenerationServiceClient: generationservice.NewGenerationServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *GenerationServiceClient) Close() error {
	return c.conn.Close()
}
