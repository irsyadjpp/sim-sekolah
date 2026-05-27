#!/bin/bash
# Startup script for Hallucination Guard Service (gRPC mode)

cd "$(dirname "$0")"

# Set environment variables
export RUN_MODE=grpc
export GRPC_PORT=${GRPC_PORT:-50073}

echo "Starting Hallucination Guard Service in gRPC mode on port $GRPC_PORT..."

# Run the gRPC server
python app/grpc_server.py
