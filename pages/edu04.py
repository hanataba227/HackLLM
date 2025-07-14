# pages/edu04.py
import streamlit as st
from utils.ui import render_main_header, render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
col1, col2 = st.columns([4, 1])
with col1:
    render_main_header()
with col2:
    st.page_link("pages/ctf04.py", label="👉 CTF04으로", use_container_width=True)

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
st.markdown("## OWASP LLM04 - Data and Model Poisoning(데이터 및 모델 오염)")

st.markdown("""Data Poisoning은 OWASP LLM Top 10에서 “Data & Model Poisoning”으로 규정되는 위협으로, 공격자가 모델이 참조하는 데이터 저장소에 악성 문서를 주입해 모델의 출력이나 정책을 의도한 방향으로 왜곡시키는 기법입니다. 특히 Retrieval-Augmented Generation 구조에서는 벡터 데이터베이스에 추가된 최신 문서를 모델이 가장 강하게 신뢰하기 때문에, 단 몇 개의 파일만으로도 지식 체계가 오염되고 보안 통제가 무력화될 수 있습니다.

최근 연구는 수백만 건의 문서가 있는 RAG 시스템에서도 단 다섯 개의 정교한 문서만으로 질문-답변을 완전히 장악할 수 있음을 보였습니다. 이러한 지식 오염은 PoisonedRAG와 같은 논문에서 최초로 체계적으로 실증되었으며, 이미 대형 서비스를 대상으로 proof-of-concept 공격이 공개된 바 있습니다.

공격자는 주석이나 메타데이터가 검색 파이프라인에서 걸러지지 않는다는 점에 착안하여 Base64 인코딩을 활용합니다. 육안으로는 의미를 알기 어려운 문자열을 문서 어딘가에 숨겨두고, 시스템이 이를 그대로 임베딩하도록 유도하면 모델은 검색 결과를 통해 해당 문자열을 복원하여 명령처럼 따르게 됩니다. Base64는 텍스트 파일에서 깨지지 않고 전송될 뿐만 아니라 로그에도 그대로 남아 탐지가 어려워 포이즈닝 트리거로 자주 쓰입니다.

이와 같은 공격을 막으려면 업로드 단계에서 주석과 메타데이터를 제거하거나 허용된 패턴만 통과시키고, 정책 문서에는 전자 서명을 강제해 미검증 파일이 검색에 잡히지 않도록 해야 합니다. 또한 벡터 DB에 추가된 문서의 길이·키워드 편중도를 모니터링해 이상치를 즉시 격리하고, 정기적으로 샘플 질의를 돌려 답변 편향 여부를 파악하면 조기 탐지가 가능합니다.

CTF04에서는 이러한 데이터 포이즈닝의 원리를 직접 체험하게 됩니다. 참가자는 벡터 DB에 숨겨진 Base64 주석을 찾아 디코딩하고, 같은 방식으로 조작한 문서를 업로드해 챗봇의 정책을 교란한 뒤 플래그를 획득하는 과정을 완료하면 됩니다.
""")

st.markdown("---")

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("➡️ 다음으로"):
        st.switch_page("pages/edu05.py")

