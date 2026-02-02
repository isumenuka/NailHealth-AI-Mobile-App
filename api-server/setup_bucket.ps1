# Setup Cloud Storage for NailHealth AI
# Usage: .\setup_bucket.ps1

$ErrorActionPreference = "Continue" # Changed to Continue to handle existence checks

Write-Host "Setting up Google Cloud Storage..." -ForegroundColor Cyan

# 0. Get Project ID (Essential for unique bucket name)
$PROJECT_ID = (gcloud config get-value project 2>$null)
if ([string]::IsNullOrEmpty($PROJECT_ID)) {
    Write-Error "No GCP project configured. Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
}
Write-Host "   Project: $PROJECT_ID"

# Configuration
$BUCKET_NAME = "nailhealth-storage-$PROJECT_ID"
$REGION = "asia-southeast1" # Singapore
$MODEL_SOURCE = ".\models\model1\MedSigLIP-Fine-tuning.pt"

Write-Host "   Target Bucket: $BUCKET_NAME"
Write-Host "   Region: $REGION"
Write-Host ""

# 1. Create Bucket
Write-Host "1. Creating Bucket..." -ForegroundColor Yellow

# Try to create bucket. Redirect stderr to suppress checking messages.
gcloud storage buckets create "gs://$BUCKET_NAME" --location=$REGION 2>&1 | Out-Null

# Check validation
$bucketExists = gcloud storage buckets describe "gs://$BUCKET_NAME" 2>$null
if ($?) {
    Write-Host "Bucket is ready." -ForegroundColor Green
}
else {
    Write-Host "Creating bucket failed or check failed." -ForegroundColor Red
    exit 1
}

Write-Host ""

# 2. Upload Model
Write-Host "2. Uploading Model (3.5 GB)..." -ForegroundColor Yellow
if (Test-Path $MODEL_SOURCE) {
    # Check if file already exists
    $exists = gcloud storage ls "gs://$BUCKET_NAME/model1/MedSigLIP-Fine-tuning.pt" 2>$null
    if ($exists) {
        Write-Host "Model file already exists in bucket. Skipping upload." -ForegroundColor Cyan
        $choice = Read-Host "   Force upload? (y/n)"
        if ($choice -eq 'y') {
            gcloud storage cp $MODEL_SOURCE "gs://$BUCKET_NAME/model1/"
            Write-Host "Model uploaded!" -ForegroundColor Green
        }
    }
    else {
        Write-Host "Starting upload... please wait..." -ForegroundColor Cyan
        gcloud storage cp $MODEL_SOURCE "gs://$BUCKET_NAME/model1/"
        Write-Host "Model uploaded!" -ForegroundColor Green
    }
}
else {
    Write-Error "Local model file not found at: $MODEL_SOURCE"
}

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
