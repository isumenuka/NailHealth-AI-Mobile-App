# MedGemma Fine-Tuning Pipeline for Nail Disease Clinical Assessment

This repository contains a two-stage fine-tuning pipeline for Google's **MedGemma** model, designed to transform it into an expert clinical assistant for nail disease assessment. The pipeline uses a text-only dataset of patient cases to train the model to output structured JSON assessments.

## 📂 Repository Contents

| File | Description |
|---|---|
| `medgemma_kaggle_finetuning.ipynb` | **Phase 1: Supervised Fine-Tuning (SFT)**<br>Initial training to teach the model the JSON format and general clinical knowledge using the dataset. |
| `medgemma4b_naildisease_grpo_finetuning_kaggle.ipynb` | **Phase 2: Reinforcement Learning (GRPO)**<br>Optimization phase using Group Relative Policy Optimization to align the model with specific reward functions (e.g., correct JSON syntax, accurate worry scores, medical priority). |
| `README.md` | This documentation file. |

## 🚀 Pipeline Overview

### Phase 1: Supervised Fine-Tuning (SFT)
**Notebook:** `medgemma_kaggle_finetuning.ipynb`

- **Goal:** Train the base MedGemma model to understand the patient input format and generate the required JSON structure.
- **Method:** QLoRA (4-bit quantization) with the `SFTTrainer`.
- **Input:** Patient demographics (age, gender), diagnosed condition, visual features, and symptoms.
- **Output:** structured JSON object containing:
    - `worry_score` (0-100)
    - `medical_priority` (Low/Medium/High)
    - `follow_up_required` (Yes/No)
    - `care_category` and `recommended_next_step`
    - `likely_causes` explanation

### Phase 2: GRPO Reinforcement Learning
**Notebook:** `medgemma4b_naildisease_grpo_finetuning_kaggle.ipynb`

- **Goal:** Refine the SFT model to maximize specific "rewards" or quality metrics.
- **Method:** Group Relative Policy Optimization (GRPO).
- **Rewards:**
    1.  `json_format_reward`: Ensures valid, parseable JSON output.
    2.  `worry_score_reward`: Penalizes deviations from the true worry score.
    3.  `priority_reward`: Rewards correct medical priority classification.
    4.  `followup_reward`: Rewards correct follow-up decisions.
    5.  `care_nextstep_reward`: Rewards correct care and next step recommendations.

## 🛠️ Usage

This pipeline is optimized for **Kaggle** or **Google Colab** environments with GPU support (T4 or better).

1.  **Run Phase 1**: Open `medgemma_kaggle_finetuning.ipynb`.
    -   Upload the dataset (`nail_disease_dataset.csv`).
    -   Execute all cells to train the SFT model.
    -   Save the adapter to Hugging Face or locally.

2.  **Run Phase 2**: Open `medgemma4b_naildisease_grpo_finetuning_kaggle.ipynb`.
    -   Update the `HF_SFT_MODEL` variable to point to your saved SFT model from Phase 1.
    -   Execute all cells to perform GRPO training.
    -   The final model will be highly aligned with the clinical assessment task.

## 📋 Dataset

The pipeline expects a CSV dataset (`nail_disease_dataset.csv`) with the following columns:
-   **Inputs:** `disease_name`, `age`, `age_group`, `gender`, `nail_visual_features`, `symptom_summary`
-   **Targets:** `worry_score`, `medical_priority`, `follow_up_required`, `care_category`, `recommended_next_step`, `likely_causes`

## ⚠️ Notes

-   **Hugging Face Token:** You will need a Hugging Face token with write access to push models to the Hub.
-   **Gemma License:** Ensure you have accepted the license for the MedGemma model on Hugging Face.
