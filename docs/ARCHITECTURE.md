# 🏗️ Technical Architecture

Complete technical overview of NailHealth AI system architecture, design decisions, and implementation details.

---

## 📊 System Overview

```
┌──────────────────────┐
│  📱 Mobile App Layer  │
│  (React Native + Expo)  │
└──────────────────────┘
           ↓ HTTPS/JSON
┌──────────────────────┐
│   ☁️ Cloud API Layer   │
│   (Google Cloud Run)   │
│    Flask REST API      │
└──────────────────────┘
           ↓
┌──────────────────────┐
│  🤖 ML Pipeline Layer  │
└──────────────────────┘
       ↓           ↓
  MedSigLIP    MedGemma 4B
  (Classify)   (Explain)
       ↓           ↓
  Nail Sign   Clinical
  Detection   Explanation
                  +
              Diseases
```

---

## 📦 Component Architecture

### 1. Mobile Application

**Technology**: React Native + Expo

**Key Components**:
```
App.js
├── CameraModule
│   ├── ImagePicker (Expo)
│   └── Camera (Expo)
├── ImagePreprocessor
│   ├── Base64 Encoder
│   └── Image Compression
├── APIClient
│   ├── Axios HTTP Client
│   ├── Error Handling
│   └── Timeout Management
└── UIComponents
    ├── ResultsDisplay
    ├── LoadingIndicator
    └── ErrorMessages
```

**Design Pattern**: Component-based architecture with hooks

**State Management**: React useState (simple state, no Redux needed)

**Styling**: StyleSheet API with design system tokens

---

### 2. API Server

**Technology**: Python Flask + Gunicorn

**Architecture Pattern**: RESTful API

**Endpoints**:

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/health` | GET | Health check | <100ms |
| `/predict` | POST | Nail analysis | ~2-3s |

**Request Flow**:
```
1. Receive POST /predict
   ↓
2. Validate JSON payload
   ↓
3. Decode base64 image
   ↓
4. Stage 1: MedSigLIP inference
   ↓
5. Stage 2: MedGemma 4B inference
   ↓
6. Format response
   ↓
7. Return JSON
```

**Error Handling**:
- 400: Bad request (invalid image)
- 500: Internal server error
- Timeout: 30 seconds

---

### 3. ML Pipeline

#### Stage 1: MedSigLIP (Image Classification)

**Model**: google/medsiglip-448

**Fine-tuning**:
- Method: LoRA (Low-Rank Adaptation)
- Dataset: 700+ nail images
- Training: Kaggle Tesla T4 GPU
- Epochs: 10
- Learning Rate: 1e-4

**Input**:
- Image: 448x448 RGB
- Format: PIL Image → Tensor

**Output**:
- Nail sign classification (7 classes)
- Confidence score (0-1)

**Inference Time**: ~300ms

#### Stage 2: MedGemma 4B (Clinical Explanation)

**Model**: google/medgemma-4b-it

**Fine-tuning**:
- Method: Instruction fine-tuning
- Dataset: 250+ clinical text pairs
- Training: Kaggle Tesla T4 GPU
- Epochs: 3
- Learning Rate: 2e-4

**Input**:
- Nail sign label
- Optional: Patient metadata

**Output**:
- Clinical explanation (text)
- Disease predictions (list)
- Confidence scores
- Recommendations

**Inference Time**: ~1.8s

---

## 📡 Data Flow

### Request Flow (Detailed)

```
[User takes photo]
        ↓
[Mobile App: Image Capture]
  - Resolution: 1:1 aspect ratio
  - Quality: 0.8 compression
  - Format: JPEG
        ↓
[Mobile App: Preprocessing]
  - Convert to base64
  - Attach to JSON payload
        ↓
[Network: HTTPS POST]
  - Endpoint: /predict
  - Timeout: 30s
        ↓
[API: Request Validation]
  - Check JSON structure
  - Validate base64
        ↓
[API: Image Decoding]
  - Base64 → bytes
  - Bytes → PIL Image
  - Convert to RGB
  - Resize to 448x448
        ↓
[ML: Stage 1 - Classification]
  - MedSigLIP inference
  - Get nail sign + confidence
        ↓
[ML: Stage 2 - Explanation]
  - MedGemma 4B inference
  - Generate explanation
  - Map to diseases
  - Get recommendations
        ↓
[API: Response Formatting]
  - Create JSON response
  - Add metadata
        ↓
[Network: HTTPS Response]
  - Return JSON
        ↓
[Mobile App: Display Results]
  - Parse JSON
  - Render UI components
  - Show results to user
```

---

## 💾 Data Structures

### API Request

```json
{
  "image": "base64_encoded_string_here..."
}
```

### API Response

```json
{
  "nail_sign": "White Nails (Terry's Nails)",
  "confidence": 0.94,
  "explanation": "White nail appearance with preserved pink nail bed...",
  "diseases": [
    {
      "name": "Liver Cirrhosis",
      "confidence": 0.94
    },
    {
      "name": "Chronic Kidney Disease",
      "confidence": 0.82
    },
    {
      "name": "Type 2 Diabetes",
      "confidence": 0.68
    }
  ],
  "recommendations": [
    "Liver function tests (AST, ALT, bilirubin)",
    "Renal function panel (creatinine, BUN)",
    "Consult hepatologist"
  ]
}
```

---

## 🔒 Security Architecture

### Authentication
- **Current**: None (public API)
- **Future**: API key authentication
- **Enterprise**: OAuth 2.0 + JWT

### Data Privacy
- **Images**: Not stored (processed in-memory only)
- **Logs**: No PII logged
- **HTTPS**: All traffic encrypted
- **HIPAA**: Not currently compliant (educational use only)

### Rate Limiting
- **Cloud Run**: Max 1000 concurrent requests
- **Per IP**: No limit (can be added)
- **Cost protection**: Max instances = 10

---

## ⚡ Performance Optimization

### Mobile App

**Image Compression**:
- Quality: 0.8 (80%)
- Max size: ~500KB
- Format: JPEG

**Network Optimization**:
- Timeout: 30s
- Retry: 1 attempt
- Connection pooling: Axios default

**UI Optimization**:
- Lazy loading: No (small app)
- Memoization: React.memo where needed
- Image caching: Expo default

### API Server

**Model Optimization**:
- Quantization: INT8 (future)
- Batch inference: No (single image)
- GPU acceleration: Available

**Container Optimization**:
- Base image: python:3.10-slim
- Multi-stage build: No (future)
- Layer caching: Yes

**Gunicorn Configuration**:
```python
- Workers: 1
- Threads: 2
- Timeout: 120s
- Max requests: 1000
```

---

## 📊 Scalability

### Current Capacity

- **Requests/month**: 2M (free tier)
- **Concurrent requests**: 80 per instance
- **Max instances**: 10
- **Theoretical max**: 800 concurrent requests

### Bottlenecks

1. **Model inference time**: ~2s per request
2. **Cold start**: ~10s for new instances
3. **Memory**: 4GB per instance

### Scaling Strategy

**Horizontal Scaling**:
- Auto-scale instances based on load
- Max instances can be increased

**Vertical Scaling**:
- Increase memory/CPU per instance
- Currently: 4GB RAM, 2 vCPU
- Max: 32GB RAM, 8 vCPU

**Optimization**:
- Model quantization for faster inference
- Caching for repeated requests
- CDN for static assets

---

## 🔄 CI/CD Pipeline

### Current: Manual Deployment

```bash
gcloud builds submit
gcloud run deploy
```

### Future: Automated Pipeline

```
GitHub Push → main branch
    ↓
GitHub Actions Triggered
    ↓
Run Tests
    ↓
Build Docker Image
    ↓
Push to Google Container Registry
    ↓
Deploy to Cloud Run
    ↓
Run Smoke Tests
    ↓
Notify Team
```

---

## 📊 Monitoring & Observability

### Metrics Tracked

- Request count
- Response time (p50, p95, p99)
- Error rate
- CPU/Memory usage
- Cold start frequency

### Logging

**Current**:
- Cloud Run logs
- Application logs (Flask)
- Access logs (Gunicorn)

**Future**:
- Structured logging (JSON)
- Log aggregation (Cloud Logging)
- Alerts (Cloud Monitoring)

---

## 🚧 Future Improvements

### Short-term (1-3 months)
- [ ] Add model quantization (2x faster)
- [ ] Implement request caching
- [ ] Add user authentication
- [ ] Improve error messages

### Medium-term (3-6 months)
- [ ] Add history tracking
- [ ] Implement offline mode
- [ ] Multi-language support
- [ ] Clinical validation study

### Long-term (6-12 months)
- [ ] HIPAA compliance
- [ ] FDA approval process
- [ ] Doctor portal
- [ ] Insurance integration

---

## 📚 Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|------------|---------|----------|
| **Mobile** | React Native | 0.73 | Cross-platform UI |
| | Expo | ~50.0 | Development framework |
| | Axios | 1.6 | HTTP client |
| **API** | Python | 3.10 | Backend language |
| | Flask | 3.0 | Web framework |
| | Gunicorn | 21.2 | WSGI server |
| **ML** | PyTorch | 2.1 | Deep learning |
| | Transformers | 4.36 | Model library |
| | MedSigLIP | 448 | Image classification |
| | MedGemma | 4B | Text generation |
| **Cloud** | Google Cloud Run | - | Serverless containers |
| | Cloud Storage | - | Model storage |
| | Cloud Build | - | Container builds |
| **DevOps** | Docker | - | Containerization |
| | Git | - | Version control |
| | GitHub Actions | - | CI/CD (future) |

---

## 👥 Team Roles

**For scaling this project, recommended team structure:**

- **ML Engineer**: Model training, optimization
- **Backend Developer**: API development, cloud infrastructure
- **Mobile Developer**: React Native app development
- **DevOps Engineer**: CI/CD, monitoring, scaling
- **Clinical Advisor**: Medical accuracy, validation
- **Product Manager**: Roadmap, user feedback

---

## 📞 Questions?

For technical discussions:
- Open an issue: [GitHub Issues](https://github.com/isumenuka/NailHealth-AI-Mobile-App/issues)
- Email: Via GitHub profile

---

**Architecture Version**: 1.0  
**Last Updated**: January 2026  
**Author**: K.G.I Enuka
