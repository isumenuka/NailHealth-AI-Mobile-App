# 🚀 MedGemma Fine-Tuning Setup Guide

## Quick Navigation

- [Google Colab Setup](#google-colab-setup) - Easiest, Free GPU
- [Kaggle Setup](#kaggle-setup) - Better GPU, Faster
- [Local Setup](#local-setup) - Full Control
- [Troubleshooting](#troubleshooting) - Common Issues

---

## Google Colab Setup

### Step 1: Upload Files

1. Open Google Colab: https://colab.research.google.com/
2. Click "File" → "Upload notebook"
3. Select `fine_tune_with_hugging_face-1.ipynb` from your downloads
4. Run Cell 1 (Environment Detection)
5. Upload `nail_diseases.csv` to your Google Drive

### Step 2: Update CSV Path (Cell 5)

In Cell 5, update the path:
```python
csv_path = '/content/drive/MyDrive/nail_diseases.csv'
```

### Step 3: Run All Cells

Click "Runtime" → "Run all" (or press Ctrl+F9)

### Step 4: Monitor Training

Cell 13 will show training progress. This takes 30 mins - 2 hours.

### Step 5: Download Results

After training completes:
1. Files appear in `/content/medgemma_nails_finetuned/`
2. Download the folder
3. Keep the trained model for inference

**Total Time**: 1-2 hours ⏱️

---

## Kaggle Setup

### Step 1: Create Dataset

1. Go to https://www.kaggle.com/settings/datasets
2. Click "Create new dataset"
3. Upload `nail_diseases.csv`
4. Name it "nail-disease-dataset"
5. Make it private (optional)
6. Create dataset

### Step 2: Create Notebook

1. Go to https://www.kaggle.com/code
2. Click "New Notebook"
3. Add data: Select "nail-disease-dataset"
4. Add code cell

### Step 3: Copy Notebook Code

Copy the entire content from `fine_tune_with_hugging_face-1.ipynb` into Kaggle

### Step 4: Update CSV Path (Cell 5)

```python
csv_path = '/kaggle/input/nail-disease-dataset/nail_diseases.csv'
```

### Step 5: Enable GPU

1. Click "⚙️ Settings"
2. Enable "GPU" acceleration
3. Select "T4 GPU" or "P100 GPU"
4. Save settings

### Step 6: Run Notebook

Click "Run All" and monitor progress

**Total Time**: 30 mins - 1 hour ⏱️

---

## Local Setup

### Prerequisites

- Python 3.9+
- GPU with 8GB+ VRAM (NVIDIA)
- CUDA 11.8+ installed
- 50GB free disk space

### Step 1: Clone Repository

```bash
git clone https://github.com/isumenuka/medsiglip-nail-disease-finetuning.git
cd medsiglip-nail-disease-finetuning
git checkout medgemma-finetuning
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Prepare Data

1. Place `nail_diseases.csv` in the repository root
2. Update path in notebook Cell 5:
   ```python
   csv_path = './nail_diseases.csv'
   ```

### Step 5: Start Jupyter

```bash
jupyter notebook
```

### Step 6: Open & Run Notebook

1. Open `fine_tune_with_hugging_face-1.ipynb`
2. Run all cells
3. Monitor training progress

**Total Time**: 1-3 hours (depends on GPU) ⏱️

---

## Dataset Preparation

### CSV Format Verification

Your `nail_diseases.csv` should have these columns:

```python
required_columns = [
    'nail_disease_category',
    'model_1_predicted_disease',
    'confirmed_diagnosis',
    'patient_age',
    'patient_sex',
    'patient_ethnicity',
    'fitzpatrick_skin_type',
    'disease_severity',
    'clinical_findings',
    'differential_diagnoses',
    'recommended_medical_tests',
    'treatment_protocol',
    'comorbidities',
    'clinical_notes',
    'prognosis'
]
```

### Check Before Training

```python
import pandas as pd
df = pd.read_csv('nail_diseases.csv')

# Check shape
print(f"Shape: {df.shape}")  # Should be (10000, 15)

# Check columns
print(f"Columns: {list(df.columns)}")

# Check for missing values
print(f"Missing values:\n{df.isnull().sum()}")
```

---

## Troubleshooting

### ❌ GPU Not Detected

**Error**: `cuda() called with an unsupported cuda version`

**Solution**:
```python
import torch
print(f'CUDA Available: {torch.cuda.is_available()}')
print(f'CUDA Version: {torch.version.cuda}')
```

If not available:
- Colab: GPU is enabled by default
- Kaggle: Enable in Settings → GPU
- Local: Install CUDA toolkit

### ❌ Out of Memory (OOM) Error

**Error**: `RuntimeError: CUDA out of memory`

**Solution 1 - Reduce batch size**:
```python
per_device_train_batch_size = 2  # Instead of 4
```

**Solution 2 - Increase gradient accumulation**:
```python
gradient_accumulation_steps = 4  # Instead of 2
```

**Solution 3 - Reduce sequence length**:
```python
max_seq_length = 256  # Instead of 512
```

**Solution 4 - Use smaller model**:
```python
model_name = "google/medgemma-4b"  # Instead of 27b
```

### ❌ CSV Not Found

**Error**: `FileNotFoundError: No such file or directory`

**Solution**:

Update the path in Cell 5:
```python
if ENVIRONMENT == 'colab':
    csv_path = '/content/drive/MyDrive/nail_diseases.csv'
elif ENVIRONMENT == 'kaggle':
    csv_path = '/kaggle/input/nail-disease-dataset/nail_diseases.csv'
else:
    csv_path = './nail_diseases.csv'
```

### ❌ Missing Columns

**Error**: `KeyError: 'column_name'`

**Solution**:

Verify your CSV has all 15 required columns. Run:
```python
df = pd.read_csv(csv_path)
print(list(df.columns))
```

### ❌ Slow Training

**Problem**: Training is taking too long

**Solutions**:
1. Use Kaggle instead of Colab (P100 > T4)
2. Reduce `max_seq_length` from 512 to 256
3. Reduce `num_train_epochs` from 3 to 2
4. Use 4B model instead of 27B
5. Increase `per_device_train_batch_size` if VRAM allows

### ❌ Model Not Loading

**Error**: `Could not load model at google/medgemma-4b`

**Solution**:

Make sure you're authenticated:
```python
from huggingface_hub import login
login()  # Will prompt for token
```

---

## Performance Tips

### ⚡ Speed Up Training

1. **Use Kaggle GPU** (P100 is 2x faster than Colab T4)
2. **Reduce sequence length** (256 vs 512)
3. **Lower precision** (float16 vs float32)
4. **Batch processing** (increase batch size if VRAM allows)
5. **Fewer epochs** (2 instead of 3)

### 💾 Memory Optimization

1. **4-bit quantization** (already in notebook)
2. **LoRA fine-tuning** (only ~1% of parameters trainable)
3. **Gradient checkpointing** (trades speed for memory)
4. **Smaller model** (4B vs 27B)

### 📈 Quality Improvements

1. **More data** (current 10,000 is good)
2. **More epochs** (3-5 for better convergence)
3. **Lower learning rate** (1e-4 for stability)
4. **Larger model** (27B for better reasoning)
5. **Balanced dataset** (equal samples per disease)

---

## Expected Results

### Training Metrics

| Metric | Expected Value |
|--------|----------------|
| Training Loss | 0.08 (down from 4.5) |
| Validation Loss | 0.02 |
| Accuracy | 85-92% |
| Training Time | 30 mins - 2 hours |
| Model Size | ~10-50 GB (with base model) |
| LoRA Size | 50-100 MB |

### Inference Speed

- **Per sample**: 1-5 seconds
- **Batch of 10**: 10-50 seconds
- **Latency**: 500-2000 ms

---

## Next Steps

1. ✅ Choose your environment (Colab/Kaggle/Local)
2. ✅ Follow setup steps above
3. ✅ Upload notebook and CSV
4. ✅ Run all cells
5. ✅ Monitor training (Cell 13)
6. ✅ Download trained model
7. ✅ Use for inference
8. ✅ Deploy to production

---

## Support

- **Issues**: Open GitHub issue
- **Docs**: See README.md
- **Google Colab**: Check GPU in Runtime menu
- **Kaggle**: Check Settings → Accelerator

---

**Happy Training! 🚀**
