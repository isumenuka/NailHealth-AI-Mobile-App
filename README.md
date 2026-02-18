# 🩺 Nail Disease Detection with MedSigLIP (Kaggle Edition)

This repository contains a specialized Kaggle notebook for fine-tuning Google's **MedSigLIP (Medical SigLIP Vision-Language Model)** to detect various nail diseases. 

## 📂 File Structure

- **`MedSigLIP_NailDisease_FinetuningKaggle.ipynb`**: The main notebook containing the entire training and evaluation pipeline. This notebook is optimized for Kaggle's GPU environment.

## 🚀 Key Features

- **State-of-the-Art Foundation**: Uses `google/medsiglip-448`, a vision-language model pre-trained on medical data.
- **Custom Classification Head**: Implements a robust classifier on top of MedSigLIP embeddings to specialize in nail textures.
- **Automated Tuning**: Includes **Optuna** integration for automated hyperparameter tuning (Learning Rate, Batch Size, Optimizer) to maximize performance.
- **Class Balancing**: Automatically handles dataset imbalances using calculated class weights.
- **Data Augmentation**: Robust training transforms (ColorJitter, RandomAffine, GaussianBlur, etc.) to improve generalization.

## 🦠 Detected Conditions

The model is trained to classify 7 specific nail conditions:
1. **Acral Lentiginous Melanoma**: Critical for early skin cancer detection.
2. **Blue Finger**: Indicator of potential circulation issues.
3. **Clubbing**: Associated with heart or lung conditions.
4. **Onychogryphosis**: "Ram's horn nails," common in elderly patients.
5. **Pitting**: Often an early sign of Psoriasis.
6. **Psoriasis**: Autoimmune condition affecting nails.
7. **Healthy Nail**: Baseline for normal cases.

## 🛠️ How to Run on Kaggle

1. **Upload Notebook**: Upload `MedSigLIP_NailDisease_FinetuningKaggle.ipynb` to Kaggle.
2. **Add Dataset**: Search for and add the `nail-disease-dataset` to your Kaggle notebook input.
   - Expected Path: `/kaggle/input/nail-disease-dataset-medsiglip` (or similar, adjust path in notebook if needed).
3. **Hugging Face Token**:
   - You need a Hugging Face account and an access token.
   - Accept the terms for `google/medsiglip-448` on Hugging Face.
   - Enter your token when prompted during the notebook execution.
4. **GPU Accelerator**: Ensure you select **GPU P100** or **GPU T4 x2** in the notebook settings for efficient training.
5. **Run All**: Execute the cells to process data, tune hyperparameters, and train the model.

## 📊 Performance
The notebook includes built-in evaluation metrics:
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix Visualization
- Training & Validation Loss Curves

---
*Note: This project focuses on accessibility and edge deployment, aiming to bring expert-level dermatology to mobile devices.*
