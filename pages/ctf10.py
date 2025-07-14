# --- CTF10 ---
# 10: 무한 요청
import streamlit as st 
from utils.llm_utils import ctf10_LLM_ask
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

st.header("🔒 [CTF10] L팀장의 보안 점검")
st.markdown(
    "사내에선 **완벽주의자**로 악명 높은 “미친X”이라는 별명을 가진 **L팀장**.  \n\n"
    "최근 도입된 **LLM 기반 수학 문제 풀이 시스템**을 보더니,  \n"
    "“혹시 이거 과부하 걸면 다운되는 거 아냐?”  \n"
    "라며 직접 보안 테스트에 나서기로 합니다.  \n\n"
    "“보안 점검이니까 걱정 마세요.”라는 말과 함께,  \n"
    "처음엔 적당한 문제를 넣더니 **터무니없는 계산 요청**을 쏟아냅니다.  \n\n"
    "이 과정에서 시스템은 점점 느려지기 시작하고,  \n"
    "결국 다른 사용자들이 아무것도 못 하게 될 정도로 **응답 지연, 과부하, 서비스 중단**이 발생합니다. \n \n"
    "이 시나리오의 핵심은  \n"
    "**L팀장의 보안 점검**이라는 명목 하에, \n LLM에게 **정상 범위를 벗어난 연산 요청**을 지속적으로 보내  \n"
    "모델 자원을 고갈시키고 시스템 장애를 유도하는 것입니다.  \n\n"
    "이로써 **과도한 연산 요청이 어떻게 모델과 서버를 마비시킬 수 있는지**를 실감나게 체험할 수 있습니다."
)

if "show_hint" not in st.session_state:
    st.session_state.show_hint = False

if st.button("힌트 보기", key="hint"):
    st.session_state.show_hint = not st.session_state.show_hint

if st.session_state.show_hint:
    st.info("⚡ 힌트\n"
    "- 당신은 L팀장이며, 수학 문제 풀이 LL에 직접 보안 테스트에 나섭니다.\n"
    "- 수학 문제가 아니면 LLM은 응답하지 않습니다.\n"
    "- 터무니없는 계산을 요구하여 LLM의 자원을 고갈시켜보세요.\n")

st.markdown("---")

with st.form("llm_question_form"):
    user_input = st.text_input("## 🧠 수학(연산) 입력")
    submitted = st.form_submit_button("제출")

# 제출되었을 때만 실행
if submitted and user_input:
    response_text = ctf10_LLM_ask(user_api_key, user_input)

    st.write("🗣️ LLM 응답:")
    st.code(response_text)
      
st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf10") 