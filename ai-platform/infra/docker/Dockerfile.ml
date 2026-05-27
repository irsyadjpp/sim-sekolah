# Base ML/PyTorch Image for AI Platform Services
# This image extends the base image with ML and PyTorch dependencies

FROM ai-platform-base:latest

LABEL maintainer="AI Platform Team"
LABEL description="Base ML/PyTorch image for AI Platform services"

# Install ML system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch and ML libraries
# Using CPU version by default, can be overridden for GPU
RUN pip install --no-cache-dir \
    torch==2.4.0 \
    torchvision==0.19.0 \
    torchaudio==2.4.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install transformers and sentence-transformers
RUN pip install --no-cache-dir \
    transformers==4.44.0 \
    sentence-transformers==3.0.1 \
    accelerate==0.34.0

# Install other ML libraries
RUN pip install --no-cache-dir \
    numpy==2.0.1 \
    pandas==2.2.2 \
    scikit-learn==1.5.1

# Set default command
CMD ["/bin/bash"]