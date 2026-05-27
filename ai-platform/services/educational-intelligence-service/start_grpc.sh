#!/bin/bash
# Startup script for Educational Intelligence Service (gRPC mode)
# Usage: ./start_grpc.sh <engine_name>
# Engines: adaptive-learning, assessment, curriculum, learning-graph, learning-progression, pedagogy, recommendation

cd "$(dirname "$0")"

# Set environment variables
export RUN_MODE=grpc

# Check if engine name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <engine_name>"
    echo "Available engines: adaptive-learning, assessment, curriculum, learning-graph, learning-progression, pedagogy, recommendation"
    exit 1
fi

ENGINE=$1
BASE_PORT=${GRPC_PORT:-50075}

# Determine port based on engine
case $ENGINE in
    adaptive-learning)
        PORT=$BASE_PORT
        ;;
    assessment)
        PORT=$((BASE_PORT + 1))
        ;;
    curriculum)
        PORT=$((BASE_PORT + 2))
        ;;
    learning-graph)
        PORT=$((BASE_PORT + 3))
        ;;
    learning-progression)
        PORT=$((BASE_PORT + 4))
        ;;
    pedagogy)
        PORT=$((BASE_PORT + 5))
        ;;
    recommendation)
        PORT=$((BASE_PORT + 6))
        ;;
    *)
        echo "Unknown engine: $ENGINE"
        echo "Available engines: adaptive-learning, assessment, curriculum, learning-graph, learning-progression, pedagogy, recommendation"
        exit 1
        ;;
esac

export GRPC_PORT=$PORT

echo "Starting Educational Intelligence Service - $ENGINE in gRPC mode on port $PORT..."

# Run the gRPC server
python app/grpc_server.py $ENGINE
