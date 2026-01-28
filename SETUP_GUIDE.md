# 🚀 Setup Guide - MedSigLIP Nail Disease Fine-tuning

## Table of Contents
1. [Google Colab Setup (Recommended)](#google-colab-setup)
2. [Local Machine Setup](#local-machine-setup)
3. [Data Preparation](#data-preparation)
4. [Troubleshooting](#troubleshooting)
5. [GPU Optimization Tips](#gpu-optimization-tips)

---

## Google Colab Setup (Recommended) ✅

### Step 1: Open the Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/isumenuka/medsiglip-nail-disease-finetuning/blob/MedSigLIP-Fine-tuning/medsiglip_nail_disease_finetuning.ipynb)

Or manually:
1. Go to [Google Colab](https://colab.research.google.com/)
2. File → Open Notebook → GitHub
3. Paste: `https://github.com/isumenuka/medsiglip-nail-disease-finetuning`
4. Select the notebook

### Step 2: Enable GPU

```
Runtime → Change Runtime Type → Hardware Accelerator: GPU (T4 or V100)
```

Verify GPU:
```python
import torch
print(torch.cuda.is_available())  # Should print: True
print(torch.cuda.get_device_name(0))  # Should show: Tesla T4, V100, etc.
```

### Step 3: Prepare Data

**Option A: Mount Google Drive**
```python
from google.colab import drive
drive.mount('/content/drive')

# Upload your data to:
# /drive/My Drive/nail_disease_data/
```

**Option B: Upload from Local**
```python
from google.colab import files
files.upload()  # Select your zipped data folder

!unzip "your_data.zip" -d /content/data/
```

**Option C: Download from Kaggle** (Recommended)
```python
!pip install kaggle

# First, get your API key from https://www.kaggle.com/settings/account
# Upload kaggle.json to Colab when prompted

from google.colab import files
files.upload()  # Select kaggle.json

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# Download datasets
!kaggle datasets download -d nikhilgurav21/nail-disease-detection-dataset
!unzip nail-disease-detection-dataset.zip -d /content/data/
```

### Step 4: Run the Notebook

1. Execute cells sequentially (⏭️ button or Shift+Enter)
2. Monitor GPU usage:
   ```python
   !nvidia-smi
   ```
3. Check progress in real-time with tqdm bars

### Step 5: Download Results

After training completes:
```python
from google.colab import files

# Download all outputs
import os
for file in os.listdir('/content/output'):
    files.download(f'/content/output/{file}')
```

---

## Local Machine Setup

### Prerequisites

- Python 3.8+
- CUDA 11.8+ (for GPU support)
- 16 GB RAM
- 50 GB free disk space

### Step 1: Clone Repository

```bash
git clone https://github.com/isumenuka/medsiglip-nail-disease-finetuning.git
cd medsiglip-nail-disease-finetuning
git checkout MedSigLIP-Fine-tuning
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**GPU Support (Optional but Recommended):**
```bash
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify installation
python -c "import torch; print(torch.cuda.is_available())"
```

### Step 4: Prepare Data

```bash
# Create data directories
mkdir -p data/train
mkdir -p data/test

# Copy your organized data:
# data/
# ├── train/
# │   ├── Acral_Lentiginous_Melanoma/
# │   ├── blue_finger/
# │   ├── ...
# └── test/
#     ├── Acral_Lentiginous_Melanoma/
#     ├── blue_finger/
#     ├── ...
```

### Step 5: Launch Jupyter

```bash
jupyter notebook medsiglip_nail_disease_finetuning.ipynb
```

Browser should open automatically. If not, go to `http://localhost:8888`

---

## Data Preparation

### Download Datasets

1. **Kaggle Datasets** (Recommended):
   ```bash
   pip install kaggle
   
   # Get API key from https://www.kaggle.com/settings/account
   # Place kaggle.json in ~/.kaggle/
   
   cd data
   kaggle datasets download -d nikhilgurav21/nail-disease-detection-dataset
   kaggle datasets download -d josephrasanjana/nail-disease-image-classification-dataset
   kaggle datasets download -d whaleeeeee/nail-disease
   kaggle datasets download -d sumitagrawal/hp-nail-images-for-early-disease-detection
   ```

2. **Mendeley Data**:
   - Visit: [Nail Psoriasis Dataset](https://data.mendeley.com/datasets/3hckgznc67)
   - Click "Download All"
   - Extract to `data/` folder

### Organize Data Structure

Create script `organize_data.py`:

```python
import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
import random

# Source and destination
SOURCE_DIR = 'data/raw'  # Your downloaded images
TRAIN_DIR = 'data/train'
TEST_DIR = 'data/test'

# Classes
CLASSES = [
    'Acral_Lentiginous_Melanoma',
    'blue_finger',
    'clubbing',
    'Healthy_Nail',
    'Onychogryphosis',
    'pitting',
    'psoriasis'
]

# Create directories
for cls in CLASSES:
    os.makedirs(f'{TRAIN_DIR}/{cls}', exist_ok=True)
    os.makedirs(f'{TEST_DIR}/{cls}', exist_ok=True)

# Organize files (80/20 split)
for cls in CLASSES:
    src_path = f'{SOURCE_DIR}/{cls}'
    if os.path.exists(src_path):
        files = os.listdir(src_path)
        random.shuffle(files)
        
        # 80% train, 20% test
        split_idx = int(len(files) * 0.8)
        train_files = files[:split_idx]
        test_files = files[split_idx:]
        
        # Copy files
        for f in train_files:
            shutil.copy(f'{src_path}/{f}', f'{TRAIN_DIR}/{cls}/{f}')
        for f in test_files:
            shutil.copy(f'{src_path}/{f}', f'{TEST_DIR}/{cls}/{f}')
        
        print(f'{cls}: {len(train_files)} train, {len(test_files)} test')

print("✅ Data organization complete!")
```

Run:
```bash
python organize_data.py
```

### Verify Data

```bash
# Check structure
ls -R data/train/
ls -R data/test/

# Count images
find data/train -type f \( -name "*.jpg" -o -name "*.png" \) | wc -l
find data/test -type f \( -name "*.jpg" -o -name "*.png" \) | wc -l
```

---

## Troubleshooting

### Issue: GPU Out of Memory (OOM)

**Error:** `RuntimeError: CUDA out of memory`

**Solutions:**
```python
# Option 1: Reduce batch size
BATCH_SIZE = 16  # or 8

# Option 2: Reduce image size
IMAGE_SIZE = 224  # from 448

# Option 3: Enable gradient accumulation
ACCUMULATION_STEPS = 2

# Clear cache
import torch
torch.cuda.empty_cache()
```

### Issue: Data Not Loading

**Error:** `FileNotFoundError: No such file or directory`

**Check:**
```bash
# Verify directory structure
ls data/train/
# Should show: Acral_Lentiginous_Melanoma blue_finger clubbing ...

ls data/train/Acral_Lentiginous_Melanoma/ | head -5
# Should show image files (*.jpg, *.png)
```

### Issue: Model Download Fails

**Error:** `Connection error` or `timeout`

**Solutions:**
```bash
# Check disk space
df -h

# Use Hugging Face cache
export HF_HOME=/path/to/large/disk
export HF_DATASETS_CACHE=/path/to/large/disk

# Manual download
git lfs install
git clone https://huggingface.co/google/MedSigLIP-2B
```

### Issue: CUDA Not Available

**Error:** `torch.cuda.is_available() returns False`

**Solutions:**
```bash
# Check NVIDIA driver
nvidia-smi

# If not found, install driver
# Ubuntu:
sudo apt-get install nvidia-driver-XXX

# Verify PyTorch installation
python -c "import torch; print(torch.version.cuda)"
```

### Issue: Slow Training

**Optimization tips:**
```python
# Use mixed precision
from torch.cuda.amp import autocast

with autocast():
    outputs = model(images)

# Pin memory for faster data loading
train_loader = DataLoader(
    dataset,
    batch_size=32,
    num_workers=4,
    pin_memory=True
)

# Use gradient checkpointing
model.gradient_checkpointing_enable()
```

---

## GPU Optimization Tips

### Monitor GPU

```bash
# Real-time GPU monitoring
watch -n 1 nvidia-smi

# Or in Python
!nvidia-smi --query-gpu=name,utilization.gpu,utilization.memory,memory.used,memory.total --format=csv,noheader -l 1
```

### Optimize CUDA Settings

```python
import torch

# Use cuDNN benchmarking
torch.backends.cudnn.benchmark = True

# Optimize memory allocation
torch.cuda.empty_cache()

# Set precision
torch.set_float32_matmul_precision('high')  # Faster but less precise
```

### Multi-GPU Training (Advanced)

```python
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs")
    model = nn.DataParallel(model)
```

---

## Performance Benchmarks

| GPU | Batch Size | Training Time | Peak Memory |
|-----|-----------|---------------|-------------|
| T4 | 32 | ~45 min | 14 GB |
| V100 | 32 | ~20 min | 15 GB |
| A100 | 32 | ~10 min | 16 GB |
| CPU | 8 | ~8 hours | - |

---

## Next Steps

1. ✅ Complete setup
2. ✅ Prepare data
3. ✅ Run training
4. ✅ Evaluate results
5. ✅ Deploy model

**Good luck! 🚀**
