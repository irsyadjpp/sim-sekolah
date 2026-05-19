package cache

import (
	"context"
	"encoding/json"
	"time"

	"github.com/redis/go-redis/v9"
)

// Cache merepresentasikan pembungkus Redis client untuk keperluan caching taktis
type Cache struct {
	client *redis.Client
}

// GlobalCache adalah instance cache global yang dapat digunakan di seluruh modul repository/service
var GlobalCache *Cache

// InitCache menginisialisasi instansi cache global dengan Redis client yang terhubung
func InitCache(client *redis.Client) {
	GlobalCache = &Cache{client: client}
}

// Get membaca entri cache berdasarkan key dan melakukan unmarshal ke objek dest
func (c *Cache) Get(ctx context.Context, key string, dest interface{}) error {
	if c.client == nil {
		return redis.Nil
	}
	val, err := c.client.Get(ctx, key).Result()
	if err != nil {
		return err
	}
	return json.Unmarshal([]byte(val), dest)
}

// Set menulis nilai baru ke dalam cache dengan key dan durasi TTL tertentu
func (c *Cache) Set(ctx context.Context, key string, value interface{}, expiration time.Duration) error {
	if c.client == nil {
		return nil
	}
	bytes, err := json.Marshal(value)
	if err != nil {
		return err
	}
	return c.client.Set(ctx, key, bytes, expiration).Err()
}

// Delete menghapus entri cache tertentu (invalidasi cache)
func (c *Cache) Delete(ctx context.Context, key string) error {
	if c.client == nil {
		return nil
	}
	return c.client.Del(ctx, key).Err()
}

// DeletePattern menghapus seluruh entri cache yang cocok dengan pola wildcard secara aman (non-blocking)
func (c *Cache) DeletePattern(ctx context.Context, pattern string) error {
	if c.client == nil {
		return nil
	}
	var cursor uint64
	for {
		keys, nextCursor, err := c.client.Scan(ctx, cursor, pattern, 100).Result()
		if err != nil {
			return err
		}
		if len(keys) > 0 {
			if err := c.client.Del(ctx, keys...).Err(); err != nil {
				return err
			}
		}
		cursor = nextCursor
		if cursor == 0 {
			break
		}
	}
	return nil
}
