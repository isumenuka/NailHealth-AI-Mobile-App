#!/bin/bash

# 🚀 Deploy NailHealth API to Google Cloud Run with API Key
# Usage: ./deploy.sh

set -e

echo "🔐 NailHealth AI - Secure API Deployment"
echo "========================================"
echo ""

# Configuration
PROJECT_ID="your-gcp-project-id"
REGION="asia-southeast1"
SERVICE_NAME="nailhealth-api"
API_KEY="zWWRlxZJPHauLozPAz9tqMiR174qt0OWk4yelnx8RyU"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "   Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get current project ID
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -z "$CURRENT_PROJECT" ]; then
    echo "⚠️  No GCP project configured"
    echo "   Run: gcloud config set project YOUR_PROJECT_ID"
    read -p "Enter your GCP Project ID: " PROJECT_ID
    gcloud config set project "$PROJECT_ID"
else
    echo "📦 Using GCP Project: $CURRENT_PROJECT"
    PROJECT_ID="$CURRENT_PROJECT"
fi

echo ""
echo "📋 Deployment Configuration:"
echo "   Project: $PROJECT_ID"
echo "   Region: $REGION"
echo "   Service: $SERVICE_NAME"
echo "   API Key: ${API_KEY:0:20}..."
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "🏗️  Building and deploying to Cloud Run..."
echo ""

# Deploy to Cloud Run
gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --region "$REGION" \
    --memory 8Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 5 \
    --min-instances 1 \
    --allow-unauthenticated \
    --set-env-vars "API_KEY=$API_KEY,MODEL_PATH=/models" \
    --platform managed \
    --execution-environment=gen2 \
    --add-volume=name=models,type=cloud-storage,bucket=nailhealth-ai-models-nailhealth \
    --add-volume-mount=volume=models,mount-path=/models

echo ""
echo "✅ Deployment Complete!"
echo ""

# Get the service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format="value(status.url)")

echo "🎉 Your API is live at:"
echo "   $SERVICE_URL"
echo ""
echo "📋 Next Steps:"
echo "   1. Update mobile app API_URL to: $SERVICE_URL/predict"
echo "   2. Ensure mobile app has API_KEY: ${API_KEY:0:20}..."
echo "   3. Test the API:"
echo ""
echo "   Health Check (no auth):"
echo "   curl $SERVICE_URL/health"
echo ""
echo "   Prediction (with auth):"
echo "   curl -X POST $SERVICE_URL/predict \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -H 'X-API-Key: $API_KEY' \\"
echo "     -d '{\"image\": \"base64data\"}'"
echo ""
