import streamlit as st
from utils.image_utils import generate_stylized_images
from utils.caption_gen import generate_captions
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
    with st.spinner("Processing your image..."):
        input_image_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        with open(input_image_path, "wb") as f:
            f.write(uploaded_file.read())

        # Generate stylized images
        stylized_paths = generate_stylized_images(input_image_path)

        st.success("Stylized images generated!")
        st.subheader("🖼️ Stylized Outputs")

        for path in stylized_paths:
            image = Image.open(path)
            st.image(image, caption=os.path.basename(path), use_column_width=True)

            # Generate caption
            with st.spinner("Generating caption..."):
                caption = generate_captions(path)
            st.markdown(f"**📝 Caption:** {caption}")
