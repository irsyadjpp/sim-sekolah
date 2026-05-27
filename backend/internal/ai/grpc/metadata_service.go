package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"sim-sekolah/internal/ai/grpc/pb/metadataservice"
)

// MetadataServiceClient is a convenience wrapper around the generated
// metadataservice.MetadataServiceClient that manages its own connection.
type MetadataServiceClient struct {
	conn *grpc.ClientConn
	metadataservice.MetadataServiceClient
}

// NewMetadataServiceClient creates a new Metadata Service gRPC client.
// The caller must call Close() when done.
func NewMetadataServiceClient(address string) (*MetadataServiceClient, error) {
	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to metadata service: %w", err)
	}

	return &MetadataServiceClient{
		conn:                  conn,
		MetadataServiceClient: metadataservice.NewMetadataServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *MetadataServiceClient) Close() error {
	return c.conn.Close()
}
