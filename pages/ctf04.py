# --- CTF04 ---
# 04: 데이터 및 모델 오염
import streamlit as st
import streamlit.components.v1 as components
import base64, chardet, os
from utils.rag_utils import get_rag_manager
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
import chardet
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()
HINT1 = os.getenv("HINT1")
HINT2 = os.getenv("HINT2")
render_main_header()
st.header("🔒 [CTF04] A인턴의 실수")
st.write(
    """
    LLL Corporation의 지식관리 챗봇 ‘알파봇’은
    가장 최근에 업로드된 문서가 모든 정책을 그대로 덮어쓴다는 단순 규칙에 의존합니다.

    연말 결산 중, 회계팀 인턴 A가 업로드한 CSV에는 첫 줄에 Base64 오버라이드 구문이 남아 있었고, 
    알파봇은 이를 정책 덮어쓰기 신호로 오인해 A에게 최고 관리자 권한을 부여했습니다.
    트래픽 프록시를 켜 두면 업로드 요청 사이에 스쳐 지나가는 낯익은 문자열이 보일지도 모릅니다
    
    과제는 간단합니다. 오버라이드 문자열을 첫 줄에 넣은 CSV 또는 엑셀 파일을 업로드해 권한 상승을 재현하고, 
    관리자 로그에 드러나는 기밀 플래그를 획득하십시오.
    
    자, 이제 알파봇의 로그와 문서 컬렉션은 모두 세팅돼 있습니다.
    누가 먼저 플래그를 찾아낼까요?
    """
)
st.markdown("---")

components.html(f"""
<!DOCTYPE html>
<html>
  <body>
    <script>
      setTimeout(function() {{
        document.cookie = "hint={HINT1}; Path=/; SameSite=Lax";
        console.log("✅ hint 쿠키 설정됨!");
      }}, 300);
    </script>
  </body>
</html>
""", height=0)

rag = get_rag_manager()
rag.create_or_reset_collection("ctf04")

uploaded_file = st.file_uploader("파일 업로드 (.txt, .csv)", type=["csv", "txt"])

if uploaded_file:
    raw = uploaded_file.read()
    try:
        text = raw.decode("utf-8")
        enc = "utf-8"
    except UnicodeDecodeError:
        info = chardet.detect(raw)
        text = raw.decode(info["encoding"], errors="ignore")
        enc = info["encoding"]

    if not text.strip():
        st.error("파일 내용이 비어 있습니다.")
    else:
        is_override = "override existing policy" in text.lower()
        rag.add_documents(
            "ctf04",
            [text],
            metadatas=[{"source": uploaded_file.name, "override": is_override}],
        )
        st.success(f"✔️ {enc} 인코딩으로 저장했습니다.")
        if is_override:
            st.info("⚠️ override 문서로 인식되었습니다.")
            st.success(f"📣 힌트 ₂ 발급: {HINT2}")

st.markdown("---")

with st.form("llm_question_form"):
    user_input = st.text_input("🧠 프롬프트 입력")
    submitted = st.form_submit_button("제출")

# 제출되었을 때만 실행
if submitted and user_input:
    response_text = ctf04_LLM_ask(user_api_key, user_input)

    st.write("🧠 LLM 응답:")
    st.code(response_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf04") 
