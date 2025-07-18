import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Product Reviewer", layout="centered")

st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll generate a smart review with affiliate links!")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Product Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    # Optional enhancement prompt
    st.markdown("📸 **Want to enhance your product photo?** Use the following prompt in a free AI image generator:")
    st.code(
        """Create a high-resolution, ultra-realistic commercial photo of [describe your product]. 
Use a bold, minimalist background and soft studio lighting. Shot with an 85mm lens, shallow depth of field. 
Format: 4:5 vertical. Export as high-resolution JPEG."""
    )

    affiliate_link = "https://www.amazon.in/dp/B08N5WRWNW?tag=your-affiliate-id"

    if st.button("Generate Review"):
        with st.spinner("Generating review..."):
            # You can later plug in a real LLM here
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
