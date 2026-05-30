package grpc

import (
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "sim-sekolah/internal/ai/grpc/pb/strategicanalysisservice"
)

// StrategicAnalysisClient is a convenience wrapper around the generated
// pb.StrategicAnalysisServiceClient that manages its own gRPC connection.
type StrategicAnalysisClient struct {
	conn *grpc.ClientConn
	pb.StrategicAnalysisServiceClient
}

// NewStrategicAnalysisClient creates a new Strategic Analysis Service gRPC client.
// The caller MUST call Close() when done to release the connection.
//
// address should be in "host:port" format, e.g. "strategic-analysis-service:50063"
func NewStrategicAnalysisClient(address string) (*StrategicAnalysisClient, error) {
	conn, err := grpc.NewClient(
		address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to strategic analysis service at %s: %w", address, err)
	}

	return &StrategicAnalysisClient{
		conn:                           conn,
		StrategicAnalysisServiceClient: pb.NewStrategicAnalysisServiceClient(conn),
	}, nil
}

// Close closes the underlying gRPC connection.
func (c *StrategicAnalysisClient) Close() error {
	return c.conn.Close()
}
