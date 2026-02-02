# Deploy NailHealth API
# PowerShell Script
# Usage: .\deploy.ps1

$ErrorActionPreference = "Continue"

Write-Host "NailHealth AI - Secure API Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$API_KEY = "zWWRlxZJPHauLozPAz9tqMiR174qt0OWk4yelnx8RyU"
$REGION = "asia-southeast1"
$SERVICE_NAME = "nailhealth-api"

# Check if gcloud is installed
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "Error: gcloud CLI is not installed" -ForegroundColor Red
    exit 1
}

# Get current project ID
$PROJECT_ID = (gcloud config get-value project 2>$null)
if (-not $PROJECT_ID) {
    Write-Host "No GCP project configured" -ForegroundColor Yellow
    $PROJECT_ID = Read-Host "Enter your GCP Project ID"
    gcloud config set project $PROJECT_ID
}
else {
    Write-Host "Using GCP Project: $PROJECT_ID" -ForegroundColor Green
}

Write-Host ""
Write-Host "Deployment Configuration:" -ForegroundColor Cyan
Write-Host "   Project: $PROJECT_ID"
Write-Host "   Region: $REGION"
Write-Host "   Service: $SERVICE_NAME"
Write-Host ""

$confirmation = Read-Host "Continue with deployment? (y/n)"
if ($confirmation -ne 'y') {
    Write-Host "Deployment cancelled" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "Building and deploying to Cloud Run..." -ForegroundColor Cyan
Write-Host ""

# Delete previous service if it exists (Cleanup)
Write-Host "Cleaning up previous deployment..." -ForegroundColor Cyan
gcloud run services delete $SERVICE_NAME --region $REGION --quiet 2>$null
# Ignore errors if service didn't exist

# Deploy command
$BUCKET_NAME = "nailhealth-storage-$PROJECT_ID"
$ENV_VARS = "API_KEY=$API_KEY,MODEL_PATH=/models"

# We construct the command carefully to avoid PowerShell parsing issues with quotes
Write-Host "Deploying service..." -ForegroundColor Green
gcloud run deploy $SERVICE_NAME `
    --source . `
    --region $REGION `
    --memory 8Gi `
    --cpu 2 `
    --timeout 300 `
    --max-instances 5 `
    --min-instances 1 `
    --allow-unauthenticated `
    --set-env-vars "$ENV_VARS" `
    --platform managed `
    --execution-environment=gen2 `
    --add-volume="name=models,type=cloud-storage,bucket=$BUCKET_NAME" `
    --add-volume-mount="volume=models,mount-path=/models"

Write-Host ""
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host ""

# Get the service URL
$SERVICE_URL = (gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")

Write-Host "Your API is live at:" -ForegroundColor Green
Write-Host "   $SERVICE_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Update mobile app API_URL to: $SERVICE_URL/predict"
Write-Host "   2. Ensure mobile app has API_KEY"
Write-Host ""
Write-Host "   Health Check (no auth):" -ForegroundColor Cyan
Write-Host "   curl $SERVICE_URL/health"
Write-Host ""
Write-Host "   Prediction (with auth):" -ForegroundColor Cyan
Write-Host "   curl -X POST $SERVICE_URL/predict"
# Use simple strings for the curl example to avoid escaping hell
Write-Host "     -H 'Content-Type: application/json'"
Write-Host "     -H 'X-API-Key: YOUR_KEY'"
Write-Host "     -d '{\"image\": \"...\"}'"
Write-Host ""
