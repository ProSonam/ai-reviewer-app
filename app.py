import streamlit as st
from PIL import Image
import io
import base64

st.set_page_config(page_title="AI Product Reviewer", layout="centered")

st.title("🛍️ AI Product Reviewer")
st.write("Upload or paste a product image and we'll generate a smart review with affiliate links!")

# File uploader
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

# Paste image option (base64-encoded clipboard image)
st.write("📋 Or paste an image directly below 👇")

pasted_image = st.text_area("Paste Base64 image string here (optional)")

# Handle image upload or pasted image
image = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

elif pasted_image:
    try:
        image_data = base64.b64decode(pasted_image)
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption="Pasted Image", use_column_width=True)
        st.success("✅ Image pasted successfully!")
    except Exception as e:
        st.error("❌ Failed to process pasted image. Please ensure it's a valid Base64 image string.")

# Only show button if an image is available
if image:
    affiliate_link = "https://www.amazon.in/dp/B08N5WRWNW?tag=your-affiliate-id"

    if st.button("Generate Review"):
        with st.spinner("Generating review..."):
            st.write("⭐ **Product Name**: [Example Product]")
            st.write("📝 **Review**: This is a great product for daily use. Highly recommended!")

            st.markdown(f"[🔗 Buy Now on Amazon]({affiliate_link})", unsafe_allow_html=True)

            st.markdown(
                """
                <small>
                🧡 **Note**: This is an honest AI-generated review. If you buy using the affiliate link above,
                I may earn a small commission — at no extra cost to you. It helps me run this AI Reviewer project.
                Thanks for your support! 😊
                </small>
                """,
                unsafe_allow_html=True
            )
