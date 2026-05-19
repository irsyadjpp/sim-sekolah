package config

import (
	"fmt"
	"log"

	amqp "github.com/rabbitmq/amqp091-go"
)

var RabbitMQConn *amqp.Connection

func ConnectRabbitMQ() {
	url := Cfg.Messaging.RabbitMQURL
	if url == "" {
		// Fallback to constructed URL
		url = fmt.Sprintf("amqp://%s:%s@%s:%s/",
			Cfg.Messaging.RabbitMQ.User,
			Cfg.Messaging.RabbitMQ.Password,
			Cfg.Messaging.RabbitMQ.Host,
			Cfg.Messaging.RabbitMQ.Port)
	}

	conn, err := amqp.Dial(url)

	if err != nil {
		log.Printf("RabbitMQ connection failed: %v", err)
		return
	}

	RabbitMQConn = conn

	log.Println("✅ RabbitMQ Connected")
}
