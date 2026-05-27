FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  g++ \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY app /app/app

# Expose ports (REST API and gRPC)
EXPOSE 8025 50074

# Run the service (supports both REST API and gRPC via environment variable)
CMD ["sh", "-c", "if [ \"$RUN_MODE\" = \"grpc\" ]; then python app/grpc_server.py; else uvicorn app.main:app --host 0.0.0.0 --port 8025; fi"]
