package main

import (
	"flag"
	"log"

	"sim-sekolah/config"
)

func main() {
	version := flag.Int("version", 46, "Migration version to force (default: 46, before 000047)")
	flag.Parse()

	config.InitConfig()
	config.ConnectPostgres()

	sqlDB, err := config.DB.DB()
	if err != nil {
		log.Fatal("Failed to get sql.DB from GORM", err)
	}

	log.Printf("Forcing migration version to %d...", *version)
	if err := config.ForceMigrationVersion(sqlDB, *version); err != nil {
		log.Fatal("Failed to force migration version:", err)
	}
	log.Println("Migration version forced successfully. You can now restart the application to re-run migrations.")
}
