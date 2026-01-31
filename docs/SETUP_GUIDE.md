# 🛠️ Local Development Setup Guide

Complete step-by-step guide to set up NailHealth AI development environment on your local machine.

---

## 💻 Prerequisites

### Required Software

- **Node.js 18+** - Download from [nodejs.org](https://nodejs.org)
- **Python 3.10+** - Download from [python.org](https://python.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)
- **Expo Go App** - Install on your phone from App Store/Play Store

### Optional (Recommended)

- **VS Code** - Code editor with React Native extensions
- **Android Studio** - For Android emulator
- **Xcode** (Mac only) - For iOS simulator
- **Docker** - For containerized API testing

---

## 📥 Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/isumenuka/NailHealth-AI-Mobile-App.git

# Navigate to project directory
cd NailHealth-AI-Mobile-App
```

---

## 📱 Step 2: Setup Mobile App

### Install Dependencies

```bash
# Navigate to mobile app directory
cd mobile-app

# Install npm packages
npm install

# Or using yarn
yarn install
```

### Configure API URL

Edit `App.js` and update the API URL:

```javascript
const API_URL = 'http://YOUR-LOCAL-IP:8080/predict';
// For local testing, use your computer's IP address (not localhost)
// Example: 'http://192.168.1.100:8080/predict'
```

**Find your local IP:**
- **Windows**: Run `ipconfig` in command prompt
- **Mac/Linux**: Run `ifconfig` or `ip addr`

### Run Development Server

```bash
# Start Expo development server
npx expo start

# Or with specific options
npx expo start --clear  # Clear cache
npx expo start --tunnel # Use tunnel for external access
```

### Test on Physical Device

1. Install **Expo Go** app on your phone
2. Open Expo Go
3. Scan QR code from terminal
4. App will load on your device

### Test on Emulator/Simulator

```bash
# Android (requires Android Studio)
npx expo start --android

# iOS (requires Xcode, Mac only)
npx expo start --ios

# Web browser
npx expo start --web
```

---

## 🔧 Step 3: Setup API Server

### Create Virtual Environment

```bash
# Navigate to API server directory
cd ../api-server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Add Your Fine-tuned Models

Create `models/` directory and add your trained models:

```bash
mkdir -p models/medsiglip
mkdir -p models/medgemma4b

# Copy your fine-tuned model files
# From Kaggle notebooks to local models/ folder
```

### Run API Server Locally

```bash
# Run Flask development server
python app.py

# Server will start at http://0.0.0.0:8080
```

### Test API Endpoint

```bash
# Health check
curl http://localhost:8080/health

# Expected response:
# {"status": "healthy", "device": "cpu", "models_loaded": false}
```

---

## 📦 Step 4: Test End-to-End Flow

1. **Start API server** (Terminal 1):
   ```bash
   cd api-server
   python app.py
   ```

2. **Start mobile app** (Terminal 2):
   ```bash
   cd mobile-app
   npx expo start
   ```

3. **Open app on phone** via Expo Go

4. **Take a test photo** and verify:
   - Image uploads successfully
   - API processes request
   - Results display correctly

---

## 🐛 Troubleshooting

### Mobile App Issues

**Problem: "Network request failed"**
- Solution: Check API URL points to your local IP (not localhost)
- Solution: Ensure phone and computer are on same Wi-Fi network
- Solution: Check firewall isn't blocking port 8080

**Problem: "Camera permission denied"**
- Solution: Grant camera permissions in phone settings
- Solution: Restart Expo Go app

**Problem: "Module not found" errors**
- Solution: Delete `node_modules` and reinstall:
  ```bash
  rm -rf node_modules
  npm install
  ```

### API Server Issues

**Problem: "Port 8080 already in use"**
- Solution: Kill existing process:
  ```bash
  # Mac/Linux:
  lsof -ti:8080 | xargs kill -9
  # Windows:
  netstat -ano | findstr :8080
  taskkill /PID <PID> /F
  ```

**Problem: "ModuleNotFoundError"**
- Solution: Verify virtual environment is activated
- Solution: Reinstall requirements:
  ```bash
  pip install -r requirements.txt
  ```

**Problem: "CUDA out of memory" (if using GPU)**
- Solution: Reduce batch size or use CPU mode
- Solution: Set environment variable: `export CUDA_VISIBLE_DEVICES=""`

---

## 📑 Project Structure

```
NailHealth-AI-Mobile-App/
├── mobile-app/              # React Native Expo app
│   ├── App.js               # Main app component
│   ├── app.json             # Expo configuration
│   ├── package.json         # Dependencies
│   └── node_modules/        # Installed packages
│
├── api-server/              # Flask API
│   ├── app.py               # API endpoints
│   ├── requirements.txt     # Python dependencies
│   ├── models/              # Fine-tuned models
│   │   ├── medsiglip/
│   │   └── medgemma4b/
│   └── venv/                # Virtual environment
│
└── docs/                    # Documentation
```

---

## ✨ Next Steps

Once local setup is working:

1. ✅ Test with different nail images
2. ✅ Verify API responses are correct
3. ✅ Customize UI/UX if needed
4. ✅ Add error handling and edge cases
5. 🚀 Ready for cloud deployment (see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md))

---

## 📞 Need Help?

- **Issues**: [GitHub Issues](https://github.com/isumenuka/NailHealth-AI-Mobile-App/issues)
- **Email**: Contact via GitHub profile
- **Documentation**: Check [README.md](../README.md) and [ARCHITECTURE.md](./ARCHITECTURE.md)

---

**✅ Setup complete! You're ready to develop.**
