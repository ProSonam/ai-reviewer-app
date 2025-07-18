import os
import base64
from io import BytesIO
from PIL import Image
import streamlit as st
import replicate

from utils.caption_gen import generate_product_caption  # 🔄 Imports your review generation logic

# ✅ Securely load token from Streamlit secrets
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# ✅ Streamlit page config
st.set_page_config(page_title="🛍️ AI Product Reviewer", layout="centered")

st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll generate a smart review with affiliate links!")

# ✅ Upload image
uploaded_file = st.file_uploader("Choose a product image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📷 Uploaded Product", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    # 🌈 Stylize image with Replicate
    if st.button("✨ Generate Stylized Image"):
        with st.spinner("Enhancing image with AI..."):
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

            output_url = replicate.run(
                "fofr/anything-style-transfer:54bc4c2067d8963d250d6745456d7ad41f7342e4997b4013eec05b77b7e53f1f",
                input={"image": f"data:image/jpeg;base64,{base64_image}"}
            )
            st.image(output_url, caption="✨ Stylized Product Image")

    # 📸 Prompt suggestion
    st.markdown("📸 **Want to enhance your product photo manually?** Try this prompt in any AI image generator:")
    st.code(
        """Create a high-resolution, ultra-realistic commercial photo of [describe your product]. 
Use a bold, minimalist background and soft studio lighting. Shot with an 85mm lens, shallow depth of field. 
Format: 4:5 vertical. Export as high-resolution JPEG."""
    )

    # 🧠 Generate Review Section
    if st.button("🧠 Generate AI Review"):
        with st.spinner("Analyzing image and writing review..."):
            review_data = generate_product_caption(image)

            if review_data:
                st.markdown(f"⭐ **Product Name**: {review_data['product_name']}")
                st.markdown(f"📝 **Review**: {review_data['review']}")
                st.markdown(f"[🔗 Buy Now on Amazon]({review_data['affiliate_link']})", unsafe_allow_html=True)

                st.markdown(
                    """
                    <small>
                    🧡 <strong>Note</strong>: This is an AI-generated honest review. If you purchase via the link above, 
                    I may earn a small commission — at no extra cost to you. This helps keep this tool running. 
                    Thank you for your support! 🙏
                    </small>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("❌ Failed to generate review. Please try again.")
