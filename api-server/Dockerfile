# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create models directory
RUN mkdir -p /app/models

# Copy your fine-tuned models (add these after training)
# COPY models/medsiglip /app/models/medsiglip
# COPY models/medgemma4b /app/models/medgemma4b

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV MODEL_PATH=/app/models
ENV PYTHONUNBUFFERED=1

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "2", "--timeout", "120", "app:app"]
