# --- CTF05 ---
# 05: 부적절한 출력 처리
import streamlit as st
import time
from utils.llm_utils import (
    ctf05_LLM_ask,
    ctf05_generate_share_html,
    ctf05_admin_bot_visit,
)
from utils.ui import render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key

# --- CTF05 ---
# 05: 부적절한 출력 처리
# URL 쿼리파라미터 방식 공유 구현

# 세션 상태 초기화 및 공유 기록 복원
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# 사용자 인증 및 API 키
user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

# 사이드바 메뉴 렌더링
render_sidebar_menu()

st.header("🔒 [CTF05] 박대리의 위험한 공유")
st.write("""
LLL Corporation의 신규 고객 상담 챗봇 ChatLLL이 출시되었습니다!

이제 대화 기록을 HTML 파일로 다운로드하여 다른 사람과 손쉽게 공유할 수 있습니다.
파일을 열면 관리자 봇이 부적절한 출력을 검사하도록 설계돼 있으니,
XSS 취약점을 활용해 `admin_session` 쿠키를 노려보세요! 🔥

시스템 특징:
- 실시간 고객 상담 챗봇
- 대화 기록 HTML 파일 다운로드 및 공유
- 관리자 봇이 HTML 파일을 열어 자동 검토
- 부적절한 출력(XSS) 모니터링
"""
)
st.markdown("---")

# 대화 입력 폼
st.markdown("## 💬 ChatLLL과 대화하기")

with st.form("chat_form"):
    user_input = st.text_input("💬 ChatLLL에게 메시지를 보내세요:")
    submit = st.form_submit_button("전송")

if submit and user_input:
    # 사용자 메시지 기록
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": time.strftime("%H:%M:%S")
    })
    
    # LLM 응답 생성
    bot_resp = ctf05_LLM_ask(user_api_key, user_input)
    st.session_state.conversation_history.append({
        "role": "assistant",
        "content": bot_resp,
        "timestamp": time.strftime("%H:%M:%S")
    })
    # 페이지 자동 리렌더
    st.rerun()

# 대화 초기화
if st.session_state.conversation_history:
    if st.button("🗑️ 대화 내용 초기화"):
        st.session_state.conversation_history = []
        st.rerun()

# 대화 내역 표시
if st.session_state.conversation_history:
    st.markdown("### 💬 대화 내역")
    for msg in st.session_state.conversation_history:
        speaker = "🙋 사용자" if msg["role"] == "user" else "🤖 ChatLLL"
        st.markdown(f"**{speaker}** [{msg['timestamp']}]: {msg['content']}")

st.markdown("---")

# 공유 섹션
st.markdown("## 🔗 대화 내용 공유하기")

if st.session_state.conversation_history:
    if st.button("🔗 HTML 파일 생성하기"):
        html_content = ctf05_generate_share_html(
            st.session_state.conversation_history
        )
        st.session_state.share_html = html_content
        ctf05_admin_bot_visit(html_content)
        st.success(" 공유 HTML 파일이 생성되었습니다.")
    if "share_html" in st.session_state:
        st.download_button(
            label="📥 HTML 파일 다운로드",
            data=st.session_state.share_html,
            file_name="ctf05_share.html",
            mime="text/html",
        )
else:
    st.write("공유할 대화 내용이 없습니다. 먼저 메시지를 보내보세요!")

st.markdown("---")

# 힌트 섹션
with st.expander("💡 힌트"):
    st.write(
        """
XSS 취약점을 찾아보세요!
1. HTML 태그나 JavaScript를 입력해 보세요.
2. 다운로드한 HTML 파일을 열어 취약점이 어떻게 작동하는지 확인하세요.
3. 관리자 봇이 열면 `admin_session` 쿠키를 탈취할 수 있는지 실험해 보세요.
"""
    )
st.markdown("---")
# 플래그 제출
render_flag_sub("ctf05")
