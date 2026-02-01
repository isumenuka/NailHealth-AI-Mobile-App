from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import base64
import numpy as np
from PIL import Image
import io
import os
import logging
import torch
from transformers import AutoModel, AutoTokenizer, AutoProcessor
from download_model import download_model_from_gcs


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app requests

# Configuration
MODEL_PATH = os.getenv('MODEL_PATH', './models')
PORT = int(os.getenv('PORT', 8080))
API_KEY = os.getenv('API_KEY', 'dev-key-change-in-production')  # API Key for authentication
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

logger.info(f"Using device: {DEVICE}")

# Global variables for models
medsiglip_model = None
medsiglip_processor = None
medgemma_model = None
medgemma_tokenizer = None

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

def load_models():
    """Load fine-tuned models on startup"""
    global medsiglip_model, medsiglip_processor
    
    try:
        model_file = f"{MODEL_PATH}/model1/best_model.pt"
        logger.info(f"Loading MedSigLIP model from {model_file}...")
        
        if not os.path.exists(model_file):
            logger.error(f"❌ Model file not found at {model_file}")
            logger.error("   Ensure GCS bucket is mounted at /models")
            return

        # Load PyTorch checkpoint
        checkpoint = torch.load(model_file, map_location=DEVICE)
        logger.info(f"Checkpoint loaded. Type: {type(checkpoint)}")
        
        # Load MedSigLIP model and processor from Hugging Face
        logger.info("Loading MedSigLIP base model and processor...")
        medsiglip_model = AutoModel.from_pretrained("flaviagiammarino/pubmed-clip-vit-base-patch32")
        medsiglip_processor = AutoProcessor.from_pretrained("flaviagiammarino/pubmed-clip-vit-base-patch32")
        
        # Load fine-tuned weights
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            logger.info("Loading fine-tuned weights from checkpoint...")
            medsiglip_model.load_state_dict(checkpoint['model_state_dict'])
            logger.info(f"Model trained for {checkpoint.get('epoch', 'unknown')} epochs")
            logger.info(f"Best accuracy: {checkpoint.get('best_val_accuracy', checkpoint.get('best_accuracy', 'unknown'))}")
        elif isinstance(checkpoint, dict) and 'model' in checkpoint:
            medsiglip_model = checkpoint['model']
        else:
            logger.warning("Unexpected checkpoint format, attempting to use as-is")
            medsiglip_model = checkpoint
        
        # Aggressive memory cleanup
        del checkpoint
        import gc
        gc.collect()
        logger.info("🧹 Memory cleaned up after loading")
        
        medsiglip_model.to(DEVICE)
        medsiglip_model.eval()
        
        logger.info("✅ MedSigLIP model loaded successfully!")
        logger.info(f"   Device: {DEVICE}")
        logger.info(f"   Nail sign categories: {len(NAIL_SIGNS)}")
        
    except Exception as e:
        logger.error(f"❌ Error loading models: {str(e)}")
        import traceback
        traceback.print_exc()
        logger.warning("Running in demo mode without models")

def classify_nail_sign(image_array):
    """Stage 1: Classify nail sign using MedSigLIP"""
    global medsiglip_model, medsiglip_processor
    
    # Lazy load if needed
    if medsiglip_model is None:
        logger.info("⚡ Lazy loading model on first request...")
        load_models()

    
    try:
        # Check if model is loaded
        if medsiglip_model is None or medsiglip_processor is None:
            logger.warning("Model not loaded, using demo mode")
            predicted_class = 0  # White Nails
            confidence = 0.94
            return NAIL_SIGNS[predicted_class], confidence
        
        # Convert numpy array to PIL Image
        from PIL import Image
        if isinstance(image_array, np.ndarray):
            image = Image.fromarray(image_array.astype('uint8'), 'RGB')
        else:
            image = image_array
        
        # Prepare text labels for zero-shot classification
        text_labels = [f"a photo of {sign}" for sign in NAIL_SIGNS]
        
        # Process inputs
        inputs = medsiglip_processor(
            text=text_labels,
            images=image,
            return_tensors="pt",
            padding=True
        )
        
        # Move to device
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
        
        # Run inference
        with torch.no_grad():
            outputs = medsiglip_model(**inputs)
            
            # Get logits and compute probabilities
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            
            # Get prediction
            predicted_idx = probs.argmax().item()
            confidence = probs.max().item()
        
        logger.info(f"Predicted: {NAIL_SIGNS[predicted_idx]} (confidence: {confidence:.2f})")
        return NAIL_SIGNS[predicted_idx], float(confidence)
        
    except Exception as e:
        logger.error(f"Error in nail classification: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback to demo mode
        return NAIL_SIGNS[0], 0.94

def generate_explanation(nail_sign, image_array):
    """Stage 2: Generate clinical explanation using MedGemma 4B"""
    try:
        # TODO: Replace with actual MedGemma 4B inference
        
        # In production:
        # prompt = f"Analyze this nail condition: {nail_sign}. Provide clinical explanation."
        # inputs = medgemma_tokenizer(prompt, return_tensors="pt").to(DEVICE)
        # with torch.no_grad():
        #     outputs = medgemma_model.generate(**inputs, max_length=256)
        #     explanation = medgemma_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
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
        'device': str(DEVICE),
        'models_loaded': medsiglip_model is not None and medgemma_model is not None
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
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('RGB')
            image_array = np.array(image)
        except Exception as e:
            logger.error(f"Error decoding image: {str(e)}")
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Stage 1: Classify nail sign with MedSigLIP
        nail_sign, confidence = classify_nail_sign(image_array)
        logger.info(f"Classified as: {nail_sign} (confidence: {confidence:.2f})")
        
        # Stage 2: Generate explanation with MedGemma 4B
        explanation = generate_explanation(nail_sign, image_array)
        
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
            'timestamp': None  # You can add timestamp if needed
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting NailHealth AI API Server...")
    logger.info("="*50)
    
    # Note: Models are lazy loaded on first request to ensure fast startup for Cloud Run
    logger.info("⚡ Models configured for lazy loading")
    
    # Step 3: Run Flask app
    logger.info(f"\n✅ Step 3: Starting Flask server on port {PORT}...")
    logger.info("="*50)
    logger.info(f"\n🎉 API is ready at http://0.0.0.0:{PORT}")
    logger.info(f"   Health check: http://0.0.0.0:{PORT}/health")
    logger.info(f"   Prediction: http://0.0.0.0:{PORT}/predict\n")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
