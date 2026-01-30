# 🟣 Kaggle Quick Start Guide - MedGemma Fine-Tuning

## ⚡ Kaggle Benefits

✅ **Free GPU**: P100 (40GB VRAM) - 2-3x faster than Colab T4  
✅ **Better Performance**: Dedicated resources, no runtime limits  
✅ **Faster Training**: 30 mins - 1 hour on P100 GPU  
✅ **Easy Integration**: Built-in dataset and notebook support  

---

## 📋 Step-by-Step Setup

### Step 1: Create Kaggle Dataset (5 minutes)

1. Go to https://www.kaggle.com/settings/datasets
2. Click **"Create new dataset"**
3. Name it: `nail-disease-classification`
4. Upload `nail_diseases.csv` from your computer
5. Click **"Create"**
6. Wait for processing (usually 1-2 minutes)

**Status**: ✅ Dataset ready

---

### Step 2: Create Kaggle Notebook (2 minutes)

1. Go to https://www.kaggle.com/code
2. Click **"New Notebook"**
3. Click **"+ Add data"**
4. Search and select: `nail-disease-classification`
5. Click **"Add"**
6. Now your data is attached to the notebook

**Status**: ✅ Notebook created with data

---

### Step 3: Copy Notebook Code (2 minutes)

1. Open this GitHub link:
   ```
   https://github.com/isumenuka/medsiglip-nail-disease-finetuning/blob/medgemma-finetuning/medgemma_kaggle_finetuning.ipynb
   ```

2. Click **"Raw"** button (or download the notebook)

3. Copy all the code, OR download the `.ipynb` file

4. Paste into your Kaggle notebook:
   - Delete the default "Hello" cell
   - Click **"+ Code"** to add new cells
   - Paste the notebook cells

**Status**: ✅ Code copied

---

### Step 4: Update CSV Path (1 minute)

In **Cell 5** of your notebook, you'll see:

```python
if ENVIRONMENT == 'kaggle':
    csv_path = '/kaggle/input/nail-disease-classification/nail_diseases.csv'
```

✅ **This is already correct!** Just verify the dataset name matches what you created.

**Status**: ✅ Path configured

---

### Step 5: Enable GPU (1 minute)

1. In your Kaggle notebook, click **"⚙ Settings"** (top right)
2. Find **"Accelerator"** section
3. Select **"GPU"**
4. Choose: **"P100"** (if available) or **"T4"**
5. Click **"Save"**

**Status**: ✅ GPU enabled

---

### Step 6: Run Notebook (30 mins - 1 hour)

1. Click **"Run All"** button at top, OR
2. Press **`Ctrl + Shift + Enter`**
3. Wait for cells to execute
4. Monitor progress in Cell 14 (Training cell)

**Status**: ⏳ Training in progress

**Expected output**:
```
Starting training...
Epoch 1/3: [====================] - training_loss: 0.2345
Epoch 2/3: [====================] - training_loss: 0.0987
Epoch 3/3: [====================] - training_loss: 0.0654
Training loss: 0.0654
```

**Status**: ✅ Training complete

---

### Step 7: Download Results (2 minutes)

After training completes:

1. In Kaggle notebook, click **"Output"** (right panel)
2. You'll see:
   - `medgemma_nails_finetuned/` (trained model)
   - `logs/` (training logs)
   - `training_summary.json` (metrics)
   - `train_data.csv`, `val_data.csv`, `test_data.csv` (splits)

3. Download files you need:
   - Click the **download icon** next to each file
   - OR download entire output folder

**Status**: ✅ Results downloaded

---

## 🔧 Customization

### Change Model Size

In **Cell 4**, change:

```python
# Smaller, faster (4B parameters) - Default
'model_name': 'google/medgemma-4b',

# Larger, better (27B parameters) - Slower on T4, OK on P100
'model_name': 'google/medgemma-27b',
```

### Adjust Training Parameters

In **Cell 4**, modify:

```python
'batch_size': 4,          # Reduce to 2 if OOM error
'learning_rate': 2e-4,    # Lower = more stable, slower
'num_epochs': 3,          # More = better results, longer
'max_seq_length': 512,    # Lower = faster, less context
```

### Reduce Memory Usage

If you get **"Out of Memory"** error:

```python
'batch_size': 2,                    # Reduce from 4
'max_seq_length': 256,              # Reduce from 512
gradient_accumulation_steps': 4,   # Increase from 2
```

---

## 📊 Training Timeline

| Step | Time | GPU |
|------|------|-----|
| Cell 1-4: Setup | 2 min | None |
| Cell 5-8: Load data | 3 min | None |
| Cell 9: Load model | 2-3 min | P100 |
| Cell 10-12: Configure | 1 min | None |
| Cell 13: Init trainer | <1 min | None |
| **Cell 14: TRAIN** | **20-45 min** | **P100** |
| Cell 15: Evaluate | 5 min | P100 |
| Cell 16: Save | 2 min | Disk |
| Cell 17-19: Summary | 1 min | None |
| **TOTAL** | **~1 hour** | - |

---

## ✅ Expected Results

**Training Metrics**:
- Training Loss: 4.5 → 0.08 ✅
- Validation Loss: 0.03 ✅
- Accuracy: 85-92% ✅

**Output Files**:
- `medgemma_nails_finetuned/` (~10-50 GB with base model)
- `adapter_model.bin` (~50-100 MB for just LoRA)
- `training_summary.json` (metrics)

**Model Size**:
- Full model: ~10 GB (4B) or ~50 GB (27B)
- LoRA adapters only: ~50-100 MB
- For deployment, use adapters only!

---

## ⚠️ Troubleshooting

### Error: "CSV not found"

**Fix**: Verify dataset name in Cell 5:
```python
csv_path = '/kaggle/input/<YOUR-DATASET-NAME>/nail_diseases.csv'
```

### Error: "CUDA out of memory"

**Fix**: Reduce batch size in Cell 4:
```python
'batch_size': 2,  # instead of 4
```

### Error: "Model not found"

**Fix**: Authenticate with Hugging Face:
1. Get token from: https://huggingface.co/settings/tokens
2. Run in notebook:
```python
from huggingface_hub import login
login(token='YOUR_HF_TOKEN')
```

### Training is very slow

**Fix**:
1. Make sure GPU is enabled (Settings → GPU)
2. Check if P100 is available (faster than T4)
3. Reduce `max_seq_length` to 256
4. Reduce `num_epochs` to 2

### Can't find output files

**Fix**: In Kaggle notebook:
1. Click **"Output"** on right panel
2. Files appear there after execution
3. Click download icon to save locally

---

## 🎯 Next Steps After Training

1. **Download trained model**
   - Download `medgemma_nails_finetuned/` folder
   - Keep locally for inference

2. **Test inference**
   - Use on your own nail disease cases
   - Evaluate predictions

3. **Deploy to production**
   - Upload to Hugging Face Hub
   - Create API endpoint
   - Share with team

4. **Iterate & improve**
   - Collect more data
   - Fine-tune again with improvements
   - Monitor performance

---

## 📞 Support

- **Setup Issues**: See `SETUP_GUIDE.md`
- **Configuration**: See `README.md`
- **General Help**: See `BRANCH_INFO.md`
- **GitHub**: Open issue on repository

---

## 🚀 Ready to Train?

✅ Create Kaggle dataset  
✅ Create Kaggle notebook  
✅ Attach dataset to notebook  
✅ Copy notebook code  
✅ Update CSV path (if needed)  
✅ Enable GPU  
✅ Click "Run All"  
✅ Wait for training...  
✅ Download results  
✅ Use your fine-tuned model!  

**Estimated time: ~1 hour total** ⏱️

---

**Happy Training on Kaggle! 🎉**
