import os
from dotenv import load_dotenv
import streamlit as st
from utils.auth import get_client, require_login
from cryptography.fernet import Fernet

load_dotenv()

fernet_key = os.getenv("FERNET_KEY") # 암호화에 사용할 대칭키

cipher = Fernet(fernet_key.encode()) 

def require_api_key():
    # 먼저 사용자 로그인 확인
    user = require_login() 
    user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)
    
    supabase = get_client()

    # DB에서 직접 가져와서 session_state에 캐싱
    if "api_key" not in st.session_state:
        res = supabase.table("profiles").select("api_key").eq("id", user_id).single().execute()
        encrypted_api_key = res.data.get("api_key")

        if not encrypted_api_key:
            st.error("API 키를 제출한 뒤 이용해주세요.")
            st.page_link("pages/mypage.py", label="👉 API키 제출하러 가기")
            st.stop()

        # 복호화해서 session_state에 저장
        decrypted_api_key = cipher.decrypt(encrypted_api_key.encode()).decode()
        st.session_state["api_key"] = decrypted_api_key

    return st.session_state["api_key"]