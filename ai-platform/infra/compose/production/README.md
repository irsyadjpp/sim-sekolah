# Production Environment Overrides

This directory contains Docker Compose overrides for the **production** environment.

## Usage

Start the full stack with production overrides:
```bash
docker-compose -f ../../docker-compose.yml -f docker-compose.yml up -d
```

Or use the Makefile:
```bash
make dev-production
```

## ⚠️ Important Note

**For production deployments, consider using Kubernetes instead of Docker Compose.**

This configuration is provided for:
- Smaller production deployments
- Testing production configurations locally
- Migration scenarios from Docker Compose to Kubernetes

For Kubernetes deployments, see `infra/kubernetes/`.

## Production Features

- **No hot-reloading**: Services use built Docker images
- **Warning logging**: Services run with `LOG_LEVEL=WARNING`
- **Strict resource limits**: Each service has defined CPU and memory limits
- **Multiple replicas**: Critical services run with 2-3 replicas for HA
- **Security hardening**:
  - `no-new-privileges` security option
  - Read-only filesystems
  - Temporary filesystems for `/tmp`
- **Restart policies**: Automatic restart on failure with backoff
- **Higher resource allocation**: More CPU/memory for production workloads

## Resource Allocation

- **Gateway**: 3 replicas, 2CPU/2G limit (critical path)
- **Parser**: 3 replicas, 2CPU/2G limit
- **Embedding**: 3 replicas, 4CPU/4G limit (ML-intensive)
- **Generation**: 3 replicas, 4CPU/4G limit (LLM-intensive)
- **Vision**: 2 replicas, 4CPU/4G limit (image processing)
- **Retrieval**: 3 replicas, 2CPU/2G limit
- **Other services**: 2 replicas each with appropriate limits

## Security Considerations

- All services run with read-only root filesystems
- `/tmp` is mounted as tmpfs for write operations
- No new privileges can be gained
- Resource limits prevent resource exhaustion attacks

## Stopping Services

```bash
docker-compose -f ../../docker-compose.yml -f docker-compose.yml down
```

Or:
```bash
make down
```

## Viewing Logs

```bash
docker-compose -f ../../docker-compose.yml -f docker-compose.yml logs -f
```

Or:
```bash
make logs
```