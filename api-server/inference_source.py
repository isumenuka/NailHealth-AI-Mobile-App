import torch
import torch.nn as nn
from transformers import AutoModel, AutoProcessor
from PIL import Image
import json

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

def load_model(model_path, device="cuda" if torch.cuda.is_available() else "cpu"):
    """Load the fine-tuned model"""
    # Load config
    with open(f"{model_path}/config.json", "r") as f:
        config = json.load(f)
    
    # Load processor
    processor = AutoProcessor.from_pretrained(model_path)
    
    # Load base MedSigLIP
    base_model = AutoModel.from_pretrained("google/medsiglip-448")
    
    # Recreate classifier
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
        nn.Linear(256, config["num_classes"])
    )
    
    # Create full model
    model = MedSigLIPClassifierSingleDevice(
        medsiglip_model=base_model,
        classifier_head=classifier,
        num_classes=config["num_classes"]
    )
    
    # Load trained weights
    checkpoint = torch.load(f"{model_path}/pytorch_model.bin", map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()
    
    return model, processor, config["class_names"]

def predict(image_path, model, processor, class_names, device="cuda" if torch.cuda.is_available() else "cpu"):
    """Make prediction on a single image"""
    # Load and preprocess image
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    pixel_values = inputs["pixel_values"].to(device)
    
    # Inference
    with torch.no_grad():
        logits = model(pixel_values)
        probs = torch.softmax(logits, dim=-1)
        pred_idx = probs.argmax(dim=-1).item()
        confidence = probs[0, pred_idx].item()
    
    return {
        "predicted_class": class_names[pred_idx],
        "confidence": confidence,
        "all_probabilities": {class_names[i]: probs[0, i].item() for i in range(len(class_names))}
    }

if __name__ == "__main__":
    # Example usage
    MODEL_PATH = "./medsiglip_nail_classifier_hf"
    IMAGE_PATH = "test_nail_image.jpg"
    
    print("Loading model...")
    model, processor, class_names = load_model(MODEL_PATH)
    
    print(f"Making prediction on {IMAGE_PATH}...")
    result = predict(IMAGE_PATH, model, processor, class_names)
    
    print(f"\nPrediction: {result['predicted_class']}")
    print(f"Confidence: {result['confidence']*100:.2f}%")
    print("\nAll probabilities:")
    for cls, prob in result['all_probabilities'].items():
        print(f"  {cls}: {prob*100:.2f}%")
