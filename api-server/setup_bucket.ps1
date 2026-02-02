# Setup Cloud Storage for NailHealth AI
# Usage: .\setup_bucket.ps1

$ErrorActionPreference = "Stop"

# Configuration (Matches deploy.ps1)
$BUCKET_NAME = "nailhealth-ai-models-nailhealth"
$REGION = "asia-southeast1" # Singapore
$MODEL_SOURCE = ".\models\model1\MedSigLIP-Fine-tuning.pt"

Write-Host "Setting up Google Cloud Storage..." -ForegroundColor Cyan
Write-Host "   Bucket: $BUCKET_NAME"
Write-Host "   Region: $REGION"
Write-Host ""

# 1. Create Bucket
Write-Host "1. Creating Bucket..." -ForegroundColor Yellow
try {
    gcloud storage buckets create "gs://$BUCKET_NAME" --location=$REGION
    Write-Host "Bucket created successfully!" -ForegroundColor Green
}
catch {
    Write-Host "Bucket creation warning (might already exist)." -ForegroundColor DarkYellow
    gcloud storage buckets describe "gs://$BUCKET_NAME" | Out-Null
    if ($?) {
        Write-Host "Bucket accessible. Proceeding..." -ForegroundColor Green
    }
    else {
        Write-Error "Could not access bucket. Please chose a unique name."
    }
}

Write-Host ""

# 2. Upload Model
Write-Host "2. Uploading Model (3.5 GB)... This may take a while." -ForegroundColor Yellow
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
        gcloud storage cp $MODEL_SOURCE "gs://$BUCKET_NAME/model1/"
        Write-Host "Model uploaded!" -ForegroundColor Green
    }
}
else {
    Write-Error "Local model file not found at: $MODEL_SOURCE"
}

Write-Host ""
Write-Host "Setup Complete! You can now run deploy.ps1" -ForegroundColor Green
