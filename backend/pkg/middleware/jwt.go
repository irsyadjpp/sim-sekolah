package middleware

import (
	"context"
	"sim-sekolah/config"
	"strings"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
)

var JWT_SECRET = []byte(config.GetEnv("JWT_SECRET", "4f9d7c2b1a8e6f5d9c3b7e1a2f4c8d6e9b1f3a7c5d8e2f6a1b9c4d7e8f2a6c1"))

type JWTCustomClaims struct {
	UserID         string   `json:"user_id"`
	Username       string   `json:"username"`
	Roles          []string `json:"roles"`
	ImpersonatorID string   `json:"impersonator_id,omitempty"`
	jwt.RegisteredClaims
}

func Protected() fiber.Handler {

	return func(c *fiber.Ctx) error {

		authHeader := c.Get("Authorization")

		if authHeader == "" {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"success": false,
				"message": "Tidak terautentikasi",
			})
		}

		tokenString := strings.Replace(authHeader, "Bearer ", "", 1)

		if config.RedisClient != nil {
			blacklisted, err := config.RedisClient.Exists(c.UserContext(), "blacklist:"+tokenString).Result()
			if err == nil && blacklisted > 0 {
				return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
					"status":  "error",
					"message": "Token telah logout",
				})
			}
		}

		token, err := jwt.ParseWithClaims(tokenString, &JWTCustomClaims{}, func(token *jwt.Token) (interface{}, error) {
			return JWT_SECRET, nil
		})

		if err != nil || !token.Valid {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"status":  "error",
				"message": "Token tidak valid",
			})
		}

		claims, ok := token.Claims.(*JWTCustomClaims)
		if !ok {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"status":  "error",
				"message": "Klaim token tidak valid",
			})
		}

		// Set to fiber locals
		c.Locals("user_id", claims.UserID)
		c.Locals("username", claims.Username)
		c.Locals("roles", claims.Roles)
		if claims.ImpersonatorID != "" {
			c.Locals("impersonator_id", claims.ImpersonatorID)
		}

		// Propagate to Go context for repositories/services
		//nolint:staticcheck // SA1029: using built-in string type as key for backward compatibility across modules
		ctx := context.WithValue(c.UserContext(), "user_id", claims.UserID)
		//nolint:staticcheck // SA1029: using built-in string type as key for backward compatibility across modules
		ctx = context.WithValue(ctx, "roles", claims.Roles)
		if claims.ImpersonatorID != "" {
			//nolint:staticcheck // SA1029: using built-in string type as key for backward compatibility across modules
			ctx = context.WithValue(ctx, "impersonator_id", claims.ImpersonatorID)
		}
		c.SetUserContext(ctx)

		return c.Next()
	}
}
