# utils/image_utils.py

import replicate
import os
from datetime import datetime
from urllib.request import urlretrieve

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_JTpfLf4C98y9yp5zMa3xvEnuufeARgn3XmxDt"

# Define style prompts
STYLE_PROMPTS = {
    "90s Cartoon": "Make this a 90s cartoon",
    "Studio Pop": "Professional product image, white background, studio lights",
    "Comic Book": "Comic book style, bold lines, halftone effect",
    "Pastel Dream": "Soft pastel colors, dreamy aesthetic, product focused"
}

def generate_stylized_images(image_path):
    output_paths = []

    for style_name, prompt in STYLE_PROMPTS.items():
        print(f"Generating style: {style_name}")

        # Upload image to Replicate CDN
        image_url = replicate.upload.open(image_path)

        # Call the new model
        output_url = replicate.run(
            "black-forest-labs/flux-kontext-pro",
            input={
                "prompt": prompt,
                "input_image": "https://replicate.delivery/pbxt/N55l5TWGh8mSlNzW8usReoaNhGbFwvLeZR3TX1NL4pd2Wtfv/replicate-prediction-f2d25rg6gnrma0cq257vdw2n4c.png",
    
                "output_format": "jpg"
            }
        )

        if isinstance(output_url, list):
            output_url = output_url[0]

        # Save output to local disk
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"{style_name.replace(' ', '_')}_{timestamp}.jpg"
        output_path = os.path.join("outputs", output_filename)
        os.makedirs("outputs", exist_ok=True)
        urlretrieve(output_url, output_path)

        output_paths.append(output_path)

    return output_paths
