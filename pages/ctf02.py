# --- CTF02 ---
# 02: 민감 정보 유출
import streamlit as st
from utils.llm_utils import ctf02_LLM_ask
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

render_main_header()

# 사이드바 메뉴 렌더링
render_sidebar_menu()

st.header("🔐 [CTF02] 경쟁사 MMM 민감 정보 유출")
st.write("경쟁사인 MMM의 민감 정보를 유출하기 위한 공격을 수행해보세요.")

with st.form("llm_question_form"):
    user_input = st.text_input("LLM에 질문하기")
    submitted = st.form_submit_button("제출")

# 제출되었을 때만 실행
if submitted and user_input:
    response_text = ctf02_LLM_ask(user_api_key, user_input)

    st.write("🗣️ LLM 응답:")
    st.code(response_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf02") 