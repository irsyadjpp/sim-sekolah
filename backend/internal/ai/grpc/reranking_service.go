package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"sim-sekolah/internal/ai/grpc/pb/rerankingservice"
)

// RerankingServiceClient is a convenience wrapper around the generated
// rerankingservice.RerankingServiceClient that manages its own connection.
type RerankingServiceClient struct {
	conn *grpc.ClientConn
	rerankingservice.RerankingServiceClient
}

// NewRerankingServiceClient creates a new Reranking Service gRPC client.
// The caller must call Close() when done.
func NewRerankingServiceClient(address string) (*RerankingServiceClient, error) {
	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to reranking service: %w", err)
	}

	return &RerankingServiceClient{
		conn:                   conn,
		RerankingServiceClient: rerankingservice.NewRerankingServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *RerankingServiceClient) Close() error {
	return c.conn.Close()
}
