# Centralized Infrastructure

This directory contains all infrastructure configurations for the SIM Sekolah monorepo, providing a centralized location for Docker Compose files, Kubernetes manifests, monitoring configurations, and service-specific configurations.

## Architecture Overview

The system uses a **monolith-only architecture** for the AI Platform, combined with a separate SIM Sekolah backend/frontend stack.

## Directory Structure

```
infrastructure/
├── README.md                          # This file
├── compose/                          # Docker Compose files
│   ├── sim-sekolah/                  # SIM Sekolah stack
│   │   └── docker-compose.yml        # Main SIM Sekolah compose file
│   └── ai-platform/                  # AI Platform monolith stack
│       └── docker-compose.yml        # Monolith architecture
├── kubernetes/                        # Kubernetes manifests
│   ├── sim-sekolah/                  # SIM Sekolah K8s resources
│   └── shared/                       # Shared K8s resources
├── monitoring/                        # Monitoring configurations
│   ├── grafana/                      # Grafana dashboards and provisioning
│   │   ├── provisioning/
│   │   └── dashboards/
│   ├── prometheus/                   # Prometheus configuration
│   │   └── prometheus.yml
│   ├── loki/                         # Loki log aggregation
│   │   └── loki-config.yml
│   └── tempo/                        # Tempo distributed tracing
│       └── tempo.yaml
├── services/                          # Service configurations
│   ├── postgres/                     # PostgreSQL configuration
│   ├── redis/                        # Redis configuration
│   ├── rabbitmq/                     # RabbitMQ configuration
│   ├── qdrant/                       # Qdrant vector database
│   ├── minio/                        # MinIO object storage
│   ├── kafka/                        # Kafka configuration
│   └── nginx/                        # Nginx configuration
└── scripts/                           # Infrastructure scripts
    ├── setup/                        # Setup scripts
    ├── backup/                       # Backup scripts
    └── migration/                    # Migration scripts
```

## Usage

### SIM Sekolah Stack

```bash
# Start SIM Sekolah services
docker compose -f infrastructure/compose/sim-sekolah/docker-compose.yml up
```

### AI Platform Monolith Stack

```bash
# Start AI Platform monolith
docker compose -f infrastructure/compose/ai-platform/docker-compose.yml up
```

### Combined Stack (All Services)

```bash
# Start both SIM Sekolah and AI Platform
docker compose -f infrastructure/compose/sim-sekolah/docker-compose.yml up -d
docker compose -f infrastructure/compose/ai-platform/docker-compose.yml up -d
```

### Quick Start from Root

```bash
# From project root, start SIM Sekolah
docker compose -f infrastructure/compose/sim-sekolah/docker-compose.yml up

# From project root, start AI Platform
docker compose -f infrastructure/compose/ai-platform/docker-compose.yml up
```

### Kubernetes Deployment

```bash
# SIM Sekolah
kubectl apply -f infrastructure/kubernetes/sim-sekolah/

# Shared resources
kubectl apply -f infrastructure/kubernetes/shared/
```

## Service Dependencies

### SIM Sekolah Stack
- **PostgreSQL**: Primary database
- **Redis**: Caching and session management
- **RabbitMQ**: Message queue for async processing
- **Qdrant**: Vector database for AI features
- **MinIO**: Object storage for documents
- **Go Backend**: Core business logic
- **OTel Collector**: Observability data collection

### AI Platform Monolith Stack
- **PostgreSQL**: Primary database
- **Qdrant**: Vector database for embeddings
- **Redis**: Caching
- **RabbitMQ**: Message queue
- **MinIO**: Object storage
- **Monolith Application**: Unified AI Platform application

### Monitoring Stack
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation
- **Tempo**: Distributed tracing

## Best Practices

1. **Use docker compose**: The system uses `docker compose` (not `docker-compose`)
2. **Resource limits**: Configure appropriate resource limits for production
3. **Security**: Enable security hardening for production deployments
4. **Monitoring**: Always run the monitoring stack in production
5. **Backups**: Use the backup scripts in `scripts/backup/` for regular backups
6. **Secrets**: Never commit secrets to version control, use environment variables

## Troubleshooting

### Port Conflicts
Check the port mappings in the docker-compose files and adjust as needed.

### Volume Issues
Ensure volume names don't conflict between different stacks.

### Network Issues
Ensure all services are on the same Docker network for inter-service communication.

### Health Check Failures
Check health check configurations in docker-compose files and adjust timeouts/retries.

## Maintenance

### Cleaning Up
```bash
# Stop all containers
docker compose -f infrastructure/compose/sim-sekolah/docker-compose.yml down
docker compose -f infrastructure/compose/ai-platform/docker-compose.yml down

# Remove volumes
docker volume prune

# Remove unused images
docker image prune
```

## Support

For infrastructure-related issues, check the documentation in the respective service directories.
