import os
from dotenv import load_dotenv
from huggingface_hub import HfApi

load_dotenv()
api_token = os.getenv("HF_API_KEY")

api = HfApi(token=api_token)

print(f"Checking access with token: {api_token[:5]}...")

try:
    user = api.whoami()
    print(f"Authenticated as: {user['name']}")
except Exception as e:
    print(f"Authentication error: {e}")

TARGET_MODEL = "isumenuka/medsiglip-nail-disease-classifier"

print(f"\n--- Checking Model {TARGET_MODEL} ---")
try:
    model_info = api.model_info(TARGET_MODEL)
    print(f"Model found!")
    print(f"Pipeline tag: {model_info.pipeline_tag}")
    print(f"Private: {model_info.private}")
    print(f"Siblings (files): {[s.rfilename for s in model_info.siblings]}")
    
    # Fetch config.json
    print("\n--- Config.json ---")
    from huggingface_hub import hf_hub_download
    import json
    config_path = hf_hub_download(repo_id=TARGET_MODEL, filename="config.json", token=api_token)
    # Fetch inference.py
    print("\n--- inference.py ---")
    inference_path = hf_hub_download(repo_id=TARGET_MODEL, filename="inference.py", token=api_token)
    with open(inference_path, 'r') as f:
        print(f.read())

except Exception as e:
    print(f"Error fetching model info: {e}")
