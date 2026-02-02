# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)  
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY download_model.py .
COPY download_hf.py .

# Pre-download Hugging Face models
RUN python download_hf.py

COPY app.py .
COPY models/ ./models/

# Create models directory
RUN mkdir -p /app/models/model1

# Set environment variables
ENV PORT=8080
ENV GCS_BUCKET=nailhealth-ai-models-nailhealth
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["python", "app.py"]
