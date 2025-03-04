# Use a more stable base image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DEFAULT_TIMEOUT=200

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install packages in stages to better handle dependencies
COPY requirements.txt .

# Install torch first
RUN pip install --no-cache-dir torch

# Install transformers and sentence-transformers
RUN pip install --no-cache-dir transformers==4.46.3 sentence-transformers>=2.2.0

# Install the rest of the requirements
RUN pip install --no-cache-dir \
    fastapi>=0.68.0 \
    uvicorn>=0.15.0 \
    pydantic>=1.8.0 \
    python-dotenv>=0.19.0 \
    huggingface-hub \
    numpy>=1.24.0 \
    regex>=2023.0.0

# Copy the application code
COPY . .

# Make port 8000 available
EXPOSE 8000

# Run the application
CMD ["uvicorn", "chatbot_api.main:app", "--host", "0.0.0.0", "--port", "8000"]