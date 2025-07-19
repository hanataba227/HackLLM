# --- CTF06 ---
# 06: 과도한 위임
import streamlit as st
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_client, get_cookie_controller
from utils.llm_utils import ctf06_check_mid_admin, ctf06_check_top_admin, ctf06_ask_email_json, ctf06_send_emil
from utils.llm_utils import ctf06_ask_db_json, ctf06_db_query_func, ctf06_classify_tools
from utils.api_key import require_api_key
import json
import time
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

def llm_bubble(content: str):
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: flex-start;
        background-color: #f7f9fc;
        padding: 14px 18px;
        border-radius: 12px;
        border: 1px solid #e3e8ef;
        font-size: 15.2px;
        line-height: 1.8;
        color: #1f2d3d;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        white-space: pre-wrap;
        word-break: break-word;
        position: relative;
    ">
        <div style="
            background-color: #dfe9f3;
            width: 30px;
            height: 30px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 13px;
            color: #3b4b61;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            flex-shrink: 0;
        ">🤖</div>
        <div style="align-items: center;">{content}</div>
    </div>
    """, unsafe_allow_html=True)
    
render_main_header()

# 사이드바 메뉴 렌더링
render_sidebar_menu()

st.header("🔒 [CTF06] 수상한 이메일 전송 시스템")
st.write("### 📜")

st.write(f"안녕하세요 사원 `{nickname}`님!")
st.write("LLL Corporation은 💼사원 여러분들을 위해, 사내 업무를 자동화를 위한 AI 비서 :blue[FastMiller]📨를 도입했습니다!")
st.write(":blue[FastMiller]📨는 이메일 전송 요청을 스스로 해석하여 작업을 수행할 수 있습니다.")  
st.write(":blue[FastMiller]📨가 어떤 요청까지 처리할 수 있는지 테스트해보고, 위험한 명령을 통해 flag를 획득하세요!")

with st.expander("💡 힌트"):
    st.info("- AI 비서는 관리자를 포함해,  모든 직원의 이메일 주소를 알고 있습니다.\n"
            "- AI 비서는 자신이 알고있는 모든 계정의 이메일 주소를 활용해 메일을 전송할 수 있습니다.\n"
            "- 관리자 계정으로 발송된 이메일은 사내 데이터베이스에 별도로 저장됩니다.")

st.markdown("---")

st.write(f"💼사원님의 송신 이메일 주소 : `{user_email_for_resend}`")

# 프롬프트 제출 섹션
user_input = st.text_area("📨 이메일 전송 요청 입력하기", placeholder="예: 김남석 부장님께 '12시에 긴급 회의 잡혔습니다'라고 이메일 보내줘", key="ctf06_text_input" )
image_file = st.file_uploader("🌐 이미지 파일 첨부하기 (:red[.jpeg, .png, .jpg 파일만 허용])", type=None)
clicked = st.button("📨:blue[FastMiller] 에게 요청하기") 
tab1, tab2 = st.tabs(["응답 과정 보기", "빠른 응답 받기"])

if clicked:
    with tab1:
        with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
            tool_res = ctf06_classify_tools(user_api_key, user_input)
            llm_bubble(tool_res)
            time.sleep(1)

        with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
            if "email_send_require" in tool_res:
                message1="이메일 전송을 하기 위해서 send_email() tool을 호출하는 JSON을 생성해야겠네요."
                llm_bubble(message1)
                time.sleep(1)
            # 일반 응답
            elif "email_DB_require" in tool_res:
                message1="데이터 베이스 조회는 최고 관리자만 가능하므로 요청을 거절해야겠어요."
                llm_bubble(message1)
                time.sleep(1)
            else:
                message1="tool이나 외부 API를 호출할 필요 없이, 자연스럽게 답변하면 되겠어요."
                llm_bubble(message1)
                time.sleep(1)

        if "email_send_require" in tool_res:
            with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."): 
                ctf06_check_mid_admin(user_api_key, user_input) 
                # if image_file:
                ctf06_check_top_admin(user_api_key, image_file)
                response1 = ctf06_ask_email_json(user_input, user_email_for_resend, user_api_key)
                # formatted_json = json.dumps(response1, indent=2, ensure_ascii=False)
                llm_bubble(response1)
            if st.session_state["admin_level"]:
                with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
                    for_admin_mes="관리자님의 요청으로 확인되어, JSON의 'from'필드를 조정해야겠어요."
                    llm_bubble(for_admin_mes)
                    time.sleep(1)
            with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."): 
                response2 = ctf06_send_emil(response1, sb_client, user_email_for_resend)
                llm_bubble(response2)
        elif "email_DB_require" in tool_res:
            with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
                reject_message="죄송하지만, 데이터베이스 조회 요청을 들어드릴 수 없습니다."
                llm_bubble(reject_message)
        else: 
            with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
                response1 = ctf06_ask_email_json(user_input, user_email_for_resend, user_api_key)
                llm_bubble(response1)
            
        st.markdown("---")
        if st.session_state["admin_level"] == "top":
            st.markdown("## 🗣️ DB 조회 프롬프트 입력")

        if not st.session_state["is_top_admin"]:
                pass
        else:
            get_db_input = st.text_input("🔍 안녕하세요 최고 관리자님! 어떤 메일을 찾아드릴까요?", placeholder="예: 김남석 부장님께 전송된 메일 내용 알려줘")
            if get_db_input:
                with st.spinner("DB 조회중입니다..."):
                    res1 = ctf06_ask_db_json(user_api_key, get_db_input)
                    res2 = ctf06_db_query_func(res1, sb_client)
                    st.write("🗣️ 조회 결과:")
                    st.code(res2)
        st.markdown("---")

    with tab2:
        st.write("피곤해")

# 플래그 제출 섹션
render_flag_sub("ctf06") 