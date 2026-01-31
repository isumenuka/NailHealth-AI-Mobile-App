# 🚀 Google Cloud Deployment Guide

Complete step-by-step guide to deploy NailHealth AI to Google Cloud Run for production use.

---

## 🎯 Overview

We'll deploy:
- **API Server** → Google Cloud Run (serverless container)
- **Models** → Google Cloud Storage
- **Mobile App** → Expo (instant updates)

**Benefits:**
- ✅ Auto-scaling (handles traffic spikes)
- ✅ Pay-per-use (only charged when API is called)
- ✅ Free tier (2M requests/month)
- ✅ HTTPS by default
- ✅ No server management

---

## 💻 Prerequisites

### Required

- Google Cloud account (free trial: $300 credit)
- Google Cloud SDK installed
- Docker installed (for testing)
- Your fine-tuned models ready

### Cost Estimate

**Free Tier Limits:**
- Cloud Run: 2M requests/month
- Cloud Storage: 5GB storage
- Cloud Build: 120 build-minutes/day

**After free tier:**
- Cloud Run: ~$0.00002400 per request (very cheap)
- Storage: ~$0.02/GB/month

**Example**: 10,000 API calls/month = **FREE** (under limit)

---

## 🌐 Step 1: Setup Google Cloud Project

### Create Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Create Project"
3. Name: `nailhealth-ai`
4. Click "Create"

### Install Google Cloud SDK

```bash
# Download from: https://cloud.google.com/sdk/docs/install

# After installation, initialize
gcloud init

# Login to your account
gcloud auth login

# Set project
gcloud config set project nailhealth-ai
```

### Enable Required APIs

```bash
# Enable Cloud Run
gcloud services enable run.googleapis.com

# Enable Container Registry
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build
gcloud services enable cloudbuild.googleapis.com

# Enable Cloud Storage
gcloud services enable storage.googleapis.com
```

---

## 📦 Step 2: Upload Models to Cloud Storage

### Create Storage Bucket

```bash
# Create bucket (replace with unique name)
gsutil mb -l us-central1 gs://nailhealth-ai-models

# Verify bucket created
gsutil ls
```

### Upload Fine-tuned Models

```bash
# Navigate to your models directory
cd api-server/models

# Upload MedSigLIP model
gsutil -m cp -r medsiglip/ gs://nailhealth-ai-models/medsiglip/

# Upload MedGemma 4B model
gsutil -m cp -r medgemma4b/ gs://nailhealth-ai-models/medgemma4b/

# Verify upload
gsutil ls gs://nailhealth-ai-models/
```

---

## 🐳 Step 3: Build and Deploy API Container

### Update Dockerfile (Optional)

Edit `api-server/Dockerfile` to download models from Cloud Storage:

```dockerfile
# Add after WORKDIR /app

# Install gsutil
RUN curl https://sdk.cloud.google.com | bash
ENV PATH=$PATH:/root/google-cloud-sdk/bin

# Download models from Cloud Storage at runtime
COPY download_models.sh .
RUN chmod +x download_models.sh
```

Create `api-server/download_models.sh`:

```bash
#!/bin/bash
gsutil -m cp -r gs://nailhealth-ai-models/* /app/models/
```

### Build Container Image

```bash
# Navigate to api-server directory
cd api-server

# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/nailhealth-ai/api

# This takes 5-10 minutes
```

### Deploy to Cloud Run

```bash
# Deploy container
gcloud run deploy nailhealth-api \
  --image gcr.io/nailhealth-ai/api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10

# Service will be deployed in 2-3 minutes
```

### Get Service URL

```bash
# Get your API URL
gcloud run services describe nailhealth-api \
  --region us-central1 \
  --format="value(status.url)"

# Output example:
# https://nailhealth-api-xxxxx-uc.a.run.app

# Save this URL!
```

---

## 📱 Step 4: Update Mobile App with Production API

### Update API URL

Edit `mobile-app/App.js`:

```javascript
// Replace with your Cloud Run URL
const API_URL = 'https://nailhealth-api-xxxxx-uc.a.run.app/predict';
```

### Test Updated App

```bash
cd mobile-app
npx expo start

# Test on your phone via Expo Go
# Verify it connects to cloud API
```

---

## ✅ Step 5: Verify Deployment

### Test API Health

```bash
# Health check
curl https://nailhealth-api-xxxxx-uc.a.run.app/health

# Expected response:
{
  "status": "healthy",
  "device": "cpu",
  "models_loaded": true
}
```

### Test Prediction Endpoint

```bash
# Test with base64 image
curl -X POST \
  https://nailhealth-api-xxxxx-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "BASE64_IMAGE_DATA"}'
```

### Test from Mobile App

1. Open app on phone (via Expo Go)
2. Take a nail photo
3. Wait for analysis
4. Verify results display correctly

---

## 📊 Step 6: Monitor and Optimize

### View Logs

```bash
# View real-time logs
gcloud run logs tail nailhealth-api --region us-central1

# Or use Cloud Console
# https://console.cloud.google.com/run
```

### Monitor Usage

Go to Cloud Console → Cloud Run → nailhealth-api:
- Request count
- Response times
- Error rates
- CPU/Memory usage

### Optimize Performance

**Reduce cold starts:**
```bash
# Set minimum instances
gcloud run services update nailhealth-api \
  --min-instances 1 \
  --region us-central1
```

**Increase resources:**
```bash
# Increase memory/CPU
gcloud run services update nailhealth-api \
  --memory 8Gi \
  --cpu 4 \
  --region us-central1
```

---

## 📦 Step 7: Build Production Mobile App

### Setup EAS Build

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Configure project
cd mobile-app
eas build:configure
```

### Build Android APK

```bash
# Build APK (for direct install)
eas build --platform android --profile preview

# Build AAB (for Play Store)
eas build --platform android --profile production

# Wait 10-20 minutes for build
```

### Build iOS App

```bash
# Requires Apple Developer account ($99/year)
eas build --platform ios --profile production

# Wait 15-30 minutes for build
```

### Download and Test

```bash
# Download builds
eas build:list

# Install APK on Android device
# Upload IPA to TestFlight for iOS
```

---

## 🔒 Step 8: Security Best Practices

### Add API Authentication (Optional)

```python
# In app.py, add API key check
from flask import request

API_KEY = os.getenv('API_KEY', 'your-secret-key')

@app.before_request
def check_api_key():
    if request.path != '/health':
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
```

Update mobile app:
```javascript
// In App.js
const apiResponse = await axios.post(
  API_URL,
  { image: base64data },
  {
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your-secret-key'
    }
  }
);
```

### Enable CORS (Already Done)

Flask-CORS is already configured in `app.py`.

### Rate Limiting

Cloud Run has built-in DDoS protection. For additional limits:

```bash
# Set max concurrent requests
gcloud run services update nailhealth-api \
  --concurrency 80 \
  --region us-central1
```

---

## 💰 Cost Management

### Monitor Costs

```bash
# View billing
gcloud billing accounts list

# Set up budget alerts in Cloud Console
# Billing → Budgets & Alerts
```

### Optimize Costs

1. **Use minimum instances only for production**
2. **Reduce memory allocation if possible**
3. **Enable request caching**
4. **Use Cloud CDN for static assets**
5. **Delete unused resources**

---

## 🔄 Step 9: CI/CD (Optional)

### Automated Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: nailhealth-ai
      
      - name: Build and Deploy
        run: |
          gcloud builds submit --tag gcr.io/nailhealth-ai/api api-server/
          gcloud run deploy nailhealth-api \
            --image gcr.io/nailhealth-ai/api \
            --region us-central1
```

---

## 🐛 Troubleshooting

### Build Fails

- Check Dockerfile syntax
- Verify requirements.txt packages
- Review build logs: `gcloud builds list`

### Deployment Fails

- Check region is correct
- Verify billing is enabled
- Ensure APIs are enabled

### API Returns Errors

- Check logs: `gcloud run logs tail nailhealth-api`
- Verify models loaded correctly
- Test locally first

### Mobile App Can't Connect

- Verify API URL is correct
- Check Cloud Run allows unauthenticated access
- Test API with curl first

---

## ✅ Deployment Checklist

- [ ] Google Cloud project created
- [ ] APIs enabled
- [ ] Models uploaded to Cloud Storage
- [ ] Container built and pushed
- [ ] Cloud Run service deployed
- [ ] API URL obtained
- [ ] Mobile app updated with API URL
- [ ] End-to-end testing completed
- [ ] Logs monitored
- [ ] Budget alerts configured

---

## 🎉 Success!

Your NailHealth AI app is now deployed to production on Google Cloud!

**Next Steps:**
- Share APK with beta testers
- Gather feedback
- Monitor usage and costs
- Iterate and improve
- Publish to app stores

---

**Questions?** Open an issue on [GitHub](https://github.com/isumenuka/NailHealth-AI-Mobile-App/issues)
