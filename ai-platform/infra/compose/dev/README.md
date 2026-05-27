# Development Environment Overrides

This directory contains Docker Compose overrides for the **development** environment.

## Usage

Start the full stack with development overrides:
```bash
docker-compose -f ../../docker-compose.yml -f docker-compose.yml up -d
```

Or use the Makefile:
```bash
make dev
```

## Development Features

- **Hot-reloading**: Source code volumes are mounted for live code updates
- **Debug logging**: All services run with `LOG_LEVEL=DEBUG`
- **Python unbuffered**: `PYTHONUNBUFFERED=1` for real-time log output
- **No resource limits**: Services can use available system resources freely

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