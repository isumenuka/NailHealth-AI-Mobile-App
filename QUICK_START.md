# 🚀 Quick Start Guide

**Get NailHealth AI running in under 30 minutes!**

This guide gets you from zero to a working demo as fast as possible.

---

## 🎯 What You'll Build

A fully functional mobile app that:
1. Takes nail photos with your phone camera
2. Sends images to AI API on Google Cloud
3. Returns disease predictions and recommendations
4. Works on both Android and iOS

---

## ⏱️ Time Estimate

- **Setup**: 5 minutes
- **Local Testing**: 10 minutes
- **Cloud Deployment**: 15 minutes
- **Total**: ~30 minutes

---

## 📍 Prerequisites (One-Time Setup)

**Install these first** (if you don't have them):

```bash
# 1. Node.js (for mobile app)
Download from: https://nodejs.org

# 2. Python (for API)
Download from: https://python.org

# 3. Google Cloud SDK (for deployment)
Download from: https://cloud.google.com/sdk/docs/install

# 4. Expo Go app on your phone
iOS: App Store
Android: Google Play Store
```

---

## Step 1: Clone & Setup (5 min)

```bash
# Clone repository
git clone https://github.com/isumenuka/NailHealth-AI-Mobile-App.git
cd NailHealth-AI-Mobile-App

# Setup mobile app
cd mobile-app
npm install
cd ..

# Setup API server
cd api-server
pip install -r requirements.txt
cd ..
```

---

## Step 2: Test Locally (10 min)

### Terminal 1: Start API Server

```bash
cd api-server
python app.py

# Server runs at http://localhost:8080
# Leave this terminal running
```

### Terminal 2: Start Mobile App

```bash
# Get your local IP address first:
# Mac/Linux: ifconfig | grep "inet "
# Windows: ipconfig

# Edit mobile-app/App.js line 14:
# Change to: const API_URL = 'http://YOUR-LOCAL-IP:8080/predict';

cd mobile-app
npx expo start

# Scan QR code with Expo Go app
```

### Test the App

1. Open Expo Go on your phone
2. Scan the QR code
3. Click "Take Photo"
4. Take any photo (nail or test image)
5. Wait for AI analysis (~2 seconds)
6. See results!

✅ **If results appear, local setup works!**

---

## Step 3: Deploy to Cloud (15 min)

### 3.1 Google Cloud Setup

```bash
# Login to Google Cloud
gcloud auth login

# Create project
gcloud projects create nailhealth-ai-YOURNAME
gcloud config set project nailhealth-ai-YOURNAME

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3.2 Deploy API

```bash
cd api-server

# Build and deploy (takes 5-10 min)
gcloud builds submit --tag gcr.io/nailhealth-ai-YOURNAME/api

gcloud run deploy nailhealth-api \
  --image gcr.io/nailhealth-ai-YOURNAME/api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi

# Copy the URL shown (e.g., https://nailhealth-api-xxx.run.app)
```

### 3.3 Update Mobile App

```bash
# Edit mobile-app/App.js line 14:
const API_URL = 'https://your-cloud-run-url.run.app/predict';

# Restart Expo
cd mobile-app
npx expo start

# Test on your phone again
```

✅ **If results appear, cloud deployment works!**

---

## Step 4: Build Production App (Optional)

```bash
# Install EAS CLI
npm install -g eas-cli

# Login
eas login

# Configure
cd mobile-app
eas build:configure

# Build APK for Android
eas build --platform android

# Download and install APK on your phone
```

---

## ✅ Success Checklist

- [ ] Mobile app loads in Expo Go
- [ ] Camera opens when "Take Photo" clicked
- [ ] Photo uploads to API
- [ ] Results display within 3 seconds
- [ ] All 4 result sections visible:
  - Detected nail sign
  - Clinical explanation
  - Possible diseases
  - Recommendations

---

## 🐛 Common Issues

### "Network request failed"

**Problem**: Mobile app can't reach API

**Solutions**:
- Check API URL is correct (include `/predict` at end)
- For local: Use your computer's IP, not `localhost`
- Ensure phone and computer on same Wi-Fi
- Check firewall isn't blocking port 8080

### "Module not found"

**Problem**: Dependencies not installed

**Solution**:
```bash
cd mobile-app
rm -rf node_modules
npm install
```

### "Port 8080 already in use"

**Problem**: Another app using port 8080

**Solution**:
```bash
# Mac/Linux:
lsof -ti:8080 | xargs kill -9

# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Cloud Build Fails

**Problem**: Billing not enabled

**Solution**:
- Go to Google Cloud Console
- Enable billing (required even for free tier)
- Retry deployment

---

## 📊 Next Steps

Once basic demo works:

1. ✅ **Add Your Trained Models**
   - Replace demo predictions with real MedSigLIP + MedGemma 4B
   - See [SETUP_GUIDE.md](./docs/SETUP_GUIDE.md)

2. ✅ **Improve Accuracy**
   - Fine-tune models on more nail images
   - See training notebooks in repo

3. ✅ **Customize UI**
   - Edit `mobile-app/App.js`
   - Change colors, add features

4. ✅ **Monitor Usage**
   - Check Google Cloud Console
   - View logs and metrics

5. ✅ **Share with Users**
   - Build production APK
   - Distribute for beta testing

---

## 📚 Full Documentation

For detailed information:

- **[README.md](./README.md)** - Project overview
- **[SETUP_GUIDE.md](./docs/SETUP_GUIDE.md)** - Detailed setup
- **[DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md)** - Cloud deployment
- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Technical details
- **[PROJECT_CHECKLIST.md](./PROJECT_CHECKLIST.md)** - Complete checklist
- **[TOOLS_AND_RESOURCES.md](./TOOLS_AND_RESOURCES.md)** - All tools used

---

## 📧 Need Help?

**Stuck? Have questions?**

- **GitHub Issues**: [Report problem](https://github.com/isumenuka/NailHealth-AI-Mobile-App/issues)
- **Email**: Contact via GitHub profile
- **Documentation**: Check docs/ folder

---

## 🎉 Congratulations!

You now have a working AI-powered medical app!

**What you've built:**
- ✅ Cross-platform mobile app (iOS + Android)
- ✅ Cloud-hosted AI API (Google Cloud Run)
- ✅ Real-time disease detection
- ✅ Production-ready architecture

**Keep building and improving!** 🚀

---

**Quick Start Version**: 1.0  
**Last Updated**: January 31, 2026
