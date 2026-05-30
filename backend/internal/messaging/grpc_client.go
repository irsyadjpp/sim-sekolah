package messaging

import (
	"context"
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	grpc_clients "sim-sekolah/internal/ai/grpc"
	"sim-sekolah/internal/ai/grpc/pb/embeddingservice"
	"sim-sekolah/internal/ai/grpc/pb/generationservice"
	"sim-sekolah/internal/ai/grpc/pb/metadataservice"
	"sim-sekolah/internal/ai/grpc/pb/parserservice"
	"sim-sekolah/internal/ai/grpc/pb/retrievalservice"
	"sim-sekolah/internal/ai/grpc/pb/semanticchunkservice"
	"sim-sekolah/internal/ai/grpc/pb/visionservice"
)

// GRPCClient manages gRPC connections to AI services
type GRPCClient struct {
	connections map[string]*grpc.ClientConn
	services    map[string]string // service name to address mapping
	// Fase 2 & 3 specific clients
	parserClient     *grpc_clients.ParserServiceClient
	visionClient     *grpc_clients.VisionServiceClient
	chunkClient      *grpc_clients.SemanticChunkServiceClient
	metadataClient   *grpc_clients.MetadataServiceClient
	embeddingClient  *grpc_clients.EmbeddingServiceClient
	retrievalClient  *grpc_clients.RetrievalServiceClient
	generationClient *grpc_clients.GenerationServiceClient
	rerankingClient  *grpc_clients.RerankingServiceClient
	strategicAnalysisClient *grpc_clients.StrategicAnalysisClient
}

// NewGRPCClient creates a new gRPC client manager
func NewGRPCClient() (*GRPCClient, error) {
	client := &GRPCClient{
		connections: make(map[string]*grpc.ClientConn),
		services: map[string]string{
			// Core RAG services
			"parser":     "parser-service:50051",
			"embedding":  "embedding-service:50052",
			"generation": "generation-service:50053",
			"retrieval":  "retrieval-service:50054",
			"vision":     "vision-service:50055",
			"chunk":      "semantic-chunk-service:50056",
			"metadata":   "metadata-service:50057",
			"reranking":  "reranking-service:50058",
			// AI Platform services (Phase 7 & 8)
			"strategic-analysis":        "strategic-analysis-service:50063",
			"ai-agents":                 "ai-agents-service:50072",
			"hallucination-guard":       "hallucination-guard-service:50073",
			"educational-observability": "educational-observability-service:50074",
			// AI Platform services (Phase 5 - Educational Intelligence)
			"adaptive-learning":    "educational-intelligence-service:50075",
			"assessment":           "educational-intelligence-service:50076",
			"curriculum":           "educational-intelligence-service:50077",
			"learning-graph":       "educational-intelligence-service:50078",
			"learning-progression": "educational-intelligence-service:50079",
			"pedagogy":             "educational-intelligence-service:50080",
			"recommendation":       "educational-intelligence-service:50081",
			// AI Platform services (Phase 6 - Advanced Enhancement)
			"retrieval-enhancement": "advanced-enhancement-service:50083",
			"semantic-enrichment":   "advanced-enhancement-service:50084",
			"educational-ontology":  "advanced-enhancement-service:50085",
		},
	}

	// Initialize Fase 2 & 3 clients
	var err error
	client.parserClient, err = grpc_clients.NewParserServiceClient(client.services["parser"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize parser client: %w", err)
	}

	client.visionClient, err = grpc_clients.NewVisionServiceClient(client.services["vision"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize vision client: %w", err)
	}

	client.chunkClient, err = grpc_clients.NewSemanticChunkServiceClient(client.services["chunk"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize chunk client: %w", err)
	}

	client.metadataClient, err = grpc_clients.NewMetadataServiceClient(client.services["metadata"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize metadata client: %w", err)
	}

	client.embeddingClient, err = grpc_clients.NewEmbeddingServiceClient(client.services["embedding"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize embedding client: %w", err)
	}

	client.retrievalClient, err = grpc_clients.NewRetrievalServiceClient(client.services["retrieval"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize retrieval client: %w", err)
	}

	client.generationClient, err = grpc_clients.NewGenerationServiceClient(client.services["generation"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize generation client: %w", err)
	}

	client.rerankingClient, err = grpc_clients.NewRerankingServiceClient(client.services["reranking"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize reranking client: %w", err)
	}

	client.strategicAnalysisClient, err = grpc_clients.NewStrategicAnalysisClient(client.services["strategic-analysis"])
	if err != nil {
		return nil, fmt.Errorf("failed to initialize strategic analysis client: %w", err)
	}

	return client, nil
}

// GetConnection gets or creates a gRPC connection to a service
func (c *GRPCClient) GetConnection(serviceName string) (*grpc.ClientConn, error) {
	if conn, exists := c.connections[serviceName]; exists {
		return conn, nil
	}

	address, exists := c.services[serviceName]
	if !exists {
		return nil, fmt.Errorf("unknown service: %s", serviceName)
	}

	conn, err := grpc.NewClient(address,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to %s: %w", serviceName, err)
	}

	c.connections[serviceName] = conn
	return conn, nil
}

// Close closes all gRPC connections
func (c *GRPCClient) Close() error {
	var lastErr error
	for serviceName, conn := range c.connections {
		if err := conn.Close(); err != nil {
			lastErr = fmt.Errorf("error closing connection to %s: %w", serviceName, err)
		}
	}

	// Close Fase 2 & 3 clients
	if c.parserClient != nil {
		c.parserClient.Close()
	}
	if c.visionClient != nil {
		c.visionClient.Close()
	}
	if c.chunkClient != nil {
		c.chunkClient.Close()
	}
	if c.metadataClient != nil {
		c.metadataClient.Close()
	}
	if c.embeddingClient != nil {
		c.embeddingClient.Close()
	}
	if c.retrievalClient != nil {
		c.retrievalClient.Close()
	}
	if c.generationClient != nil {
		c.generationClient.Close()
	}
	if c.rerankingClient != nil {
		c.rerankingClient.Close()
	}
	if c.strategicAnalysisClient != nil {
		c.strategicAnalysisClient.Close()
	}

	return lastErr
}

// UpdateServiceAddress updates the address for a service
func (c *GRPCClient) UpdateServiceAddress(serviceName, address string) {
	c.services[serviceName] = address
	// Close existing connection if any
	if conn, exists := c.connections[serviceName]; exists {
		conn.Close()
		delete(c.connections, serviceName)
	}
}

// Fase 2 Service Client Accessors

// GetParserClient returns the Parser Service client
func (c *GRPCClient) GetParserClient() *grpc_clients.ParserServiceClient {
	return c.parserClient
}

// GetVisionClient returns the Vision Service client
func (c *GRPCClient) GetVisionClient() *grpc_clients.VisionServiceClient {
	return c.visionClient
}

// GetChunkClient returns the Semantic Chunk Service client
func (c *GRPCClient) GetChunkClient() *grpc_clients.SemanticChunkServiceClient {
	return c.chunkClient
}

// GetMetadataClient returns the Metadata Service client
func (c *GRPCClient) GetMetadataClient() *grpc_clients.MetadataServiceClient {
	return c.metadataClient
}

// Fase 3 Service Client Accessors

// GetEmbeddingClient returns the Embedding Service client
func (c *GRPCClient) GetEmbeddingClient() *grpc_clients.EmbeddingServiceClient {
	return c.embeddingClient
}

// GetRetrievalClient returns the Retrieval Service client
func (c *GRPCClient) GetRetrievalClient() *grpc_clients.RetrievalServiceClient {
	return c.retrievalClient
}

// GetGenerationClient returns the Generation Service client
func (c *GRPCClient) GetGenerationClient() *grpc_clients.GenerationServiceClient {
	return c.generationClient
}

// GetRerankingClient returns the Reranking Service client
func (c *GRPCClient) GetRerankingClient() *grpc_clients.RerankingServiceClient {
	return c.rerankingClient
}

// GetStrategicAnalysisClient returns the Strategic Analysis Service client
func (c *GRPCClient) GetStrategicAnalysisClient() *grpc_clients.StrategicAnalysisClient {
	return c.strategicAnalysisClient
}

// Legacy compatibility methods - these maintain backward compatibility with existing code

// ParserServiceClient - legacy wrapper
type ParserServiceClient struct {
	client *grpc_clients.ParserServiceClient
}

// NewParserServiceClient is a legacy constructor that maintains backward compatibility.
// New code should use GRPCClient.GetParserClient() instead.
func NewParserServiceClient(serviceName string) (*ParserServiceClient, error) {
	return nil, fmt.Errorf("use GRPCClient.GetParserClient() instead")
}

// ParseDocument - legacy wrapper using generated protobuf types
func (c *ParserServiceClient) ParseDocument(ctx context.Context, documentID string, documentData []byte, documentType string, metadata map[string]string) (map[string]interface{}, error) {
	req := &parserservice.ParseDocumentRequest{
		DocumentId:   documentID,
		DocumentData: documentData,
		DocumentType: documentType,
		Metadata:     metadata,
	}
	resp, err := c.client.ParseDocument(ctx, req)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"success":  resp.Success,
		"message":  resp.Message,
		"result":   resp.Result,
		"metadata": resp.Metadata,
	}, nil
}

// EmbeddingServiceClient - legacy wrapper
type EmbeddingServiceClient struct {
	client *grpc_clients.EmbeddingServiceClient
}

// NewEmbeddingServiceClient is a legacy constructor.
func NewEmbeddingServiceClient(serviceName string) (*EmbeddingServiceClient, error) {
	return nil, fmt.Errorf("use GRPCClient.GetEmbeddingClient() instead")
}

// EmbedText - legacy wrapper using generated protobuf types
func (c *EmbeddingServiceClient) EmbedText(ctx context.Context, textID, textContent, model string, metadata map[string]string) (map[string]interface{}, error) {
	req := &embeddingservice.EmbedTextRequest{
		TextId:      textID,
		TextContent: textContent,
		Model:       model,
		Options:     metadata,
	}
	resp, err := c.client.EmbedText(ctx, req)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"success":  resp.Success,
		"message":  resp.Message,
		"result":   resp.Result,
		"metadata": resp.Metadata,
	}, nil
}

// GenerationServiceClient - legacy wrapper
type GenerationServiceClient struct {
	client *grpc_clients.GenerationServiceClient
}

// NewGenerationServiceClient is a legacy constructor.
func NewGenerationServiceClient(serviceName string) (*GenerationServiceClient, error) {
	return nil, fmt.Errorf("use GRPCClient.GetGenerationClient() instead")
}

// GenerateText - legacy wrapper using generated protobuf types
func (c *GenerationServiceClient) GenerateText(ctx context.Context, prompt, provider, model string, temperature float32, maxTokens int32, metadata map[string]string) (map[string]interface{}, error) {
	req := &generationservice.GenerateTextRequest{
		RequestId:   "legacy-request",
		Prompt:      prompt,
		Provider:    provider,
		Model:       model,
		Temperature: temperature,
		MaxTokens:   maxTokens,
		Parameters:  metadata,
	}
	resp, err := c.client.GenerateText(ctx, req)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"success":  resp.Success,
		"message":  resp.Message,
		"result":   resp.Result,
		"metadata": resp.Metadata,
	}, nil
}

// RetrievalServiceClient - legacy wrapper
type RetrievalServiceClient struct {
	client *grpc_clients.RetrievalServiceClient
}

// NewRetrievalServiceClient is a legacy constructor.
func NewRetrievalServiceClient(serviceName string) (*RetrievalServiceClient, error) {
	return nil, fmt.Errorf("use GRPCClient.GetRetrievalClient() instead")
}

// SemanticSearch - legacy wrapper using generated protobuf types
func (c *RetrievalServiceClient) SemanticSearch(ctx context.Context, query, collectionName string, limit int32, filters map[string]string) (map[string]interface{}, error) {
	req := &retrievalservice.SemanticSearchRequest{
		QueryId:        "legacy-query",
		QueryText:      query,
		CollectionName: collectionName,
		Limit:          limit,
		Filters:        filters,
	}
	resp, err := c.client.SemanticSearch(ctx, req)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"success":  resp.Success,
		"message":  resp.Message,
		"result":   resp.Result,
		"metadata": resp.Metadata,
	}, nil
}

// VisionServiceClient - legacy wrapper
type VisionServiceClient struct {
	client *grpc_clients.VisionServiceClient
}

// NewVisionServiceClient is a legacy constructor.
func NewVisionServiceClient(serviceName string) (*VisionServiceClient, error) {
	return nil, fmt.Errorf("use GRPCClient.GetVisionClient() instead")
}

// ProcessOCR - legacy wrapper using generated protobuf types
func (c *VisionServiceClient) ProcessOCR(ctx context.Context, imageID string, imageData []byte, language string, metadata map[string]string) (map[string]interface{}, error) {
	req := &visionservice.ProcessOCRRequest{
		ImageId:   imageID,
		ImageData: imageData,
		Language:  language,
		Options:   metadata,
	}
	resp, err := c.client.ProcessOCR(ctx, req)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"success":  resp.Success,
		"message":  resp.Message,
		"result":   resp.Result,
		"metadata": resp.Metadata,
	}, nil
}

// ChunkServiceClient - legacy wrapper
type ChunkServiceClient struct {
	client *grpc_clients.SemanticChunkServiceClient
}

// NewChunkServiceClient is a legacy constructor.
func NewChunkServiceClient(serviceName string) (*ChunkServiceClient, error) {
	return nil, fmt.Errorf("use GRPCClient.GetChunkClient() instead")
}

// ChunkCompetency - legacy wrapper using generated protobuf types
func (c *ChunkServiceClient) ChunkCompetency(ctx context.Context, contentID, content, competencyType string, metadata map[string]string) (map[string]interface{}, error) {
	req := &semanticchunkservice.ChunkCompetencyRequest{
		ContentId:  contentID,
		Content:    content,
		Competency: competencyType,
		Options:    metadata,
	}
	resp, err := c.client.ChunkCompetency(ctx, req)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"success":  resp.Success,
		"message":  resp.Message,
		"result":   resp.Result,
		"metadata": resp.Metadata,
	}, nil
}

// MetadataServiceClient - legacy wrapper
type MetadataServiceClient struct {
	client *grpc_clients.MetadataServiceClient
}

// NewMetadataServiceClient is a legacy constructor.
func NewMetadataServiceClient(serviceName string) (*MetadataServiceClient, error) {
	return nil, fmt.Errorf("use GRPCClient.GetMetadataClient() instead")
}

// EnrichDifficulty - legacy wrapper using generated protobuf types
func (c *MetadataServiceClient) EnrichDifficulty(ctx context.Context, contentID, content, contentType string, metadata map[string]string) (map[string]interface{}, error) {
	req := &metadataservice.EnrichDifficultyRequest{
		ContentId:   contentID,
		Content:     content,
		ContentType: contentType,
		Options:     metadata,
	}
	resp, err := c.client.EnrichDifficulty(ctx, req)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"success":  resp.Success,
		"message":  resp.Message,
		"result":   resp.Result,
		"metadata": resp.Metadata,
	}, nil
}
