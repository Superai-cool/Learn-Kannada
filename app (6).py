import streamlit as st
from auth import login_user, logout
from utils import update_credits
from your_easyreply_code import main_easyreply_ui

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to EasyReply")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(email, password):
            st.success(f"Welcome, {st.session_state.user_name}!")
            st.rerun()
        else:
            st.error("Invalid email or password.")
else:
    st.markdown(f"👋 Welcome **{st.session_state.user_name}** | Remaining Credits: `{st.session_state.credits}`")

    if st.session_state.credits > 0:
        main_easyreply_ui()

        if st.session_state.reply:
            st.session_state.credits -= 1
            update_credits(st.session_state.email, st.session_state.credits)
    else:
        st.warning("⚠️ You have no credits left. Please contact admin.")

    if st.button("Logout"):
        logout()
        st.rerun()
