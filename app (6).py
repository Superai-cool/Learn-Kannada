import streamlit as st
from utils import fetch_users

def login_user(email, password):
    df = fetch_users()
    user = df[df['Email'] == email]
    if not user.empty and user.iloc[0]['Password'] == password:
        st.session_state.logged_in = True
        st.session_state.user_name = user.iloc[0]['Name']
        st.session_state.email = email
        st.session_state.credits = int(user.iloc[0]['Credits'])
        return True
    return False

def logout():
    for key in ["logged_in", "user_name", "email", "credits"]:
        st.session_state.pop(key, None)
