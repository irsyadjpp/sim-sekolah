package messaging

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	amqp "github.com/rabbitmq/amqp091-go"
)

// RabbitMQProducer handles publishing messages to RabbitMQ
type RabbitMQProducer struct {
	conn    *amqp.Connection
	channel *amqp.Channel
}

// NewRabbitMQProducer creates a new RabbitMQ producer
func NewRabbitMQProducer(conn *amqp.Connection) (*RabbitMQProducer, error) {
	ch, err := conn.Channel()
	if err != nil {
		return nil, fmt.Errorf("failed to open channel: %w", err)
	}

	producer := &RabbitMQProducer{
		conn:    conn,
		channel: ch,
	}

	// Declare exchanges and queues
	if err := producer.setupInfrastructure(); err != nil {
		return nil, fmt.Errorf("failed to setup infrastructure: %w", err)
	}

	return producer, nil
}

// setupInfrastructure declares exchanges and queues
func (p *RabbitMQProducer) setupInfrastructure() error {
	// Declare topic exchange
	if err := p.channel.ExchangeDeclare(
		"ai.platform.exchange",
		"topic",
		true,
		false,
		false,
		false,
		nil,
	); err != nil {
		return fmt.Errorf("failed to declare exchange: %w", err)
	}

	// Declare direct exchange for results
	if err := p.channel.ExchangeDeclare(
		"ai.platform.direct",
		"direct",
		true,
		false,
		false,
		false,
		nil,
	); err != nil {
		return fmt.Errorf("failed to declare direct exchange: %w", err)
	}

	// Declare queues
	queues := map[string]string{
		"parser.queue":            "parser.*",
		"chunk.queue":             "chunk.*",
		"embedding.queue":         "embedding.*",
		"retrieval.queue":         "retrieval.*",
		"generation.queue":        "generation.*",
		"vision.queue":            "vision.*",
		"metadata.queue":          "metadata.*",
		"reranking.queue":         "reranking.*",
		"parser.result.queue":     "parser.result.*",
		"chunk.result.queue":      "chunk.result.*",
		"embedding.result.queue":  "embedding.result.*",
		"generation.result.queue": "generation.result.*",
		"vision.result.queue":     "vision.result.*",
		"metadata.result.queue":   "metadata.result.*",
		"reranking.result.queue":  "reranking.result.*",
	}

	for queueName, routingKey := range queues {
		_, err := p.channel.QueueDeclare(
			queueName,
			true,
			false,
			false,
			false,
			amqp.Table{
				"x-max-length":  10000,
				"x-message-ttl": 3600000,
			},
		)
		if err != nil {
			return fmt.Errorf("failed to declare queue %s: %w", queueName, err)
		}

		// Bind queue to exchange
		exchange := "ai.platform.exchange"
		if queueName[len(queueName)-6:] == ".queue" && queueName[:7] != "parser." && queueName[:6] != "chunk." && queueName[:10] != "embedding." && queueName[:11] != "generation." && queueName[:6] != "vision." && queueName[:9] != "metadata." && queueName[:11] != "reranking." {
			exchange = "ai.platform.direct"
		}

		if err := p.channel.QueueBind(
			queueName,
			routingKey,
			exchange,
			false,
			nil,
		); err != nil {
			return fmt.Errorf("failed to bind queue %s: %w", queueName, err)
		}
	}

	return nil
}

// PublishMessage publishes a message to RabbitMQ
func (p *RabbitMQProducer) PublishMessage(ctx context.Context, queueName, routingKey string, message *BaseMessage) error {
	body, err := json.Marshal(message)
	if err != nil {
		return fmt.Errorf("failed to marshal message: %w", err)
	}

	exchange := "ai.platform.exchange"
	if queueName[len(queueName)-6:] == ".result" {
		exchange = "ai.platform.direct"
	}

	err = p.channel.PublishWithContext(
		ctx,
		exchange,
		routingKey,
		false,
		false,
		amqp.Publishing{
			ContentType:   "application/json",
			DeliveryMode:  amqp.Persistent,
			ReplyTo:       message.ReplyTo,
			CorrelationId: message.CorrelationID,
			Body:          body,
		},
	)

	if err != nil {
		return fmt.Errorf("failed to publish message: %w", err)
	}

	log.Printf("Published message to %s: %s", routingKey, message.MessageType)
	return nil
}

// PublishParseDocument publishes a document parsing request
func (p *RabbitMQProducer) PublishParseDocument(ctx context.Context, documentID, documentData, documentType string, metadata map[string]interface{}) error {
	message := NewBaseMessage(MessageTypeParseDocument, "high", map[string]interface{}{
		"document_id":   documentID,
		"document_data": documentData,
		"document_type": documentType,
		"metadata":      metadata,
	})

	return p.PublishMessage(ctx, "parser.queue", "parser.parse_document", message)
}

// PublishEmbedText publishes a text embedding request
func (p *RabbitMQProducer) PublishEmbedText(ctx context.Context, textID, textContent, model string, metadata map[string]interface{}) error {
	message := NewBaseMessage(MessageTypeEmbedText, "medium", map[string]interface{}{
		"text_id":      textID,
		"text_content": textContent,
		"model":        model,
		"metadata":     metadata,
	})

	return p.PublishMessage(ctx, "embedding.queue", "embedding.embed_text", message)
}

// PublishSemanticSearch publishes a semantic search request
func (p *RabbitMQProducer) PublishSemanticSearch(ctx context.Context, query, collectionName string, limit int, filters map[string]interface{}) error {
	message := NewBaseMessage(MessageTypeSemanticSearch, "medium", map[string]interface{}{
		"query":           query,
		"collection_name": collectionName,
		"limit":           limit,
		"filters":         filters,
	})

	return p.PublishMessage(ctx, "retrieval.queue", "retrieval.semantic_search", message)
}

// PublishGenerateText publishes a text generation request
func (p *RabbitMQProducer) PublishGenerateText(ctx context.Context, prompt, provider, model string, temperature float64, maxTokens int, metadata map[string]interface{}) error {
	message := NewBaseMessage(MessageTypeGenerateText, "medium", map[string]interface{}{
		"prompt":      prompt,
		"provider":    provider,
		"model":       model,
		"temperature": temperature,
		"max_tokens":  maxTokens,
		"metadata":    metadata,
	})

	return p.PublishMessage(ctx, "generation.queue", "generation.generate_text", message)
}

// PublishChunkCompetency publishes a competency-based chunking request
func (p *RabbitMQProducer) PublishChunkCompetency(ctx context.Context, contentID, content, competencyType string, metadata map[string]interface{}) error {
	message := NewBaseMessage(MessageTypeParseDocument, "medium", map[string]interface{}{
		"content_id":      contentID,
		"content":         content,
		"competency_type": competencyType,
		"metadata":        metadata,
	})

	return p.PublishMessage(ctx, "chunk.queue", "chunk.chunk_competency", message)
}

// PublishEnrichDifficulty publishes a difficulty enrichment request
func (p *RabbitMQProducer) PublishEnrichDifficulty(ctx context.Context, contentID, content, contentType string, metadata map[string]interface{}) error {
	message := NewBaseMessage(MessageTypeParseDocument, "medium", map[string]interface{}{
		"content_id":   contentID,
		"content":      content,
		"content_type": contentType,
		"metadata":     metadata,
	})

	return p.PublishMessage(ctx, "metadata.queue", "metadata.enrich_difficulty", message)
}

// PublishProcessOCR publishes an OCR processing request
func (p *RabbitMQProducer) PublishProcessOCR(ctx context.Context, imageID, imageData, language string, metadata map[string]interface{}) error {
	message := NewBaseMessage(MessageTypeProcessOCR, "high", map[string]interface{}{
		"image_id":   imageID,
		"image_data": imageData,
		"language":   language,
		"metadata":   metadata,
	})

	return p.PublishMessage(ctx, "vision.queue", "vision.process_ocr", message)
}

// PublishRerankCrossEncoder publishes a cross-encoder reranking request
func (p *RabbitMQProducer) PublishRerankCrossEncoder(ctx context.Context, query string, documents []map[string]interface{}, topK int, metadata map[string]interface{}) error {
	message := NewBaseMessage(MessageTypeSemanticSearch, "medium", map[string]interface{}{
		"query":     query,
		"documents": documents,
		"top_k":     topK,
		"metadata":  metadata,
	})

	return p.PublishMessage(ctx, "reranking.queue", "reranking.rerank_cross_encoder", message)
}

// Close closes the RabbitMQ producer
func (p *RabbitMQProducer) Close() error {
	if p.channel != nil {
		if err := p.channel.Close(); err != nil {
			return fmt.Errorf("failed to close channel: %w", err)
		}
	}
	return nil
}
