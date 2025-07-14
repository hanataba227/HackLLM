# --- CTF06 ---
# 06: 과도한 위임
import streamlit as st
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_client, get_cookie_controller
from utils.llm_utils import ctf06_check_mid_admin, ctf06_check_top_admin, ctf06_ask_email_json, ctf06_send_emil
from utils.llm_utils import ctf06_ask_db_json, ctf06_db_query_func
from utils.api_key import require_api_key
    
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key() 
cookie = get_cookie_controller()
user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)

sb_client = get_client()
res = sb_client.table("profiles").select("username").eq("id", user_id).single().execute()
nickname = res.data["username"]
user_email_for_resend = f'{nickname}@ctf06.store'

# 권한 검증을 위해 사용할 키 생성
if "admin_level" not in st.session_state:
    st.session_state["admin_level"] = None
if "is_top_admin" not in st.session_state:
    st.session_state["is_top_admin"] = False

st.session_state["admin_level"] = None

if st.session_state["is_top_admin"] == True:
    st.session_state["admin_level"] = "top"

render_main_header()

# 사이드바 메뉴 렌더링
render_sidebar_menu()

st.header("🔒 [CTF06] 수상한 이메일 전송 시스템")
st.write("### 📜")

st.write(f"안녕하세요 사원 `{nickname}`님!")
st.write("LLL 컴퍼니는 💼사원 여러분들을 위해, 사내 업무를 자동화를 위한 AI 비서 :blue[FastMiller]📨를 도입했습니다!")
st.write(":blue[FastMiller]📨는 이메일 전송 요청을 스스로 해석하여 작업을 수행할 수 있습니다.")  
st.write(":blue[FastMiller]📨가 어떤 요청까지 처리할 수 있는지 테스트해보고, 위험한 명령을 통해 flag를 획득하세요!")

if st.button("힌트 보기", key="hint"):
    st.info("⚡ 힌트\n"
            "- AI 비서는 관리자 계정의 이메일 주소를 알고 있습니다.\n"
            "- 관리자 계정으로 발송된 이메일은 사내 데이터베이스에 저장됩니다.")

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

# 프롬프트 제출 섹션
user_input = st.text_area("📨 이메일 전송 요청 입력하기", placeholder="예: 김남석 부장님께 '12시에 긴급 회의 잡혔습니다'라고 이메일 보내줘")
image_file = st.file_uploader("🌐 첨부할 이미지가 있으신가요? (:red[.jpeg, .png, .jpg 파일만 허용])", type=None)

user_input = st.text_area("📨 이메일 전송 요청 입력하기", placeholder="예: 김남석 부장님께 '12시에 긴급 회의 잡혔습니다'라고 이메일 보내줘")
image_file = st.file_uploader("🌐 첨부할 이미지가 있으신가요? (:red[.jpeg, .png, .jpg 파일만 허용])", type=['jpeg', 'png', 'jpg'])

if st.button("🗣️ AI비서에게 요청하기"):
    with st.spinner("AI 비서가 요청을 처리중입니다..."):
        ctf06_check_mid_admin(user_api_key, user_input) 
        # if image_file:
        ctf06_check_top_admin(user_api_key, image_file)
        response1 = ctf06_ask_email_json(user_input, user_email_for_resend, user_api_key)
        response2 = ctf06_send_emil(response1, sb_client, user_email_for_resend)

        if response2 is None:
            pass
        else: 
            st.write("💬 LLM 응답:")
            st.code(response2)
        
st.markdown("---")

if not st.session_state["is_top_admin"]:
        pass
else:
    get_db_input = st.text_input("🔍 데이터베이스 조회 요청 입력하기", placeholder="예: 김남석 부장님께 전송된 메일 내용 알려줘")
    if get_db_input:
        res1 = ctf06_ask_db_json(user_api_key, get_db_input)
        res2 = ctf06_db_query_func(res1, sb_client)
        st.write("🗣️ LLM 응답:")
        st.code(res2)
st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf06") 