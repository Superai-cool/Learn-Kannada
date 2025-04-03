import streamlit as st
import openai
import os

# ------------------ App Configuration ------------------
st.set_page_config(
    page_title="🗣️ Learn Kannada",
    page_icon="🗣️",
    layout="centered"
)

# ------------------ Styling ------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stTextArea textarea {
        font-size: 14px;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ Load API Key ------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API key not found. Please set it in your Streamlit Cloud Secrets or local environment.")
    st.stop()
openai.api_key = api_key

# ------------------ App Header ------------------
st.title("🗣️ Learn Kannada")
st.markdown("""
##### Your smart, beginner-friendly Kannada learning assistant!
Ask anything in English or your language, and get clear, structured Kannada learning in seconds.
""")

# ------------------ Prompt ------------------
LEARN_KANNADA_PROMPT = """
You are \"Learn Kannada\" – a custom GPT designed to help users learn local, conversational Kannada in a clear, friendly, and structured way.

Users can ask questions in any language, and you must respond using this consistent four-part format:

• **Kannada Translation** – Provide the correct modern, everyday Kannada word or sentence.
• **Transliteration** – Show the Kannada sentence using English phonetics.
• **Meaning/Context** – Explain the meaning in simple terms using user's input language.
• **Example Sentence** – Include a realistic, locally used sentence in Kannada with transliteration and English meaning.

Be friendly, encouraging, and clear. Do not include overly formal or classical Kannada.
If a user asks something unrelated to Kannada learning, gently refuse and remind them to ask only Kannada-related questions.
"""

# ------------------ Function ------------------
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
        result += "\n\n---\nDeveloped by **SuperAI labs**"
        return result
    except Exception as e:
        return f"❌ OpenAI Error: {e}"

# ------------------ App Body ------------------
query = st.text_area(
    "💬 What would you like to learn in Kannada?",
    placeholder="E.g., How do I say 'Where is the train station?' in Kannada?",
    height=140
)

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
