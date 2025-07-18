import streamlit as st
from PIL import Image
import os
import replicate
from dotenv import load_dotenv
import base64
import tempfile

# Load the Replicate API token from .env
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

st.set_page_config(page_title="AI Product Reviewer", layout="centered")

st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll enhance it and generate a smart review with affiliate links!")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Product Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    if st.button("✨ Enhance Image"):
        with st.spinner("Enhancing image using AI..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                image.save(temp_file.name)
                output = replicate.run(
                    "fofr/anything-3.0:28c5720cb37b5b0c7765eb4fda1ad84715c399617c0de1f974187c431c4598f8",
                    input={
                        "prompt": "a high-resolution, ultra-realistic commercial photo of the product with a clean studio background, professional lighting, product photography, DSLR, 85mm lens, 4k, shallow depth of field",
                        "image": open(temp_file.name, "rb"),
                        "num_outputs": 1,
                        "guidance_scale": 7.5,
                        "num_inference_steps": 50,
                    },
                )

            enhanced_image_url = output[0]
            st.image(enhanced_image_url, caption="✨ Enhanced Product Image", use_column_width=True)
            st.success("✨ Image enhanced successfully!")

    affiliate_link = "https://www.amazon.in/dp/B08N5WRWNW?tag=your-affiliate-id"

    if st.button("📝 Generate Review"):
        with st.spinner("Generating review..."):
            # Placeholder - replace with actual LLM response
            product_name = "Example Product"
            review = "This product is well-made, reliable, and perfect for daily use. A great choice for anyone looking for quality and value."

            st.markdown(f"⭐ **Product Name**: {product_name}")
            st.markdown(f"📝 **Review**: {review}")
            st.markdown(f"[🔗 Buy Now on Amazon]({affiliate_link})", unsafe_allow_html=True)

            st.markdown(
                """
                <small>
                🧡 <strong>Note</strong>: This is an honest AI-generated review. If you purchase through the affiliate link above, 
                I may earn a small commission — at no extra cost to you. This helps keep the AI Reviewer project running. 
                Thank you for your support! 🙏
                </small>
                """,
                unsafe_allow_html=True
            )
