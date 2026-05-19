package common

import (
	"context"
	"encoding/json"
	"time"

	"github.com/redis/go-redis/v9"
)

// GetOrSetCache fetches data from cache or runs fetchFunc to retrieve and cache it.
func GetOrSetCache[T any](
	ctx context.Context,
	rdb *redis.Client,
	key string,
	expiration time.Duration,
	fetchFunc func() (T, error),
) (T, error) {
	var result T

	if rdb == nil {
		return fetchFunc()
	}

	// 1. Try to get from Redis
	val, err := rdb.Get(ctx, key).Result()
	if err == nil {
		// Cache Hit
		if err := json.Unmarshal([]byte(val), &result); err == nil {
			return result, nil
		}
	}

	// 2. Cache Miss - Fetch from database
	result, err = fetchFunc()
	if err != nil {
		return result, err
	}

	// 3. Serialize and save to Redis
	jsonData, err := json.Marshal(result)
	if err == nil {
		_ = rdb.Set(ctx, key, jsonData, expiration).Err()
	}

	return result, nil
}
