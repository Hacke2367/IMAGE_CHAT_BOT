from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv
import os
import logging
from PIL import Image
import io

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

configure(api_key=GEMINI_API_KEY)


class ChatbotSession:
    def __init__(self, model_name: str = "models/gemini-1.5-flash"):
        self.model = GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])
        logging.info(f"New multimodal chatbot session started with model: {model_name}")

    def send_message(self, prompt: str, image: Image.Image = None) -> str:
        try:
            if image:
                if image.mode != "RGB":
                    image = image.convert('RGB')

                response = self.model.generate_content([prompt, image])
                return response.text
            else:
                response = self.chat.send_message(prompt)
                return response.text

        except Exception as e:
            logging.error(f"Error in send_message: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    def get_history(self):
        return self.chat.history

    def reset_session(self):
        self.chat = self.model.start_chat(history=[])
        logging.info("Chatbot session reset.")


def initialize_gemini():
    try:
        model = GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content("Test connection")
        logging.info("Gemini API initialized successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to initialize Gemini API: {e}")
        return False