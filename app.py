import streamlit as st

st.set_page_config(page_title="AI Product Reviewer", layout="centered")

st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll generate a smart review with affiliate links!")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    # Replace this with your actual affiliate link
    affiliate_link = "https://www.amazon.in/dp/B08N5WRWNW?tag=your-affiliate-id"

    if st.button("Generate Review"):
        with st.spinner("Generating review..."):
            st.write("⭐ **Product Name**: [Example Product]")
            st.write("📝 **Review**: This is a great product for daily use. Highly recommended!")

            st.markdown(f"[🔗 Buy Now on Amazon]({affiliate_link})", unsafe_allow_html=True)

            st.markdown(
                """
                <small>
                🧡 **Note**: This is an honest AI-generated review. If you buy using the affiliate link above, I may earn a small commission — at no extra cost to you. It helps me run this AI Reviewer project. Thanks for your support! 😊
                </small>
                """,
                unsafe_allow_html=True
            )
