package config

import (
	"log"
	"strings"

	"github.com/spf13/viper"
)

type Config struct {
	App struct {
		Name             string `mapstructure:"name"`
		Port             string `mapstructure:"port"`
		Env              string `mapstructure:"env"`
		CORSAllowOrigins string `mapstructure:"cors_allow_origins"`
		LogLevel         string `mapstructure:"log_level"`
	} `mapstructure:"app"`

	Auth struct {
		JWT struct {
			Secret     string `mapstructure:"secret"`
			ExpireHour int    `mapstructure:"expire_hour"`
		} `mapstructure:"jwt"`
		Bcrypt struct {
			Cost int `mapstructure:"cost"`
		} `mapstructure:"bcrypt"`
	} `mapstructure:"auth"`

	Database struct {
		Postgres struct {
			Host     string `mapstructure:"host"`
			Port     string `mapstructure:"port"`
			User     string `mapstructure:"user"`
			Password string `mapstructure:"password"`
			Name     string `mapstructure:"name"`
			SSLMode  string `mapstructure:"ssl_mode"`
		} `mapstructure:"postgres"`
		Redis struct {
			Host     string `mapstructure:"host"`
			Port     string `mapstructure:"port"`
			Password string `mapstructure:"password"`
			DB       int    `mapstructure:"db"`
		} `mapstructure:"redis"`
	} `mapstructure:"database"`

	Storage struct {
		RustFSURL string `mapstructure:"rustfs_url"`
	} `mapstructure:"storage"`

	AI struct {
		OllamaURL string `mapstructure:"ollama_url"`
	} `mapstructure:"ai"`

	Messaging struct {
		RabbitMQ struct {
			Host     string `mapstructure:"host"`
			Port     string `mapstructure:"port"`
			User     string `mapstructure:"user"`
			Password string `mapstructure:"password"`
		} `mapstructure:"rabbitmq"`
		RabbitMQURL  string `mapstructure:"rabbitmq_url"`
		KafkaBrokers string `mapstructure:"kafka_brokers"`
	} `mapstructure:"messaging"`
}

var Cfg Config

func InitConfig() {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	viper.AddConfigPath("./config")

	// Environment variables
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
	viper.AutomaticEnv()

	// Bind legacy environment variables to nested config
	_ = viper.BindEnv("messaging.rabbitmq_url", "RABBITMQ_URL")
	_ = viper.BindEnv("database.redis.host", "REDIS_HOST")
	_ = viper.BindEnv("database.redis.port", "REDIS_PORT")
	_ = viper.BindEnv("database.redis.password", "REDIS_PASSWORD")
	_ = viper.BindEnv("database.redis.db", "REDIS_DB")

	// Default values
	viper.SetDefault("app.name", "SIM Sekolah")
	viper.SetDefault("app.env", "development")
	viper.SetDefault("app.port", "8080")
	viper.SetDefault("app.cors_allow_origins", "http://localhost:3000")
	viper.SetDefault("database.redis.port", "6379")
	viper.SetDefault("database.postgres.ssl_mode", "disable")

	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			log.Printf("⚠️ Config file 'config.yaml' not found, falling back to environment variables")
		} else {
			log.Printf("❌ Error reading config file: %v", err)
		}
	}

	if err := viper.Unmarshal(&Cfg); err != nil {
		log.Fatalf("Unable to decode into struct, %v", err)
	}

	log.Println("✅ Configuration Loaded")
}
