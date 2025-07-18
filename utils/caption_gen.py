import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

def generate_caption(review_text):
    prompt = f"""
You are a product caption generator. Given the review below, create:
1. A short one-liner caption
2. A star rating (out of 5)
3. Add this fake affiliate link: https://amzn.to/example

Review: \"{review_text}\"
    """

    response = model.generate_content(prompt)
    return response.text
