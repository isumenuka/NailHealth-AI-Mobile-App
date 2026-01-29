# 🚀 Quick Start Guide - 5 Minutes to Training

## 1️⃣ Create Hugging Face Account (2 min)

**Never done this before?**

```
1. Go to https://huggingface.co/signup
2. Create account & verify email
3. Go to https://huggingface.co/google/MedSigLIP-2B
4. Click "Access repository" button
```

**Already have account?**

```
1. Go to https://huggingface.co/google/MedSigLIP-2B
2. Click "Access repository" button
```

## 2️⃣ Get Your Access Token (1 min)

```
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it: "MedSigLIP-Colab"
4. Select: "Read" permission
5. Copy the token to clipboard
```

## 3️⃣ Open Colab Notebook (1 min)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/isumenuka/medsiglip-nail-disease-finetuning/blob/MedSigLIP-Fine-tuning/medsiglip_nail_disease_finetuning.ipynb)

```
Click the button above, or:
1. Go to colab.research.google.com
2. File → Open notebook
3. Paste: https://github.com/isumenuka/medsiglip-nail-disease-finetuning
```

## 4️⃣ Setup GPU (1 min)

```
Runtime → Change runtime type
↓
Select "GPU" (T4 or V100)
↓
Click "Save"
```

## 5️⃣ Login to Hugging Face (1 min)

**Run the FIRST cell:**

```python
from huggingface_hub import login
login(token=None, add_to_git_credential=True)
```

When prompted:
```
Paste your token and press Enter
```

---

## 📝 What to Do Next

### If you have nail disease data:

```
1. Upload to Google Drive or Colab
2. Update these paths in the notebook:
   TRAIN_DATA_PATH = '/content/data/train'
   TEST_DATA_PATH = '/content/data/test'
3. Run all cells
4. Wait 30-60 minutes
5. Download results
```

### If you DON'T have data:

```
1. Download from Kaggle:
   https://www.kaggle.com/datasets/nikhilgurav21/nail-disease-detection-dataset
   
2. Extract and upload to Colab

3. Continue with steps above
```

---

## ⚠️ Common Issues

### ❌ "gated repo" Error

**Fix:** You haven't accepted access yet
- Go to https://huggingface.co/google/MedSigLIP-2B
- Click "Access repository"
- Wait a few seconds
- Regenerate token
- Try again

### ❌ "Token not found" Error

**Fix:** Check your token is copied correctly
- Go back to https://huggingface.co/settings/tokens
- Copy token again
- Paste in the login cell
- Run the cell

### ❌ "GPU Not Available"

**Fix:** Change runtime to GPU
- Runtime → Change runtime type
- Select GPU (T4 or V100)
- Click Save

### ❌ "Out of Memory"

**Fix:** Reduce batch size
```python
BATCH_SIZE = 16  # Change from 32 to 16
```

---

## 📖 Files Mentioned

- **[HUGGING_FACE_SETUP.md](HUGGING_FACE_SETUP.md)** - Detailed HF guide
- **[README.md](README.md)** - Full documentation
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Advanced setup

---

## 🚀 You're Ready!

Now scroll to the first cell and click the play button ▶️

**Need help?**
- Check [HUGGING_FACE_SETUP.md](HUGGING_FACE_SETUP.md)
- Open an issue on GitHub
- Email: isumenuka@gmail.com

---

**Happy training! 🚀**
