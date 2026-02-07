import os
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
import shutil

load_dotenv()
api_token = os.getenv("HF_API_KEY")
MODEL_ID = "isumenuka/medsiglip-nail-disease-classifier"

print(f"Downloading inference.py from {MODEL_ID}...")
file_path = hf_hub_download(repo_id=MODEL_ID, filename="inference.py", token=api_token)

shutil.copy(file_path, "inference_source.py")
print("Saved to inference_source.py")
