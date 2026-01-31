# 🔧 API Server Documentation

Flask REST API for NailHealth AI nail disease detection.

---

## 📊 Overview

This API server processes nail images and returns disease predictions using fine-tuned HAI-DEF models:
- **MedSigLIP**: Image classification (nail sign detection)
- **MedGemma 4B**: Clinical explanation generation

---

## 🚀 Quick Start

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Server runs at http://localhost:8080
```

### Docker Development

```bash
# Build image
docker build -t nailhealth-api .

# Run container
docker run -p 8080:8080 nailhealth-api
```

---

## 📝 API Endpoints

### Health Check

**GET** `/health`

Check if API is running and models are loaded.

**Response**:
```json
{
  "status": "healthy",
  "device": "cpu",
  "models_loaded": true
}
```

### Nail Analysis

**POST** `/predict`

Analyze nail image and return disease predictions.

**Request**:
```json
{
  "image": "base64_encoded_image_string"
}
```

**Response**:
```json
{
  "nail_sign": "White Nails (Terry's Nails)",
  "confidence": 0.94,
  "explanation": "Clinical explanation text...",
  "diseases": [
    {"name": "Liver Cirrhosis", "confidence": 0.94},
    {"name": "Chronic Kidney Disease", "confidence": 0.82}
  ],
  "recommendations": [
    "Liver function tests",
    "Consult hepatologist"
  ]
}
```

**Error Responses**:
- `400`: Invalid image or missing data
- `500`: Internal server error

---

## 💾 Model Structure

```
models/
├── medsiglip/
│   ├── config.json
│   ├── pytorch_model.bin
│   └── preprocessor_config.json
└── medgemma4b/
    ├── config.json
    ├── pytorch_model.bin
    └── tokenizer_config.json
```

---

## ⚙️ Configuration

### Environment Variables

```bash
PORT=8080                    # Server port
MODEL_PATH=./models          # Model directory
FLASK_ENV=development        # Flask environment
```

### Gunicorn Configuration

```bash
gunicorn \
  --bind 0.0.0.0:8080 \
  --workers 1 \
  --threads 2 \
  --timeout 120 \
  app:app
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|----------|
| flask | 3.0.0 | Web framework |
| flask-cors | 4.0.0 | CORS support |
| transformers | 4.36.0 | Model inference |
| torch | 2.1.0 | Deep learning |
| pillow | 10.1.0 | Image processing |
| numpy | 1.24.3 | Array operations |
| gunicorn | 21.2.0 | Production server |

---

## 📊 Performance

- **Average response time**: 2.1 seconds
- **Throughput**: ~30 requests/minute per instance
- **Memory usage**: ~3GB with models loaded
- **CPU usage**: ~50% during inference

---

## 🧪 Testing

### Manual Testing

```bash
# Health check
curl http://localhost:8080/health

# Prediction (replace with actual base64)
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "BASE64_STRING"}'
```

### Python Testing

```python
import requests
import base64

# Read and encode image
with open('nail_image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# Send request
response = requests.post(
    'http://localhost:8080/predict',
    json={'image': image_data}
)

print(response.json())
```

---

## 🚀 Deployment

See [DEPLOYMENT_GUIDE.md](../docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

**Quick deploy to Cloud Run**:

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/YOUR-PROJECT/api
gcloud run deploy nailhealth-api \
  --image gcr.io/YOUR-PROJECT/api \
  --platform managed \
  --memory 4Gi
```

---

## 🐛 Troubleshooting

### Models not loading
- Check `models/` directory exists
- Verify model files are present
- Check file permissions

### Out of memory
- Reduce batch size
- Use CPU instead of GPU
- Increase container memory

### Slow inference
- Enable GPU if available
- Use model quantization
- Reduce image resolution

---

## 📞 Support

For issues or questions:
- GitHub Issues: [Report Issue](https://github.com/isumenuka/NailHealth-AI-Mobile-App/issues)
- Documentation: [Main README](../README.md)

---

**Version**: 1.0  
**Last Updated**: January 2026
