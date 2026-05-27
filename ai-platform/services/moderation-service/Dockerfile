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

# Expose port
EXPOSE 8005

# Run the service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]