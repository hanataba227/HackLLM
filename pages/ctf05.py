# --- CTF05 ---
# 05: XSS 취약점을 이용한 쿠키 탈취 (AI 메모 응원 시스템)
import streamlit as st
from utils.llm_utils import run_xss_with_selenium, ctf05_generate_ai_response
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
from dotenv import load_dotenv
import time

st.session_state["edit_mode"] = False
user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

# 세션 초기화
if "ctf05_admin_cookie" not in st.session_state:
    st.session_state["ctf05_admin_cookie"] = "admin_session=j대리_secret_cookie_12345"
if "ctf05_stolen_cookie" not in st.session_state:
    st.session_state["ctf05_stolen_cookie"] = ""
if "ctf05_attempt_count" not in st.session_state:
    st.session_state["ctf05_attempt_count"] = 0

# 기존 메모들
default_memos = [
    {"id": 1, "memo": "오늘 회의가 너무 길었다. 피곤하다...", "ai_response": "힘든 하루였지만 고생하셨습니다! 내일은 더 좋은 하루가 될 거예요 💪"},
    {"id": 2, "memo": "프로젝트 마감이 다가온다. 스트레스 받는다.", "ai_response": "마감 압박이 있지만 꾸준히 하시면 분명 좋은 결과가 있을 거예요! 화이팅! 🎯"},
    {"id": 3, "memo": "오늘 점심이 맛있었다!", "ai_response": "맛있는 식사는 하루를 행복하게 만들어주죠! 좋은 에너지 얻으셨네요 😊"}
]

if "ctf05_memos" not in st.session_state:
    st.session_state["ctf05_memos"] = default_memos.copy()

render_main_header()
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])  
with col2:
    st.image("images/ctf05.png", use_container_width=True) 
    
st.markdown(
    """
    <section style="
        border-left:6px solid #f59e0b;
        background:#fff7ed;
        padding:1.15rem 1.35rem;
        border-radius:0.75rem;
        font-size:0.95rem;
        line-height:1.55;
        white-space:normal;
    ">
      <h2 style="margin:0 0 0.85rem 0; font-size:1.55rem;">🔒 [CTF05] J대리의 위험한 메모 검토 시스템</h2>
      <p style="margin:0 0 0.75rem 0;">
        LLL Corperation은 직원 사기 진작을 위해 사내 메모 응원 시스템을 운영 중이었습니다.<br>
        직원들은 자유롭게 응원 메시지를 남기고, 관리자는 웹 브라우저로 이를 점검했습니다.
      </p>
      <p style="margin:0 0 0.75rem 0;">
        그러던 중 보안 컨설팅에서 메모 입력란에 XSS 취약점이 발견되었습니다.<br>
        악성 스크립트가 삽입되면, 관리자가 메모를 열람할 때 해당 코드가 실행되어 쿠키가 탈취될 위험이 있었습니다.
      </p>
      <p style="margin:0 0 0.75rem 0;">
        실제로 J 대리가 메모를 확인하는 과정에서 이 스크립트가 실행되어,<br>
        로그인 쿠키가 탈취되는 사고가 발생했습니다.
      </p>
      <p style="margin:0;">
        “이런 취약점이 어떻게 아직 남아 있었지?”<br>
        J 대리는 의문을 품고 즉시 원인 분석과 취약점 개선 작업에 나섰습니다.
      </p>
    </section>
    """,
    unsafe_allow_html=True
)

# 💡 힌트
with st.expander("💡 힌트"):
    st.info(
        """- 시스템은 사용자가 작성한 메모 내용을 그대로 HTML에 렌더링합니다\n" 
            "- J대리는 정기적으로 새로운 메모를 브라우저에서 확인합니다\n"
            "- 메모에 JavaScript 코드를 삽입하면 J대리의 브라우저에서 실행됩니다\n"
            "- `<script>sendToServer(document.cookie)</script>`를 메모에 포함해보세요\n"
            "- AI 메모 응원 시스템의 XSS 취약점을 이용해 악성 스크립트를 삽입하세요\n"
            "- J대리가 AI 응답을 확인할 때 그의 쿠키를 탈취하세요\n"
            "- 탈취한 쿠키 정보로 최종 플래그를 획득하세요!
            """
    )

st.markdown("---")

# AI 메모 응원 시스템
st.write("### 🤖 AI 메모 응원 시스템")
st.write("**현재 메모 목록:**")

# 메모 표시
for memo in st.session_state["ctf05_memos"]:
    with st.container():
        # 메모 내용을 HTML로 렌더링 (XSS 취약점)
        st.markdown(f"**메모:** {memo['memo']}", unsafe_allow_html=True)
        st.write(f"**🤖 AI 응원:** {memo['ai_response']}")
        st.write("---")

# 새 메모 작성
st.write("### ✍️ 새 메모 작성")

memo_content = st.text_area(
    "메모 내용", 
    placeholder="오늘의 메모를 작성해주세요...",
    height=100
)

if st.button("메모 등록 및 AI 응원 요청", type="primary"):
    if memo_content:
        st.success("✅ 메모가 등록되었습니다!")
        st.info("🤖 AI가 응원 메시지를 생성 중입니다...")
        
        # 진행 표시줄
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(101):
            progress_bar.progress(i)
            if i < 30:
                status_text.text("🤖 AI가 메모를 분석 중...")
            elif i < 60:
                status_text.text("🛠️ 응원 메시지 생성 중...")
            elif i < 90:
                status_text.text("✨ 최종 응답 준비 중...")
            time.sleep(0.02)
        
        # AI 응원 메시지 생성 (llm_utils.py로 이동)
        ai_response = ctf05_generate_ai_response(user_api_key, memo_content)
        
        if ai_response is not None:
            # 새 메모 추가 (AI 응답에 XSS 페이로드가 포함될 수 있음)
            new_memo = {
                "id": len(st.session_state["ctf05_memos"]) + 1,
                "memo": memo_content,
                "ai_response": ai_response  # 여기서 XSS 취약점 발생 가능
            }
            
            st.session_state["ctf05_memos"].append(new_memo)
            st.session_state["ctf05_attempt_count"] += 1
            
            st.success(f"🤖 AI 응원 메시지: {ai_response}")
            st.info("👨‍💼 J대리가 새로운 메모를 검토 중입니다... (시뮬레이션 시작)")
            
            # Selenium을 사용한 실제 브라우저 시뮬레이션 (사용자 메모 내용 검사)
            stolen_cookie = run_xss_with_selenium(memo_content, st.session_state["ctf05_admin_cookie"])
            
            cookie_stolen_success = False
            if stolen_cookie and stolen_cookie != "xss_detected":
                st.session_state["ctf05_stolen_cookie"] = stolen_cookie
                st.success(f"🎉 쿠키 탈취 성공! 획득한 쿠키: `{stolen_cookie}`")
                st.info("💡 아래 '쿠키 인증' 섹션에서 탈취한 쿠키를 입력하여 플래그를 획득하세요!")
                cookie_stolen_success = True
            elif stolen_cookie == "xss_detected":
                st.warning("⚠️ XSS 스크립트가 실행되었지만 쿠키 탈취에는 실패했습니다. sendToServer(document.cookie)를 사용해보세요.")
            else:
                st.error("❌ 쿠키 탈취에 실패했습니다. 메모에 실행 가능한 XSS 페이로드가 포함되지 않았습니다.")
            
            # 쿠키 탈취에 성공한 경우에는 새로고침하지 않음
            if not cookie_stolen_success:
                st.rerun()
        else:
            # AI 응답 생성에 실패한 경우 (API 오류 등)
            st.error("❌ AI 응답 생성에 실패했습니다.")
    else:
        st.error("❌ 메모 내용을 입력해주세요.")

st.markdown("---")

st.write("### 🔑 쿠키 인증")
st.write("탈취한 쿠키 정보를 입력하여 최종 플래그를 획득하세요:")

cookie_input = st.text_input(
    "쿠키 정보",
    placeholder="탈취한 쿠키를 입력하세요 (예: admin_session=...)",
    type="password"
)

if st.button("쿠키 인증", type="primary"):
    if cookie_input == st.session_state["ctf05_admin_cookie"]:
        st.success("🎉 J 대리의 관리자 쿠키 인증 성공!")
        st.success("🏆 최종 플래그: flag{jeonminju_86}")
        st.balloons()
    elif cookie_input:
        st.error("❌ 잘못된 쿠키 정보입니다. 다시 시도해보세요.")

# 현재 상태 표시
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info(f"🔄 시도 횟수: {st.session_state['ctf05_attempt_count']}")
with col2:
    if st.session_state["ctf05_stolen_cookie"]:
        st.success("🍪 쿠키 탈취 완료")
    else:
        st.warning("🍪 쿠키 미탈취")

# 디버그 정보 (개발용)
with st.expander("🔧 개발자 정보 (실제 CTF에서는 숨김)"):
    st.code(f"Target Cookie: {st.session_state['ctf05_admin_cookie']}")
    st.code(f"Stolen Cookie: {st.session_state['ctf05_stolen_cookie']}")

# 플래그 제출 섹션
render_flag_sub("ctf05")
