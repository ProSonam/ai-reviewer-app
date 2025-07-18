# utils/image_utils.py

import replicate
import os
from datetime import datetime
from urllib.request import urlretrieve

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_JTpfLf4C98y9yp5zMa3xvEnuufeARgn3XmxDt"

# New model and version
MODEL_ID = "black-forest-labs/flux-kontext-pro"

# Define style prompts
STYLE_PROMPTS = {
    "90s Cartoon": "Make this a 90s cartoon",
    "Comic Style": "Comic book inked lines, saturated colors",
    "Cyberpunk Anime": "Futuristic cyberpunk anime style",
    "Dreamy Pastel": "Soft pastel illustration with dreamy tones"
}

def generate_stylized_images(image_path):
    output_paths = []

    for style_name, style_prompt in STYLE_PROMPTS.items():
        print(f"Generating for style: {style_name}")

        # Upload the image to Replicate first
        image_url = replicate.files.upload(image_path)

        # Run the model with required input
        output_url = replicate.run(
            MODEL_ID,
            input={
                "prompt": style_prompt,
                "input_image": image_url,
                "output_format": "jpg"
            }
        )

        if isinstance(output_url, list):
            output_url = output_url[0]

        # Save the output image
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"{style_name.replace(' ', '_')}_{timestamp}.jpg"
        output_path = os.path.join("outputs", output_filename)

        os.makedirs("outputs", exist_ok=True)
        urlretrieve(output_url, output_path)

        output_paths.append(output_path)

    return output_paths
