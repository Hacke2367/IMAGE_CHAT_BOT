import logging
import os
import torch
from datetime import datetime
from PIL import Image
from pathlib import Path

try:
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

    if torch.cuda.is_available() and torch.cuda.get_device_properties(0).major >= 8:
        DTYPE = torch.bfloat16
        DEVICE = "cuda"
    elif torch.cuda.is_available():
        DTYPE = torch.float16
        DEVICE = "cuda"
    else:
        DTYPE = torch.float32
        DEVICE = "cpu"

    LOCAL_PIPELINE_AVAILABLE = True
    logging.info(f"Local Stable Diffusion setup: Using device '{DEVICE}' with dtype '{DTYPE}'.")

except ImportError as e:
    LOCAL_PIPELINE_AVAILABLE = False
    logging.error(f"Failed to import diffusers or torch. Local image generation will not work. Error: {e}")
except Exception as e:
    LOCAL_PIPELINE_AVAILABLE = False
    logging.error(f"Error during local Stable Diffusion initialization. Local generation will not work. Error: {e}")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL_ID = "stabilityai/stable-diffusion-2-1"

local_pipe = None
if LOCAL_PIPELINE_AVAILABLE:
    try:
        logging.info(f"Loading Stable Diffusion pipeline from '{MODEL_ID}' to {DEVICE}...")
        local_pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=DTYPE)
        local_pipe.scheduler = DPMSolverMultistepScheduler.from_config(local_pipe.scheduler.config)
        local_pipe.enable_attention_slicing()
        local_pipe = local_pipe.to(DEVICE)
        logging.info("Stable Diffusion pipeline loaded successfully.")
    except Exception as e:
        local_pipe = None
        LOCAL_PIPELINE_AVAILABLE = False
        logging.error(f"Failed to load local Stable Diffusion pipeline. Error: {e}")


def generate_image_from_prompt(text_prompt: str) -> list[str]:
    if not text_prompt:
        logging.error("Image generation prompt cannot be empty.")
        return []

    if not LOCAL_PIPELINE_AVAILABLE or local_pipe is None:
        logging.error("Local Stable Diffusion pipeline is not available. Check installation and initialization logs.")
        return ["Local image generation setup failed. Please check logs."]

    logging.info(f"Generating image locally for prompt: '{text_prompt[:60]}...'")

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        frontend_dir = os.path.join(project_root, "frontend")
        output_dir = os.path.join(frontend_dir, "generated_images")

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.png"
        image_path = os.path.join(output_dir, filename)

        results = local_pipe(
            text_prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
            height=512,
            width=512
        )

        image = results.images[0]
        image.save(image_path)

        logging.info(f"Image saved as: {image_path}")
        return [image_path]

    except Exception as e:
        logging.error(f"Error during local image generation: {e}")
        return [f"Local image generation failed: {e}"]

