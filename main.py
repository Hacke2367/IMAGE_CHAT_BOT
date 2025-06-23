import os
import sys
import logging
from PIL import Image
import io
import google.generativeai as genai


sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'core'))

from core.gemini_client import initialize_gemini, send_text_prompt, send_multimodal_prompt, ChatbotSession
from core.image_generation import generate_image_from_prompt
from config import TEXT_MODEL_NAME, VISION_MODEL_NAME, IMAGEN_MODEL_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_text_to_text():
    logging.info(f"\n--- Testing Text-to-Text Conversation with {TEXT_MODEL_NAME} ---")
    try:
        user_prompt = "Tell me a fun fact about Mumbai, India."
        print(f"You: {user_prompt}")
        response = send_text_prompt(user_prompt)
        print(f"Chatbot: {response}")
    except Exception as e:
        print(f"Error during text-to-text test: {e}")

def list_all_available_models():
    logging.info("\n--- Listing ALL Available Models for your API Key ---")
    try:
        found_imagen_model = False
        for m in genai.list_models():
            logging.info(f"  Model Name: {m.name}, Methods: {m.supported_generation_methods}")
            if "imagen" in m.name.lower() and 'generateContent' in m.supported_generation_methods:
                logging.info(f"    *** Found a potentially usable Imagen model: {m.name} ***")
                found_imagen_model = True
        if not found_imagen_model:
            logging.warning("No Imagen-like models supporting generateContent were found for your API Key.")
    except Exception as e:
        logging.error(f"Error listing models: {e}")

def test_multiturn_conversation():
    logging.info(f"\n--- Testing Multi-turn Conversation with {TEXT_MODEL_NAME} ---")
    try:
        session = ChatbotSession()

        prompts = [
            "Hi there! What can you do?",
            "Can you tell me about the benefits of exercise?",
            "What kind of exercises are good for beginners?",
            "Thanks!"
        ]

        for i, prompt in enumerate(prompts):
            print(f"You ({i+1}): {prompt}")
            response = session.send_message(prompt)
            print(f"Chatbot ({i+1}): {response}\n")

        session.reset_session()
        print("\nChatbot session reset. New conversation starting.")
        print(f"You: What was our last conversation about?")
        response = session.send_message("What was our last conversation about?")
        print(f"Chatbot: {response}")

    except Exception as e:
        print(f"Error during multi-turn conversation test: {e}")


def test_multimodal_image_understanding():
    logging.info(f"\n--- Testing Multimodal (Image Understanding) with {VISION_MODEL_NAME} ---")

    dummy_image_path = "temp_test_image.jpg"
    try:
        dummy_img = Image.new('RGB', (60, 30), color = 'red')
        dummy_img.save(dummy_image_path)
        logging.info(f"Created a temporary dummy image for test: {dummy_image_path}")

        uploaded_image_file = genai.upload_file(dummy_image_path, display_name="My Test Image")
        logging.info(f"Uploaded temporary image to Gemini service: {uploaded_image_file.name}")

        text_query = "What do you see in this image? Describe it briefly."

        print(f"Sending image and query: '{text_query}'")

        response = send_multimodal_prompt(image_parts=[uploaded_image_file], text_prompt=text_query)
        print(f"Chatbot: {response}")

        genai.delete_file(uploaded_image_file.name)
        logging.info(f"Deleted uploaded file from Gemini service: {uploaded_image_file.name}")

    except Exception as e:
        print(f"Error during multimodal image understanding test: {e}")
    finally:
        if os.path.exists(dummy_image_path):
            os.remove(dummy_image_path)
            logging.info(f"Deleted local temporary dummy image: {dummy_image_path}")

def test_image_generation():
    logging.info(f"\n--- Testing Image Generation with {IMAGEN_MODEL_NAME} ---")
    image_prompt = "A majestic lion standing on a savannah at sunset, photorealistic"
    print(f"You: Generate an image of: '{image_prompt}'")

    try:
        image_results = generate_image_from_prompt(image_prompt)

        if image_results:
            print(f"Chatbot: Generated image(s) for you!")
            for i, result in enumerate(image_results):
                print(f"Image {i+1}: {result}")
        else:
            print("Chatbot: Could not generate image for the given prompt.")
    except Exception as e:
        print(f"Error during image generation test: {e}")

def main():
    try:

        test_image_generation()

    except ValueError as ve:
        print(f"\nConfiguration Error: {ve}")
        print("Please ensure your GEMINI_API_KEY is correctly set in your .env file and has proper permissions.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during main execution: {e}")

if __name__ == "__main__":
    main()