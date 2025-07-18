import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

def generate_caption(review_text):
    prompt = f"""
You are a product caption generator with a strong focus on highlighting sustainability, wellness, affordability, and usefulness. Given the review below, generate:

1. A short, catchy one-liner caption emphasizing any of the following aspects if applicable: 
   - Environmentally friendly
   - Health benefits
   - Cost-effective or value for money
   - Long-term usability
   - Practical/helpful in everyday life

2. A realistic star rating (out of 5) based on the tone of the review.

3. Add this fake affiliate link at the end: https://amzn.to/example

Make sure the output is formatted cleanly.

Review: \"{review_text}\"
    """

    response = model.generate_content(prompt)
    return response.text
