package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"sim-sekolah/internal/ai/grpc/pb/semanticchunkservice"
)

// SemanticChunkServiceClient is a convenience wrapper around the generated
// semanticchunkservice.SemanticChunkServiceClient that manages its own connection.
type SemanticChunkServiceClient struct {
	conn *grpc.ClientConn
	semanticchunkservice.SemanticChunkServiceClient
}

// NewSemanticChunkServiceClient creates a new Semantic Chunk Service gRPC client.
// The caller must call Close() when done.
func NewSemanticChunkServiceClient(address string) (*SemanticChunkServiceClient, error) {
	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to semantic chunk service: %w", err)
	}

	return &SemanticChunkServiceClient{
		conn:                       conn,
		SemanticChunkServiceClient: semanticchunkservice.NewSemanticChunkServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *SemanticChunkServiceClient) Close() error {
	return c.conn.Close()
}
