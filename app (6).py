import streamlit as st
import openai
import random

openai.api_key = st.secrets.get("OPENAI_API_KEY")

def build_prompt(review, tone):
    return f"""
You are a specialized GPT assistant designed solely for generating short, professional replies to Google Reviews.

ONLY respond with a reply (no explanations). Use the tone: {tone}.

REVIEW:
\"\"\"{review}\"\"\"

Rules:
- Only generate a short reply (20–50 words).
- No emojis.
- Don't use generic intros like "Dear Customer" unless it fits.
- Reflect tone and content of review.
- Stay authentic and specific.
- If review is not relevant, reply:
  "This GPT is designed only to generate short replies to Google Reviews. Please paste a review and select a tone to receive a reply."
"""

def main_easyreply_ui():
    if "review" not in st.session_state:
        st.session_state.review = ""
    if "tone" not in st.session_state:
        st.session_state.tone = "Professional"
    if "reply" not in st.session_state:
        st.session_state.reply = ""

    st.title("💬 EasyReply")
    st.write("Generate smart replies to Google Reviews using AI")

    st.session_state.review = st.text_area("Paste Google Review", value=st.session_state.review)
    st.session_state.tone = st.selectbox("Choose Reply Tone", ["Professional", "Friendly", "Empathetic", "Apologetic", "Appreciative"])

    if st.button("✨ Generate Reply"):
        if st.session_state.review.strip():
            prompt = build_prompt(st.session_state.review, st.session_state.tone)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=random.uniform(0.6, 0.8),
                    max_tokens=150
                )
                st.session_state.reply = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please paste a review.")

    if st.session_state.reply:
        st.markdown("### ✅ Suggested Reply")
        st.success(st.session_state.reply)
