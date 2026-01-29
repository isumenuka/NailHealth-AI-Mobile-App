# 🔧 Google Drive Setup Guide

## Quick Start for Google Colab Users

This notebook requires your dataset to be uploaded to Google Drive. Follow these steps:

### Step 1: Prepare Your Dataset Folder

Organize your nail disease images in the following structure:

```
nail-disease-dataset/
├── train/
│   ├── Acral_Lentiginous_Melanoma/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── blue_finger/
│   │   ├── image1.jpg
│   │   └── ...
│   ├── clubbing/
│   ├── Healthy_Nail/
│   ├── Onychogryphosis/
│   ├── pitting/
│   └── psoriasis/
│
└── test/
    ├── Acral_Lentiginous_Melanoma/
    ├── blue_finger/
    ├── clubbing/
    ├── Healthy_Nail/
    ├── Onychogryphosis/
    ├── pitting/
    └── psoriasis/
```

### Step 2: Upload to Google Drive

1. Go to [Google Drive](https://drive.google.com)
2. Create a new folder called `nail-disease-dataset` in your "My Drive"
3. Upload the entire dataset folder structure
4. Wait for upload to complete

### Step 3: Update the Notebook Path (if needed)

In the notebook, Cell 3 (Mount Google Drive), update this line if your path differs:

```python
GDRIVE_DATASET_PATH = '/content/gdrive/My Drive/nail-disease-dataset'  # Update if different
```

Common alternative paths:
- If in a subfolder: `/content/gdrive/My Drive/Datasets/nail-disease-dataset`
- If in a shared drive: `/content/gdrive/Shareddrives/YourSharedDrive/nail-disease-dataset`

### Step 4: Run the Notebook

1. Open the `MedSigLIP_NailDisease_FinetuningColab.ipynb` in Google Colab
2. Set runtime to **GPU (T4 or V100)** for faster training
3. Run cells in order from top to bottom
4. The notebook will:
   - Mount your Google Drive
   - Load your dataset from Google Drive
   - Fine-tune the MedSigLIP model
   - Save results to `/content/output`

## 📊 Expected Dataset Statistics

- **Total Images**: ~6,650 images
- **Training Set**: ~5,300 images (80%)
- **Test Set**: ~1,350 images (20%)
- **Classes**: 7 nail disease categories
- **Image Format**: JPG/PNG
- **Recommended Resolution**: 448x448 pixels (will be resized automatically)

## 🐛 Troubleshooting

### "Dataset not found" Error

**Solution**: 
1. Verify the path is correct by printing it in the notebook
2. Check that your folder structure matches exactly (including capitalization)
3. Ensure files are fully uploaded before running the notebook

### "Permission Denied" Error

**Solution**:
1. Run the Google Drive mount cell again
2. Authorize the notebook to access your Google Drive
3. Re-run the data loading cell

### "Out of Memory" Error

**Solution**:
1. Reduce `BATCH_SIZE` from 32 to 16 or 8
2. Reduce `IMAGE_SIZE` from 448 to 224
3. Use V100 GPU instead of T4

### Slow Data Loading

**Optimization**:
1. Use Google Colab's "Fast Runtime" option
2. Ensure your dataset is in the same Google Drive account
3. Reduce `NUM_WORKERS` if experiencing issues

## 💾 Output Files

After training, check `/content/output` in Colab for:

- `best_model.pt` - Best trained model weights
- `training_history.json` - Training metrics
- `training_results.png` - Visualization plots

## 📥 Download Results

1. In Colab, click Files panel on the left
2. Navigate to `/content/output`
3. Right-click files and select "Download"

## 🚀 Using Trained Model

After training, you can use your model for inference:

```python
import torch
from PIL import Image

# Load model
classifier.load_state_dict(torch.load('best_model.pt'))
classifier.eval()

# Prepare image
image = Image.open('nail_image.jpg')
image_tensor = val_transforms(image).unsqueeze(0).to(device)

# Predict
with torch.no_grad():
    output = classifier(image_tensor)
    prediction = output.argmax(dim=1).item()
    class_name = train_dataset.classes[prediction]

print(f"Predicted: {class_name}")
```

## 📝 Notes

- The notebook uses **MedSigLIP-2B** model (large variant)
- Training time: ~30-60 minutes on T4 GPU
- Expected accuracy: 88-95% on test set
- Batch size: 32 images per batch
- Learning rate: 1e-4 (AdamW optimizer)

---

**Questions?** Check the notebook's error messages and the troubleshooting section above.
