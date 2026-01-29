# 🚀 Kaggle MedSigLIP - 5-Minute Quick Start

**Just want to get started?** Follow these 5 simple steps. 🌟

---

## Step 1️⃣: Prepare Your Dataset (2 min)

### Organize your images:
```
data/
├── train/
│   ├── Acral_Lentiginous_Melanoma/    (images here)
│   ├── blue_finger/                   (images here)
│   ├── clubbing/
│   ├── Healthy_Nail/
│   ├── Onychogryphosis/
│   ├── pitting/
│   └── psoriasis/
└── test/                         (same structure)
    ├── Acral_Lentiginous_Melanoma/
    ├── blue_finger/
    └── ...
```

### Create ZIP:
```bash
zip -r nail-disease-dataset.zip data/
```

---

## Step 2️⃣: Create Kaggle Dataset (1 min)

1. Go: https://www.kaggle.com/settings/datasets
2. **"Create New Dataset"** → Upload ZIP
3. **Title**: "Nail Disease Classification Dataset"
4. **"Create"** → **"Publish"** ✓

---

## Step 3️⃣: Create Kaggle Notebook (30 sec)

1. Go: https://www.kaggle.com/code
2. **"New Notebook"** ✓
3. **Settings** ⚙️ → **Accelerator: GPU (P100)**
4. **"Apply"** ✓

---

## Step 4️⃣: Setup Notebook (1 min)

1. **"+ Add Input"** → Find your dataset
2. Copy code from: [MedSigLIP_NailDisease_FinetuningKaggle.ipynb](./MedSigLIP_NailDisease_FinetuningKaggle.ipynb)
3. Paste into notebook

---

## Step 5️⃣: Run & Get Results (30 sec)

### Cell 1: Hugging Face Login
```python
from huggingface_hub import notebook_login
notebook_login()
```

**Get token**: https://huggingface.co/settings/tokens (new token with Read permission)

**Request access**: https://huggingface.co/google/medsiglip-448

Paste token when prompted ✓

### Run all cells ▶️

- Installs packages (✅)
- Checks GPU (✅)
- Auto-detects your ZIP (✅)
- Loads dataset (✅)
- Downloads model (✅)
- **TRAINS MODEL** (✅)
- Shows results (✅)

---

## 🌟 After Training (2-5 min)

### Download Results

1. Notebook → **Output** tab
2. Download:
   - `best_model.pt` (your model!)
   - `training_results.png` (plots)
   - `training_history.json` (metrics)

### Check Performance

- **Accuracy**: 88-95% (expected)
- **Speed**: P100 = 30-40 min
- **Model Size**: 420 MB

---

## ⚠️ Common Issues

### 📄 "No ZIP files found!"
```
1. Check ZIP in /kaggle/input
2. Re-add dataset input
3. Run cell again
```

### ✋ "CUDA out of memory"
```python
# In training setup cell, change:
BATCH_SIZE = 16  # (was 32)
# or
IMAGE_SIZE = 224  # (was 448)
```

### 🔒 "401 Unauthorized"
```
1. Request access: https://huggingface.co/google/medsiglip-448
2. Get new token: https://huggingface.co/settings/tokens
3. Re-run login cell with new token
```

### 📁 "Data loading failed"
```
✅ Check your ZIP has:
  - data/train/Healthy_Nail/ (and others)
  - data/test/Healthy_Nail/ (and others)
  - Images directly in class folders (no subfolders)
```

---

## 📋 Full Guides

Need more details?

- **Complete Setup**: [README_KAGGLE_VERSION.md](./README_KAGGLE_VERSION.md)
- **Kaggle Guide**: [KAGGLE_SETUP.md](./KAGGLE_SETUP.md)
- **Colab vs Kaggle**: [NOTEBOOK_COMPARISON.md](./NOTEBOOK_COMPARISON.md)
- **Original README**: [README.md](./README.md)

---

## 🙋 Need Help?

**Stuck?** 🤘

1. Check troubleshooting above
2. Read [README_KAGGLE_VERSION.md](./README_KAGGLE_VERSION.md)
3. Open [GitHub Issue](https://github.com/isumenuka/medsiglip-nail-disease-finetuning/issues)

---

## 🌟 Pro Tips

- **Keep browser open** during training
- **Use P100** (faster than T4)
- **Balance classes** across 7 diseases
- **High-res images** work best (448x448+)
- **Save outputs** immediately after training

---

**Ready?** Start with Step 1! 🚀

Good luck! 🌟
