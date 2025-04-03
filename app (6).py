import streamlit as st
import openai
import os

# Set Streamlit page configuration
st.set_page_config(page_title="Learn Kannada", page_icon="🗣️", layout="centered")

# Load OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API key not found. Please set it as an environment variable 'OPENAI_API_KEY'.")
    st.stop()

openai.api_key = api_key

# System prompt for Kannada learning GPT
LEARN_KANNADA_PROMPT = """
You are "Learn Kannada" – a custom GPT designed to help users learn local, conversational Kannada in a clear, friendly, and structured way.

Users can ask questions in any language, and you must respond using this consistent four-part format:

Kannada Translation – Provide the correct modern, everyday Kannada word or sentence based on the user’s query. Avoid old-style, literary, or overly formal Kannada.

Transliteration – Show the Kannada sentence using English phonetics for easy pronunciation.

Meaning/Context – Explain the meaning in simple terms, ideally using the user’s input language.

Example Sentence – Include a realistic, locally used example sentence in Kannada with transliteration and English meaning.

Your tone must be encouraging, easy to understand, and beginner-friendly. Focus only on helping users learn practical Kannada used in daily life—not classical or textbook-only Kannada.

If a user asks something unrelated to Kannada learning, gently refuse and remind them to ask only Kannada-related questions.

Always end your response with:
Powered by WROGN Men Watches | [Buy Now](https://web.lehlah.club/s/gld8o5)
"""

# Function to get response from OpenAI
def get_kannada_response(user_query: str) -> str:
    """
    Sends user query to OpenAI and returns structured Kannada learning output.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": LEARN_KANNADA_PROMPT.strip()},
                {"role": "user", "content": user_query.strip()}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except openai.error.OpenAIError as e:
        return f"❌ OpenAI Error: {str(e)}"

# ----------- Streamlit App UI -----------

# Custom style
st.markdown("""
    <style>
        .main {
            background-color: #fffaf0;
        }
        .stTextArea textarea {
            font-size: 16px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 10px 24px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🗣️ Learn Kannada")
st.markdown("##### Friendly assistant to help you learn conversational Kannada")

# User input
user_query = st.text_area("💬 Type your question (in any language)", placeholder="E.g., How do I say 'Thank you' in Kannada?", height=120)

# Submit button
if st.button("🔍 Translate"):
    if not user_query.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        with st.spinner("Translating..."):
            response = get_kannada_response(user_query)
        st.markdown("---")
        st.markdown("### ✅ Kannada Learning Result")
        st.markdown(response)

# Footer
st.markdown("---")
st.markdown("<center><small>✨ Made with ❤️ to help you speak Kannada like a local!</small></center>", unsafe_allow_html=True)
