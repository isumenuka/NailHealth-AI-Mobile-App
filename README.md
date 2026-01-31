# 🏥 NailHealth AI - Mobile Disease Detection App

<div align="center">

![Project Banner](https://img.shields.io/badge/Medical_AI-Nail_Disease_Detection-32B8C6?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-iOS%20%7C%20Android-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge)

**AI-powered mobile app that detects systemic diseases through nail photo analysis**

[Demo Video](#) • [Documentation](./docs/) • [Report Issue](https://github.com/isumenuka/NailHealth-AI-Mobile-App/issues)

</div>

---

## 🎯 Project Overview

NailHealth AI uses Google's Health AI Developer Foundations (HAI-DEF) models to detect serious diseases through nail signs captured via smartphone camera. The app provides instant clinical explanations and disease predictions.

### 🔬 Medical Capabilities

Detects 7 nail conditions indicating systemic diseases:
- **White Nails (Terry's Nails)** → Liver disease, kidney disease, diabetes
- **Blue Nails** → Oxygen deficiency, lung disease, heart failure  
- **Clubbing** → Lung cancer, COPD, heart disease
- **Spoon Nails (Koilonychia)** → Iron deficiency anemia
- **Black Lines** → Melanoma, trauma, endocarditis
- **Psoriasis** → Psoriatic arthritis, metabolic syndrome
- **Onychogryphosis** → Poor circulation, fungal infection

---

## 🏗️ Architecture

### 2-Model AI Pipeline

```
📱 User Photo
    ↓
☁️ Google Cloud Run API
    ↓
🤖 Model 1: MedSigLIP (Fine-tuned)
   → Classifies nail sign type
    ↓
🤖 Model 2: MedGemma 4B (Fine-tuned)
   → Generates clinical explanation
   → Predicts diseases
   → Recommends actions
    ↓
📊 JSON Response → Mobile App
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| **Mobile App** | React Native + Expo |
| **Backend API** | Flask (Python) |
| **Cloud Hosting** | Google Cloud Run |
| **ML Models** | MedSigLIP + MedGemma 4B |
| **Storage** | Google Cloud Storage |
| **Training** | Kaggle GPU (Tesla T4) |

---

## 📁 Repository Structure

```
NailHealth-AI-Mobile-App/
├── 📱 mobile-app/          # React Native Expo app
│   ├── App.js              # Main app component
│   ├── app.json            # Expo configuration
│   ├── package.json        # Dependencies
│   └── assets/             # Images, icons
│
├── 🔧 api-server/          # Flask API for model inference
│   ├── app.py              # API endpoints
│   ├── Dockerfile          # Container configuration
│   ├── requirements.txt    # Python dependencies
│   └── models/             # Fine-tuned model checkpoints
│
├── 📚 docs/                # Documentation
│   ├── SETUP_GUIDE.md      # Local setup instructions
│   ├── DEPLOYMENT_GUIDE.md # Cloud deployment steps
│   └── ARCHITECTURE.md     # Technical architecture
│
├── 📓 notebooks/           # Training notebooks
│   ├── medsiglip_training.ipynb
│   └── medgemma4b_training.ipynb
│
└── 📋 README.md            # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Google Cloud account (free tier)
- Expo account (free)
- Smartphone (iOS/Android)

### 1. Clone Repository

```bash
git clone https://github.com/isumenuka/NailHealth-AI-Mobile-App.git
cd NailHealth-AI-Mobile-App
```

### 2. Setup Mobile App

```bash
cd mobile-app
npm install
npx expo start
```

Scan QR code with Expo Go app on your phone.

### 3. Setup API Server (Local Testing)

```bash
cd api-server
pip install -r requirements.txt
python app.py
```

API runs at `http://localhost:8080`

### 4. Deploy to Google Cloud

See [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md) for detailed steps.

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/nailhealth-api
gcloud run deploy nailhealth-api \
  --image gcr.io/YOUR-PROJECT-ID/nailhealth-api \
  --platform managed \
  --region us-central1 \
  --memory 4Gi
```

---

## 📱 Mobile App Features

### Current Features ✅
- 📸 Camera integration with photo capture
- 🔄 Real-time image upload to API
- 🤖 AI-powered nail disease classification
- 📊 Clinical explanation generation
- 🏥 Disease probability ranking
- 📋 Recommended medical tests
- 🎨 Professional medical UI design
- ⚡ Expo Go instant testing
- 📱 Cross-platform (iOS + Android)

### Coming Soon 🔜
- 📜 Disease history tracking
- 📈 Progress monitoring over time
- 🌍 Multi-language support
- 🔔 Appointment reminders
- 📤 PDF report export
- 👨‍⚕️ Doctor consultation booking

---

## 🛠️ Development

### Mobile App Development

```bash
cd mobile-app

# Start development server
npm start

# Run on specific platform
npm run android  # Android emulator
npm run ios      # iOS simulator
npm run web      # Web browser
```

### API Server Development

```bash
cd api-server

# Run with auto-reload
export FLASK_ENV=development
python app.py

# Build Docker image locally
docker build -t nailhealth-api .
docker run -p 8080:8080 nailhealth-api
```

### Model Training

Training notebooks are in `notebooks/` folder:
1. **MedSigLIP Fine-tuning**: Nail image classification
2. **MedGemma 4B Fine-tuning**: Clinical explanation generation

Both trained on Kaggle with Tesla T4 GPU (free tier).

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Nail Sign Classification Accuracy | 91.2% |
| F1-Score (Weighted) | 0.89 |
| API Response Time | ~2.1 seconds |
| App Load Time | <1 second |
| Supported Image Formats | JPG, PNG |
| Max Image Size | 5 MB |

### Model Details

**MedSigLIP Fine-tuned**
- Base: google/medsiglip-448
- Parameters: 400M
- Training: LoRA (Low-Rank Adaptation)
- Dataset: 700+ nail images (custom collected)

**MedGemma 4B Fine-tuned**
- Base: google/medgemma-4b-it
- Parameters: 4B
- Training: Instruction fine-tuning
- Dataset: 250+ clinical text pairs

---

## 🌐 Deployment Options

### Option 1: Google Cloud Run (Recommended)
- ✅ Auto-scaling
- ✅ Pay-per-use
- ✅ Free tier (2M requests/month)
- ✅ HTTPS out-of-the-box
- ⚙️ Memory: 4GB, CPU: 2 vCPU

### Option 2: AWS Lambda + API Gateway
- ✅ Serverless
- ✅ Low cost
- ❌ Cold start delay

### Option 3: Heroku
- ✅ Simple deployment
- ✅ Good for prototypes
- ❌ Sleep on free tier

**Current Deployment**: Google Cloud Run (`us-central1`)

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [SETUP_GUIDE.md](./docs/SETUP_GUIDE.md) | Complete local development setup |
| [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md) | Cloud deployment instructions |
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Technical architecture details |

---

## 🔑 Environment Variables

### Mobile App (`mobile-app/.env`)
```bash
API_URL=https://your-api-url.run.app
ENVIRONMENT=production
```

### API Server (`api-server/.env`)
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
MODEL_PATH=/app/models
PORT=8080
```

---

## 📈 Roadmap

### Phase 1: MVP ✅ (Completed)
- [x] MedSigLIP fine-tuning
- [x] MedGemma 4B fine-tuning
- [x] Flask API development
- [x] React Native mobile app
- [x] Google Cloud deployment
- [x] Basic UI/UX

### Phase 2: Enhancement 🔄 (In Progress)
- [ ] Improve classification accuracy to 95%+
- [ ] Add disease history tracking
- [ ] Implement user authentication
- [ ] Create admin dashboard
- [ ] Multi-language support

### Phase 3: Scale 📅 (Planned)
- [ ] Clinical validation study
- [ ] Regulatory compliance (FDA/CE)
- [ ] Doctor consultation integration
- [ ] App Store publication

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📜 License

This project uses models from Google's Health AI Developer Foundations (HAI-DEF):
- **MedSigLIP**: Apache 2.0 License
- **MedGemma 4B**: Apache 2.0 License

**Project License**: Apache 2.0

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for educational and research purposes only.

- ❌ NOT a substitute for professional medical advice
- ❌ NOT approved by FDA or medical authorities
- ❌ NOT for clinical diagnosis
- ✅ Use only as a screening tool
- ✅ Always consult licensed healthcare professionals

---

## 🙏 Acknowledgments

- **Google Health AI**: For HAI-DEF models (MedSigLIP, MedGemma)
- **Kaggle**: For free GPU resources
- **Expo Team**: For amazing mobile development framework
- **Medical Community**: For nail disease datasets and research

---

## 📞 Contact

**Developer**: K.G.I Enuka  
**GitHub**: [@isumenuka](https://github.com/isumenuka)  
**Twitter**: [@ezsumm](https://twitter.com/ezsumm)  
**Website**: [isumenuka.me](https://isumenuka.me)

**Project Link**: [https://github.com/isumenuka/NailHealth-AI-Mobile-App](https://github.com/isumenuka/NailHealth-AI-Mobile-App)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [K.G.I Enuka](https://github.com/isumenuka)

</div>
