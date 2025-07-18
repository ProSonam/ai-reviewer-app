import replicate
import uuid
import os
from PIL import Image
from io import BytesIO
import requests

# Change to the new model
REPLICATE_MODEL = "black-forest-labs/flux-kontext-pro"
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

def generate_stylized_images(image_path, num_images=1):
    if not REPLICATE_API_TOKEN:
        raise Exception("REPLICATE_API_TOKEN is not set")

    client = replicate.Client(api_token=REPLICATE_API_TOKEN)

    # Read and convert image to RGB
    image = Image.open(image_path).convert("RGB")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()

    # Upload image to Replicate
    image_url = replicate.files.upload(image_bytes)

    # 🔥 Old custom prompt
    prompt = (
        "Create a high-resolution, ultra-realistic commercial product photograph "
        "of a woman holding the product in natural light. The focus is on the product "
        "with shallow depth of field and soft studio lighting. Style: clean, minimal, elegant."
    )

    generated_images = []

    for _ in range(num_images):
        output_urls = client.run(
            REPLICATE_MODEL,
            input={
                "prompt": prompt,
                "image": image_url,
                "scale": 7,
                "sampler": "DPM++ 2M Karras",
                "width": 512,
                "height": 512
            }
        )

        if isinstance(output_urls, list):
            for url in output_urls:
                response = requests.get(url)
                filename = f"generated_{uuid.uuid4().hex[:8]}.jpg"
                output_dir = "generated_images"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, filename)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                generated_images.append(output_path)

    return generated_images
