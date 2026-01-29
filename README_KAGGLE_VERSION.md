# 🔬 MedSigLIP Nail Disease Fine-tuning - Kaggle Edition

[![Kaggle](https://img.shields.io/badge/Kaggle-Notebook-blue?logo=kaggle)](https://www.kaggle.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-Latest-red?logo=pytorch)](https://pytorch.org)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)

This is the **Kaggle-specific version** of the MedSigLIP fine-tuning project. It requires **NO Google Drive setup** and uses Kaggle's built-in GPU acceleration.

---

## 🚀 Quick Start (2 Minutes)

### Option 1: Use This Notebook Directly

1. **Open Kaggle**: [Kaggle.com](https://kaggle.com)
2. **Create/Upload your dataset as ZIP**
3. **Copy this notebook code** into a Kaggle notebook
4. **Add your dataset as input**
5. **Run all cells** ▶️

### Option 2: Manual Setup

```bash
# 1. Prepare your ZIP file
zip -r nail-disease-dataset.zip data/

# 2. Upload to Kaggle
# Via Kaggle website or CLI

# 3. Create notebook and add as input

# 4. Copy notebook code from this repo
```

---

## 📋 Prerequisites

### Software
- ✅ Kaggle Account (free)
- ✅ Hugging Face Account (free)
- ✅ Web browser

### Data
- ✅ ZIP file with your nail disease dataset
- ✅ Organized as: `data/train/class1/, class2/, ...` and `data/test/class1/, ...`

### Access
- ✅ Request access to [google/medsiglip-448](https://huggingface.co/google/medsiglip-448)
- ✅ Get Hugging Face token: [Settings → Tokens](https://huggingface.co/settings/tokens)

---

## 📂 Dataset Preparation

### Step 1: Organize Your Data

```
my-nail-images/
├── Acral_Lentiginous_Melanoma/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── blue_finger/
│   ├── image1.jpg
│   └── ...
├── clubbing/
├── Healthy_Nail/
├── Onychogryphosis/
├── pitting/
└── psoriasis/
```

### Step 2: Split Train/Test

```
data/
├── train/                # 80% of images
│   ├── Acral_Lentiginous_Melanoma/
│   ├── blue_finger/
│   ├── clubbing/
│   ├── Healthy_Nail/
│   ├── Onychogryphosis/
│   ├── pitting/
│   └── psoriasis/
└── test/                 # 20% of images
    ├── Acral_Lentiginous_Melanoma/
    ├── blue_finger/
    ├── clubbing/
    ├── Healthy_Nail/
    ├── Onychogryphosis/
    ├── pitting/
    └── psoriasis/
```

### Step 3: Create ZIP File

```bash
# Linux/Mac
zip -r nail-disease-dataset.zip data/

# Windows (use 7-Zip or built-in)
# Right-click → Send to → Compressed folder
```

### Step 4: Upload to Kaggle

1. Go to [Kaggle Datasets](https://www.kaggle.com/settings/datasets)
2. Click **"Create New Dataset"**
3. Upload your `nail-disease-dataset.zip`
4. Fill in metadata:
   - **Title**: "Nail Disease Classification Dataset"
   - **Description**: Your description
   - **License**: Creative Commons
5. Click **"Create"** → **"Publish"**

---

## 🎯 Running the Notebook

### Step 1: Create Kaggle Notebook

1. Go to [Kaggle Code](https://www.kaggle.com/code)
2. Click **"New Notebook"**
3. From the menu: **"Settings"** ⚙️
4. Under **"Accelerator"** select **"GPU (P100 or T4)"**
5. Click **"Apply"**

### Step 2: Add Dataset Input

1. Click **"+ Add Input"** (top right)
2. Search for your dataset
3. Click it to add
4. It will appear in `/kaggle/input`

### Step 3: Copy Notebook Code

1. Get the notebook from: [MedSigLIP_NailDisease_FinetuningKaggle.ipynb](./MedSigLIP_NailDisease_FinetuningKaggle.ipynb)
2. Copy all cells
3. Paste into your Kaggle notebook
4. Or upload the `.ipynb` file via import

### Step 4: Run the Notebook

#### Cell 1️⃣: Hugging Face Login

```python
from huggingface_hub import notebook_login
notebook_login()
```

- Get token: https://huggingface.co/settings/tokens
- Paste when prompted
- **RUN THIS FIRST!**

#### Cells 2️⃣-3️⃣: Setup

- Installs dependencies
- Checks GPU availability
- Auto-detects your ZIP file

#### Cells 4️⃣-7️⃣: Data Loading

- Auto-extracts ZIP
- Validates dataset structure
- Loads into PyTorch DataLoaders
- Shows class distribution

#### Cells 8️⃣-9️⃣: Model Setup

- Loads MedSigLIP base model
- Creates classification head
- Configures optimizer

#### Cells 🔟-1️⃣1️⃣: Training

- Runs 10 epochs by default
- Displays real-time progress
- Saves best model automatically
- Shows training metrics

#### Cell 1️⃣2️⃣: Results

- Generates loss/accuracy plots
- Creates confusion matrix
- Shows per-class metrics
- Saves all outputs

---

## 📊 Configuration Options

Edit these variables in the **Training Setup** cell:

```python
NUM_EPOCHS = 10              # How many times to train on data
LEARNING_RATE = 1e-4        # How fast model learns
WEIGHT_DECAY = 1e-5         # L2 regularization strength
BATCH_SIZE = 32             # Images per batch (lower if OOM)
IMAGE_SIZE = 448            # Input resolution
```

---

## 📈 Expected Performance

### GPU: P100 (Recommended)
```
⏱️  Training time: 30-40 minutes
🎯 Expected accuracy: 90-95%
⚡ Inference speed: 250-350ms per image
```

### GPU: T4 (Alternative)
```
⏱️  Training time: 45-60 minutes
🎯 Expected accuracy: 88-93%
⚡ Inference speed: 400-500ms per image
```

---

## 📁 Output Files

All outputs saved to `/kaggle/working/output/`:

| File | Size | Purpose |
|------|------|--------|
| `best_model.pt` | 420 MB | Trained model weights |
| `training_results.png` | 500 KB | Loss/accuracy plots |
| `training_history.json` | 10 KB | Detailed metrics |

### Download Files

1. After training completes
2. Click **"Output"** tab (right side)
3. Click download icon on each file
4. Or select all and download as ZIP

---

## ⚠️ Troubleshooting

### "No ZIP files found!"

**Problem**: Dataset not detected

**Solution**:
1. Verify ZIP uploaded to Kaggle
2. Add dataset via "+ Add Input"
3. Re-run Cell 4
4. Check `/kaggle/input` contains your dataset

### "CUDA out of memory"

**Problem**: GPU memory exceeded

**Solution**:
```python
# Reduce batch size
BATCH_SIZE = 16  # or 8

# Or reduce image size
IMAGE_SIZE = 224  # instead of 448

# Or use P100 instead of T4
```

### "Error loading model: 401"

**Problem**: No access to MedSigLIP

**Solution**:
1. Request access: https://huggingface.co/google/medsiglip-448
2. Get new token: https://huggingface.co/settings/tokens
3. Re-run Cell 1 with new token
4. Wait 5-10 minutes for access grant

### "Data loading failed"

**Problem**: Dataset structure incorrect

**Solution**:
```
✓ Check ZIP contains: data/train/ and data/test/
✓ Each has class folders: Healthy_Nail/, psoriasis/, etc.
✓ Each class folder has .jpg/.png images
✓ No nested folders
```

### "Connection timeout during training"

**Problem**: Kaggle session disconnected

**Solution**:
1. Keep browser tab open
2. Enable notifications (Settings)
3. Kaggle auto-saves progress
4. Reconnect to view latest status

---

## 🔄 Comparing Colab vs Kaggle

| Feature | Colab | Kaggle |
|---------|-------|--------|
| **Setup** | Mount Drive (complex) | Add dataset (simple) |
| **GPU** | T4, V100 | **P100 (faster!)** |
| **Storage** | Google Drive | `/kaggle/working` |
| **Best for** | Google ecosystem | Dataset-centric |
| **Speed** | 45-60 min | **30-40 min** |

**→ Use Kaggle if your data is already here!**

---

## 📚 Full Documentation

- **Kaggle Setup Guide**: [KAGGLE_SETUP.md](./KAGGLE_SETUP.md)
- **Notebook Comparison**: [NOTEBOOK_COMPARISON.md](./NOTEBOOK_COMPARISON.md)
- **Colab Version**: [MedSigLIP_NailDisease_FinetuningColab.ipynb](./MedSigLIP_NailDisease_FinetuningColab.ipynb)
- **Original README**: [README.md](./README.md)

---

## 🎓 How It Works

### 1️⃣ Load MedSigLIP
- Pre-trained medical vision-language model
- Already understands medical images
- Freezes base model (save memory)

### 2️⃣ Add Classification Head
- 3-layer neural network
- 1152 → 512 → 256 → 7 classes
- BatchNorm & Dropout for stability

### 3️⃣ Fine-tune
- Train ONLY the head
- Learn to classify nail diseases
- Save best performing model

### 4️⃣ Evaluate
- Test on held-out dataset
- Calculate accuracy, precision, recall, F1
- Generate confusion matrix

---

## 💡 Tips for Best Results

1. ✅ **Use high-res images** (min 448×448)
2. ✅ **Balance dataset** across all 7 classes
3. ✅ **Enable GPU** (P100 recommended)
4. ✅ **Run full 10 epochs** before judging
5. ✅ **Download outputs** immediately
6. ✅ **Test your model** on new images
7. ✅ **Share your results** on Kaggle!

---

## 🤝 Contributing

Have improvements?

1. Fork the repository
2. Create feature branch
3. Commit your changes
4. Push to branch
5. Open pull request

---

## 📞 Support

**Issues?** Check:
1. Troubleshooting section above
2. [KAGGLE_SETUP.md](./KAGGLE_SETUP.md) for detailed guide
3. [GitHub Issues](https://github.com/isumenuka/medsiglip-nail-disease-finetuning/issues)

---

## 📜 License

Apache License 2.0 - See [LICENSE](./LICENSE)

---

## 🙏 Acknowledgments

- **MedSigLIP**: Google Research
- **PyTorch**: Meta AI
- **Kaggle**: Google Cloud
- **Hugging Face**: Model hosting

---

## 📊 Citation

If you use this notebook, please cite:

```bibtex
@software{medsiglip_nails_2026,
  title={MedSigLIP Fine-tuning for Nail Disease Classification},
  author={Your Name},
  year={2026},
  url={https://github.com/isumenuka/medsiglip-nail-disease-finetuning}
}
```

---

**Ready to train?** 🚀

1. Prepare your dataset
2. Upload to Kaggle
3. Create notebook
4. Run cells
5. Download results

**Happy training!** 🎉
