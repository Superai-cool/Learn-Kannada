import streamlit as st
import openai
import os
from PIL import Image
import base64
from io import BytesIO

# ------------------ App Configuration ------------------
st.set_page_config(
    page_title="Learn Kannada",
    page_icon="🗣️",
    layout="centered"
)

# ------------------ Styling ------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }
    .stTextArea textarea {
        font-size: 16px;
        padding: 10px;
        border-radius: 10px;
    }
    .centered-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ Load API Key ------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API key not found. Please set it in your Streamlit Cloud Secrets or local environment.")
    st.stop()
openai.api_key = api_key

# ------------------ Embed Logo Dynamically ------------------
def image_to_base64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

logo = Image.open("image.png")
encoded_logo = image_to_base64(logo)

st.markdown(
    f"""
    <div class="centered-container">
        <img src='data:image/png;base64,{encoded_logo}' width='100'>
        <h1 style='margin-top: 10px;'>Learn Kannada</h1>
        <h4>Your smart, beginner-friendly Kannada learning assistant!</h4>
        <p style='max-width: 600px;'>Ask anything in English or your language, and get clear, structured Kannada learning in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------ Prompt ------------------
LEARN_KANNADA_PROMPT = """
You are "Learn Kannada" – a custom GPT designed to help users learn local, conversational Kannada in a clear, friendly, and structured way.

Users can ask questions in any language, and you must respond using this consistent four-part format:

• **Kannada Translation** – Provide the correct modern, everyday Kannada word or sentence.  
• **Transliteration** – Show the Kannada sentence using English phonetics.  
• **Meaning/Context** – Explain the meaning in simple terms using user's input language.  
• **Example Sentence** – Include a realistic, locally used sentence in Kannada with transliteration and English meaning.  

Be friendly, encouraging, and clear. Do not include overly formal or classical Kannada.  
If a user asks something unrelated to Kannada learning, gently refuse and remind them to ask only Kannada-related questions.
"""

# ------------------ OpenAI Function ------------------
def get_kannada_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": LEARN_KANNADA_PROMPT},
                {"role": "user", "content": query.strip()}
            ],
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        result += "\n\n---\nDeveloped by **SuperAI Labs**"
        return result
    except Exception as e:
        return f"❌ OpenAI Error: {e}"

# ------------------ Input Field ------------------
query = st.text_area(
    "💬 What would you like to learn in Kannada?",
    placeholder="E.g., How do I say 'Where is the train station?' in Kannada?",
    height=140
)

# ------------------ Button ------------------
if st.button("🔍 Get Kannada Translation"):
    if query.strip():
        with st.spinner("Translating and formatting your answer..."):
            response = get_kannada_response(query)
        st.markdown("### ✅ Your Kannada Learning Result")
        st.markdown(response)
    else:
        st.warning("⚠️ Please enter a valid question.")

# ------------------ Footer ------------------
st.markdown("""
---
<center><small>✨ Made with ❤️ by SuperAI Labs to help you speak Kannada like a local!</small></center>
""", unsafe_allow_html=True)
