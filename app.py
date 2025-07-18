import streamlit as st
from utils.caption_gen import generate_product_caption
from utils.image_utils import generate_stylized_images

st.title("🪄 AI Product Reviewer")
st.subheader("Upload product image + review → Get catchy caption & star rating!")

uploaded_image = st.file_uploader("📸 Upload a product image", type=["jpg", "jpeg", "png"])
review_text = st.text_area("📝 Paste a customer review")

if st.button("✨ Generate Caption"):
    if not uploaded_image or not review_text:
        st.warning("Please upload an image and paste a review.")
    else:
        # Process image
        enhanced = enhance_image(uploaded_image)
        st.image(enhanced, caption="Enhanced Image", use_column_width=True)

        # Generate caption
        with st.spinner("Generating caption..."):
            caption = generate_product_caption(review_text)

        st.markdown("### 📢 Caption + Rating")
        st.success(caption)
