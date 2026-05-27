# Staging Environment Overrides

This directory contains Docker Compose overrides for the **staging** environment.

## Usage

Start the full stack with staging overrides:
```bash
docker-compose -f ../../docker-compose.yml -f docker-compose.yml up -d
```

Or use the Makefile:
```bash
make dev-staging
```

## Staging Features

- **No hot-reloading**: Services use built Docker images (no volume mounts)
- **Info logging**: Services run with `LOG_LEVEL=INFO`
- **Resource limits**: Each service has CPU and memory limits defined
- **Multiple replicas**: Critical services run with 2-3 replicas for high availability
- **Production-like**: Simulates production deployment characteristics

## Resource Allocation

- **Gateway**: 2 replicas, 1CPU/1G limit
- **Parser**: 2 replicas, 1CPU/1G limit
- **Embedding**: 2 replicas, 2CPU/2G limit (higher for ML workloads)
- **Generation**: 2 replicas, 2CPU/2G limit (higher for LLM workloads)
- **Vision**: 1 replica, 2CPU/2G limit (higher for image processing)
- **Other services**: 1 replica each with appropriate resource limits

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