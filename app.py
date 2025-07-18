import os
import base64
from io import BytesIO
from PIL import Image
import streamlit as st
import replicate

# Import your custom review generation function
from caption_utils import generate_review  # Make sure caption_utils.py exists

# ✅ Set Replicate API securely
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# ✅ Streamlit App Setup
st.set_page_config(page_title="AI Product Reviewer", layout="centered")
st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll generate a smart review with affiliate links!")

uploaded_file = st.file_uploader("📤 Choose a product image", type=["jpg", "jpeg", "png"])

# ✅ If user uploads an image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Product Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    # Stylize Image Button
    if st.button("✨ Enhance Image with AI Style Transfer"):
        with st.spinner("🎨 Enhancing your image..."):
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

            try:
                output_url = replicate.run(
                    "fofr/anything-style-transfer:54bc4c2067d8963d250d6745456d7ad41f7342e4997b4013eec05b77b7e53f1f",
                    input={"image": f"data:image/jpeg;base64,{base64_image}"}
                )
                st.image(output_url, caption="✨ Stylized Product Photo", use_column_width=True)
            except Exception as e:
                st.error(f"⚠️ Failed to generate stylized image: {e}")

    # Manual Prompt Recommendation
    st.markdown("📸 **Want to enhance your product photo manually?** Try this prompt in an AI image tool:")
    st.code(
        """Create a high-resolution, ultra-realistic commercial photo of [describe your product]. 
Use a bold, minimalist background and soft studio lighting. Shot with an 85mm lens, shallow depth of field. 
Format: 4:5 vertical. Export as high-resolution JPEG."""
    )

    # Generate Smart Review
    if st.button("🧠 Generate AI Review"):
        with st.spinner("📝 Generating review..."):
            try:
                # 🔁 Use your own model/logic here
                product_name, review = generate_review(image)

                # Replace with your actual affiliate link
                affiliate_link = "https://www.amazon.in/dp/B08N5WRWNW?tag=your-affiliate-id"

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
            except Exception as e:
                st.error(f"⚠️ Could not generate review: {e}")
