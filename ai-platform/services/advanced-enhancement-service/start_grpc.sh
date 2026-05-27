#!/bin/bash
# Startup script for Advanced Enhancement Service (gRPC mode)
# Usage: ./start_grpc.sh <service_name>
# Services: retrieval-enhancement, semantic-enrichment, educational-ontology

cd "$(dirname "$0")"

# Set environment variables
export RUN_MODE=grpc

# Check if service name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <service_name>"
    echo "Available services: retrieval-enhancement, semantic-enrichment, educational-ontology"
    exit 1
fi

SERVICE=$1
BASE_PORT=${GRPC_PORT:-50083}

# Determine port based on service
case $SERVICE in
    retrieval-enhancement)
        PORT=$BASE_PORT
        ;;
    semantic-enrichment)
        PORT=$((BASE_PORT + 1))
        ;;
    educational-ontology)
        PORT=$((BASE_PORT + 2))
        ;;
    *)
        echo "Unknown service: $SERVICE"
        echo "Available services: retrieval-enhancement, semantic-enrichment, educational-ontology"
        exit 1
        ;;
esac

export GRPC_PORT=$PORT

echo "Starting Advanced Enhancement Service - $SERVICE in gRPC mode on port $PORT..."

# Run the gRPC server
python app/grpc_server.py $SERVICE
