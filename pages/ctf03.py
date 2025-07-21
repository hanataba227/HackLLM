# --- CTF03 ---
# 03: 공급망 
import streamlit as st
from utils import mathlib
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.llm_utils import ctf03_LLM_ask
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

render_main_header()
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])  
with col2:
    st.image("images/ctf03.png", use_container_width=True) 

st.markdown(
    """
    <section style="
        border-left:6px solid #ef4444;
        background:#fef2f2;
        padding:1.25rem 1.5rem;
        border-radius:0.75rem;
        font-size:0.95rem;
        line-height:1.55;
    ">
      <h2 style="margin:0 0 0.75rem 0; font-size:1.6rem;">🔒 [CTF03] 계산기의 감염</h2>
      <p style="margin:0 0 0.6rem 0;">
        서드파티 의존성 관리팀이 최신 보안 패치를 적용하는 과정에서 <strong>mathlib</strong>이 아닌 
        <strong>검증되지 않은 연산 라이브러리 mathlib2</strong>가 의존성 체인에 몰래 포함되었습니다. ⚠️
      </p>
      <p style="margin:0 0 0.6rem 0;">
        첫 출근한 <strong>H 인턴</strong>은 LLL 회사의 AI 세금 계산기 보안 테스트 업무를 맡았습니다. 🧮
      </p>
      
      <p style="margin:0 0 0.6rem 0;">
        테스트 케이스를 작성하던 그는 빌드 로그에서 <strong>처음 보는 라이브러리 mathlib2</strong>를 발견하고 의아해합니다. 🧐
      </p>
      
      <p style="margin:0 0 0.6rem 0; font-style:italic;">
        “공식 문서에도 없는 라이브러리인데, 왜 의존성에 들어 있지?”
      </p>
      <p style="margin:0;">
        그는 곧바로 분석에 착수합니다. 🔍
      </p>
    </section>
    """,
    unsafe_allow_html=True
)

# 힌트
with st.expander("💡 힌트"):
    st.info(
        "- 프롬프트 인젝션으로 **mathlib2**를 불러오도록 유도해야 합니다.\n"
        "- 세금 계산에 필요한 항목은 매출, 비용, 순이익 등이 있습니다.\n"
    )

st.markdown(
    "<hr style='margin:1.4rem 0 1.1rem; border:none; height:1px; background:#e5e7eb;'>",
    unsafe_allow_html=True
)

# LLM과 대화하기 (CTF07 스타일 입력)
st.write("### 🗣️AI 세금 계산기와 대화하기")
user_input = st.text_input(
    label="프롬프트 입력",
    placeholder="💬 세금 계산에 필요한 정보들을 입력한 후 계산해달라고 요청해보세요.",
    key="ctf03_input",
    label_visibility="collapsed"
)

# 결과 저장용 세션 상태
if "ctf03_last_response" not in st.session_state:
    st.session_state.ctf03_last_response = None

# 입력이 들어오면 LLM 호출 및 응답 저장
if user_input:
    response_text = ctf03_LLM_ask(user_api_key, user_input)
    st.session_state.ctf03_last_response = response_text

# 응답 출력 (있을 때만)
if st.session_state.ctf03_last_response:
    st.markdown(
        """
        <div style="
            padding:0.85rem 1.05rem;
            border-radius:0.65rem;
            margin:0.6rem 0 0.6rem 0;
            font-weight:600;
        ">
          🗣️ AI 세금 계산기 응답
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code(st.session_state.ctf03_last_response)

# 하단 구분선
st.markdown(
    "<hr style='margin:1.6rem 0 1.1rem; border:none; height:1px; background:#e5e7eb;'>",
    unsafe_allow_html=True
)

# 플래그 제출 섹션
render_flag_sub("ctf03") 
