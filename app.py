import streamlit as st

st.set_page_config(page_title="AI Product Reviewer", layout="centered")

st.title("🛍️ AI Product Reviewer")
st.write("Upload a product image and we'll generate a smart review with affiliate links!")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    # Placeholder for caption + affiliate logic
    if st.button("Generate Review"):
        with st.spinner("Generating review..."):
            st.write("⭐ Product Name: [Example Product]")
            st.write("📝 Review: This is a great product for daily use. Highly recommended!")
            st.markdown("[🔗 Buy Now on Amazon](https://www.amazon.in/)")


