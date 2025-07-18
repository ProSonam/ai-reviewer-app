import streamlit as st
import base64
import replicate
from PIL import Image
from io import BytesIO

from utils.caption_gen import generate_product_caption  # Make sure this function exists

st.set_page_config(page_title="🛍️ AI Product Reviewer")
st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll generate a smart review with affiliate links!")

uploaded_file = st.file_uploader("Choose a product image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="📷 Uploaded Product", use_container_width=True)
    st.success("✅ Image uploaded successfully!")

    # Convert image to base64
    image = Image.open(uploaded_file)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode()

    try:
        st.write("🧠 Generating smart review...")

        # Optional: stylize image using Replicate (comment out if not needed)
        output_url = replicate.run(
            "fofr/anything-style-transfer:54bc4c2067d8963d250d6745456d7ad41f7342e4997b4013eec05b77b7e53f1f",
            input={"image": f"data:image/jpeg;base64,{base64_image}"}
        )

        st.image(output_url, caption="🎨 AI-Stylized Image", use_container_width=True)

        # Generate product caption
        caption = generate_product_caption(base64_image)

        st.subheader("📝 Smart Product Review")
        st.write(caption)

    except replicate.exceptions.ReplicateError as e:
        st.error("❌ Failed to process the image. Please check your Replicate model version ID and input.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.stop()
