import streamlit as st
import os
import sys
import logging
import re
from PIL import Image
import io
import time

# Setup paths
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'core'))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import core logic
try:
    from core.gemini_client import initialize_gemini, ChatbotSession
    from core.image_generation import generate_image_from_prompt, local_pipe as sd_pipeline
except ImportError as e:
    st.error(f"Failed to import core modules: {e}")
    st.stop()

# Streamlit page config
st.set_page_config(page_title="Multimodal AI Chatbot", layout="centered")
st.title("Multimodal AI Chatbot")

# Initialize Gemini and chat session
if 'gemini_initialized' not in st.session_state:
    try:
        initialize_gemini()
        st.session_state.gemini_initialized = True
    except Exception as e:
        st.error(f"Failed to initialize Gemini API: {e}")
        st.stop()

if 'chat_session' not in st.session_state:
    try:
        st.session_state.chat_session = ChatbotSession()
    except Exception as e:
        st.error(f"Failed to start chatbot session: {e}")
        st.stop()

# Initialize session states
st.session_state.setdefault("messages", [])
st.session_state.setdefault("uploaded_image", None)
st.session_state.setdefault("processing", False)
st.session_state.setdefault("show_confirmation", False)
st.session_state.setdefault("show_history", False)

# Sidebar controls
with st.sidebar:
    st.header("Chat Controls")
    if st.button("Start New Conversation"):
        st.session_state.show_confirmation = True

    if st.session_state.show_confirmation:
        if st.checkbox("Confirm reset?"):
            st.session_state.chat_session.reset_session()
            st.session_state.messages = []
            st.session_state.uploaded_image = None
            st.session_state.show_confirmation = False
            st.rerun()
        if st.button("Cancel"):
            st.session_state.show_confirmation = False

    if st.button("Show Raw History"):
        st.session_state.show_history = not st.session_state.show_history

    if st.session_state.show_history:
        with st.expander("Conversation History"):
            st.json(st.session_state.chat_session.get_history())

# Welcome message
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "bot",
        "content": "Hello! I'm your AI assistant.\n- Ask questions\n- Generate images (type: **generate an image of: [description]**)\n- Analyze uploaded images",
        "type": "text"
    })

# Image uploader
uploaded_image = st.file_uploader("Upload an image for analysis", type=['png', 'jpg', 'jpeg'])
if uploaded_image and not st.session_state.processing:
    st.session_state.processing = True
    with st.spinner("Processing uploaded image..."):
        try:
            img = Image.open(uploaded_image)
            img = img.convert("RGB")
            img.thumbnail((1024, 1024))
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            st.session_state.uploaded_image = img_bytes.getvalue()
            st.session_state.messages.append({
                "role": "user",
                "content": "Uploaded an image for analysis.",
                "type": "image_upload",
                "image_bytes": st.session_state.uploaded_image
            })
        finally:
            if "trigger_rerun" in st.session_state and st.session_state.trigger_rerun:
                st.session_state.processing = False
                st.rerun()

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        msg_type = message.get("type", "text")
        if msg_type == "text":
            st.markdown(message["content"])
        elif msg_type == "image_upload":
            try:
                img = Image.open(io.BytesIO(message["image_bytes"]))
                st.image(img, caption="Uploaded Image", use_container_width=True)
            except:
                st.error("Could not display uploaded image")
        elif msg_type == "image":
            for path in message["content"]:
                if os.path.exists(path):
                    st.image(path, use_container_width=True)

# Handle new prompt
if prompt := st.chat_input("Type your message..."):
    user_msg = {"role": "user", "content": prompt, "type": "text"}
    st.session_state.messages.append(user_msg)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("bot"):
        with st.spinner("Thinking..."):
            prompt_lower = prompt.lower()
            image_match = re.search(r"generate an? image of:?(.*)", prompt_lower)
            ask_uploaded = "uploaded image" in prompt_lower
            ask_generated = "generated image" in prompt_lower

            current_image = None
            if ask_uploaded and st.session_state.uploaded_image:
                current_image = Image.open(io.BytesIO(st.session_state.uploaded_image))
            elif ask_generated:
                for msg in reversed(st.session_state.messages):
                    if msg.get("type") == "image" and msg.get("content"):
                        last_image_path = msg["content"][-1]
                        if os.path.exists(last_image_path):
                            current_image = Image.open(last_image_path)
                        break

            try:
                if image_match:
                    prompt_text = image_match.group(1).strip()
                    paths = generate_image_from_prompt(prompt_text)
                    if paths and not any("Error" in p for p in paths):
                        st.image(paths[0], use_container_width=True)
                        st.session_state.messages.append({"role": "bot", "content": paths, "type": "image"})
                    else:
                        error = paths[0] if paths else "Image generation failed"
                        st.markdown(error)
                        st.session_state.messages.append({"role": "bot", "content": error, "type": "text"})
                else:
                    if current_image:
                        current_image = current_image.convert("RGB")
                        response = st.session_state.chat_session.send_message(prompt, image=current_image)
                    else:
                        response = st.session_state.chat_session.send_message(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "bot", "content": response, "type": "text"})
            except Exception as e:
                st.error("Something went wrong while processing your request.")
                st.session_state.messages.append({"role": "bot", "content": str(e), "type": "text"})
