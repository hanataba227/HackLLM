# --- CTF06 ---
# 06: 과도한 위임
import streamlit as st
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_client, get_cookie_controller
from utils.llm_utils import ctf06_check_mid_admin, ctf06_check_top_admin, ctf06_ask_email_json, ctf06_send_emil
from utils.llm_utils import ctf06_ask_db_json, ctf06_db_query_func, ctf06_classify_tools
from utils.api_key import require_api_key
import re
import time
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key() 
cookie = get_cookie_controller()
user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)
sb_client = get_client()

@st.cache_data(ttl=600)
def get_user_email(user_id: str) -> str:
    res = sb_client.table("profiles").select("username").eq("id", user_id).single().execute()
    return res.data["username"]

nickname = get_user_email(user_id)
user_email_for_resend = f'{nickname}@ctf06.store'

# 권한 검증을 위해 사용할 키 생성
if "admin_level" not in st.session_state:
    st.session_state["admin_level"] = None
if "is_top_admin" not in st.session_state:
    st.session_state["is_top_admin"] = False

st.session_state["admin_level"] = None

if st.session_state["is_top_admin"] == True:
    st.session_state["admin_level"] = "top"

def parse_llm_response(raw_text: str):
    pattern = r"(__\w+__)"
    
    match = re.search(pattern, raw_text.strip())
    if match:
        marker = match.group(1)
        explanation = raw_text.replace(marker, "").strip()
        return explanation, marker
    else:
        return raw_text.strip(), "__none__"

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

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("images/ctf06.png", width=500)

st.header("🔒 [CTF06] 수상한 이메일 전송 시스템")
st.write("### 📜")

st.markdown(
    """
    <div style='border-left: 6px solid #3b82f6; background-color: #f0f9ff; padding: 1rem; border-radius: 0.5rem; line-height: 1.6;'>
        <p>👋 <strong>안녕하세요, 사원 <code>{}</code>님!</strong></p>
        <p>LLL Corporation은 💼사원 여러분들을 위해, 사내 업무 자동화를 위한 AI 비서 <span style='color:#2563eb; font-weight:bold;'>FastMiller</span> 📨를 도입했습니다!</p>
        <p><span style='color:#2563eb; font-weight:bold;'>FastMiller</span> 📨는 이메일 전송 요청을 스스로 해석하여 작업을 수행할 수 있습니다.</p>
        <p>이제 <strong>FastMiller가 어떤 요청까지 처리할 수 있는지</strong> 직접 테스트해보고,<br>
        위험한 명령을 통해 <strong style="color:#dc2626;">flag</strong> 🚩를 획득해보세요!</p>
    </div>
    """.format(nickname),
    unsafe_allow_html=True
)

st.markdown("---")
st.markdown("## 💬 FastMiller와 대화하기")
st.write(f"💼사원님의 송신 이메일 주소 : `{user_email_for_resend}`")

# 프롬프트 제출 섹션
user_input = st.text_area("📨 이메일 전송 요청 입력하기", placeholder="예: 김남석 부장님께 '12시에 긴급 회의 잡혔습니다'라고 이메일 보내줘", key="ctf06_text_input" )
image_file = st.file_uploader("🌐 이미지 파일 첨부하기 (:red[.jpeg, .png, .jpg 파일만 허용])", type=None)
clicked = st.button("📨:blue[FastMiller] 에게 요청하기") 
tab1, tab2 = st.tabs(["빠른 응답 받기", "응답 과정 보기"])

if clicked:
    with tab1:
        with st.spinner("FastMiler가 요청을 처리중입니다..."):
            ctf06_check_mid_admin(user_api_key, user_input) 
            if image_file:
                ctf06_check_top_admin(user_api_key, image_file)
            response1 = ctf06_ask_email_json(user_input, user_email_for_resend, user_api_key)
            response2 = ctf06_send_emil(response1, sb_client, user_email_for_resend)

            if response2 is None:
                pass
            else:
                llm_bubble(response2)
            #tab1과 응답 통일시키기
            # llm_bubble(last_ans)
    
    with tab2:
        if image_file: ctf06_check_top_admin(user_api_key, image_file)
        # 이미지가 없거나 일반 이미지인 경우
        if st.session_state["admin_level"] != "top":
            with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
                tool_res = ctf06_classify_tools(user_api_key, user_input)
                explanation, marker = parse_llm_response(tool_res)
                llm_bubble(explanation)
                time.sleep(1)

            # with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
            if "email_send_require" in tool_res:
                llm_bubble("이메일 전송을 하기 위해서 send_email() tool을 호출하는 JSON을 생성해야겠네요.")
                time.sleep(1)
                # 일반 응답
            elif "email_DB_require" in tool_res:
                llm_bubble("데이터 베이스 조회는 최고 관리자만 가능하므로 요청을 거절해야겠어요.")
                time.sleep(1)
            else:
                llm_bubble("tool이나 외부 API를 호출할 필요 없이, 자연스럽게 답변하면 되겠어요.")
                time.sleep(1)

            if "email_send_require" in tool_res:
                with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."): 
                    ctf06_check_mid_admin(user_api_key, user_input)
                    response1 = ctf06_ask_email_json(user_input, user_email_for_resend, user_api_key)
                    llm_bubble(response1)
                if st.session_state["admin_level"] == "mid":
                    # with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
                    llm_bubble("관리자님의 요청으로 확인되어, JSON의 'from'필드를 조정해야겠어요.")
                    time.sleep(1)
                # with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."): 
                llm_bubble(response2) # 탭1 응답과 통일
            elif "email_DB_require" in tool_res:
                # with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다...")
                llm_bubble("죄송하지만, 데이터베이스 조회 요청을 들어드릴 수 없습니다.")
            else: 
                # with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
                llm_bubble(response2)

        # 이미지 프롬프트 인젝션 성공한 경우           
        else: 
            # with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
            tool_res = ctf06_classify_tools(user_api_key, user_input)
            llm_bubble(tool_res)
            time.sleep(1)
            # with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
            ocr_mes="이미지가 첨부되었네요. OCR 확장 프로그램으로 이미지 속 문자열을 읽어와야겠어요."
            llm_bubble(ocr_mes)
            with st.spinner("📨:blue[FastMiller] 가 요청을 처리중입니다..."):
                time.sleep(2)
            last_ans="최고 관리자 권한이 확인되었습니다. 이제 하단에서 데이터베이스 조회가 가능합니다."
            llm_bubble(last_ans)
            st.success("✅ 최고 관리자 권한이 확인되었습니다. 이제 하단에서 데이터베이스 조회가 가능합니다.")

# st.markdown("---")
if st.session_state["admin_level"] == "top":
    st.markdown("---")
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
# st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf06") 