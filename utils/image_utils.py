# utils/image_utils.py

import replicate
import os
from datetime import datetime
from PIL import Image

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "your_replicate_api_token_here"

# Model name
MODEL_ID = "fofr/sdxl-style-transfer"
MODEL_VERSION = "b54b1994be8fe984210cc363a2a20a2a6f69c445cccb2f7b8fcd36a1227f12f9"

# Define style prompts
STYLE_PROMPTS = {
    "Minimalist Studio": "product in a clean studio, soft shadows, minimal background, high detail, commercial product photo",
    "Vibrant Ad": "bright colors, energetic vibe, professional commercial product photo, sharp focus",
    "Dark Luxury": "moody lighting, dark background, elegant, premium product style, high contrast",
    "Natural Light": "sunlit background, natural wooden table, casual environment, warm tone"
}

def generate_stylized_images(image_path):
    output_paths = []
    model = replicate.models.get(MODEL_ID).versions.get(MODEL_VERSION)

    for style_name, style_prompt in STYLE_PROMPTS.items():
        print(f"Generating for style: {style_name}")

        output_url = model.predict(
            input={
                "image": open(image_path, "rb"),
                "prompt": style_prompt,
                "seed": 42
            }
        )

        if isinstance(output_url, list):
            output_url = output_url[0]

        # Save the image from URL
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"{style_name.replace(' ', '_')}_{timestamp}.jpg"
        output_path = os.path.join("outputs", output_filename)

        os.makedirs("outputs", exist_ok=True)

        # Download image from URL
        from urllib.request import urlretrieve
        urlretrieve(output_url, output_path)

        output_paths.append(output_path)

    return output_paths
