package auth

import (
	"context"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
	"gorm.io/gorm"

	"sim-sekolah/config"
	"sim-sekolah/pkg/cache"
)

type JWTCustomClaims struct {
	UserID   string   `json:"user_id"`
	Username string   `json:"username"`
	Roles    []string `json:"roles"`
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

		token, err := jwt.ParseWithClaims(
			tokenString,
			&JWTCustomClaims{},
			func(token *jwt.Token) (interface{}, error) {
				return []byte(config.GetEnv("JWT_SECRET", "4f9d7c2b1a8e6f5d9c3b7e1a2f4c8d6e9b1f3a7c5d8e2f6a1b9c4d7e8f2a6c1")), nil
			},
		)

		if err != nil {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"status":  "error",
				"message": "Token tidak valid",
			})
		}

		claims, ok := token.Claims.(*JWTCustomClaims)

		if !ok || !token.Valid {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"status":  "error",
				"message": "Klaim token tidak valid",
			})
		}

		c.Locals("user_id", claims.UserID)
		c.Locals("username", claims.Username)
		c.Locals("roles", claims.Roles)

		// Inject to fiber UserContext so it propagates to repository/service context
		//nolint:staticcheck // SA1029: using built-in string type as key for backward compatibility across modules
		ctx := context.WithValue(c.UserContext(), "user_id", claims.UserID)
		//nolint:staticcheck // SA1029: using built-in string type as key for backward compatibility across modules
		ctx = context.WithValue(ctx, "roles", claims.Roles)
		c.SetUserContext(ctx)

		return c.Next()
	}
}

func RoleMiddleware(allowedRoles ...string) fiber.Handler {

	return func(c *fiber.Ctx) error {

		userRoles, ok := c.Locals("roles").([]string)
		if !ok {
			return c.Status(fiber.StatusForbidden).JSON(fiber.Map{
				"success": false,
				"message": "Akses ditolak: peran tidak ditemukan",
			})
		}

		// Admins and Super Admins bypass role checks
		for _, userRole := range userRoles {
			if userRole == "ADMIN" || userRole == "SUPER_ADMIN" {
				return c.Next()
			}
		}

		// Check if any of the user's roles matches any of the allowed roles
		for _, userRole := range userRoles {
			for _, allowed := range allowedRoles {
				if userRole == allowed {
					return c.Next()
				}
			}
		}

		return c.Status(fiber.StatusForbidden).JSON(fiber.Map{
			"success": false,
			"message": "Akses ditolak",
		})
	}
}

// PermissionMiddleware checks dynamic dynamic permissions associated with user roles
func PermissionMiddleware(db *gorm.DB, permissionName string) fiber.Handler {
	return func(c *fiber.Ctx) error {
		userRoles, ok := c.Locals("roles").([]string)
		if !ok || len(userRoles) == 0 {
			return c.Status(fiber.StatusForbidden).JSON(fiber.Map{
				"success": false,
				"message": "Akses ditolak: peran tidak ditemukan",
			})
		}

		// Super Admins & Admins bypass all permission checks
		for _, userRole := range userRoles {
			if userRole == "ADMIN" || userRole == "SUPER_ADMIN" {
				return c.Next()
			}
		}

		// 1. Check Redis cache first (ultra-fast dynamic permission validation)
		ctx := c.UserContext()
		cacheKey := "perms:" + strings.Join(userRoles, ",") + ":" + permissionName
		var allowed bool
		if cache.GlobalCache != nil {
			if err := cache.GlobalCache.Get(ctx, cacheKey, &allowed); err == nil && allowed {
				return c.Next()
			}
		}

		// 2. Query Postgres if cache miss
		var count int64
		err := db.Table("auth_role r").
			Joins("JOIN auth_role_permission rp ON rp.role_id = r.id").
			Joins("JOIN auth_permission p ON p.id = rp.permission_id").
			Where("r.role_name IN ? AND p.permission_name = ?", userRoles, permissionName).
			Count(&count).Error

		if err != nil || count == 0 {
			return c.Status(fiber.StatusForbidden).JSON(fiber.Map{
				"success": false,
				"message": "Akses ditolak: izin tidak memadai",
			})
		}

		// 3. Cache permission allow result for 1 Hour
		if cache.GlobalCache != nil {
			allowed = true
			_ = cache.GlobalCache.Set(ctx, cacheKey, allowed, 1*time.Hour)
		}

		return c.Next()
	}
}
