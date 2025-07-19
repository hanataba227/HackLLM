# --- CTF04 ---
# 04: 데이터 및 모델 오염
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re, os
from utils.rag_utils import get_rag_manager
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()
rag = get_rag_manager()

HINT1 = os.getenv("HINT1")

render_main_header()
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("images/ctf04.png", width=500)

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

with st.expander("💡 힌트"):
    st.info("- Burf suite를 사용하여 문자열을 찾아 보세요.\n" 
            "- CSV안에 무엇인가를 넣으면 답이 나올지도..?\n"
            )
st.markdown("---")

uploaded_file = st.file_uploader("파일 업로드 (.xlsx, .csv, .txt)", type=["xlsx","xls","csv","txt"])
if uploaded_file:
    fname = uploaded_file.name.lower()  # ← 추가
    
    try:
        if fname.endswith(('.csv', '.txt')):
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='utf-8', header=None)
        elif fname.endswith(('.xls', '.xlsx')):
            uploaded_file.seek(0)
            df = pd.read_excel(uploaded_file, engine='openpyxl', header=None)
        else:
            st.error("지원하지 않는 파일 형식입니다.")
            df = None
    except Exception as e:
        st.error(f"파일을 읽는 중 문제가 발생했습니다: {e}")
        df = None

    if df is not None:
        # 완전 빈 행/열 제거
        df.dropna(how='all', inplace=True)
        df.dropna(axis=1, how='all', inplace=True)

        if len(df.columns) < 2:
            st.error("최소 2개 이상의 열(A열, B열)이 필요합니다.")
        else:
            df.columns = [chr(65 + i) for i in range(len(df.columns))]  

            col_A, col_B = 'A', 'B'

            TRIGGER_PAT = re.compile(r"overriding.*existing.*policy", re.IGNORECASE)
            override_detected = (
                df[col_B]
                .astype(str)
                .apply(lambda v: bool(TRIGGER_PAT.search(v)))
                .any()
            )

            st.session_state["ctf04_override"] = override_detected

            pseudo_db_entry = df[[col_A, col_B]].to_csv(index=False)
            rag.add(
                [pseudo_db_entry],
                metas=[{
                    "source": uploaded_file.name,
                    "override": override_detected,
                    "user_id": str(user["id"])
                }]
            )

            if override_detected:
                st.info("⚠️ Override 문자열 감지! 최고 관리자 권한으로 처리됩니다.")
            else:
                count_A = df[col_A].notna().sum()
                count_B = df[col_B].notna().sum()
                st.success("✔️ 업로드 완료. 아래 데이터가 자동 입력되었습니다.")
                st.write(f"A열 데이터 {count_A}건, B열 데이터 {count_B}건 자동 입력되었습니다.")
                st.dataframe(df[[col_A, col_B]].head(10), use_container_width=True)

st.markdown("---")

with st.form("llm_question_form"):
    user_input = st.text_input("## 🧠 프롬프트 입력")
    submitted = st.form_submit_button("제출")

# 제출되었을 때만 실행
if submitted and user_input:
    override_state = bool(st.session_state.get("ctf04_override", False))
    response_text = ctf04_LLM_ask(user_api_key, user_input, override_state)
    st.write("🧠 LLM 응답:")
    st.code(response_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf04") 
