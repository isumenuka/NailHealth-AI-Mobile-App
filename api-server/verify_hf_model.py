import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_ID = "isumenuka/medsiglip-nail-disease-classifier"

print(f"Checking model: {MODEL_ID}")
print(f"Using key: {HF_API_KEY[:5]}...")

api_url = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

try:
    response = requests.get(api_url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
