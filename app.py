import streamlit as st
from utils.image_utils import generate_stylized_images
from utils.caption_gen import generate_product_caption

import os
from PIL import Image

# Set Streamlit page config
st.set_page_config(page_title="AI Product Image & Caption Generator", layout="centered")

st.title("📸 AI Product Image & Caption Generator")
st.markdown("Upload a product image and get stylized commercial-quality versions with auto-generated Amazon-style captions.")

# File uploader
uploaded_file = st.file_uploader("Upload your product image", type=["png", "jpg", "jpeg"])

# Generate on button click
if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    input_image_path = os.path.join("uploads", uploaded_file.name)

    # Save uploaded image in RGB format
    image = Image.open(uploaded_file).convert("RGB")
    image.save(input_image_path, format="JPEG")  # Ensure JPEG for Replicate

    st.image(image, caption="Original Uploaded Image", use_use_container_width=True)

    with st.spinner("Processing your image and generating stylized versions..."):
        try:
            stylized_paths = generate_stylized_images(input_image_path)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    st.success("Stylized images generated!")
    st.subheader("🖼️ Stylized Outputs")

    for path in stylized_paths:
        output_image = Image.open(path)
        st.image(output_image, caption=os.path.basename(path), use_column_width=True)

        with st.spinner("Generating caption..."):
            caption = generate_product_caption(path)
        st.markdown(f"**📝 Caption:** {caption}")
