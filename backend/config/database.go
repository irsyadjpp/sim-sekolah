package config

import (
	"log"
	"time"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConnectPostgres() {
	dsn := Cfg.Database.Postgres.Host
	if dsn == "" {
		// Fallback to Env if host is empty in yaml
		dsn = GetEnv("DATABASE_URL", "")
	} else {
		dsn = "host=" + Cfg.Database.Postgres.Host +
			" user=" + Cfg.Database.Postgres.User +
			" password=" + Cfg.Database.Postgres.Password +
			" dbname=" + Cfg.Database.Postgres.Name +
			" port=" + Cfg.Database.Postgres.Port +
			" sslmode=" + Cfg.Database.Postgres.SSLMode
	}

	database, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed connect PostgreSQL: ", err)
	}

	// Optimize DB Connection Pool
	sqlDB, err := database.DB()
	if err == nil {
		sqlDB.SetMaxIdleConns(15)
		sqlDB.SetMaxOpenConns(100)
		sqlDB.SetConnMaxLifetime(time.Hour)
	}

	DB = database
	log.Println("✅ PostgreSQL Connected (Connection Pool Tuned)")
}
