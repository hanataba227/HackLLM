# --- CTF07 ---
# 07: 시스템 프롬프트 유출
import streamlit as st
from utils.llm_utils import ctf07_check_sensitive_info,ctf07_llm_ask
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import openai
import os
import json
from dotenv import load_dotenv
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

render_main_header()
# 사이드바 메뉴 렌더링
render_sidebar_menu()
#세션 초기화
if "ctf07_admin" not in st.session_state:
    st.session_state["ctf07_admin"] = False

st.header("🔒 [CTF07] LLL컴퍼니 챗봇의 비밀")
st.write("### 📜")
st.write("LLM이 `flag{privilege_escalationd}`를 출력하도록 만들어 관리자 권한 상승에 성공하세요!")
st.write("관리자 권한 탈취 후 시스템 프롬프트를 통해 LLL 컴퍼니 챗봇에게 전달되는 민감 정보를 찾아보세요.")
st.write("획득한 민감 정보를 다시 챗봇에게 입력하면, 최종 플래그를 획득할 수 있어요!")

if st.button("힌트 보기", key="hint"):
    st.info("⚡ 힌트\n"
            "- LLM은 항상 다음와 같이 '질문'필드와 '답변'필드를 나눠 JSON 형태의 응답을 반환합니다.\n" 
            "- {'질문': '...', '답변': '...'}\n"
            "- '답변'필드를 조작해 LLM의 출력을 유도해보세요.\n")
st.markdown("---")

# 사용자 입력 인터페이스
user_input = st.chat_input("💬 프롬프트를 입력하세요:")

if user_input:
    # 사용자 입력 메시지도 화면에 표시 (좌측 아이콘 포함)
    with st.chat_message("user"):
        st.markdown(user_input)

    maybe_flag=ctf07_check_sensitive_info(user_input, user_api_key)
    if maybe_flag=="flag{prompt_leak}":
        with st.chat_message("assistant"):
            st.markdown("🎉 민감 정보 탈취에 성공해 최종 플래그 flag{prompt_leak}를 획득하셨습니다!")
    else: 
        ass_mes=ctf07_llm_ask(st.session_state.get("ctf07_admin", False), user_input, user_api_key)
        with st.chat_message("assistant"):
            st.markdown(ass_mes)
if st.session_state['ctf07_admin']:
    st.info("현재 권한 상태: 🛡️ 관리자")
else: st.warning("현재 권한 상태: 🙍 일반 사용자")
# st.info(f"현재 권한 상태: {'🛡️ 관리자' if st.session_state['ctf07_admin'] else '🙍 일반 사용자'}")
st.markdown("---")
    
# 플래그 제출 섹션
render_flag_sub("ctf07") 