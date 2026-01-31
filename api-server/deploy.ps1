# NailHealth AI - Cloud Run Deployment Commands
# Run these commands in PowerShell from the api-server directory

# STEP 1: Navigate to api-server directory
Write-Host "📂 Step 1: Navigate to api-server directory" -ForegroundColor Green
cd "c:\Users\Isum Enuka\Downloads\NailHealth-AI-Mobile-App\api-server"

# STEP 2: Set your Google Cloud project
Write-Host "`n🔧 Step 2: Setting Google Cloud project..." -ForegroundColor Green
gcloud config set project nailhealth-ai

# STEP 3: Build the container image
Write-Host "`n📦 Step 3: Building container image (this takes 5-15 minutes)..." -ForegroundColor Green
Write-Host "   Building and pushing to Google Container Registry..." -ForegroundColor Yellow
gcloud builds submit --tag gcr.io/nailhealth-ai/api

# STEP 4: Deploy to Cloud Run
Write-Host "`n🚀 Step 4: Deploying to Cloud Run..." -ForegroundColor Green
gcloud run deploy nailhealth-api `
  --image gcr.io/nailhealth-ai/api `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 4Gi `
  --cpu 2 `
  --timeout 600 `
  --max-instances 10 `
  --set-env-vars GCS_BUCKET=nailhealth-ai-models-nailhealth

# STEP 5: Get the deployment URL
Write-Host "`n🌐 Step 5: Getting your API URL..." -ForegroundColor Green
$API_URL = gcloud run services describe nailhealth-api `
  --region us-central1 `
  --format="value(status.url)"

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "   Your API URL: $API_URL" -ForegroundColor Cyan
Write-Host "   Health check: $API_URL/health" -ForegroundColor Cyan
Write-Host "   Prediction: $API_URL/predict" -ForegroundColor Cyan

# STEP 6: Test the health endpoint
Write-Host "`n🏥 Step 6: Testing health endpoint..." -ForegroundColor Green
curl "$API_URL/health"

Write-Host "`n🎉 All done! Your API is deployed and running!" -ForegroundColor Green
