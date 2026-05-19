package config

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gofiber/fiber/v2"
)

func GracefulShutdown(app *fiber.App) {
	// Create channel to signify a signal being sent
	quit := make(chan os.Signal, 1)

	// When an interrupt or termination signal is sent, notify the channel
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

	// Wait for the channel to receive a signal
	<-quit

	log.Println("Gracefully shutting down...")

	// Create a context with a timeout for the shutdown process
	_, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Shutdown Fiber app
	if err := app.Shutdown(); err != nil {
		log.Fatalf("Fiber shutdown error: %v", err)
	}

	// Close Database Connections
	if DB != nil {
		sqlDB, err := DB.DB()
		if err == nil {
			log.Println("Closing Postgres Connection...")
			sqlDB.Close()
		}
	}

	if RedisClient != nil {
		log.Println("Closing Redis Connection...")
		RedisClient.Close()
	}

	// Neo4j, RabbitMQ etc should also be closed here
	// For now we rely on the process exit, but in a real app
	// we should have explicit Close() calls for all drivers.

	log.Println("Server stopped successfully")
}
