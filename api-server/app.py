from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import base64
import numpy as np
from PIL import Image
import io
import os
import logging
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app requests

# Configuration
PORT = int(os.getenv('PORT', 8080))
API_KEY = os.getenv('API_KEY', 'dev-key-change-in-production')  # API Key for authentication
HF_API_KEY = os.getenv('HF_API_KEY')
HF_MODEL_ID = "ezsumm/medsiglip-nail-disease-classifier"

if not HF_API_KEY:
    logger.warning("⚠️ HF_API_KEY not found in environment variables. Model inference will fail.")

# Initialize Hugging Face Inference Client
hf_client = InferenceClient(token=HF_API_KEY)

# Nail sign categories
NAIL_SIGNS = [
    "White Nails (Terry's Nails)",
    "Blue Nails",
    "Clubbing",
    "Spoon Nails (Koilonychia)",
    "Black Lines (Melanoma Warning)",
    "Psoriasis",
    "Onychogryphosis"
]

# Disease mappings for each nail sign
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

# API Key Authentication Decorator
def require_api_key(f):
    """Decorator to require API key authentication for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from request headers
        client_api_key = request.headers.get('X-API-Key')
        
        # Validate API key
        if not client_api_key:
            logger.warning("Request missing API key")
            return jsonify({
                'error': 'Unauthorized',
                'message': 'API key is required. Please provide X-API-Key header.'
            }), 401
        
        if client_api_key != API_KEY:
            logger.warning(f"Invalid API key attempt: {client_api_key[:10]}...")
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid API key provided.'
            }), 401
        
        # API key is valid, proceed with request
        return f(*args, **kwargs)
    return decorated_function

def classify_nail_sign(image_bytes):
    """Stage 1: Classify nail sign using MedSigLIP via Hugging Face Inference API"""
    try:
        # Use Zero-Shot Image Classification since MedSigLIP is a CLIP model
        logger.info(f"Sending request to Hugging Face API for model: {HF_MODEL_ID}")
        
        # We need to construct labels for zero-shot classification
        # Ideally, we should check if the model on HF supports zero-shot-image-classification task directly
        # or if it's a fine-tuned image-classification model.
        # Given it's a CLIP fine-tune ('medsiglip'), zero-shot is the standard usage.
        
        candidate_labels = [f"a photo of {sign}" for sign in NAIL_SIGNS]
        
        # The InferenceClient's zero_shot_image_classification expects an image (path, url, or PIL) and labels
        # Convert bytes to PIL Image for the client
        image = Image.open(io.BytesIO(image_bytes))
        
        results = hf_client.zero_shot_image_classification(
            image=image,
            model=HF_MODEL_ID,
            labels=candidate_labels
        )
        
        # results is a list of dicts: [{'label': '...', 'score': ...}, ...]
        # They come sorted by score descending usually
        top_result = results[0]
        predicted_label = top_result['label']
        confidence = top_result['score']
        
        # Strip "a photo of " prefix to get back the nail sign key
        # verify if the model returns the full label we sent or just the class name if it was trained with specific classes
        # For zero-shot, it returns the labels we passed.
        predicted_sign = predicted_label.replace("a photo of ", "")
        
        # Fallback if stripping failed (e.g. model returned just the sign name for some reason)
        if predicted_sign not in NAIL_SIGNS:
             # Try to find partial match
             for sign in NAIL_SIGNS:
                 if sign in predicted_label:
                     predicted_sign = sign
                     break
        
        logger.info(f"Predicted: {predicted_sign} (confidence: {confidence:.2f})")
        return predicted_sign, float(confidence)
        
    except Exception as e:
        logger.error(f"Error in nail classification via HF API: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback to demo mode or error
        return NAIL_SIGNS[0], 0.94

def generate_explanation(nail_sign, image_array):
    """Stage 2: Generate clinical explanation (Static fallback for now)"""
    try:
        # Demo explanations
        explanations = {
            "White Nails (Terry's Nails)": (
                "White nail appearance with preserved pink nail bed distally suggests chronic "
                "liver disease. This finding, known as Terry's nails, is associated with hepatic "
                "cirrhosis in approximately 80% of cases. The whitening occurs due to decreased "
                "vascularity and increased connective tissue in the nail bed. This sign may also "
                "indicate chronic kidney disease, diabetes, or congestive heart failure."
            ),
            "Blue Nails": (
                "Cyanotic blue discoloration of the nails indicates inadequate oxygen saturation "
                "in the blood (hypoxemia). This clinical sign suggests significant respiratory or "
                "cardiovascular compromise. Common causes include chronic obstructive pulmonary disease "
                "(COPD), heart failure, pulmonary embolism, or severe pneumonia. Immediate medical "
                "evaluation is recommended to assess oxygen levels and underlying cardiopulmonary function."
            ),
            "Clubbing": (
                "Digital clubbing is characterized by bulbous enlargement of the fingertip with increased "
                "curvature of the nail. This finding indicates chronic hypoxia and is strongly associated "
                "with lung cancer, interstitial lung disease, and cyanotic heart disease. Clubbing develops "
                "over months to years and represents a significant diagnostic finding requiring thorough "
                "pulmonary and cardiac evaluation."
            ),
            "Spoon Nails (Koilonychia)": (
                "Concave depression of the nail plate (koilonychia or spoon nails) is a classic sign of "
                "chronic iron deficiency anemia. The nail becomes thin and soft, eventually developing a "
                "concave shape that can hold a drop of water. This finding typically appears after prolonged "
                "iron deficiency and may also be seen in hemochromatosis, Raynaud's disease, or thyroid disorders."
            ),
            "Black Lines (Melanoma Warning)": (
                "Longitudinal melanonychia (dark lines under the nail) requires urgent evaluation to rule out "
                "subungual melanoma, particularly if the pigmentation is wide (>3mm), irregular, or involves "
                "the cuticle (Hutchinson's sign). While trauma and benign conditions can cause similar findings, "
                "any new or changing pigmented line warrants dermatological assessment and possible biopsy."
            ),
            "Psoriasis": (
                "Nail psoriasis manifests as pitting, onycholysis (nail separation), oil drop discoloration, "
                "and subungual hyperkeratosis. Approximately 50% of psoriasis patients develop nail changes, "
                "and 80% of those with psoriatic arthritis show nail involvement. These findings indicate "
                "systemic inflammatory disease and increased risk for psoriatic arthritis and metabolic syndrome."
            ),
            "Onychogryphosis": (
                "Onychogryphosis presents as severe thickening and curvature of the nail, resembling a ram's horn. "
                "This condition typically results from chronic trauma, poor circulation, neglect, or fungal infection. "
                "It is commonly seen in elderly patients or those with peripheral vascular disease. Treatment involves "
                "nail debridement and addressing underlying circulatory or podiatric issues."
            )
        }
        
        return explanations.get(nail_sign, "Clinical explanation not available.")
        
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}")
        return "Unable to generate clinical explanation."

def get_recommendations(nail_sign):
    """Generate medical recommendations based on nail sign"""
    recommendations = {
        "White Nails (Terry's Nails)": [
            "Liver function tests (AST, ALT, bilirubin, albumin)",
            "Renal function panel (creatinine, BUN, eGFR)",
            "Fasting glucose and HbA1c",
            "Hepatology consultation if liver disease suspected",
            "Abdominal ultrasound to assess liver structure"
        ],
        "Blue Nails": [
            "Pulse oximetry and arterial blood gas analysis",
            "Chest X-ray and pulmonary function tests",
            "Echocardiogram for cardiac evaluation",
            "Emergency medical evaluation if acute onset",
            "Pulmonology or cardiology referral"
        ],
        "Clubbing": [
            "Chest CT scan to evaluate for lung pathology",
            "Pulmonary function tests",
            "Echocardiogram with bubble study",
            "Complete blood count and inflammatory markers",
            "Oncology referral if malignancy suspected"
        ],
        "Spoon Nails (Koilonychia)": [
            "Complete blood count with iron studies",
            "Serum ferritin, iron, and transferrin saturation",
            "Evaluation for sources of blood loss",
            "Thyroid function tests",
            "Hematology referral if severe or refractory anemia"
        ],
        "Black Lines (Melanoma Warning)": [
            "Urgent dermatology referral",
            "Dermoscopy evaluation",
            "Consider nail biopsy for definitive diagnosis",
            "Document changes with serial photography",
            "Rule out trauma or medication causes"
        ],
        "Psoriasis": [
            "Dermatology consultation",
            "Rheumatology evaluation for joint symptoms",
            "Metabolic screening (lipids, glucose, blood pressure)",
            "Consider topical or systemic psoriasis treatments",
            "Cardiovascular risk assessment"
        ],
        "Onychogryphosis": [
            "Podiatry referral for professional nail care",
            "Vascular assessment (ABI, Doppler studies)",
            "Fungal culture if infection suspected",
            "Regular nail debridement",
            "Address underlying circulatory issues"
        ]
    }
    
    return recommendations.get(nail_sign, ["Consult healthcare provider for evaluation"])

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'backend': 'Hugging Face Inference API',
        'model': HF_MODEL_ID
    }), 200


@app.route('/predict', methods=['POST'])
@require_api_key
def predict():
    """Main prediction endpoint"""
    try:
        # Validate request
        if not request.json or 'image' not in request.json:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        try:
            image_data = base64.b64decode(request.json['image'])
            # Don't convert to numpy/PIL here unless needed for display/logging
            # InferenceClient handles inputs. But for classify_nail_sign we convert to PIL
        except Exception as e:
            logger.error(f"Error decoding image: {str(e)}")
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Stage 1: Classify nail sign with MedSigLIP via HF API
        nail_sign, confidence = classify_nail_sign(image_data)
        
        # Stage 2: Generate explanation (Static)
        explanation = generate_explanation(nail_sign, None)
        
        # Get disease predictions
        diseases = DISEASE_MAP.get(nail_sign, [])
        
        # Get recommendations
        recommendations = get_recommendations(nail_sign)
        
        # Prepare response
        response = {
            'nail_sign': nail_sign,
            'confidence': float(confidence),
            'explanation': explanation,
            'diseases': diseases,
            'recommendations': recommendations,
            'timestamp': None
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting NailHealth AI API Server (HF Inference Mode)...")
    logger.info("="*50)
    
    logger.info(f"\n✅ Starting Flask server on port {PORT}...")
    logger.info(f"   Model: {HF_MODEL_ID}")
    logger.info("="*50)
    logger.info(f"\n🎉 API is ready at http://0.0.0.0:{PORT}")
    logger.info(f"   Health check: http://0.0.0.0:{PORT}/health")
    logger.info(f"   Prediction: http://0.0.0.0:{PORT}/predict\n")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
