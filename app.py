import streamlit as st
import base64
import replicate
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from utils.caption_gen import generate_product_caption

st.set_page_config(page_title="🛍️ AI Product Reviewer")
st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll generate a smart review with affiliate links!")

uploaded_file = st.file_uploader("Choose a product image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Load and convert to RGB to avoid JPEG errors
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="📷 Uploaded Product", use_container_width=True)
        st.success("✅ Image uploaded successfully!")

        # Convert to base64 for API input
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode()

        st.write("🧠 Generating smart review and stylized image...")

        # Use a working generic style-transfer model
        output_urls = replicate.run(
            "fofr/style-transfer",
            input={"image": base64_image}
        )

        # Display returned stylized images
        if isinstance(output_urls, list):
            for idx, url in enumerate(output_urls):
                st.image(url, caption=f"🎨 Stylized Image #{idx+1}", use_container_width=True)
        else:
            st.image(output_urls, caption="🎨 Stylized Image", use_container_width=True)

        # Generate AI-based review
        caption = generate_product_caption(base64_image)
        st.subheader("📝 Smart Product Review")
        st.write(caption)

    except UnidentifiedImageError:
        st.error("❌ The image is invalid or corrupted. Please upload a proper JPEG/PNG file.")
    except replicate.exceptions.ReplicateError:
        st.warning("⚠️ Could not stylize image (Replicate). The rest of the flow will continue.")
        caption = generate_product_caption(base64_image)
        st.subheader("📝 Smart Product Review")
        st.write(caption)
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
