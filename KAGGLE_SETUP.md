# 🎯 MedSigLIP Fine-tuning on Kaggle - Complete Guide

This guide explains how to use the `MedSigLIP_NailDisease_FinetuningKaggle.ipynb` notebook to train the MedSigLIP model on Kaggle with your nail disease dataset.

---

## 📋 Prerequisites

1. **Kaggle Account** - Free account at [kaggle.com](https://kaggle.com)
2. **Hugging Face Account** - For accessing the gated MedSigLIP model
3. **Dataset ZIP File** - Your nail disease dataset organized as:
   ```
   nail-disease-dataset.zip
   └── data/
       ├── train/
       │   ├── Acral_Lentiginous_Melanoma/
       │   ├── blue_finger/
       │   ├── clubbing/
       │   ├── Healthy_Nail/
       │   ├── Onychogryphosis/
       │   ├── pitting/
       │   └── psoriasis/
       └── test/
           ├── Acral_Lentiginous_Melanoma/
           ├── blue_finger/
           ├── clubbing/
           ├── Healthy_Nail/
           ├── Onychogryphosis/
           ├── pitting/
           └── psoriasis/
   ```

---

## 🚀 Step-by-Step Setup

### Step 1: Upload Dataset to Kaggle

1. Go to [Kaggle Datasets](https://www.kaggle.com/settings/datasets)
2. Click **"Create New Dataset"**
3. Upload your `nail-disease-dataset.zip` file
4. Add metadata:
   - **Title**: "Nail Disease Classification Dataset"
   - **Description**: Your description
   - **License**: Creative Commons (or your preferred license)
5. Click **"Create"**
6. Once published, note your dataset name/slug (e.g., `username/nail-disease-dataset`)

### Step 2: Create Kaggle Notebook

1. Go to [Kaggle Code](https://www.kaggle.com/code)
2. Click **"New Notebook"**
3. In the notebook, click **"+ Add Input"**
4. Search for your dataset and add it
5. Click **"+ Add Input"** again
6. Search for and add the following (optional but helpful):
   - Any public medical imaging datasets for reference

### Step 3: Enable GPU Acceleration

1. Click **"Settings"** (⚙️) in the top right
2. Under **"Accelerator"**, select:
   - **GPU** (P100 or T4 recommended)
3. Click **"Apply"**

### Step 4: Import the Notebook

Option A: **Copy from GitHub**
1. Download `MedSigLIP_NailDisease_FinetuningKaggle.ipynb` from this repository
2. In your Kaggle notebook, click **"File"** → **"Import Notebook"**
3. Upload the downloaded file

Option B: **Manual Setup**
1. Copy the entire notebook content
2. Paste into your Kaggle notebook
3. Adjust dataset paths if needed

---

## 🔑 Running the Notebook

### Cell 1️⃣: Hugging Face Login

**Run this first!**

1. Get your Hugging Face token:
   - Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
   - Create a new token with **"Read"** permission
   - Copy the token

2. Run the cell
3. When prompted, paste your token
4. Confirm you have access to `google/medsiglip-448`

### Cell 2️⃣-3️⃣: Setup & Dependencies

Run in order - these install all required packages

### Cell 4️⃣: GPU Check

Verifies your GPU is available and shows specs

### Cell 5️⃣: Kaggle Dataset Setup

**This is the key cell for your dataset!**

- Auto-detects ZIP files in `/kaggle/input`
- Extracts to `/tmp/nail_disease_dataset`
- Shows directory structure
- Verifies data integrity

### Cell 6️⃣-9️⃣: Data Loading & Model Setup

Auto-detects data paths and loads:
- Training dataset
- Test dataset
- MedSigLIP model
- Classification head

### Cells 🔟-1️⃣2️⃣: Training & Results

Runs full training pipeline:
- 10 epochs by default (modify `NUM_EPOCHS` if needed)
- Saves best model
- Generates training visualizations
- Outputs performance metrics

---

## 📊 Outputs

All outputs saved to `/kaggle/working/output/`:

```
/kaggle/working/output/
├── best_model.pt              # Best trained model
├── training_results.png       # Loss & accuracy plots
└── training_history.json      # Detailed training metrics
```

**Download these files** to use in production!

---

## 🔧 Troubleshooting

### ❌ "No ZIP files found!"

**Problem**: Dataset not detected

**Solution**:
1. Verify ZIP file is uploaded to Kaggle dataset
2. Check dataset is added to notebook inputs
3. Try re-running Cell 5 after a few seconds

### ❌ "CUDA out of memory"

**Problem**: GPU memory exceeded

**Solutions**:
1. Reduce `BATCH_SIZE` (try 16 or 8)
2. Use P100 GPU instead of T4
3. Reduce `IMAGE_SIZE` (try 224 instead of 448)

### ❌ "Error loading model: 401 Client Error"

**Problem**: No access to MedSigLIP

**Solution**:
1. Request access: [google/medsiglip-448](https://huggingface.co/google/medsiglip-448)
2. Re-login in Cell 1
3. Wait a few minutes for access grant

### ❌ "Data loading failed"

**Problem**: Dataset structure incorrect

**Solution**:
1. Verify ZIP contains `data/train/` and `data/test/`
2. Classes should be in subdirectories (one folder per class)
3. Re-check file organization matches the expected structure above

---

## ⚙️ Configuration Options

Edit these variables in Cell 8️⃣ to customize training:

```python
NUM_EPOCHS = 10              # Number of training epochs
LEARNING_RATE = 1e-4        # Learning rate
WEIGHT_DECAY = 1e-5         # L2 regularization
BATCH_SIZE = 32             # Batch size (reduce if OOM)
IMAGE_SIZE = 448            # Input image resolution
```

---

## 🎓 Expected Results

- **Training Time**: 30-60 minutes (P100)
- **Expected Accuracy**: 88-95%
- **Model Size**: ~420 MB
- **Performance**: Real-time inference (<500ms per image)

---

## 📚 Additional Resources

- [Hugging Face MedSigLIP Documentation](https://huggingface.co/google/medsiglip-448)
- [Kaggle Notebooks Guide](https://www.kaggle.com/notebooks)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Transformers Library Docs](https://huggingface.co/docs/transformers/)

---

## 💡 Tips for Best Results

1. ✅ **Use high-resolution images** (min 448x448)
2. ✅ **Balance your dataset** across all 7 classes
3. ✅ **Enable GPU acceleration** for training
4. ✅ **Save your best model** after training
5. ✅ **Download outputs** before closing notebook
6. ✅ **Version your training runs** with different hyperparameters

---

## 🤝 Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review the [GitHub repository](https://github.com/isumenuka/medsiglip-nail-disease-finetuning)
3. Open an issue on GitHub

---

**Happy training! 🚀**
