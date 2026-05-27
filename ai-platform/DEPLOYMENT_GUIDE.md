# AI Platform Deployment Guide

## Overview
This guide covers deployment of the AI Platform with the updated architecture using gRPC and RabbitMQ for internal service communication.

## Architecture Summary

**Target Architecture**:
```
External Client → Gateway Service (REST API) → Backend (Go)
                                                    ↓
                                              gRPC / RabbitMQ
                                                    ↓
                                            AI Platform Services
                                            (Internal Only)
```

**Key Changes from Previous Architecture**:
- AI services no longer expose REST endpoints externally
- Single entry point through Gateway Service (port 8002)
- Internal communication via gRPC (sync) and RabbitMQ (async)
- Reduced attack surface (1 external port vs 9+)

## Prerequisites

### System Requirements
- Docker 20.10+
- Docker Compose 2.0+
- Kubernetes 1.24+ (for K8s deployment)
- 8GB RAM minimum
- 50GB disk space
- GPU support (optional, for embedding/reranking services)

### Software Dependencies
- Python 3.11+
- Go 1.21+
- PostgreSQL 15
- Qdrant 1.7+
- RabbitMQ 3.12+
- Redis 7+

## Environment Configuration

### Environment Variables

Create `.env` file based on `.env.example`:

```bash
# Gateway Service
GATEWAY_PORT=8002
JWT_SECRET=your-secret-key
RATE_LIMIT_ENABLED=true

# Backend (Go)
BACKEND_PORT=8080
DATABASE_URL=postgresql://user:password@postgres:5432/ai_platform
REDIS_URL=redis://redis:6379
RABBITMQ_URL=amqp://user:password@rabbitmq:5672/

# AI Services - Common
ENABLE_GRPC_SERVER=true
ENABLE_RABBITMQ_CONSUMER=true
RABBITMQ_URL=amqp://user:password@rabbitmq:5672/

# Service-Specific gRPC Ports
PARSER_GRPC_PORT=50051
VISION_GRPC_PORT=50055
CHUNK_GRPC_PORT=50056
METADATA_GRPC_PORT=50057
EMBEDDING_GRPC_PORT=50052
RETRIEVAL_GRPC_PORT=50054
RERANKING_GRPC_PORT=50058
GENERATION_GRPC_PORT=50053

# Database
POSTGRES_USER=ai_platform
POSTGRES_PASSWORD=your-password
POSTGRES_DB=ai_platform

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_BUCKET=ai-platform-documents

# RabbitMQ
RABBITMQ_USER=ai_platform
RABBITMQ_PASSWORD=your-password

# Redis
REDIS_PASSWORD=your-password

# Optional: LLM API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
```

## Docker Compose Deployment

### Updated docker-compose.yml

Key changes from previous configuration:

```yaml
services:
  # Gateway Service - ONLY external entry point
  gateway-service:
    ports:
      - "8002:8002"  # KEEP - only external access
    environment:
      - ENABLE_GRPC_SERVER=false
      - ENABLE_RABBITMQ_CONSUMER=false
    depends_on:
      - backend

  # Backend (Go)
  backend:
    ports:
      - "8080:8080"  # Internal only, can be removed in production
    environment:
      - RABBITMQ_URL=amqp://user:password@rabbitmq:5672/
    depends_on:
      - postgres
      - redis
      - rabbitmq

  # AI Services - NO external ports
  parser-service:
    # REMOVE: ports: "8001:8001"
    expose:
      - 50051  # gRPC port only
    environment:
      - ENABLE_GRPC_SERVER=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - GRPC_PORT=50051
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - qdrant

  vision-service:
    # REMOVE: ports: "8005:8002"
    expose:
      - 50055  # gRPC port only
    environment:
      - ENABLE_GRPC_SERVER=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - GRPC_PORT=50055
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - qdrant

  semantic-chunk-service:
    # REMOVE: ports: "8003:8003"
    expose:
      - 50056  # gRPC port only
    environment:
      - ENABLE_GRPC_SERVER=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - GRPC_PORT=50056
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - qdrant

  metadata-service:
    # REMOVE: ports: "8004:8004"
    expose:
      - 50057  # gRPC port only
    environment:
      - ENABLE_GRPC_SERVER=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - GRPC_PORT=50057
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - qdrant

  embedding-service:
    # REMOVE: ports: "8006:8006"
    expose:
      - 50052  # gRPC port only
    environment:
      - ENABLE_GRPC_SERVER=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - GRPC_PORT=50052
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - qdrant

  retrieval-service:
    # REMOVE: ports: "8007:8007"
    expose:
      - 50054  # gRPC port only
    environment:
      - ENABLE_GRPC_SERVER=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - GRPC_PORT=50054
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - qdrant

  reranking-service:
    # REMOVE: ports: "8008:8008"
    expose:
      - 50058  # gRPC port only
    environment:
      - ENABLE_GRPC_SERVER=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - GRPC_PORT=50058
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - qdrant

  generation-service:
    # REMOVE: ports: "8009:8009"
    expose:
      - 50053  # gRPC port only
    environment:
      - ENABLE_GRPC_SERVER=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - GRPC_PORT=50053
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - qdrant

  # Infrastructure - No changes
  postgres:
    ports:
      - "5432:5432"  # Can be removed in production

  qdrant:
    ports:
      - "6333:6333"  # Can be removed in production

  redis:
    ports:
      - "6379:6379"  # Can be removed in production

  rabbitmq:
    ports:
      - "5672:5672"  # AMQP
      - "15672:15672"  # Management UI (can be removed in production)

  minio:
    ports:
      - "9000:9000"  # API
      - "9001:9001"  # Console (can be removed in production)

  # Monitoring - No changes
  prometheus:
    ports:
      - "9090:9090"

  grafana:
    ports:
      - "3000:3000"

  loki:
    ports:
      - "3100:3100"

  tempo:
    ports:
      - "3200:3200"
```

### Deployment Steps

1. **Clone repository**:
```bash
git clone <repository-url>
cd ai-platform
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Build images**:
```bash
docker-compose build
```

4. **Start services**:
```bash
docker-compose up -d
```

5. **Verify deployment**:
```bash
# Check all services are running
docker-compose ps

# Check Gateway health
curl http://localhost:8002/health

# Check Backend health
curl http://localhost:8080/health

# Check RabbitMQ Management UI
# Access: http://localhost:15672 (admin/admin)
```

6. **View logs**:
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f gateway-service
docker-compose logs -f backend
docker-compose logs -f parser-service
```

## Kubernetes Deployment

### Updated Kubernetes Manifests

Each AI service should use `ClusterIP` (internal only):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: parser-service
  namespace: ai-platform
spec:
  type: ClusterIP  # Internal only
  ports:
    - port: 50051  # gRPC port
      targetPort: 50051
      protocol: TCP
  selector:
    app: parser-service
```

Gateway Service remains `LoadBalancer` or `NodePort`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: gateway-service
  namespace: ai-platform
spec:
  type: LoadBalancer  # External access
  ports:
    - port: 8002
      targetPort: 8002
      protocol: TCP
  selector:
    app: gateway-service
```

### Deployment Steps

1. **Create namespace**:
```bash
kubectl create namespace ai-platform
```

2. **Create ConfigMap**:
```bash
kubectl apply -f infra/kubernetes/configmap.yaml
```

3. **Create Secrets**:
```bash
kubectl apply -f infra/kubernetes/secret.yaml
```

4. **Deploy infrastructure**:
```bash
kubectl apply -f infra/kubernetes/postgres.yaml
kubectl apply -f infra/kubernetes/qdrant.yaml
kubectl apply -f infra/kubernetes/redis.yaml
kubectl apply -f infra/kubernetes/rabbitmq.yaml
kubectl apply -f infra/kubernetes/minio.yaml
```

5. **Deploy monitoring stack**:
```bash
kubectl apply -f infra/kubernetes/prometheus.yaml
kubectl apply -f infra/kubernetes/grafana.yaml
kubectl apply -f infra/kubernetes/loki.yaml
kubectl apply -f infra/kubernetes/tempo.yaml
```

6. **Deploy AI services**:
```bash
kubectl apply -f infra/kubernetes/parser-service.yaml
kubectl apply -f infra/kubernetes/vision-service.yaml
kubectl apply -f infra/kubernetes/semantic-chunk-service.yaml
kubectl apply -f infra/kubernetes/metadata-service.yaml
kubectl apply -f infra/kubernetes/embedding-service.yaml
kubectl apply -f infra/kubernetes/retrieval-service.yaml
kubectl apply -f infra/kubernetes/reranking-service.yaml
kubectl apply -f infra/kubernetes/generation-service.yaml
```

7. **Deploy Gateway and Backend**:
```bash
kubectl apply -f infra/kubernetes/gateway-service.yaml
kubectl apply -f infra/kubernetes/backend.yaml
```

8. **Verify deployment**:
```bash
# Check pods
kubectl get pods -n ai-platform

# Check services
kubectl get svc -n ai-platform

# Check logs
kubectl logs -f deployment/gateway-service -n ai-platform
kubectl logs -f deployment/backend -n ai-platform
```

## Migration from REST to gRPC/RabbitMQ

### Phase 1: Enable gRPC/RabbitMQ (Current State)

1. **Update environment variables**:
```bash
# Add to each AI service
ENABLE_GRPC_SERVER=true
ENABLE_RABBITMQ_CONSUMER=true
```

2. **Restart services**:
```bash
docker-compose restart parser-service vision-service semantic-chunk-service metadata-service embedding-service retrieval-service reranking-service generation-service
```

3. **Verify gRPC servers are running**:
```bash
# Check logs for gRPC server startup
docker-compose logs parser-service | grep "gRPC server started"
```

4. **Verify RabbitMQ consumers are running**:
```bash
# Check RabbitMQ Management UI
# Access: http://localhost:15672
# Navigate to Queues tab
# Verify consumers are connected
```

### Phase 2: Update Backend to Use gRPC/RabbitMQ

1. **Update Backend code** to use gRPC client:
```go
// Instead of REST HTTP calls
// Use gRPC client
client := messaging.NewParserServiceClient(conn)
result, err := client.ParseDocument(ctx, ...)
```

2. **Or use RabbitMQ producer**:
```go
// For async operations
producer := messaging.NewRabbitMQProducer(conn)
err = producer.PublishParseDocument(ctx, ...)
```

3. **Test communication**:
```bash
# Test gRPC connection
# Test RabbitMQ message flow
# Verify results
```

### Phase 3: Remove REST Endpoints (Future)

1. **Backup current `main.py` files**:
```bash
cp services/*/app/main.py services/*/app/main.py.backup
```

2. **Remove REST route handlers**:
```python
# Remove all @app.post, @app.get decorators
# Keep only health check endpoints
```

3. **Remove external port mappings**:
```yaml
# Remove ports: "8001:8001" from docker-compose.yml
# Keep only gRPC ports in expose
```

4. **Restart services**:
```bash
docker-compose restart
```

5. **Verify functionality**:
```bash
# Test through Gateway only
# Verify internal services not accessible externally
```

## Monitoring and Observability

### Prometheus Configuration

Update `prometheus.yml` to scrape gRPC metrics:

```yaml
scrape_configs:
  - job_name: 'gateway'
    static_configs:
      - targets: ['gateway-service:8002']

  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8080']

  # AI services - gRPC metrics (if available)
  - job_name: 'parser-service'
    static_configs:
      - targets: ['parser-service:50051']

  - job_name: 'vision-service'
    static_configs:
      - targets: ['vision-service:50055']

  # ... other services
```

### Grafana Dashboards

Update dashboards to monitor:
- gRPC request latency
- RabbitMQ queue depth
- Message processing rates
- Consumer lag
- Connection health

### Log Aggregation

Ensure Loki is configured to capture:
- gRPC server logs
- RabbitMQ consumer logs
- Backend gRPC client logs
- RabbitMQ producer logs

## Troubleshooting

### gRPC Connection Issues

**Problem**: Backend cannot connect to AI service via gRPC

**Solutions**:
1. Verify service is running: `docker-compose ps`
2. Check gRPC server logs: `docker-compose logs parser-service`
3. Verify port is exposed: `docker-compose config | grep parser-service`
4. Check network connectivity: `docker network inspect ai-platform-network`
5. Verify gRPC port is correct (50051-50058)

### RabbitMQ Connection Issues

**Problem**: Messages not being consumed

**Solutions**:
1. Check RabbitMQ Management UI: http://localhost:15672
2. Verify queue exists and has messages
3. Check consumer is connected
4. Verify RabbitMQ URL in environment variables
5. Check consumer logs for errors

### Service Not Starting

**Problem**: AI service fails to start

**Solutions**:
1. Check service logs: `docker-compose logs <service-name>`
2. Verify dependencies are ready: `docker-compose ps`
3. Check environment variables
4. Verify gRPC/RabbitMQ configuration
5. Check for port conflicts

### Performance Issues

**Problem**: Slow response times

**Solutions**:
1. Check RabbitMQ queue depth
2. Monitor consumer lag
3. Check resource utilization: `docker stats`
4. Scale services: `docker-compose up -d --scale parser-service=3`
5. Enable GPU for embedding/reranking services

## Security Considerations

### Production Deployment

1. **Enable TLS for gRPC**:
```python
# In grpc_server.py
server.add_secure_port(
    '[::]:50051',
    grpc.ssl_server_credentials(ssl_server_credentials)
)
```

2. **Enable TLS for RabbitMQ**:
```yaml
# In docker-compose.yml
rabbitmq:
  environment:
    - RABBITMQ_SSL=true
    - RABBITMQ_SSL_CERT_FILE=/etc/rabbitmq/cert.pem
    - RABBITMQ_SSL_KEY_FILE=/etc/rabbitmq/key.pem
```

3. **Remove external infrastructure ports**:
```yaml
# Remove from docker-compose.yml
postgres:
  # ports: "5432:5432"  # REMOVE

qdrant:
  # ports: "6333:6333"  # REMOVE

redis:
  # ports: "6379:6379"  # REMOVE
```

4. **Use Kubernetes Network Policies**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ai-platform-policy
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ai-platform
```

## Backup and Recovery

### Database Backup

```bash
# PostgreSQL backup
docker exec postgres pg_dump -U ai_platform ai_platform > backup.sql

# Restore
docker exec -i postgres psql -U ai_platform ai_platform < backup.sql
```

### Qdrant Backup

```bash
# Qdrant snapshot
curl -X PUT http://localhost:6333/collections/{collection_name}/snapshots/{snapshot_name}

# Restore
curl -X PUT http://localhost:6333/collections/{collection_name}/snapshots/{snapshot_name}/recover
```

### MinIO Backup

```bash
# Using mc client
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mirror local/ai-platform-documents /backup/minio
```

## Scaling

### Horizontal Scaling

```bash
# Scale specific services
docker-compose up -d --scale parser-service=3
docker-compose up -d --scale embedding-service=2
docker-compose up -d --scale retrieval-service=2
```

### Kubernetes HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: parser-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: parser-service
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Rollback Plan

If issues arise after migration:

1. **Re-enable REST endpoints**:
```bash
# Restore backup main.py files
cp services/*/app/main.py.backup services/*/app/main.py

# Restore port mappings
# Edit docker-compose.yml to add back ports
```

2. **Disable gRPC/RabbitMQ**:
```bash
# Update environment variables
ENABLE_GRPC_SERVER=false
ENABLE_RABBITMQ_CONSUMER=false
```

3. **Restart services**:
```bash
docker-compose restart
```

4. **Verify functionality**:
```bash
# Test REST endpoints directly
curl http://localhost:8001/health
```

## Documentation References

- RabbitMQ Implementation: `PRIORITY2_RABBITMQ_IMPLEMENTATION.md`
- gRPC Implementation: `PRIORITY3_GRPC_IMPLEMENTATION.md`
- Cleanup & Documentation: `PRIORITY4_CLEANUP_DOCUMENTATION.md`
- Architecture Diagrams: `ARCHITECTURE_DIAGRAMS.md`
- Architecture Recommendations: `ARCHITECTURE_FIX_RECOMMENDATIONS.md`

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f <service>`
2. Check documentation in `/docs` directory
3. Review architecture diagrams
4. Check monitoring dashboards (Grafana)
