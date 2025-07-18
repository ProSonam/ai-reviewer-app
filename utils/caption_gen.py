import openai
import os

# Make sure your OPENAI_API_KEY is stored as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_caption(review_text):
    prompt = f"""
You are a helpful assistant who writes short, punchy product captions for Instagram.
Given the user review below, write:
1. A friendly one-liner caption
2. Star rating (out of 5)
3. Add this placeholder affiliate link at the end: https://amzn.to/example

User review: \"{review_text}\"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if using free tier
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message['content']

