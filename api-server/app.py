from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import base64
import numpy as np
from PIL import Image
import io
import os
import logging
import json
import torch
import torch.nn as nn
from transformers import AutoModel, AutoProcessor
from huggingface_hub import snapshot_download
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
PORT = int(os.getenv('PORT', 8080))
API_KEY = os.getenv('API_KEY', 'dev-key-change-in-production')
HF_API_KEY = os.getenv('HF_API_KEY')
HF_MODEL_ID = "isumenuka/medsiglip-nail-disease-classifier"

if not HF_API_KEY:
    logger.warning("⚠️ HF_API_KEY not found. Model download might fail if repo is private.")

# --- Model Definition (Matched to inference.py) ---
class MedSigLIPClassifierSingleDevice(nn.Module):
    """Unified model for deployment"""
    def __init__(self, medsiglip_model, classifier_head, num_classes):
        super().__init__()
        self.medsiglip = medsiglip_model
        self.classifier = classifier_head
        self.num_classes = num_classes
        
    def forward(self, pixel_values):
        with torch.no_grad():
            outputs = self.medsiglip.vision_model(pixel_values=pixel_values)
            embeddings = outputs.pooler_output
        logits = self.classifier(embeddings.float())
        return logits

# --- Global Model Variables ---
model = None
processor = None
device = "cpu" # Force CPU for Cloud Run unless GPU is available
class_names = []

def load_local_model():
    global model, processor, class_names, device
    try:
        logger.info(f"⬇️ Downloading model snapshot from {HF_MODEL_ID}...")
        model_path = snapshot_download(repo_id=HF_MODEL_ID, token=HF_API_KEY)
        logger.info(f"✅ Model downloaded to {model_path}")

        # Load config
        with open(f"{model_path}/config.json", "r") as f:
            config = json.load(f)
        
        class_names = config.get("class_names", [])
        num_classes = config.get("num_classes", len(class_names))

        logger.info("loading processor...")
        processor = AutoProcessor.from_pretrained(model_path)
        
        logger.info("loading base model (google/medsiglip-448)...")
        base_model = AutoModel.from_pretrained("google/medsiglip-448")
        
        # Recreate classifier structure (Exact copy from inference.py)
        classifier = nn.Sequential(
            nn.Linear(1152, 768),
            nn.LayerNorm(768),
            nn.GELU(),
            nn.Dropout(0.4),
            nn.Linear(768, 512),
            nn.LayerNorm(512),
            nn.GELU(),
            nn.Dropout(0.4),
            nn.Linear(512, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
        
        logger.info("Assembling full model...")
        model = MedSigLIPClassifierSingleDevice(
            medsiglip_model=base_model,
            classifier_head=classifier,
            num_classes=num_classes
        )
        
        # Load weights
        weights_path = f"{model_path}/pytorch_model.bin"
        logger.info(f"Loading weights from {weights_path}...")
        checkpoint = torch.load(weights_path, map_location=device)
        
        # Handle state dict key mismatch if necessary (usually strict=False helps inside load_state_dict if keys match)
        # inference.py used: checkpoint["model_state_dict"]
        if "model_state_dict" in checkpoint:
            model.load_state_dict(checkpoint["model_state_dict"])
        else:
            model.load_state_dict(checkpoint)
            
        model.to(device)
        model.eval()
        logger.info("🎉 Model loaded successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        raise e

# Load model at startup
with app.app_context():
    load_local_model()

# --- Clinical Knowledge Base ---
DISEASE_MAP = {
    "White Nails (Terry's Nails)": [
        {"name": "Liver Cirrhosis", "confidence": 0.94},
        {"name": "Chronic Kidney Disease", "confidence": 0.82},
        {"name": "Type 2 Diabetes", "confidence": 0.68}
    ],
    "Blue Nails": [
        {"name": "Chronic Obstructive Pulmonary Disease (COPD)", "confidence": 0.91},
        {"name": "Heart Failure", "confidence": 0.85},
        {"name": "Pulmonary Embolism", "confidence": 0.72}
    ],
    "Clubbing": [
        {"name": "Lung Cancer", "confidence": 0.88},
        {"name": "Interstitial Pulmonary Fibrosis", "confidence": 0.83},
        {"name": "Congenital Heart Disease", "confidence": 0.76}
    ],
    "Spoon Nails (Koilonychia)": [
        {"name": "Iron Deficiency Anemia", "confidence": 0.93},
        {"name": "Hemochromatosis", "confidence": 0.71},
        {"name": "Raynaud's Disease", "confidence": 0.64}
    ],
    "Black Lines (Melanoma Warning)": [
        {"name": "Subungual Melanoma", "confidence": 0.89},
        {"name": "Bacterial Endocarditis", "confidence": 0.74},
        {"name": "Trauma-related Hemorrhage", "confidence": 0.62}
    ],
    "Psoriasis": [
        {"name": "Psoriatic Arthritis", "confidence": 0.87},
        {"name": "Metabolic Syndrome", "confidence": 0.69},
        {"name": "Cardiovascular Disease Risk", "confidence": 0.58}
    ],
    "Onychogryphosis": [
        {"name": "Poor Peripheral Circulation", "confidence": 0.81},
        {"name": "Fungal Infection (Onychomycosis)", "confidence": 0.78},
        {"name": "Chronic Trauma", "confidence": 0.65}
    ]
}

def generate_explanation(nail_sign, image_array):
    explanations = {
        "White Nails (Terry's Nails)": "White nail appearance with preserved pink nail bed distally suggests chronic liver disease.",
        "Blue Nails": "Cyanotic blue discoloration indicates inadequate oxygen saturation (hypoxemia).",
        "Clubbing": "Digital clubbing is characterized by bulbous enlargement of the fingertip, often linked to lung/heart issues.",
        "Spoon Nails (Koilonychia)": "Concave depression of the nail plate is a classic sign of iron deficiency anemia.",
        "Black Lines (Melanoma Warning)": "Longitudinal melanonychia requires urgent evaluation to rule out subungual melanoma.",
        "Psoriasis": "Nail psoriasis manifests as pitting and onycholysis, often indicating systemic inflammatory disease.",
        "Onychogryphosis": "Severe thickening and curvature of the nail, typically from chronic trauma or poor circulation."
    }
    return explanations.get(nail_sign, "Clinical explanation not available.")

def get_recommendations(nail_sign):
    recommendations = {
        "White Nails (Terry's Nails)": ["Liver function tests", "Renal function panel", "Abdominal ultrasound"],
        "Blue Nails": ["Pulse oximetry", "Chest X-ray", "Cardiology referral"],
        "Clubbing": ["Chest CT scan", "Pulmonary function tests", "Echocardiogram"],
        "Spoon Nails (Koilonychia)": ["Iron studies", "Complete blood count", "Thyroid tests"],
        "Black Lines (Melanoma Warning)": ["Urgent dermatology referral", "Dermoscopy", "Biopsy"],
        "Psoriasis": ["Dermatology consultation", "Rheumatology evaluation", "Metabolic screening"],
        "Onychogryphosis": ["Podiatry referral", "Vascular assessment", "Regular debridement"]
    }
    return recommendations.get(nail_sign, ["Consult healthcare provider."])

# --- Endpoints ---

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'online',
        'message': 'NailHealth AI API is running (Local Inference Mode)',
        'model': HF_MODEL_ID,
        'endpoints': {'health': '/health', 'predict': '/predict'}
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy' if model else 'loading',
        'backend': 'Local Inference (Container)',
        'model': HF_MODEL_ID
    }), 200

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_key = request.headers.get('X-API-Key')
        if not client_key or client_key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/predict', methods=['POST'])
@require_api_key
def predict():
    try:
        if not request.json or 'image' not in request.json:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode image
        image_bytes = base64.b64decode(request.json['image'])
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Preprocess
        inputs = processor(images=image, return_tensors="pt")
        pixel_values = inputs["pixel_values"].to(device)
        
        # Inference
        with torch.no_grad():
            logits = model(pixel_values)
            probs = torch.softmax(logits, dim=-1)
            pred_idx = probs.argmax(dim=-1).item()
            confidence = probs[0, pred_idx].item()
            
        predicted_sign = class_names[pred_idx]
        
        logger.info(f"Prediction: {predicted_sign} ({confidence:.2f})")
        
        # Response Construction
        response = {
            'nail_sign': predicted_sign,
            'confidence': float(confidence),
            'explanation': generate_explanation(predicted_sign, None),
            'diseases': DISEASE_MAP.get(predicted_sign, []),
            'recommendations': get_recommendations(predicted_sign),
            'timestamp': None
        }
        
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
