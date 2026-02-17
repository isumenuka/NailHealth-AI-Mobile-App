#  🤗 Hugging Face Inference Endpoint Setup Guide

This guide explains how to set up your **NailHealth AI** model (`medsiglip-nail-disease-classifier`) on Hugging Face using their Inference Endpoints.

> **Note**: This setup uses **AWS** infrastructure provided by Hugging Face to avoid any dependency on Google Cloud Platform (GCP).

---

## 🚀 Step-by-Step Configuration

Go to https://ui.endpoints.huggingface.co/new and configure the following settings:

### 1. Model Repository
*   **Repository**: `isumenuka/medsiglip-nail-disease-classifier`
*   **Revision**: Leave as default (latest commit)

### 2. Cloud Provider & Region
*   **Cloud Provider**: **AWS** (Amazon Web Services)
    *   *Why?* This is the default and most reliable provider for Hugging Face, ensuring no Google Cloud services are used.
*   **Region**: `us-east-1` (N. Virginia)
    *   *Why?* Cheapest ecosystem with the best availability for instances.

### 3. Instance Configuration (Hardware)
*   **Instance Type**: **CPU - Intel Sapphire Rapids** (or similar "Small" CPU)
    *   **Cost**: ~$0.13 / hour
    *   **Recommendation**: Start with this for testing. It interacts efficiently but may take 1-3 seconds per image.
    *   *Upgrade Option*: If the mobile app feels too slow, switch to **GPU [small] (Nvidia T4)** (~$0.60/hr) for sub-second inference.

### 4. Security Level
*   **Selection**: **Protected** (Recommended) or **Public**
    *   **Protected**: Requires a Hugging Face Token to access.
        *   *Best for:* Restricting access so random people don't use your paid quota. You will need to add your HF Token to the mobile app code.
    *   **Public**: Open to the entire internet.
        *   *Best for:* Easiest testing if you don't want to manage tokens yet. ⚠️ **Warning**: Anyone with the link can use your API and run up your bill.
    *   **Private**: ❌ **Do not use**. This requires logging in via a browser, which your mobile app cannot do easily.

### 5. Advanced Settings
*   **Inference Engine**: `Default` (as shown in your screenshot)
    *   *Why?* This automatically uses the standard Transformers pipeline which works perfectly for your model.
*   **Download Pattern**: `Safetensors files (with fallback to PyTorch files)` (Default)

---

## 💰 Cost Management
*   **Pause Strategy**: Set "Automatic Scale-to-Zero" to **15 minutes** or **1 hour**.
    *   *Why?* This ensures you stop paying when no one is using the app. The endpoint will "sleep" and wake up (takes ~1-2 mins) when a new user arrives.

## 📱 Mobile App integration
Once deployed, you will get an Endpoint URL (e.g., `https://xyz-nail-disease.us-east-1.aws.endpoints.huggingface.cloud`).

1.  Copy this URL.
2.  Update your mobile app's `.env` or configuration file:
    ```env
    API_URL=https://your-new-endpoint-url.aws.endpoints.huggingface.cloud
    HF_TOKEN=hf_XXXXXXXXXXXXXXXXX  # Only if you selected "Protected"
    ```
