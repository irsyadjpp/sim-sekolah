package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"sim-sekolah/internal/ai/grpc/pb/embeddingservice"
)

// EmbeddingServiceClient is a convenience wrapper around the generated
// embeddingservice.EmbeddingServiceClient that manages its own connection.
type EmbeddingServiceClient struct {
	conn *grpc.ClientConn
	embeddingservice.EmbeddingServiceClient
}

// NewEmbeddingServiceClient creates a new Embedding Service gRPC client.
// The caller must call Close() when done.
func NewEmbeddingServiceClient(address string) (*EmbeddingServiceClient, error) {
	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to embedding service: %w", err)
	}

	return &EmbeddingServiceClient{
		conn:                   conn,
		EmbeddingServiceClient: embeddingservice.NewEmbeddingServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *EmbeddingServiceClient) Close() error {
	return c.conn.Close()
}
