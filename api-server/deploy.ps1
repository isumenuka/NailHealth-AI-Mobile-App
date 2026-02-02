# 🚀 Deploy NailHealth API to Google Cloud Run with API Key
# PowerShell script for Windows
# Usage: .\deploy.ps1

$ErrorActionPreference = "Stop"

Write-Host "🔐 NailHealth AI - Secure API Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$API_KEY = "zWWRlxZJPHauLozPAz9tqMiR174qt0OWk4yelnx8RyU"
$REGION = "us-central1"
$SERVICE_NAME = "nailhealth-api"

# Check if gcloud is installed
if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: gcloud CLI is not installed" -ForegroundColor Red
    Write-Host "   Install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Get current project ID
$PROJECT_ID = (gcloud config get-value project 2>$null)
if ([string]::IsNullOrEmpty($PROJECT_ID)) {
    Write-Host "⚠️  No GCP project configured" -ForegroundColor Yellow
    Write-Host "   Run: gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Yellow
    $PROJECT_ID = Read-Host "Enter your GCP Project ID"
    gcloud config set project $PROJECT_ID
}
else {
    Write-Host "📦 Using GCP Project: $PROJECT_ID" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Deployment Configuration:" -ForegroundColor Cyan
Write-Host "   Project: $PROJECT_ID"
Write-Host "   Region: $REGION"
Write-Host "   Service: $SERVICE_NAME"
Write-Host "   API Key: $($API_KEY.Substring(0,20))..."
Write-Host ""

$confirmation = Read-Host "Continue with deployment? (y/n)"
if ($confirmation -ne 'y') {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🏗️  Building and deploying to Cloud Run..." -ForegroundColor Cyan
Write-Host ""

# Deploy to Cloud Run
# Note: --allow-unauthenticated is needed so the Cloud Run service itself is reachable,
# but our application logic (app.py) handles the API Key validation.
# We use Gen2 environment for GCS Fuse (Model streaming)
# Deploy to Cloud Run (Single line to avoid PowerShell parsing issues)
Write-Host "🚀 Executing deployment command..." -ForegroundColor Cyan

# Delete previous service if it exists (Cleanup)
Write-Host "🗑️  Cleaning up previous deployment..." -ForegroundColor Cyan
gcloud run services delete $SERVICE_NAME --region $REGION --quiet 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Previous service removed." -ForegroundColor Green
}
else {
    Write-Host "   No previous service found or deletion failed (continuing...)" -ForegroundColor Yellow
}

# gcloud run services update $SERVICE_NAME --region $REGION --min-instances 1 --max-instances 5
gcloud run deploy $SERVICE_NAME --source . --region $REGION --memory 8Gi --cpu 2 --timeout 300 --max-instances 5 --min-instances 1 --allow-unauthenticated --set-env-vars "API_KEY=$API_KEY" --platform managed

Write-Host ""
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host ""

# Get the service URL
$SERVICE_URL = (gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")

Write-Host "🎉 Your API is live at:" -ForegroundColor Green
Write-Host "   $SERVICE_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Update mobile app API_URL to: $SERVICE_URL/predict"
Write-Host "   2. Ensure mobile app has API_KEY: $($API_KEY.Substring(0,20))..."
Write-Host "   3. Test the API:"
Write-Host ""
Write-Host "   Health Check (no auth):" -ForegroundColor Cyan
Write-Host "   curl $SERVICE_URL/health"
Write-Host ""
Write-Host "   Prediction (with auth):" -ForegroundColor Cyan
Write-Host "   curl -X POST $SERVICE_URL/predict \"
Write-Host "     -H 'Content-Type: application/json' \"
Write-Host "     -H 'X-API-Key: $API_KEY' \"
Write-Host "     -d '{`"image`": `"base64data`"}'"
Write-Host ""
