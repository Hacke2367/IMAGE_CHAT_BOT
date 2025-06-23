import requests
from PIL import Image
import io
from config import HUGGING_FACE_API


model_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {HUGGING_FACE_API}"}
payload = {"inputs": "A majestic lion standing on a savannah at sunset, photorealistic"}

res = requests.post(model_url, headers=headers, json=payload)

if res.status_code == 200:
    image = Image.open(io.BytesIO(res.content))
    image.save("lion_sunset.png")
    print("✅ Image saved!")
else:
    print(f"❌ Failed! Status: {res.status_code}, Message: {res.text}")
