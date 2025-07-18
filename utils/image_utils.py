import replicate
import uuid
import os
from PIL import Image
from io import BytesIO
import requests

REPLICATE_MODEL = "fofr/anything-v4.0"  # Change this to your preferred model
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")  # Set this in your environment

def generate_stylized_images(image_path, num_images=3):
    if not REPLICATE_API_TOKEN:
        raise Exception("REPLICATE_API_TOKEN is not set")

    replicate.Client(api_token=REPLICATE_API_TOKEN)

    # Ensure image is in RGB mode (not RGBA)
    image = Image.open(image_path).convert("RGB")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    prompt = (
        "Ultra-realistic commercial product photo. Studio lighting, clean background, "
        "crisp focus on product. Style: professional advertisement for Amazon."
    )

    generated_images = []
    for _ in range(num_images):
        output_url = replicate.run(
            REPLICATE_MODEL,
            input={
                "prompt": prompt,
                "image": img_bytes,
                "width": 512,
                "height": 512,
                "guidance_scale": 7,
            }
        )
        if isinstance(output_url, list) and output_url:
            img_url = output_url[0]
            response = requests.get(img_url)
            filename = f"stylized_{uuid.uuid4().hex[:8]}.jpg"
            output_path = os.path.join("generated_images", filename)
            os.makedirs("generated_images", exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
            generated_images.append(output_path)

    return generated_images
