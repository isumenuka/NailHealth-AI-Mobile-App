from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import base64
import os
import logging
import requests
import io
from PIL import Image
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
HF_ENDPOINT_URL = os.getenv('HF_ENDPOINT_URL')

if not HF_API_KEY:
    logger.warning("⚠️ HF_API_KEY not found. Model access might fail.")
if not HF_ENDPOINT_URL:
    logger.warning("⚠️ HF_ENDPOINT_URL not found. Predictions will fail.")

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

def generate_explanation(nail_sign):
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
        'message': 'NailHealth AI API is running (HF Inference Endpoint Mode)',
        'endpoints': {'health': '/health', 'predict': '/predict'}
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'backend': 'Hugging Face Inference Endpoint',
        'endpoint_configured': bool(HF_ENDPOINT_URL)
    }), 200

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_key = request.headers.get('X-API-Key')
        if not client_key or client_key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def query_hf_endpoint(image_bytes):
    """
    Sends image bytes to the Hugging Face Inference Endpoint.
    Expects the endpoint to return a list of dicts: [{'label': 'Label', 'score': 0.99}, ...]
    """
    if not HF_ENDPOINT_URL:
        raise ValueError("HF_ENDPOINT_URL is not set.")

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/octet-stream"
    }

    try:
        response = requests.post(HF_ENDPOINT_URL, headers=headers, data=image_bytes)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"HF Endpoint Request Failed: {e}")
        if e.response is not None:
             logger.error(f"HF Endpoint Response: {e.response.text}")
        raise e

@app.route('/predict', methods=['POST'])
@require_api_key
def predict():
    try:
        if not request.json or 'image' not in request.json:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image from client
        image_data = base64.b64decode(request.json['image'])
        
        # Verify it's a valid image (optional consistency check)
        try:
            Image.open(io.BytesIO(image_data)).verify()
        except Exception:
            return jsonify({'error': 'Invalid image data'}), 400

        # Query Hugging Face Endpoint
        # We send the raw bytes directly
        hf_response = query_hf_endpoint(image_data)
        
        # Log response for debugging
        logger.info(f"HF Response: {hf_response}")

        # Parse Response
        # Expected format: [{'label': 'Class Name', 'score': 0.95}, ...]
        # We assume the endpoint returns sorted results or we sort them
        if isinstance(hf_response, list) and len(hf_response) > 0:
            # Sort by score just in case
            sorted_predictions = sorted(hf_response, key=lambda x: x['score'], reverse=True)
            top_prediction = sorted_predictions[0]
            
            predicted_sign = top_prediction['label']
            confidence = top_prediction['score']
        elif isinstance(hf_response, dict) and 'error' in hf_response:
             raise Exception(f"HF Endpoint Error: {hf_response['error']}")
        else:
            raise Exception(f"Unexpected response format from HF Endpoint: {hf_response}")

        logger.info(f"Prediction: {predicted_sign} ({confidence:.2f})")
        
        # Response Construction (Matching original API format)
        response = {
            'nail_sign': predicted_sign,
            'confidence': float(confidence),
            'explanation': generate_explanation(predicted_sign),
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
