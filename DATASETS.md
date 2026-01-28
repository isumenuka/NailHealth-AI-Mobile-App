# 📄 Dataset Information

## Overview

This project uses 7 nail disease categories from publicly available medical image datasets. The model is trained on images from multiple sources to ensure diversity and robustness.

---

## Dataset Folder Structure

```
data/
├── train/                    (80% of images)
│   ├── Acral_Lentiginous_Melanoma/  (~300 images)
│   ├── blue_finger/                 (~200 images)
│   ├── clubbing/                    (~350 images)
│   ├── Healthy_Nail/                (~400 images)
│   ├── Onychogryphosis/             (~250 images)
│   ├── pitting/                     (~350 images)
│   ├── psoriasis/                   (~300 images)
│   └── Total: ~2,150 images
└── test/                     (20% of images)
    ├── Acral_Lentiginous_Melanoma/  (~75 images)
    ├── blue_finger/                 (~50 images)
    ├── clubbing/                    (~87 images)
    ├── Healthy_Nail/                (~100 images)
    ├── Onychogryphosis/             (~62 images)
    ├── pitting/                     (~87 images)
    ├── psoriasis/                   (~75 images)
    └── Total: ~536 images
```

**Total dataset: ~2,700 nail images**

---

## Data Sources

### Primary Datasets (7,573+ images)

#### 1. 🜟 Nail Disease Detection Dataset
- **Source**: [Kaggle - Nikhil Gurav](https://www.kaggle.com/datasets/nikhilgurav21/nail-disease-detection-dataset)
- **Size**: 67 MB
- **Images**: 3,835 files
- **Conditions**: ALM, Healthy, Onychogryphosis, Blue Nails, Clubbing, Pitting
- **Download**:
  ```bash
  kaggle datasets download -d nikhilgurav21/nail-disease-detection-dataset
  ```

#### 2. Nail Disease Image Classification Dataset
- **Source**: [Kaggle - Joseph Rasanjana](https://www.kaggle.com/datasets/josephrasanjana/nail-disease-image-classification-dataset)
- **Size**: 125 MB
- **Images**: 1,466 files
- **Quality**: Classified by specialists
- **Download**:
  ```bash
  kaggle datasets download -d josephrasanjana/nail-disease-image-classification-dataset
  ```

#### 3. Nail Disease Dataset (Whale)
- **Source**: [Kaggle - Whaleeeeee](https://www.kaggle.com/datasets/whaleeeeee/nail-disease)
- **Size**: 11 MB
- **Images**: 1,432 files
- **Breakdown**: ALM (370), Healthy (358), Clubbing (375), Pitting (329)
- **Download**:
  ```bash
  kaggle datasets download -d whaleeeeee/nail-disease
  ```

#### 4. HP Nail Images for Early Disease Detection
- **Source**: [Kaggle - Sumit Agrawal](https://www.kaggle.com/datasets/sumitagrawal/hp-nail-images-for-early-disease-detection)
- **Size**: 52 MB
- **Images**: 840 files
- **Quality**: High precision, early-stage indicators
- **Download**:
  ```bash
  kaggle datasets download -d sumitagrawal/hp-nail-images-for-early-disease-detection
  ```

---

## Supplementary Datasets (Optional)

### 5. Nail Psoriasis Dataset
- **Source**: [Mendeley Data](https://data.mendeley.com/datasets/3hckgznc67)
- **Images**: 2,520 nail psoriasis images
- **Format**: High-resolution dermatoscopic images
- **Use**: Augment psoriasis class

### 6. SCIN (Skin Condition Image Network)
- **Source**: [Google Research](https://research.google.com/blog/scin-a-new-resource-for-representative-dermatology-images/)
- **Images**: 10,000+ diverse skin/nail images
- **Quality**: Real-world diversity, balanced demographics
- **Use**: Validation and diversity augmentation

### 7. HAM10000 (Transfer Learning)
- **Source**: [Kaggle](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)
- **Images**: 10,015 dermatoscopic images
- **Use**: Pre-training or transfer learning

---

## Class Definitions

### 1. 💇 Acral Lentiginous Melanoma (ALM)
**Medical Definition**: Subungual melanoma with longitudinal pigmentation

**Characteristics**:
- Black/brown vertical bands under the nail
- Uneven pigmentation
- Can be cancerous
- Most common form of nail melanoma

**Clinical Importance**: ⚠️ **HIGH PRIORITY** - Requires immediate medical attention

**Images**: 300-370 per dataset

### 2. 👵 Blue Finger (Blue Nails)
**Medical Definition**: Cyanotic nails due to poor oxygenation

**Characteristics**:
- Blue/purple discoloration of nail bed
- Indicates circulatory or respiratory issues
- Often associated with: heart disease, lung disease, high altitude
- Reversible if underlying condition is treated

**Clinical Importance**: 🔴 **MEDIUM-HIGH** - Indicates underlying health issue

**Images**: 200-300 per dataset

### 3. 💈 Clubbing
**Medical Definition**: Bulbous enlargement of fingers/nail bed

**Characteristics**:
- Loss of nail angle (>180°)
- Spongy, bulbous nail bed
- Associated with: COPD, cystic fibrosis, heart disease
- Can be congenital or acquired

**Clinical Importance**: 🔴 **MEDIUM-HIGH** - Indicates systemic disease

**Images**: 350-375 per dataset

### 4. 💅 Healthy Nail
**Medical Definition**: Normal nail anatomy and coloration

**Characteristics**:
- Smooth, uniform color
- Healthy nail bed
- Slight curvature at tip
- No discoloration or deformity
- Reference/control group

**Clinical Importance**: ✅ **Baseline** - Normal appearance

**Images**: 350-400 per dataset

### 5. 🛠 Onychogryphosis
**Medical Definition**: Extreme thickening and curvature of nail

**Characteristics**:
- Thickened nail (>3mm)
- Ram's horn-like appearance
- Difficult to cut
- Associated with: aging, fungi, trauma, psoriasis
- Can cause pain

**Clinical Importance**: 🔴 **MEDIUM** - Affects quality of life, may indicate fungal infection

**Images**: 250-300 per dataset

### 6. 📄 Pitting
**Medical Definition**: Small depressions in nail plate surface

**Characteristics**:
- Multiple small holes/dots in nail
- Associated with: psoriasis, alopecia areata, eczema
- Non-scars (nail grows out)
- Cosmetically concerning

**Clinical Importance**: 🔴 **MEDIUM** - Sign of inflammatory dermatosis

**Images**: 300-350 per dataset

### 7. 💚 Psoriasis
**Medical Definition**: Nail involvement in psoriatic disease

**Characteristics**:
- Pitting (most common)
- Onycholysis (nail separation)
- Discoloration ("oil spot")
- Nail thickening
- Subungual hyperkeratosis

**Clinical Importance**: 🔴 **MEDIUM** - Indicates systemic psoriasis

**Images**: 300-350 per dataset

---

## Data Quality Standards

All images in this dataset meet the following criteria:

- ✅ Minimum resolution: 224x224 pixels (resizable to 448x448)
- ✅ Format: JPEG, PNG
- ✅ Clear visibility of nail bed and plate
- ✅ Proper lighting and exposure
- ✅ Single nail per image (usually)
- ✅ Dermatologist-reviewed or clinically verified
- ✅ De-identified (no patient data)

---

## Usage Rights

All datasets are available under **open-access licenses**:

- Kaggle Datasets: Free to use
- Mendeley Data: Creative Commons or CC0
- Google SCIN: Google Research license

**Always cite the original sources in your work!**

---

## Data Preparation Pipeline

### Step 1: Download
```bash
# Use the provided quick start scripts
./download_datasets.sh
```

### Step 2: Extract
```bash
find . -name "*.zip" -exec unzip {} \;
```

### Step 3: Organize
```bash
python organize_data.py
```

### Step 4: Validate
```bash
python validate_data.py
```

---

## Statistics

### Class Distribution
```
Acral_Lentiginous_Melanoma:  375 images (13.9%)
blue_finger:                 250 images (9.3%)
clubbing:                    437 images (16.2%)
Healthy_Nail:                500 images (18.5%)
Onychogryphosis:             312 images (11.5%)
pitting:                     437 images (16.2%)
psoriasis:                   375 images (13.9%)

Total:                       2,686 images (100%)
```

### Image Statistics
```
Average resolution:  Variable (prep to 448x448)
Color space:         RGB
File formats:        JPEG (90%), PNG (10%)
Total size:          ~1.2 GB (uncompressed)
```

---

## Citation

If you use these datasets, please cite:

```bibtex
@dataset{nail_disease_kaggle,
  title={Nail Disease Detection Dataset},
  author={Gurav, Nikhil},
  year={2024},
  url={https://www.kaggle.com/datasets/nikhilgurav21/nail-disease-detection-dataset}
}

@dataset{nail_disease_classification,
  title={Nail Disease Image Classification Dataset},
  author={Rasanjana, Joseph},
  year={2024},
  url={https://www.kaggle.com/datasets/josephrasanjana/nail-disease-image-classification-dataset}
}

@dataset{mendeley_nail_psoriasis,
  title={Skin Disease Classification Dataset},
  author={Agrawal, Sumita},
  year={2024},
  url={https://data.mendeley.com/datasets/3hckgznc67}
}
```

---

## Privacy & Ethics

✅ All images are de-identified
✅ No personal health information included
✅ Available for research and educational use
✅ Commercial use allowed (check individual licenses)
✅ Diverse representation across skin tones

---

## Issues?

If you encounter:
- **Missing files**: Check folder structure matches expected layout
- **Corrupted images**: Remove and re-download from source
- **License questions**: Contact dataset authors directly
- **Dataset errors**: Report to Kaggle/Mendeley

---

**Last Updated**: January 28, 2026
**Total Images**: 2,686+
**Classes**: 7
**Format**: JPEG/PNG
**Status**: Ready for Training ✅
