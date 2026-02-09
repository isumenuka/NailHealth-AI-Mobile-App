import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_ENDPOINT_URL = os.getenv("HF_ENDPOINT_URL")

print(f"Testing Endpoint: {HF_ENDPOINT_URL}")

if "your-endpoint-url-here" in HF_ENDPOINT_URL:
    print("❌ PLEASE UPDATE HF_ENDPOINT_URL IN .env FIRST!")
    exit(1)

# Create a dummy white image for testing
# (1x1 pixel white image encoded in base64)
dummy_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
image_bytes = base64.b64decode(dummy_image_b64)

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/octet-stream"
}

try:
    print("Sending request...")
    response = requests.post(HF_ENDPOINT_URL, headers=headers, data=image_bytes)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Endpoint is working!")
    else:
        print("❌ Endpoint returned an error.")

except Exception as e:
    print(f"❌ Error: {e}")
