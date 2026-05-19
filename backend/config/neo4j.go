package config

import (
	"context"
	"log"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

var Neo4jDriver neo4j.DriverWithContext

func ConnectNeo4j() {
	uri := Cfg.Graph.Neo4j.URI
	username := Cfg.Graph.Neo4j.User
	password := Cfg.Graph.Neo4j.Password

	driver, err := neo4j.NewDriverWithContext(
		uri,
		neo4j.BasicAuth(username, password, ""),
	)

	if err != nil {
		log.Println("Neo4j connection failed")
		return
	}

	err = driver.VerifyConnectivity(context.Background())

	if err != nil {
		log.Println("Neo4j verify failed")
		return
	}

	Neo4jDriver = driver

	log.Println("✅ Neo4j Connected")
}
