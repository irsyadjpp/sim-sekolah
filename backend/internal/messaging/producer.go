package messaging

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

// MessageTypes defines all message types for AI Platform communication
type MessageTypes string

const (
	// Parser Service messages
	MessageTypeParseDocument MessageTypes = "parse_document"
	MessageTypeProcessOCR    MessageTypes = "process_ocr"

	// Embedding Service messages
	MessageTypeEmbedText      MessageTypes = "embed_text"
	MessageTypeEmbedTextBatch MessageTypes = "embed_text_batch"
	MessageTypeEmbedImage     MessageTypes = "embed_image"

	// Retrieval Service messages
	MessageTypeSemanticSearch MessageTypes = "semantic_search"
	MessageTypeHybridSearch   MessageTypes = "hybrid_search"

	// Generation Service messages
	MessageTypeGenerateText          MessageTypes = "generate_text"
	MessageTypeGenerateWithCitations MessageTypes = "generate_with_citations"
)

// BaseMessage represents the base structure for all RabbitMQ messages
type BaseMessage struct {
	MessageID     string                 `json:"message_id"`
	MessageType   string                 `json:"message_type"`
	Timestamp     string                 `json:"timestamp"`
	Priority      string                 `json:"priority"`
	Data          map[string]interface{} `json:"data"`
	CorrelationID string                 `json:"correlation_id,omitempty"`
	ReplyTo       string                 `json:"reply_to,omitempty"`
}

// NewBaseMessage creates a new base message
func NewBaseMessage(messageType MessageTypes, priority string, data map[string]interface{}) *BaseMessage {
	return &BaseMessage{
		MessageID:   generateMessageID(),
		MessageType: string(messageType),
		Timestamp:   time.Now().UTC().Format(time.RFC3339),
		Priority:    priority,
		Data:        data,
	}
}

// AIPlatformProducer handles publishing messages to AI Platform services
type AIPlatformProducer struct {
	conn     *amqp.Connection
	channel  *amqp.Channel
	exchange string
}

// NewAIPlatformProducer creates a new producer instance
func NewAIPlatformProducer(conn *amqp.Connection) (*AIPlatformProducer, error) {
	if conn == nil {
		return nil, fmt.Errorf("connection is nil")
	}

	ch, err := conn.Channel()
	if err != nil {
		return nil, fmt.Errorf("failed to open channel: %w", err)
	}

	// Declare exchange
	err = ch.ExchangeDeclare(
		"ai.platform.exchange", // name
		"topic",                // type
		true,                   // durable
		false,                  // auto-deleted
		false,                  // internal
		false,                  // no-wait
		nil,                    // arguments
	)
	if err != nil {
		return nil, fmt.Errorf("failed to declare exchange: %w", err)
	}

	return &AIPlatformProducer{
		conn:     conn,
		channel:  ch,
		exchange: "ai.platform.exchange",
	}, nil
}

// PublishMessage publishes a message to the specified queue
func (p *AIPlatformProducer) PublishMessage(
	ctx context.Context,
	queueName string,
	message *BaseMessage,
) error {
	body, err := json.Marshal(message)
	if err != nil {
		return fmt.Errorf("failed to marshal message: %w", err)
	}

	// Use routing key based on queue name
	routingKey := fmt.Sprintf("%s.*", queueName)

	err = p.channel.PublishWithContext(
		ctx,
		p.exchange,
		routingKey,
		false, // mandatory
		false, // immediate
		amqp.Publishing{
			ContentType:  "application/json",
			Body:         body,
			DeliveryMode: amqp.Persistent,
			Timestamp:    time.Now(),
			MessageId:    message.MessageID,
		},
	)

	if err != nil {
		return fmt.Errorf("failed to publish message: %w", err)
	}

	log.Printf("✅ Published message to queue %s: %s", queueName, message.MessageType)
	return nil
}

// PublishParseDocument publishes a document parsing request
func (p *AIPlatformProducer) PublishParseDocument(
	ctx context.Context,
	documentID string,
	documentData string,
	documentType string,
	metadata map[string]interface{},
) error {
	data := map[string]interface{}{
		"document_id":   documentID,
		"document_data": documentData,
		"document_type": documentType,
		"metadata":      metadata,
	}

	message := NewBaseMessage(MessageTypeParseDocument, "high", data)
	return p.PublishMessage(ctx, "parser", message)
}

// PublishEmbedText publishes a text embedding request
func (p *AIPlatformProducer) PublishEmbedText(
	ctx context.Context,
	textID string,
	textContent string,
	model string,
	metadata map[string]interface{},
) error {
	data := map[string]interface{}{
		"text_id":      textID,
		"text_content": textContent,
		"model":        model,
		"metadata":     metadata,
	}

	message := NewBaseMessage(MessageTypeEmbedText, "medium", data)
	return p.PublishMessage(ctx, "embedding", message)
}

// PublishEmbedTextBatch publishes a batch text embedding request
func (p *AIPlatformProducer) PublishEmbedTextBatch(
	ctx context.Context,
	textIDs []string,
	textContents []string,
	model string,
	batchSize int,
	metadata map[string]interface{},
) error {
	data := map[string]interface{}{
		"text_ids":      textIDs,
		"text_contents": textContents,
		"model":         model,
		"batch_size":    batchSize,
		"metadata":      metadata,
	}

	message := NewBaseMessage(MessageTypeEmbedTextBatch, "high", data)
	return p.PublishMessage(ctx, "embedding", message)
}

// PublishSemanticSearch publishes a semantic search request
func (p *AIPlatformProducer) PublishSemanticSearch(
	ctx context.Context,
	query string,
	collectionName string,
	limit int,
	filters map[string]interface{},
) error {
	data := map[string]interface{}{
		"query":           query,
		"collection_name": collectionName,
		"limit":           limit,
		"filters":         filters,
	}

	message := NewBaseMessage(MessageTypeSemanticSearch, "medium", data)
	return p.PublishMessage(ctx, "retrieval", message)
}

// PublishHybridSearch publishes a hybrid search request
func (p *AIPlatformProducer) PublishHybridSearch(
	ctx context.Context,
	query string,
	collectionName string,
	limit int,
	filters map[string]interface{},
	semanticWeight float64,
	keywordWeight float64,
) error {
	data := map[string]interface{}{
		"query":           query,
		"collection_name": collectionName,
		"limit":           limit,
		"filters":         filters,
		"semantic_weight": semanticWeight,
		"keyword_weight":  keywordWeight,
	}

	message := NewBaseMessage(MessageTypeHybridSearch, "medium", data)
	return p.PublishMessage(ctx, "retrieval", message)
}

// PublishGenerateText publishes a text generation request
func (p *AIPlatformProducer) PublishGenerateText(
	ctx context.Context,
	prompt string,
	provider string,
	model string,
	temperature float64,
	maxTokens int,
	metadata map[string]interface{},
) error {
	data := map[string]interface{}{
		"prompt":      prompt,
		"provider":    provider,
		"model":       model,
		"temperature": temperature,
		"max_tokens":  maxTokens,
		"metadata":    metadata,
	}

	message := NewBaseMessage(MessageTypeGenerateText, "medium", data)
	return p.PublishMessage(ctx, "generation", message)
}

// PublishGenerateWithCitations publishes a text generation with citations request
func (p *AIPlatformProducer) PublishGenerateWithCitations(
	ctx context.Context,
	prompt string,
	context string,
	documents []map[string]interface{},
	provider string,
	model string,
	temperature float64,
	maxTokens int,
) error {
	data := map[string]interface{}{
		"prompt":      prompt,
		"context":     context,
		"documents":   documents,
		"provider":    provider,
		"model":       model,
		"temperature": temperature,
		"max_tokens":  maxTokens,
	}

	message := NewBaseMessage(MessageTypeGenerateWithCitations, "high", data)
	return p.PublishMessage(ctx, "generation", message)
}

// Close closes the producer's channel and connection
func (p *AIPlatformProducer) Close() error {
	if p.channel != nil {
		if err := p.channel.Close(); err != nil {
			return fmt.Errorf("failed to close channel: %w", err)
		}
	}
	return nil
}

// generateMessageID generates a unique message ID
func generateMessageID() string {
	return fmt.Sprintf("%d", time.Now().UnixNano())
}
