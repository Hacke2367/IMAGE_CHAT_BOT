# 🤖 IMAGE_CHAT_BOT: Smart AI Chatbot with Image Generation & Analysis

## ✨ Overview

**IMAGE_CHAT_BOT** is a cutting-edge AI chatbot built using the powerful multimodal capabilities of the **Google Gemini API**, combined with a local **Stable Diffusion** model. It allows users to:

- Chat conversationally with AI
- Generate images using text prompts
- Upload and analyze images with Gemini Pro Vision

This project also serves as a modern learning application that demonstrates how to integrate LLMs, vision models, and frontend UIs like Streamlit into a cohesive experience.

---

## 🚀 Features

- 💬 **AI Text Chat:** Talk naturally with Gemini Pro via smart context-aware chat.
- 🎨 **Image Generation:** Generate images from prompts using local Stable Diffusion.
- 🖼️ **Image Analysis:** Upload your own images and ask the AI to explain them using Gemini Vision.
- ⚡ **Fast & Interactive UI:** Built using Streamlit with custom loaders and real-time response.
- 🧱 **Modular Codebase:** Clean separation between core logic and UI using Python modules.

---

## 🛠️ Technologies Used

- **Python 3.9+**
- **Streamlit** – for frontend UI
- **Google Gemini API** via:
  - `google-generativeai`
  - `gemini-pro` (Text)
  - `gemini-pro-vision` (Image)
- **Diffusers (Hugging Face)** – for image generation
  - `torch`, `transformers`, `accelerate`
- **Pillow (PIL)** – for image processing

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/[Your-GitHub-Username]/IMAGE_CHAT_BOT.git
cd IMAGE_CHAT_BOT
```

---

### 2️⃣ Create & Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows (CMD)
.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Up Google Gemini API Key

🛠️ Go to **Google AI Studio**, generate your API key, and set it as an environment variable:

```bash
# On Windows (CMD)
set GOOGLE_API_KEY="YOUR_API_KEY"

# On Windows (PowerShell)
$env:GOOGLE_API_KEY="YOUR_API_KEY"

# On macOS/Linux
export GOOGLE_API_KEY="YOUR_API_KEY"
```

---

### 5️⃣ Run the App

```bash
streamlit run frontend/app.py
```

> 📝 On first image generation, Stable Diffusion (~2–5 GB) will be downloaded. Ensure a stable internet connection and enough disk space.

## 💡 Usage Guide

### 🗨️ Text Chat  
Type any question into the chat input and press **Enter**.  
Example:  
> Tell me about the history of AI.

---

### 🎨 Image Generation

Use the prompt format below inside chat to generate an image:

```bash
generate an image of: a futuristic city under a full moon
```

This will trigger the Stable Diffusion model to generate the image.

---

### 🖼️ Image Upload + Analysis

1. Go to the **Upload Image** section on the UI.  
2. Upload your desired image (JPEG/PNG).  
3. Ask a follow-up like:

```bash
what do you see in our uploaded image?
```

The bot will respond using Gemini Pro Vision based on the uploaded image.

---

## 📂 Project Structure

```bash
IMAGE_CHAT_BOT/
├── core/
│   ├── gemini_client.py        # Gemini Pro / Vision client
│   └── image_generation.py     # Stable Diffusion image generation logic
├── frontend/
│   └── app.py                  # Streamlit frontend logic
├── .venv/                      # Virtual environment
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## ❗ Troubleshooting (Common Issues)

| Issue                                  | Solution                                                                 |
|----------------------------------------|--------------------------------------------------------------------------|
| `KeyError: 'type'`                     | Stop the Streamlit app (`Ctrl + C`) and rerun it to reset the session.   |
| `File does not exist: app.py`         | Make sure you're in the root directory before running the app.           |
| “I can't generate images...”          | Check prompt format or SD model loading errors in terminal logs.         |
| `google.api_core.exceptions.InvalidArgument` | Ensure `GOOGLE_API_KEY` is set correctly and prompt is not empty.     |

---

## 🧪 Known Challenges

- **Initial Image Generation Failures**  
  Solved by optimizing local Stable Diffusion pipeline and managing memory.

- **Gemini Model Initialization Failures**  
  Handled using robust error logs + Streamlit fallback warnings.

- **Image Confusion in Chat Context**  
  Fixed using logic to only use image if user explicitly refers to it.

---

## 🔮 Future Enhancements

- 💾 Persistent Chat History (SQLite or JSON)
- 🖌️ Advanced UI with themes, animations
- 📦 Efficient In-Memory Image Management
- 🔊 Voice Input/Output Interaction
- 🔐 Multi-user Authentication & Profiles

---

## 🤝 Contributing

We love contributions! Here's how you can help:

- 🐞 Report bugs via GitHub Issues
- ✨ Suggest features or enhancements
- 📥 Submit a pull request with improvements

---

## 📄 License

Licensed under the **MIT License** — feel free to use, modify, and share!

---

## 📞 Contact & Support

**👤 Abhishek Maurya**  
📧 abhishekmlen25@gmail.com  




