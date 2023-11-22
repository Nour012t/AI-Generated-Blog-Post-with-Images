import streamlit as st
import openai
import requests

# Set your OpenAI GPT-3 API key
openai.api_key = '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'

# Streamlit app
st.title("AI-Generated Blog Post with Images")

# Step 1: Keyword Selection
keywords = st.text_input("Enter keywords (comma-separated):")

# Step 2: Text Generation
# Generate blog post content using GPT-3
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Write a blog post about {keywords}.",
    temperature=0.7,
    max_tokens=500
)

generated_text = response['choices'][0]['text']

# Step 3: Divide the generated text into Introduction, Body, and Conclusion
paragraphs = generated_text.split("\n\n")
introduction = paragraphs[1]
body = paragraphs[2:-1]
conclusion = paragraphs[-1]

# Step 4: Image Generation
# Replace 'your_access_key' with your Unsplash API key
access_key = '-Nr_5kEhxGcLMfS826pXrMqUoMWQWmpQ0xobT7zQtg4'

# Unsplash API endpoint for searching photos
url = 'https://api.unsplash.com/search/photos'

# Set up the request headers with your API key
headers = {
    'Authorization': f'Client-ID {access_key}',
}

# Make a request to the Unsplash API with the generated text as the query
params = {'query': keywords}
response = requests.get(url, headers=headers, params=params)

# Step 5: Blog Post Formatting
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    photo_data = response.json()

    # Extract the image URL from the response (use the first result)
    if photo_data and 'results' in photo_data and len(photo_data['results']) > 0:
        image_url = photo_data['results'][0]['urls']['regular']
    else:
        st.warning("No matching images found.")
        image_url = None

    # Display generated text
    st.header(keywords)
    st.subheader("Main Headings")
    for paragraph in paragraphs[1:]:
        st.markdown(f"**{paragraph.split('.')[0].strip()}**")
    # Display Introduction
    st.subheader("Introduction")
    st.write(introduction)

    # Display Body
    st.subheader("Body")
    for paragraph in body:
        st.write(paragraph)

    # Display Conclusion
    st.subheader("Conclusion")
    st.write(conclusion)
   
    # Step 6: Image Integration
    # Display generated image
    st.header("Generated Image")
    if image_url:
        st.image(image_url, caption='Generated Image', use_column_width=True)
else:
    # Handle the case when the request to Unsplash API is not successful
    st.error(f"Failed to fetch image from Unsplash. Status Code: {response.status_code}")
