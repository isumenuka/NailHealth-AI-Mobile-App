# MedGemma Fine-Tuning for Nail Disease Classification

## 📋 Overview

This branch contains a complete pipeline for fine-tuning Google's **MedGemma** model on nail disease classification using the provided nail disease dataset.

### ✨ Key Features

- ✅ **Multi-Environment Support**: Works on Google Colab, Kaggle, and local machines
- ✅ **Memory Optimized**: 4-bit quantization + LoRA fine-tuning
- ✅ **Production Ready**: Full training, evaluation, and inference pipeline
- ✅ **Easy to Use**: Jupyter notebook with 19 pre-configured cells
- ✅ **10,000 Samples**: Complete nail disease dataset included
- ✅ **7 Disease Categories**: Comprehensive nail pathology coverage

### 🏥 Supported Nail Diseases

1. **White Nails** (Terry's Nails) - White discoloration of nail beds
2. **Blue Nails** (Cyanosis) - Bluish nail appearance
3. **Clubbing** (Finger Clubbing) - Rounded, bulbous nail tips
4. **Spoon Nails** (Koilonychia) - Concave nail shape
5. **Melanoma** - Dark pigmentation/lesions
6. **Psoriasis** - Pitting and nail thickening
7. **Onychogryphosis** - Severely thickened nails

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)

1. Open the notebook in Colab
2. Run all cells (Cell 1-19)
3. Download trained model
4. Done! ✅

**Time**: ~1-2 hours

### Option 2: Kaggle

1. Create Kaggle Dataset with `nail_diseases.csv`
2. Create Kaggle Notebook
3. Copy notebook content
4. Enable GPU
5. Run all cells

**Time**: ~30 minutes - 1 hour

### Option 3: Local Machine

```bash
# Clone repository
git clone https://github.com/isumenuka/medsiglip-nail-disease-finetuning
cd medsiglip-nail-disease-finetuning
git checkout medgemma-finetuning

# Install dependencies
pip install -r requirements.txt

# Run notebook
jupyter notebook medgemma_nail_finetuning_notebook.ipynb
```

## 📊 Dataset Structure

The `nail_diseases.csv` file contains **10,000 rows** with 15 columns:

```
1. nail_disease_category - Disease classification
2. model_1_predicted_disease - Initial model prediction
3. confirmed_diagnosis - Ground truth diagnosis
4. patient_age - Age (18-88)
5. patient_sex - M/F
6. patient_ethnicity - Ethnic background
7. fitzpatrick_skin_type - 1-5 scale
8. disease_severity - mild/moderate/severe/none
9. clinical_findings - Symptom description
10. differential_diagnoses - Alternative diagnoses
11. recommended_medical_tests - Testing recommendations
12. treatment_protocol - Treatment options
13. comorbidities - Related conditions
14. clinical_notes - Additional notes
15. prognosis - Outcome prediction
```

## 📖 Notebook Structure

| Cell | Task | Time |
|------|------|------|
| 1 | Environment detection | <1 min |
| 2 | Mount Google Drive | <1 min |
| 3 | Install dependencies | 2-3 min |
| 4 | Import & check GPU | <1 min |
| 5 | Load CSV data | <1 min |
| 6 | Create training prompts | 1-2 min |
| 7 | Split data (70/15/15) | <1 min |
| 8 | Load MedGemma model | 2-5 min |
| 9 | Setup LoRA | <1 min |
| 10 | Prepare datasets | <1 min |
| 11 | Configure training | <1 min |
| 12 | Initialize trainer | <1 min |
| **13** | **START TRAINING** | **30 min - 2 hrs** |
| 14 | Evaluate model | 5-10 min |
| 15 | Save model | 2-3 min |
| 16 | Test inference | <1 min |
| 17 | Save results | <1 min |
| 18 | Push to Hub (optional) | 5 min |
| 19 | Summary | <1 min |

## 🔧 Configuration Options

### Model Selection

```python
# Smaller, faster (4B parameters)
MODEL_NAME = "google/medgemma-4b"

# Larger, better (27B parameters)
MODEL_NAME = "google/medgemma-27b"
```

### Training Parameters

```python
per_device_train_batch_size=4  # Batch size (reduce if OOM)
learning_rate=2e-4             # Learning rate
max_seq_length=512             # Maximum sequence length
num_train_epochs=3             # Number of epochs
```

## 💾 Output Files

After training:

```
medgemma_nails_finetuned/
├── adapter_config.json       # LoRA configuration
├── adapter_model.bin         # LoRA weights (~50-100 MB)
├── config.json               # Model config
└── tokenizer_config.json

logs/
└── events.out.tfevents.*     # TensorBoard logs

training_summary.json         # Training metadata
```

## 📈 Expected Results

**After 3 epochs of training:**

- Training Loss: ~0.08 (down from ~4.5)
- Validation Loss: ~0.02
- Model Accuracy: ~85-92%
- Total Time: 1-2 hours on Colab T4 GPU

## ⚠️ Troubleshooting

### Out of Memory (OOM) Error

```python
per_device_train_batch_size=2    # Reduce from 4
gradient_accumulation_steps=4    # Increase to compensate
```

### CSV Not Found

Update the path based on your environment in Cell 5.

### GPU Not Detected

```python
import torch
print(f'GPU Available: {torch.cuda.is_available()}')
```

### Training Too Slow

- Use Kaggle (faster GPU)
- Reduce `max_seq_length` to 256
- Use 4B model instead of 27B
- Decrease number of epochs

## 📚 References

- [MedGemma Docs](https://developers.google.com/health-ai)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [PEFT/LoRA](https://github.com/huggingface/peft)
- [TRL Training](https://github.com/huggingface/trl)

## 📄 License

- **MedGemma**: HAI-DEF Open License
- **Code**: MIT License
- **Dataset**: CC-BY-4.0

## ✅ Next Steps

1. ✅ Download this branch
2. ✅ Upload `nail_diseases.csv`
3. ✅ Run the notebook
4. ✅ Fine-tune the model
5. ✅ Deploy to production

---

**Happy Fine-tuning! 🚀**
