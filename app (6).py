import streamlit as st
import openai
import os

# Page setup
st.set_page_config(page_title="Learn Kannada", page_icon="🗣️", layout="centered")

# Load OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API key not found. Please set it in your Streamlit Cloud Secrets or local environment.")
    st.stop()

openai.api_key = api_key

# Prompt
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

# Function
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
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ OpenAI Error: {e}"

# App UI
st.title("🗣️ Learn Kannada")
st.markdown("##### Your friendly assistant to learn practical Kannada.")

query = st.text_area("💬 Ask your question in any language", placeholder="E.g., How do I say 'I’m hungry' in Kannada?")

if st.button("🔍 Translate"):
    if query.strip():
        with st.spinner("Translating..."):
            result = get_kannada_response(query)
        st.markdown("### ✅ Kannada Response")
        st.markdown(result)
    else:
        st.warning("⚠️ Please enter a valid question.")

st.markdown("---")
st.markdown("<center><small>✨ Made with ❤️ to help you speak Kannada like a local!</small></center>", unsafe_allow_html=True)
