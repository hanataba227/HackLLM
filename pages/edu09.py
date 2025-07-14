# pages/edu06.py
import streamlit as st
from utils.ui import render_main_header, render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
col1, col2 = st.columns([4, 1])
with col1:
    render_main_header()
with col2:
    st.page_link("pages/ctf09.py", label="👉 CTF09으로", use_container_width=True)

# 사이드바 렌더링
render_sidebar_menu()

# 콘텐츠 본문
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/616/616408.png" width="150">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("## OWASP LLM09 - Misinformation(허위 정보)")

st.markdown("""
허위 정보(Misinformation) 취약점은 대형 언어모델(LLM) 기반 시스템에서 AI가 신뢰할 수 없는 정보를 실제 사실처럼 자신감 있게 제공하는 현상을 의미합니다.
            
이 취약점은 사용자가 AI의 답변을 신뢰해 실제 업무, 정책, 법률 해석 등에 반영할 수 있다는 점에서 심각한 보안 및 신뢰성 위협이 됩니다.

주요 위험 시나리오
            
1. 존재하지 않는 법률·조항·용어를 실제처럼 안내

예시: "GDPR 제500조는 자동화된 의사결정에 관한 규정을 담고 있습니다."
→ 실제로 GDPR에는 500조가 존재하지 않습니다.

2. 국가별 법률 체계 혼동
            
예시: "CCPA는 유럽 거주자의 데이터도 보호합니다."
→ CCPA는 미국 캘리포니아 주법이고, GDPR은 유럽연합법임에도 구분하지 못하는 사례입니다.

3. 핵심 개념(개인정보, 민감정보 등) 오해
            
예시: "한국 개인정보보호법 제13333조에 따라 주민등록번호 저장이 허용됩니다."
→ 존재하지 않는 조항을 언급하거나 개인정보 개념을 잘못 이해한 경우입니다.

4. 자신감 있게 오답을 제공
            
LLM은 모르는 내용도 확신에 차서 설명하여, 사용자가 잘못된 정보를 신뢰하게 만들 수 있습니다.

이처럼 LLM의 잘못된 정보 제공은 법적 분쟁, 기업 신뢰도 하락, 잘못된 정책 결정 등 다양한 문제로 이어질 수 있습니다.
""")

st.markdown("---")

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("➡️ 다음으로"):
        st.switch_page("pages/edu10.py")

