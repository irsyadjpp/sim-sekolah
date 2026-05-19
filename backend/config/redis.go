package config

import (
	"context"
	"fmt"
	"log"

	"github.com/redis/go-redis/v9"
)

var RedisClient *redis.Client
var ctx = context.Background()

func ConnectRedis() {
	host := Cfg.Database.Redis.Host
	port := Cfg.Database.Redis.Port
	password := Cfg.Database.Redis.Password
	db := Cfg.Database.Redis.DB

	RedisClient = redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", host, port),
		Password: password,
		DB:       db,
	})

	_, err := RedisClient.Ping(ctx).Result()
	if err != nil {
		log.Printf("⚠️ Redis connection failed: %v", err)
	} else {
		log.Println("✅ Redis Connected")
	}
}
