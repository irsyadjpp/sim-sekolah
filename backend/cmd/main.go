package main

import (
	"context"
	"fmt"
	"strconv"
	"time"

	"github.com/gofiber/contrib/otelfiber/v2"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/compress"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/helmet"
	"github.com/gofiber/fiber/v2/middleware/limiter"
	"github.com/gofiber/fiber/v2/middleware/recover"
	"github.com/gofiber/fiber/v2/middleware/requestid"
	redisstorage "github.com/gofiber/storage/redis/v2"
	"github.com/gofiber/swagger"
	"log/slog"

	"sim-sekolah/config"
	_ "sim-sekolah/docs"
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"
	"sim-sekolah/pkg/cache"
	"sim-sekolah/pkg/logger"
	"sim-sekolah/routes"
)

// ======================================================
// ======================================================
// SWAGGER CONFIG
// ======================================================

// @title SIM Sekolah API
// @version 1.0
// @description Dokumentasi API Terpadu SIM Sekolah SD Negeri.
// @termsOfService http://example.com/terms/

// @contact.name Developer Team
// @contact.email admin@simsekolah.com

// @license.name MIT
// @license.url https://opensource.org/licenses/MIT

// @host localhost:8080
// @BasePath /api/v1

// @securityDefinitions.apikey BearerAuth
// @in header
// @name Authorization
func main() {
	// 1. Initialize Config (Required by Logger & DB)
	config.InitConfig()

	// 2. Initialize Logger (Structured JSON)
	logger.InitLogger()

	// 3. Initialize OpenTelemetry (Enterprise OTLP)
	shutdownOTel, err := logger.InitOTel(context.Background(), config.Cfg.App.Name)
	if err != nil {
		logger.Error("Failed to initialize OTel", err)
	} else {
		defer func() {
			_ = shutdownOTel(context.Background())
		}()
	}

	// ======================================================
	// LOAD ENV (Backward compatibility for now)
	// ======================================================
	config.LoadEnv()

	// ======================================================
	// CONNECT DATABASE
	// ======================================================
	config.ConnectPostgres()

	// Run versioned database migrations (menggantikan GORM AutoMigrate)
	sqlDB, err := config.DB.DB()
	if err != nil {
		logger.Fatal("Failed to get sql.DB from GORM", err)
	}
	if err := config.RunMigrations(sqlDB); err != nil {
		logger.Fatal("Database migration failed", err)
	}

	// Initialize System Views
	if err := system.NewSystemRepository(config.DB).InitViewsAndSeed(context.Background()); err != nil {
		logger.Error("Failed to initialize system views", err)
	}

	// ======================================================
	// CONNECT RABBITMQ
	// ======================================================
	config.ConnectRabbitMQ()

	// ======================================================
	// CONNECT REDIS
	// ======================================================
	config.ConnectRedis()
	if config.RedisClient != nil {
		cache.InitCache(config.RedisClient)
	}

	// ======================================================
	// CREATE FIBER APP
	// ======================================================
	app := fiber.New(fiber.Config{
		AppName:      config.Cfg.App.Name,
		ServerHeader: "Fiber",

		ErrorHandler: func(c *fiber.Ctx, err error) error {

			code := fiber.StatusInternalServerError

			if e, ok := err.(*fiber.Error); ok {
				code = e.Code
			}

			msg := common.UserMessage(err)
			if msg == err.Error() && code == fiber.StatusNotFound {
				msg = "Resource tidak ditemukan"
			}
			return c.Status(code).JSON(fiber.Map{
				"success": false,
				"message": msg,
				"error":   err.Error(),
			})
		},
	})

	// ======================================================
	// MIDDLEWARE
	// ======================================================

	// RECOVER PANIC
	app.Use(recover.New())

	// COMPRESSION MIDDLEWARE (extremely important for island's limited bandwidth)
	app.Use(compress.New(compress.Config{
		Level: compress.LevelBestSpeed,
	}))

	// REQUEST ID
	app.Use(requestid.New())

	// OTEL TRACING
	app.Use(otelfiber.Middleware())

	// ENTERPRISE LOGGER
	app.Use(logger.Middleware())

	// HELMET (Security Headers)
	app.Use(helmet.New())

	// GLOBAL RATE LIMITER (Redis-backed, persists across restarts)
	redisPort, _ := strconv.Atoi(config.Cfg.Database.Redis.Port)
	if redisPort == 0 {
		redisPort = 6379
	}
	rateLimitStore := redisstorage.New(redisstorage.Config{
		Host:     config.Cfg.Database.Redis.Host,
		Port:     redisPort,
		Password: config.Cfg.Database.Redis.Password,
		Database: config.Cfg.Database.Redis.DB,
	})
	app.Use(limiter.New(limiter.Config{
		Storage:    rateLimitStore,
		Max:        100,             // 100 requests
		Expiration: 1 * time.Minute, // per 1 minute
		KeyGenerator: func(c *fiber.Ctx) string {
			return c.IP() // per IP
		},
		LimitReached: func(c *fiber.Ctx) error {
			return c.Status(fiber.StatusTooManyRequests).JSON(fiber.Map{
				"success": false,
				"message": "Terlalu banyak permintaan. Harap tunggu sebentar.",
			})
		},
	}))

	// CORS
	allowOrigins := config.Cfg.App.CORSAllowOrigins
	if allowOrigins == "" {
		allowOrigins = "http://localhost:3000" // Default to avoid wildcard panic
	}

	app.Use(cors.New(cors.Config{
		AllowOrigins:     allowOrigins,
		AllowHeaders:     "Origin, Content-Type, Accept, Authorization, X-Request-ID",
		AllowMethods:     "GET,POST,PUT,DELETE,PATCH,OPTIONS",
		AllowCredentials: true,
	}))

	// ======================================================
	// HEALTH CHECK
	// ======================================================
	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"success": true,
			"message": "SIM Sekolah Backend Running",
		})
	})

	// ======================================================
	// API DOCUMENTATION (Swagger, ReDoc, Scalar)
	// ======================================================
	app.Get("/swagger/*", swagger.HandlerDefault)

	app.Get("/redoc", func(c *fiber.Ctx) error {
		c.Type("html")
		return c.SendString(`
<!DOCTYPE html>
<html>
<head>
  <title>SIM Sekolah API - ReDoc (Enterprise Business View)</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
  <style>body { margin: 0; padding: 0; }</style>
</head>
<body>
  <!-- Mengambil data langsung dari endpoint Swagger bawaan Fiber -->
  <redoc 
    spec-url="/swagger/doc.json" 
    theme='{
      "colors": {
        "primary": { "main": "#8b5cf6" },
        "success": { "main": "#10b981" },
        "warning": { "main": "#f59e0b" },
        "error": { "main": "#ef4444" },
        "text": { "primary": "#1f2937" }
      },
      "typography": {
        "fontFamily": "Montserrat, sans-serif",
        "headings": {
          "fontFamily": "Montserrat, sans-serif",
          "fontWeight": "700"
        }
      }
    }'
    expand-responses="200,201"
    required-props-first="true"
    hide-hostname="false"
    no-auto-auth="false">
  </redoc>
  <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
</body>
</html>
		`)
	})

	app.Get("/scalar", func(c *fiber.Ctx) error {
		c.Type("html")
		return c.SendString(`
<!DOCTYPE html>
<html>
<head>
  <title>SIM Sekolah API - Scalar (Technical Sandbox View)</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>body { margin: 0; padding: 0; }</style>
</head>
<body>
  <!-- Mengambil data langsung dari endpoint Swagger bawaan Fiber -->
  <script 
    id="api-reference" 
    data-url="/swagger/doc.json" 
    data-configuration='{
      "theme": "purple",
      "showSidebar": true,
      "searchHotKey": "k",
      "layout": "modern",
      "authentication": {
        "preferredSecurityScheme": "BearerAuth"
      },
      "defaultHttpClient": {
        "targetKey": "javascript",
        "clientKey": "fetch"
      }
    }'></script>
  <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
</body>
</html>
		`)
	})

	// ======================================================
	// API ROUTES
	// ======================================================
	api := app.Group("/api/v1")

	routes.SetupRoutes(api, config.DB, config.RedisClient)

	// ======================================================
	// START SERVER
	// ======================================================
	port := config.Cfg.App.Port

	// Start async job queue worker in background (Redis List BRPOP)
	if config.RedisClient != nil {
		queueSvc := system.NewQueueService(config.RedisClient, config.DB)
		go queueSvc.StartWorker(context.Background())
		logger.Info("🔁 System queue worker started")
	}

	logger.Info("🚀 Server starting",
		slog.String("port", port),
		slog.String("swagger", fmt.Sprintf("http://localhost:%s/swagger/index.html", port)),
	)

	// Graceful Shutdown
	go func() {
		if err := app.Listen(":" + port); err != nil {
			logger.Fatal("Failed to start server", err)
		}
	}()

	// Wait for interrupt signal
	config.GracefulShutdown(app)
}
