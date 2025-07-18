import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="AI Product Reviewer", layout="centered")

st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and get a smart AI-generated review with affiliate links!")

uploaded_file = st.file_uploader("Choose a product image", type=["jpg", "jpeg", "png"])

# Dummy affiliate link
affiliate_link = "https://www.amazon.in/dp/B08N5WRWNW?tag=your-affiliate-id"

def generate_review(product_name="Sample Product"):
    return {
        "name": product_name,
        "review": "This product stands out for its excellent quality and performance. It's ideal for everyday use and offers great value for money!"
    }

def generate_variations(image_bytes):
    # Use Replicate (Free Tier): Replace with your own token if needed
    replicate_url = "https://api-inference.huggingface.co/models/hogiahien/counterfeit-v30-edited"
    headers = {"Authorization": f"Bearer YOUR_HUGGINGFACE_TOKEN_HERE"}
    files = {"inputs": image_bytes}
    response = requests.post(replicate_url, headers=headers, files=files)

    if response.status_code == 200:
        return [Image.open(BytesIO(image_bytes))]  # Replace with real enhanced images
    else:
        st.warning("⚠️ Could not generate variations right now. Showing original image.")
        return [Image.open(BytesIO(image_bytes))]

if uploaded_file:
    st.image(uploaded_file, caption="Original Product Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    if st.button("✨ Generate Smart Review"):
        with st.spinner("AI is writing your product review..."):
            image_bytes = uploaded_file.read()

            # Simulate enhanced image generation
            images = generate_variations(image_bytes)

            for idx, img in enumerate(images):
                st.image(img, caption=f"AI-Enhanced Image {idx + 1}", use_column_width=True)

            review_data = generate_review()
            st.markdown(f"### ⭐ Product Name: {review_data['name']}")
            st.markdown(f"📝 **Review**: {review_data['review']}")

            st.markdown(f"[🔗 Buy Now on Amazon]({affiliate_link})", unsafe_allow_html=True)

            st.markdown(
                """
                <small>
                🧡 <b>Note</b>: This is an honest AI-generated review. If you buy using the affiliate link above, 
                I may earn a small commission — at no extra cost to you. It helps me keep improving this project. Thank you! 😊
                </small>
                """,
                unsafe_allow_html=True
            )

            st.divider()
            st.markdown(
                """
                <center>
                🚀 Want higher-quality reviews & advanced AI editing? 
                [Upgrade to Pro 🔒](#) (coming soon)
                </center>
                """,
                unsafe_allow_html=True
            )
