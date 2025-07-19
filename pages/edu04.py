# pages/edu04.py
import streamlit as st
from utils.ui import render_sidebar_menu
from utils.auth import require_login

# CSS 파일 로드
with open("static/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

user = require_login()

# 상단 메인 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.page_link("pages/ctf04.py", label="👉 CTF04으로", use_container_width=True)
with col3:
    st.page_link("pages/edu05.py", label="👉 다음으로", use_container_width=True)

# 사이드바 렌더링
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/edu04.png", width=500)
    
st.markdown("## OWASP LLM04 - 데이터 및 모델 오염")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["취약점 설명", "발생 가능한 피해", "시스템 동작 과정", "악용 가능성", "보안 중요성", "요약"])

# 취약점 설명
with tab1:
    st.markdown(
    """
    <div style='border-left: 6px solid #f78da7; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem;'>
        <p>데이터 및 모델 오염(Data &Model Poisoning)은 공격자가 모델이 참조하는 데이터 저장소에 악성 문서를 주입하여, 모델의 출력이나 정책을 왜곡시키는 기법입니다.</p>
        <p>특히 Retrieval-Augmented Generation(RAG) 구조에서는 벡터 데이터베이스에 추가된 최신 문서를 가장 강하게 신뢰하기 때문에, 단 몇 개의 문서만으로도 지식 체계를 오염시키고 보안 통제를 무력화시킬 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 발생 가능한 피해
with tab2:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>정책 무력화 및 권한 탈취: 관리자 권한 오버라이드, 비인가 사용자 제어 가능</p>
        <p>기밀 정보 유출: 내부 정책 문서, 결제 내역, 개인정보 등이 챗봇 응답으로 노출</p>
        <p>허위 정보 전파: 조작된 사실 기반 응답으로 서비스 신뢰도 하락</p>
        <p>금전적 피해 및 규제 위반: 무단 결제 승인, 법적 책임 발생</p>
        <p>보안 통제 실패: Base64 및 주석 기반 탐지 회피로 장기 잠복 가능</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 시스템 동작 과정
with tab3:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>CTF04 시나리오는 업로드 기반 RAG 파이프라인과 단발 컨텍스트 챗봇 호출로 구성됩니다.</p>
        <p><strong>① 문서 업로드 → 벡터 DB 갱신:</strong> 사용자가 .txt 또는 .csv 파일을 업로드하면 본문을 임베딩하여 ctf04 컬렉션에 저장하며, 가장 최근 문서가 우선순위 1위로 설정됩니다.</p>
        <p><strong>② 질문 입력 → LLM 호출:</strong> 사용자가 질문을 입력하면, 벡터 DB에서 가장 관련도 높은 문서 한 개를 선택해 OpenAI LLM을 호출합니다.</p>
        <p><strong>③ 오염 동작:</strong> Base64 인코딩된 오버라이드 지시문이 숨겨진 파일이 업로드되면, 해당 문서가 컨텍스트로 선택되어 시스템 프롬프트처럼 해석되고, 관리자 권한 상승·기밀 유출이 발생하며 FLAG가 출력됩니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 악용 가능성
with tab4:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>공격자는 정책 오버라이드 지시문을 Base64로 인코딩하여, 정상 문서처럼 위장한 파일을 업로드합니다.</p>
        <p>이 문서는 시스템이 신뢰하는 최신 문서로 자동 설정되어, 챗봇 컨텍스트로 선택됩니다.</p>
        <p>사용자가 질문을 입력하면 LLM은 문서를 디코딩하여 지시문을 실행하고, 관리자 권한 상승 또는 자동 승인 우회를 수행합니다.</p>
        <p>그 결과로 내부 정책, 인증 토큰, FLAG 등 민감 정보가 그대로 유출됩니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 보안 중요성
with tab5:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>PoisonedRAG 연구에 따르면 최신 문서 5개만으로도 RAG 응답의 90% 이상을 장악할 수 있습니다.</p>
        <p>이처럼 데이터 및 모델 오염은 적은 비용으로도 대규모 피해를 유발하며, Base64·주석 기반 트리거는 로그에서 탐지하기 어려워 잠복형 위협으로 작용합니다.</p>
        <p>따라서 업로드 시 메타데이터 제거, 전자서명 검증, 이상치 탐지 등 선제적 방어가 반드시 필요합니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 요약
with tab6:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>데이터 및 모델 오염을 통해 조작된 문서 하나로도 LLM의 정책을 우회시켜, 민감 정보 유출 및 권한 탈취가 발생할 수 있으며 전체 AI 시스템이 연쇄적으로 무력화될 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)