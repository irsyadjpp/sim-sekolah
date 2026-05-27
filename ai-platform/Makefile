.PHONY: help dev test proto deploy build up down restart logs clean install-dev lint format dev-setup k8s-deploy k8s-delete k8s-logs dev-staging dev-production build-base

# Default target
help:
	@echo "AI Platform Management Commands"
	@echo "================================"
	@echo "dev            - Start full local stack (infra + services) in dev mode"
	@echo "dev-staging    - Start full local stack in staging mode"
	@echo "dev-production- Start full local stack in production mode"
	@echo "test           - Run tests (unit, integration, e2e)"
	@echo "proto          - Generate protobuf stubs (Go + Python)"
	@echo "deploy         - Deploy to Kubernetes (staging/production)"
	@echo ""
	@echo "build-base     - Build base Docker images (base, ocr, ml, document)"
	@echo "build          - Build Docker images for services"
	@echo "up             - Start services only (infra must be running)"
	@echo "down           - Stop services"
	@echo "restart        - Restart services"
	@echo "logs           - Show logs from all services"
	@echo "clean          - Remove all containers, volumes, and networks"
	@echo "install-dev     - Install development dependencies"
	@echo "lint           - Run linting"
	@echo "format         - Format code"
	@echo "dev-setup       - First-time development environment setup"
	@echo ""
	@echo "k8s-deploy     - Deploy to Kubernetes (staging/production)"
	@echo "k8s-delete     - Delete from Kubernetes"
	@echo "k8s-logs       - Show Kubernetes logs"

# Dev: Start full local stack (infra + services) in dev mode
dev:
	@echo "Starting full local stack (infra + services) in dev mode..."
	docker-compose -f docker-compose.yml -f infra/compose/dev/docker-compose.yml up -d

# Dev: Start full local stack in staging mode
dev-staging:
	@echo "Starting full local stack in staging mode..."
	docker-compose -f docker-compose.yml -f infra/compose/staging/docker-compose.yml up -d

# Dev: Start full local stack in production mode
dev-production:
	@echo "Starting full local stack in production mode..."
	docker-compose -f docker-compose.yml -f infra/compose/production/docker-compose.yml up -d

# Test: Run all tests
test:
	@echo "Running tests..."
	@echo "Running unit tests..."
	pytest shared/ services/ -v --cov=.
	@echo "Running integration tests..."
	pytest tests/integration/ -v
	@echo "Running E2E tests..."
	pytest tests/e2e/ -v

# Proto: Generate protobuf stubs
proto:
	@echo "Generating protobuf stubs..."
	@echo "Generating Python stubs..."
	buf generate
	@echo "Generating Go stubs for backend SDK..."
	cd ../backend && /tmp/protoc/bin/protoc --proto_path=../ai-platform/proto --go_out=internal/ai/grpc/pb --go_opt=paths=source_relative --go-grpc_out=internal/ai/grpc/pb --go-grpc_opt=paths=source_relative internal/ai/proto/*.proto
	@echo "Proto generation complete!"

# Build base Docker images
build-base:
	@echo "Building base Docker images..."
	cd infra/docker && docker-compose build

# Deploy: Deploy to Kubernetes
deploy:
	@echo "Deploying to Kubernetes..."
	@if [ -z "$(ENV)" ]; then \
		echo "Error: ENV not set. Usage: make deploy ENV=staging|production"; \
		exit 1; \
	fi
	@echo "Deploying to $(ENV)..."
	kubectl apply -f infra/kubernetes/namespace.yaml
	kubectl apply -f infra/kubernetes/configmap.yaml
	kubectl apply -f infra/kubernetes/secret.yaml
	kubectl apply -f infra/kubernetes/
	@echo "Deployment to $(ENV) complete!"

# Build Docker images for services
build:
	@echo "Building Docker images for services..."
	docker-compose build gateway-service
	docker-compose build parser-service
	docker-compose build semantic-chunk-service
	docker-compose build metadata-service
	docker-compose build embedding-service
	docker-compose build retrieval-service
	docker-compose build generation-service
	docker-compose build audit-service
	docker-compose build monitoring-service
	docker-compose build moderation-service
	docker-compose build reranking-service
	docker-compose build vision-service

# Start services only (infra must be running separately)
up:
	@echo "Starting services only (infra must be running separately)..."
	docker-compose up -d

# Stop services
down:
	@echo "Stopping services..."
	docker-compose down

# Restart services
restart:
	@echo "Restarting services..."
	docker-compose restart

# Show logs from all services
logs:
	@echo "Showing logs from all services..."
	docker-compose logs -f

# Clean everything
clean:
	@echo "Cleaning up..."
	docker-compose down -v
	docker system prune -f

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest pytest-cov black ruff mypy buf
	@echo "Development dependencies installed!"

# Lint code
lint:
	@echo "Linting code..."
	ruff check shared/ services/ pipelines/ workers/
	mypy shared/ services/ pipelines/ workers/

# Format code
format:
	@echo "Formatting code..."
	black shared/ services/ pipelines/ workers/
	ruff check --fix shared/ services/ pipelines/ workers/

# First-time development environment setup
dev-setup:
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env created from .env.example"; \
	fi
	pip install -r requirements.txt
	@echo "Development environment setup complete!"
	@echo "Run 'make dev' to start the full local stack."

# Kubernetes deployment (legacy)
k8s-deploy:
	@echo "Deploying to Kubernetes..."
	kubectl apply -f infra/kubernetes/namespace.yaml
	kubectl apply -f infra/kubernetes/configmap.yaml
	kubectl apply -f infra/kubernetes/secret.yaml
	kubectl apply -f infra/kubernetes/

# Kubernetes delete (legacy)
k8s-delete:
	@echo "Deleting from Kubernetes..."
	kubectl delete -f infra/kubernetes/

# Kubernetes logs (legacy)
k8s-logs:
	@echo "Showing Kubernetes logs..."
	kubectl logs -n ai-platform -f deployment/gateway-service