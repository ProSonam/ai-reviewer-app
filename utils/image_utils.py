import replicate
import os
from PIL import Image
import requests
from io import BytesIO

# Ensure 'outputs' directory exists
os.makedirs("outputs", exist_ok=True)

def generate_stylized_images(image_path):
    """
    Stylize the uploaded image using Replicate's Flux-Kontext-Pro model with a 90s cartoon prompt.
    Saves the stylized image in the outputs directory and returns the local path.
    """

    # Open image file
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Send request to Replicate
    output_url = replicate.run(
        "black-forest-labs/flux-kontext-pro",
        input={
            "prompt": "Make this a 90s cartoon",
            "input_image": image_bytes,
            "output_format": "jpg"
        }
    )

    if isinstance(output_url, list):
        output_url = output_url[0]  # Get the first URL if list

    # Download the output image
    response = requests.get(output_url)
    output_image = Image.open(BytesIO(response.content))

    # Save it locally
    output_filename = os.path.basename(image_path).split('.')[0] + "_stylized.jpg"
    output_path = os.path.join("outputs", output_filename)
    output_image.save(output_path)

    return [output_path]
