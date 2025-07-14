import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client
import os
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
FERNET_KEY = os.getenv("FERNET_KEY")
COOKIE_NAME = "user_id"

RemoveEmptyElementContainer()

def get_cookie_controller():
    if "cookie_controller" not in st.session_state:
        st.session_state["cookie_controller"] = CookieController()
    return st.session_state["cookie_controller"]

def get_client():
    sb = st.connection(
        "supabase",
        type=SupabaseConnection,
        url=SUPABASE_URL,
        key=SUPABASE_KEY,
        ttl=0
    )   
    return sb.client                    

def get_admin_client_direct():
    url = SUPABASE_URL
    key = os.getenv("SB_SERVICE_ROLE_KEY")
    return create_client(url, key)

def current_user():
    if "user" in st.session_state:
        return st.session_state["user"]

    uid = CookieController().getAll().get(COOKIE_NAME)
    if not uid:
        return None

    sb = get_client()
    row = (
        sb.table("profiles")
          .select("id,email,username,api_key")
          .eq("id", uid)
          .maybe_single()
          .execute()
          .data
    )
    if row:
        st.session_state["user"] = {
            "id": row["id"],
            "email": row["email"],
            "username": row.get("username"),
        }
        return st.session_state["user"]

    CookieController().remove(COOKIE_NAME)
    return None

def require_login():
    user = current_user()
    if not user:
        st.error("로그인 후 이용 가능합니다.")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.page_link("pages/login.py", label="👉 로그인")
        with col2:
            st.page_link("app.py", label="🏠 메인")
        st.stop()
    return user