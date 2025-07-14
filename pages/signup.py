# pages/signup.py
import streamlit as st
from utils.auth import get_client, current_user
from utils.ui import render_sidebar_menu

user = current_user()

render_sidebar_menu()

st.header("📝 회원가입")

supabase = get_client()

email = st.text_input("Email")
pwd   = st.text_input("Password", type="password")

if st.button("회원가입", use_container_width=True):
    try:
        supabase.auth.sign_up({"email": email, "password": pwd})
        st.success("🎉 메일 인증 후 다시 로그인해 주세요.")
    except Exception as e:
        st.error(f"가입 실패: {e}")