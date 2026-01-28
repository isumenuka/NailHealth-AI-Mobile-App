# 🏥 MedSigLIP Fine-tuning for Nail Disease Classification

Fine-tune Google's **MedSigLIP** (Medical SigLIP Vision-Language Model) for detecting and classifying nail diseases using custom nail image datasets.

![GitHub](https://img.shields.io/badge/license-Apache%202.0-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red)
![Python](https://img.shields.io/badge/Python-3.8+-green)

---

## 📋 Overview

This repository contains a complete pipeline for fine-tuning Google's MedSigLIP model specifically for nail disease classification. The notebook includes:

✅ Data loading and preprocessing  
✅ MedSigLIP model fine-tuning  
✅ Custom classification head training  
✅ Comprehensive evaluation metrics  
✅ Visualization and reporting  
✅ Model export for deployment  

---

## 🎯 Nail Disease Categories

The model is trained to recognize 7 nail conditions:

1. **Acral Lentiginous Melanoma (ALM)** - Black/brown lines under nail (cancerous)
2. **Blue Finger** - Blue discoloration of nail bed
3. **Clubbing** - Bulging, rounded nail appearance
4. **Healthy Nail** - Normal reference
5. **Onychogryphosis** - Thickened, curved nails
6. **Pitting** - Small depressions in nail plate
7. **Psoriasis** - Nail pitting and discoloration from psoriasis

---

## 📊 Dataset Structure

```
data/
├── train/                    (80% - ~5,300 images)
│   ├── Acral_Lentiginous_Melanoma/
│   ├── blue_finger/
│   ├── clubbing/
│   ├── Healthy_Nail/
│   ├── Onychogryphosis/
│   ├── pitting/
│   └── psoriasis/
└── test/                     (20% - ~1,350 images)
    ├── Acral_Lentiginous_Melanoma/
    ├── blue_finger/
    ├── clubbing/
    ├── Healthy_Nail/
    ├── Onychogryphosis/
    ├── pitting/
    └── psoriasis/
```

**Prepare your dataset before running the notebook!**

Download from these sources:
- **Kaggle**: [Nail Disease Detection](https://www.kaggle.com/datasets/nikhilgurav21/nail-disease-detection-dataset)
- **Kaggle**: [Nail Classification](https://www.kaggle.com/datasets/josephrasanjana/nail-disease-image-classification-dataset)
- **Mendeley**: [Nail Psoriasis](https://data.mendeley.com/datasets/3hckgznc67)

---

## 🚀 Quick Start

### Option 1: Run in Google Colab (Recommended)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/isumenuka/medsiglip-nail-disease-finetuning/blob/MedSigLIP-Fine-tuning/medsiglip_nail_disease_finetuning.ipynb)

1. Click the Colab badge above
2. Upload your data to Google Drive or Colab
3. Update data paths in the notebook
4. Select **GPU (T4 or V100)** from Runtime → Change Runtime Type
5. Run all cells!

### Option 2: Local Setup

```bash
# Clone the repository
git clone https://github.com/isumenuka/medsiglip-nail-disease-finetuning.git
cd medsiglip-nail-disease-finetuning
git checkout MedSigLIP-Fine-tuning

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Jupyter
jupyter notebook medsiglip_nail_disease_finetuning.ipynb
```

---

## 📦 Requirements

- Python 3.8+
- PyTorch 2.0+
- CUDA 11.8+ (for GPU support)
- 16 GB RAM minimum
- 50 GB storage for models and data

**Installation:**
```bash
pip install torch torchvision transformers datasets pillow scikit-learn matplotlib tqdm numpy pandas open-clip-torch
```

---

## 🎓 Notebook Contents

| Section | Description |
|---------|-------------|
| **1-2** | Setup & GPU Check |
| **3** | Mount Google Drive (optional) |
| **4-5** | Data Loading & DataLoaders |
| **6** | Load MedSigLIP Model |
| **7** | Add Classification Head |
| **8** | Training Configuration |
| **9** | Training Loop Implementation |
| **10** | Main Training (10 epochs) |
| **11** | Results Visualization |
| **12** | Classification Report |
| **13** | Save Model & Artifacts |
| **14** | Single Image Inference |
| **15** | Batch Inference & Visualization |
| **16** | Export for Deployment |

---

## 📊 Expected Results

| Metric | Value |
|--------|-------|
| **Training Time** | 30-60 min (T4 GPU) |
| **Final Accuracy** | 88-95% |
| **Model Size** | ~420 MB |
| **Inference Time** | <500ms/image |
| **Supported Formats** | PyTorch (.pt), ONNX (.onnx) |

---

## 💾 Model Architecture

```
MedSigLIP-2B (Pre-trained)
    ↓
Image Embedding (1152-dim)
    ↓
Classification Head
├─ Linear(1152 → 512)
├─ BatchNorm1d(512)
├─ ReLU
├─ Dropout(0.3)
├─ Linear(512 → 256)
├─ BatchNorm1d(256)
├─ ReLU
├─ Dropout(0.3)
└─ Linear(256 → 7 classes)
    ↓
Logits (7-dim)
```

---

## 🔍 Usage Examples

### Single Image Prediction

```python
class_name, confidence, image = predict_image(
    'path/to/nail_image.jpg',
    classifier,
    processor,
    device,
    train_dataset.classes
)

print(f"Prediction: {class_name} ({confidence:.2%})")
```

### Batch Predictions

```python
test_loader = DataLoader(test_dataset, batch_size=32)

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        outputs = classifier(images)
        predictions = outputs.argmax(dim=1)
```

---

## 📈 Training Configuration

```python
NUM_EPOCHS = 10
LEARNING_RATE = 1e-4
BATCH_SIZE = 32
IMAGE_SIZE = 448
WEIGHT_DECAY = 1e-5
OPTIMIZER = AdamW
SCHEDULER = CosineAnnealingLR
```

---

## 📁 Output Files

After training, the `/content/output` directory contains:

```
output/
├── best_model.pt                    # Best model checkpoint
├── classifier_head.pt               # Classifier head only
├── classifier_head.onnx             # ONNX format (deployment)
├── training_history.json            # Training metrics
├── model_metadata.json              # Model info
├── classification_report.json       # Per-class metrics
├── deployment_info.json             # Deployment guide
├── training_results.png             # Loss/accuracy plots
└── predictions_visualization.png    # Predictions on test set
```

---

## 🌍 Deployment

### Export for Inference

```python
# PyTorch format (recommended)
model_state = torch.load('best_model.pt')
classifier.load_state_dict(model_state)

# ONNX format (for TensorFlow Lite/ONNX Runtime)
# Already exported in notebook
```

### Mobile Deployment

The model is optimized for mobile:
- **Input size**: 448×448 pixels
- **Format**: JPEG images
- **Inference**: <500ms on mobile GPU
- **Size**: ~420 MB

---

## 🛠️ Troubleshooting

### Issue: Out of Memory (OOM)

**Solution:** Reduce batch size
```python
BATCH_SIZE = 16  # or 8
```

### Issue: GPU Not Detected

**Solution (Colab):** Runtime → Change Runtime Type → GPU (T4)

**Solution (Local):** 
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

### Issue: Data Not Loading

**Check structure:**
```bash
ls data/train/
# Should show: Acral_Lentiginous_Melanoma/ blue_finger/ clubbing/ ...
```

### Issue: Model Download Fails

**Solution:** Ensure 5+ GB free disk space
```bash
df -h  # Check disk space
```

---

## 📚 References

- **MedSigLIP**: [Google Health AI](https://developers.google.com/health-ai/medsiglip)
- **MedGemma**: [Google Cloud Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/models/medgemma)
- **Transformers Library**: [Hugging Face](https://huggingface.co/docs/transformers)

---

## 📜 License

This project is licensed under the **Apache License 2.0** - see [LICENSE](LICENSE) file.

Google's MedSigLIP model is licensed under the **Health AI Developer Foundations (HAI-DEF)** license.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📧 Support

For issues, questions, or suggestions:

- **GitHub Issues**: [Create an issue](https://github.com/isumenuka/medsiglip-nail-disease-finetuning/issues)
- **Email**: isumenuka@gmail.com
- **Website**: [isumenuka.me](https://isumenuka.me)

---

## 🎉 Citation

If you use this project in your research, please cite:

```bibtex
@software{medsiglip_nails_2026,
  title={MedSigLIP Fine-tuning for Nail Disease Classification},
  author={Enuka, K.G.I},
  year={2026},
  url={https://github.com/isumenuka/medsiglip-nail-disease-finetuning}
}
```

---

## 🙏 Acknowledgments

- Google Health AI Team (MedSigLIP Model)
- Kaggle Community (Nail Disease Datasets)
- PyTorch Foundation
- Hugging Face Transformers

---

**Last Updated**: January 28, 2026  
**Version**: 1.0.0  
**Status**: Active Development ✅
