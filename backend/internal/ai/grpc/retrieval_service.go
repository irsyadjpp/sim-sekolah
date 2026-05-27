package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"sim-sekolah/internal/ai/grpc/pb/retrievalservice"
)

// RetrievalServiceClient is a convenience wrapper around the generated
// retrievalservice.RetrievalServiceClient that manages its own connection.
type RetrievalServiceClient struct {
	conn *grpc.ClientConn
	retrievalservice.RetrievalServiceClient
}

// NewRetrievalServiceClient creates a new Retrieval Service gRPC client.
// The caller must call Close() when done.
func NewRetrievalServiceClient(address string) (*RetrievalServiceClient, error) {
	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to retrieval service: %w", err)
	}

	return &RetrievalServiceClient{
		conn:                   conn,
		RetrievalServiceClient: retrievalservice.NewRetrievalServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *RetrievalServiceClient) Close() error {
	return c.conn.Close()
}
