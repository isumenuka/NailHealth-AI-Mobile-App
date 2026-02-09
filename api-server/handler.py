from typing import Dict, List, Any
from transformers import AutoModel, AutoProcessor
import torch
import torch.nn as nn
from PIL import Image
import io
import base64
import numpy as np

class MedSigLIPClassifierSingleDevice(nn.Module):
    """Unified model for deployment"""
    def __init__(self, medsiglip_model, classifier_head, num_classes):
        super().__init__()
        self.medsiglip = medsiglip_model
        self.classifier = classifier_head
        self.num_classes = num_classes
        
    def forward(self, pixel_values):
        outputs = self.medsiglip.vision_model(pixel_values=pixel_values)
        embeddings = outputs.pooler_output
        logits = self.classifier(embeddings.float())
        return logits

class EndpointHandler:
    def __init__(self, path=""):
        # Load model and processor
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load processor
        self.processor = AutoProcessor.from_pretrained(path)
        
        # Load base model
        base_model = AutoModel.from_pretrained("google/medsiglip-448")
        
        # Define class names (hardcoded from your config to ensure consistency)
        self.class_names = [
            "White Nails (Terry's Nails)",
            "Blue Nails",
            "Clubbing",
            "Spoon Nails (Koilonychia)",
            "Black Lines (Melanoma Warning)",
            "Psoriasis",
            "Onychogryphosis"
        ]
        num_classes = len(self.class_names)

        # Recreate classifier structure
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
        
        # Assemble model
        self.model = MedSigLIPClassifierSingleDevice(
            medsiglip_model=base_model,
            classifier_head=classifier,
            num_classes=num_classes
        )
        
        # Load weights
        weights_path = f"{path}/pytorch_model.bin"
        checkpoint = torch.load(weights_path, map_location=self.device)
        
        if "model_state_dict" in checkpoint:
            self.model.load_state_dict(checkpoint["model_state_dict"])
        else:
            self.model.load_state_dict(checkpoint)
            
        self.model.to(self.device)
        self.model.eval()

    def __call__(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Args:
            data (:obj:):
                includes the input data and the parameters for the inference.
        """
        # Process Input
        inputs = data.pop("inputs", data)
        
        # Handle different input types (raw bytes, base64, PIL Image)
        if isinstance(inputs, Image.Image):
            image = inputs
        elif isinstance(inputs, bytes):
            image = Image.open(io.BytesIO(inputs))
        elif isinstance(inputs, str):
            # Try to decode base64 if it's a string
            try:
                if inputs.startswith("data:image"):
                    # Remove header if present
                    inputs = inputs.split(",")[1]
                image_bytes = base64.b64decode(inputs)
                image = Image.open(io.BytesIO(image_bytes))
            except:
                # Fallback: maybe it's a URL or path (not supported here for simplicity, assume b64 or raw)
                raise ValueError("Input string is not valid base64 image data.")
        else:
             raise ValueError(f"Unsupported input type: {type(inputs)}")

        image = image.convert("RGB")

        # Inference
        inputs = self.processor(images=image, return_tensors="pt")
        pixel_values = inputs["pixel_values"].to(self.device)
        
        with torch.no_grad():
            logits = self.model(pixel_values)
            probs = torch.softmax(logits, dim=-1)
            
        # Format Output
        # Return list of {label: str, score: float}
        scores = probs[0].cpu().numpy()
        result = [
            {"label": self.class_names[i], "score": float(scores[i])}
            for i in range(len(self.class_names))
        ]
        
        # Sort by score descending
        result.sort(key=lambda x: x["score"], reverse=True)
        
        return result
