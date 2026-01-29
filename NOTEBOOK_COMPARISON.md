# 📱 MedSigLIP Fine-tuning Notebook Comparison

## Quick Decision Guide

### Choose **Colab Notebook** if:
- ✅ You use Google Drive for storage
- ✅ You prefer Google's interface
- ✅ You want free T4 GPU easily
- ✅ You're already in the Google ecosystem
- ✅ You need to access other Drive files

### Choose **Kaggle Notebook** if:
- ✅ You prefer Kaggle environment
- ✅ Your dataset is already on Kaggle
- ✅ You want better GPU options (P100)
- ✅ You don't want to set up Google Drive
- ✅ You prefer notebook version control on Kaggle
- ✅ You want integrated dataset versioning

---

## Feature Comparison

| Feature | Colab | Kaggle |
|---------|-------|--------|
| **Notebook Type** | Google Colab | Kaggle Notebooks |
| **GPU Options** | T4, V100 (free), A100 (paid) | T4, P100, TPU (free) |
| **Setup Complexity** | Medium (Google Drive mount) | Low (built-in dataset) |
| **Storage** | Google Drive | /kaggle/working |
| **Dataset Import** | Via Drive or Upload | Via Kaggle Dataset |
| **Code Organization** | Single notebook | Notebook with data inputs |
| **Collaboration** | Share via link | Kaggle platform |
| **Output Download** | Manual or Drive sync | Direct from /kaggle/working |
| **Version Control** | Basic (cell history) | Kaggle version history |
| **Max Runtime** | 12 hours | 9 hours (continuous) |
| **Cost** | Free (with limits) | Free (with limits) |
| **Best For** | Flexible, quick setup | Dataset-centric projects |

---

## Installation Requirements

### Colab: `MedSigLIP_NailDisease_FinetuningColab.ipynb`

**Setup Time**: ~5 minutes

```
1. Open notebook in Google Colab
2. Mount Google Drive
3. Upload dataset to Drive (optional)
4. Run cells sequentially
```

**Dependencies**:
- Google Account (free)
- Dataset uploaded to Google Drive (or provided inline)
- Hugging Face token

---

### Kaggle: `MedSigLIP_NailDisease_FinetuningKaggle.ipynb`

**Setup Time**: ~10 minutes

```
1. Create Kaggle dataset from ZIP
2. Create Kaggle notebook
3. Add dataset as input
4. Copy notebook code
5. Run cells sequentially
```

**Dependencies**:
- Kaggle Account (free)
- Dataset uploaded as Kaggle Dataset
- Hugging Face token

---

## Dataset Handling

### Colab

**Location**: Google Drive (`My Drive/nail-disease-dataset/`)

```python
# Mount Drive
from google.colab import drive
drive.mount('/content/gdrive')

# Define path
GDRIVE_DATASET_PATH = '/content/gdrive/My Drive/nail-disease-dataset'
```

**Pros**:
- Access from anywhere
- Easy backup
- No reuploading needed

**Cons**:
- Takes time to mount
- Manual organization needed

---

### Kaggle

**Location**: Kaggle Dataset (`/kaggle/input/`)

```python
# Auto-detect from /kaggle/input
KAGGLE_INPUT_PATH = '/kaggle/input'

# ZIP auto-extraction
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(LOCAL_DATASET_PATH)
```

**Pros**:
- No manual organization
- Version control built-in
- Shareable datasets

**Cons**:
- Limited to uploaded datasets
- Requires ZIP file preparation

---

## GPU Performance Comparison

### Colab (T4 GPU - Free Tier)
```
- VRAM: 16 GB
- Expected Training Time: 45-60 minutes (10 epochs)
- Inference: 400-500ms per image
```

### Kaggle (P100 GPU - Free Tier)
```
- VRAM: 16 GB
- Expected Training Time: 30-40 minutes (10 epochs)
- Inference: 250-350ms per image
- 20-30% faster than T4
```

---

## File Structure Differences

### Colab
```
/content/
├── data/
│   ├── train/
│   └── test/
├── gdrive/         # Google Drive mount
└── output/         # Results saved here
```

### Kaggle
```
/kaggle/
├── input/          # Dataset inputs
│   └── dataset-name/
└── working/        # Output directory
    └── output/     # Results saved here
```

---

## Output File Locations

### Colab
```
/content/output/
├── best_model.pt
├── training_results.png
└── training_history.json
```

**Download**: Manual download from Colab files panel

---

### Kaggle
```
/kaggle/working/output/
├── best_model.pt
├── training_results.png
└── training_history.json
```

**Download**: Auto-available in Output section after notebook run

---

## Step-by-Step Migration Guide

### Migrating FROM Colab TO Kaggle

1. **Export your Colab notebook**
   - File → Download → .ipynb

2. **Prepare your dataset as ZIP**
   - Create: `data/train/` and `data/test/`
   - Zip everything: `nail-disease-dataset.zip`

3. **Upload to Kaggle**
   - Create Kaggle dataset from ZIP
   - Publish dataset

4. **Create Kaggle notebook**
   - Import downloaded .ipynb
   - Or use `MedSigLIP_NailDisease_FinetuningKaggle.ipynb`
   - Add dataset as input

5. **Adjust paths** (if needed)
   - Colab: `/content/data/` → Kaggle: `/kaggle/input/dataset-name/data/`
   - Kaggle notebook auto-detects paths

---

### Migrating FROM Kaggle TO Colab

1. **Export your Kaggle notebook**
   - Click options → Download notebook as .ipynb

2. **Export your dataset**
   - Download from Kaggle dataset page
   - Upload to Google Drive

3. **Create Colab notebook**
   - Import downloaded .ipynb
   - Or use `MedSigLIP_NailDisease_FinetuningColab.ipynb`

4. **Adjust paths**
   - Kaggle: `/kaggle/input/` → Colab: `/content/gdrive/My Drive/`
   - Update `GDRIVE_DATASET_PATH` variable

---

## Troubleshooting: Choose Your Environment

### "My GPU keeps disconnecting"

**Colab** → Enable background execution
```
Tools → Settings → Enable notifications
```

**Kaggle** → Better connection stability (9 hours continuous)

---

### "I want to share my training run"

**Colab** → Share notebook directly via link

**Kaggle** → Publish notebook + dataset with versioning

---

### "I need faster training"

**Colab** → Upgrade to V100 or A100

**Kaggle** → Use free P100 (faster than T4)

---

### "I already have the dataset on Kaggle"

**Recommendation**: Use Kaggle notebook! ✓
- No re-uploading needed
- Built-in versioning
- Direct dataset access

---

## Quick Reference Commands

### Check GPU (Both)
```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

### List Kaggle Inputs
```python
import os
print(os.listdir('/kaggle/input'))
```

### Mount Colab Drive
```python
from google.colab import drive
drive.mount('/content/gdrive')
```

---

## Final Recommendation

```
IF dataset on Kaggle:
  USE: Kaggle Notebook ✅

IF dataset on Google Drive:
  USE: Colab Notebook ✅

IF starting fresh:
  CHOICE: Your preference
  - Want simplicity? → Kaggle
  - Want flexibility? → Colab
```

---

## Resources

- **Colab Setup**: [HUGGING_FACE_SETUP.md](./HUGGING_FACE_SETUP.md)
- **Kaggle Setup**: [KAGGLE_SETUP.md](./KAGGLE_SETUP.md)
- **Colab Notebook**: [MedSigLIP_NailDisease_FinetuningColab.ipynb](./MedSigLIP_NailDisease_FinetuningColab.ipynb)
- **Kaggle Notebook**: [MedSigLIP_NailDisease_FinetuningKaggle.ipynb](./MedSigLIP_NailDisease_FinetuningKaggle.ipynb)

---

**Choose your platform and start training! 🚀**
