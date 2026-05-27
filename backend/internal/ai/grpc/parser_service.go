package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"sim-sekolah/internal/ai/grpc/pb/parserservice"
)

// ParserServiceClient is a convenience wrapper around the generated
// parserservice.ParserServiceClient that manages its own connection.
type ParserServiceClient struct {
	conn *grpc.ClientConn
	parserservice.ParserServiceClient
}

// NewParserServiceClient creates a new Parser Service gRPC client.
// The caller must call Close() when done.
func NewParserServiceClient(address string) (*ParserServiceClient, error) {
	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to parser service: %w", err)
	}

	return &ParserServiceClient{
		conn:                conn,
		ParserServiceClient: parserservice.NewParserServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *ParserServiceClient) Close() error {
	return c.conn.Close()
}
