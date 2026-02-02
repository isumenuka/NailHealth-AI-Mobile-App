from transformers import AutoModel, AutoProcessor
import os

model_name = "flaviagiammarino/pubmed-clip-vit-base-patch32"
print(f"Downloading {model_name}...")
# This will download to the default cache directory (usually ~/.cache/huggingface)
AutoModel.from_pretrained(model_name)
AutoProcessor.from_pretrained(model_name)
print("Done! Model cached.")
