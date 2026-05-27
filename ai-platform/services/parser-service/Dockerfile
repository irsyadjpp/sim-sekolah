FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  tesseract-ocr \
  tesseract-ocr-ind \
  tesseract-ocr-eng \
  libtesseract-dev \
  libleptonica-dev \
  pkg-config \
  gcc \
  g++ \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ../../requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Copy shared components
COPY ../../shared /app/shared

# Expose ports (REST API and gRPC)
EXPOSE 8001 50051

# Run the service (supports both REST API and gRPC via environment variable)
CMD ["sh", "-c", "if [ \"$RUN_MODE\" = \"grpc\" ]; then python app/grpc_server.py; else python -m app.main; fi"]