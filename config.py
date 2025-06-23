import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HUGGING_FACE_API = os.getenv("HUGGING_FACE_API")


if HUGGING_FACE_API:
    print("API Key loaded successfully from .env!")
else:
    print("WARNING: API Key not loaded. Check your .env file.")


if GEMINI_API_KEY:
    print("API Key loaded successfully from .env!")
else:
    print("WARNING: API Key not loaded. Check your .env file.")


TEXT_MODEL_NAME = "models/gemini-1.5-flash"
# TEXT_MODEL_NAME = "models/gemini-1.0-pro"
VISION_MODEL_NAME = "models/gemini-1.5-flash"
IMAGEN_MODEL_NAME = "models/gemini-2.0-flash-preview-image-generation"
# IMAGEN_MODEL_NAME = "models/imagen-3.0-generate-002"
# TEXT_MODEL_NAME = "gemini-pro"
# VISION_MODEL_NAME = "gemini-pro-vision"

MAX_RESPONSE_TOKENS = 800
TEMPERATURE = 0.9
TOP_P = 1.0
TOP_K= 1

# CLIENT_OPTIONS = {'api_endpoint': 'https://generativelanguage.googleapis.com'}
