import streamlit as st
import openai
import requests
import io
import base64
from PIL import Image

# Set your OpenAI GPT-3 API key
openai.api_key = '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'

# Hugging Face model API details
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Streamlit app
st.title("AI-Generated Blog Post with Images")

# Step 1: Keyword Selection
keywords = st.text_input("Enter keywords (comma-separated):")

# Step 2: Text Generation
# Generate blog post content using GPT-3
prompt = f"Write a blog post about **{keywords}**. Format the generated text and images into a coherent blog post structure, including an introduction, body, conclusion, and specify relevant keywords related to **{keywords}**."
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=500
)

generated_text = response['choices'][0]['text']

# Step 3: Image Generation
# Query Hugging Face model for image
def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.content

image_bytes = query({
    "inputs": keywords,
})

# Convert image data to base64
image_base64 = base64.b64encode(image_bytes).decode("utf-8")

# Display generated text
st.write(generated_text)

# Display generated image
st.header("Generated Image")
st.image(f"data:image/png;base64,{image_base64}", caption='Generated Image', use_column_width=True)
