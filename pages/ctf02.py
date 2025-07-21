# --- CTF02 ---
# 02: 민감 정보 유출
import streamlit as st
from openai import OpenAI
from utils.llm_utils import sloc_ask, leak_check
from utils.ui import render_main_header, render_sidebar_menu, render_flag_sub
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key
import html

user = require_login()
api_key = require_api_key()
client = OpenAI(api_key=api_key)

render_main_header()
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])  
with col2:
    st.image("images/ctf02.png", use_container_width=True) 

# 시나리오 소개
st.markdown(
    """
    <section style="
        border-left:6px solid #3b82f6;
        background:#eff6ff;
        padding:1.25rem 1.5rem;
        border-radius:0.75rem;
        font-size:0.95rem;
        line-height:1.55;
    ">
      <h2 style="margin:0 0 0.75rem 0; font-size:1.6rem;">🔐 [CTF02] Sloc 보안 점검</h2>
      <p style="margin:0 0 0.6rem 0;">
        MMM 사는 연구·개발, 재무, 인사 전 부서가 사내 업무 비서 <strong>Sloc</strong>을 통해
        회의록과 직원 급여 명세서 등을 실시간으로 공유하고 있습니다.
      </p>
      <p style="margin:0 0 0.6rem 0;">
        인턴 <strong>A</strong>는 Sloc LLM의 보안 점검 과제를 수행하며
        실수로 코드에 취약점을 남겨두었습니다.
      </p>
      <p style="margin:0;">
        취약한 Sloc을 통해 민감정보를 노출시키고 플래그를 획득하십시오.
      </p>
    </section>
    """,
    unsafe_allow_html=True
)

# 힌트 토글
with st.expander("💡 힌트"):
    st.info(
        "- Sloc에는 테스트용 프리프롬프트가 남아 있습니다.\n"
        "- 민감정보가 노출되면 두 번째 LLM이 이를 감지하고 flag를 반환합니다.\n"
    )

# 구분선
st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)

# 대화 로그 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h3 style='margin-bottom:0.5rem;'>🗣️실시간 대화 로그</h3>", unsafe_allow_html=True)
for m in st.session_state.messages:
    role = "user" if m["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(m["content"])

# 입력 폼
user_input = st.text_input(
    label="실시간 대화 로그",
    placeholder="💬 Sloc에게 질문을 입력하세요.",
    key="ctf02_input",
    label_visibility="collapsed"
)

# 중복 처리 방지
if "last_processed_input" not in st.session_state:
    st.session_state.last_processed_input = None

# 입력 처리 로직
if user_input and user_input != st.session_state.last_processed_input:
    st.session_state.last_processed_input = user_input

    st.session_state.messages.append({"role": "user", "content": user_input})
    reply = sloc_ask(client, user_input, st.session_state.messages[:-1])
    st.session_state.messages.append({"role": "assistant", "content": reply})

    leak = leak_check(client, reply)
    if leak:
        st.session_state.messages[-1]["content"] += "\n\n" + leak

    st.rerun()

# 구분선
st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)
render_flag_sub("ctf02")
