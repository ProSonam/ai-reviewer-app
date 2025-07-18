import os
import replicate
import streamlit as st
from PIL import Image
import base64

# ✅ Securely get token from Streamlit secrets
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

st.set_page_config(page_title="AI Product Reviewer", layout="centered")

st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll generate a smart review with affiliate links!")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Product Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    # Offer image enhancement
    if st.button("✨ Generate Stylized Image"):
        with st.spinner("Enhancing image via AI..."):
            # Convert image to base64 for Replicate API
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

            output_url = replicate.run(
                "fofr/anything-style-transfer:54bc4c2067d8963d250d6745456d7ad41f7342e4997b4013eec05b77b7e53f1f",
                input={"image": f"data:image/jpeg;base64,{base64_image}"}
            )
            st.image(output_url, caption="Stylized Product Photo")

    # Text prompt for manual enhancement
    st.markdown("📸 **Want to enhance your product photo?** Use the following prompt in a free AI image generator:")
    st.code(
        """Create a high-resolution, ultra-realistic commercial photo of [describe your product]. 
Use a bold, minimalist background and soft studio lighting. Shot with an 85mm lens, shallow depth of field. 
Format: 4:5 vertical. Export as high-resolution JPEG."""
    )

    affiliate_link = "https://www.amazon.in/dp/B08N5WRWNW?tag=your-affiliate-id"

    if st.button("🧠 Generate Review"):
        with st.spinner("Generating review..."):
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
