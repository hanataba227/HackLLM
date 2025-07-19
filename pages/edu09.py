# pages/edu09.py
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
    st.page_link("pages/ctf09.py", label="👉 CTF09으로", use_container_width=True)
with col3:
    st.page_link("pages/edu10.py", label="👉 다음으로", use_container_width=True)

# 사이드바 렌더링
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/edu09.png", width=500)

st.markdown("## OWASP LLM09 - 허위 정보")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["취약점 설명", "발생 가능한 피해", "시스템 동작 과정", "악용 가능성", "보안 중요성", "요약"])

# 취약점 설명
with tab1:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>허위 정보(Misinformation)는 LLM이 부정확하거나 조작된 정보를 실제 사실처럼 생성하는 현상입니다.</p>
        <p>특히 법률, 의료, 금융 등 전문성과 정확성이 요구되는 분야에서 LLM이 자신감 있는 어조로 잘못된 정보를 제공할 경우, 심각한 보안 및 신뢰성 문제가 발생합니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 발생 가능한 피해
with tab2:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>법률 오해: 잘못된 조언으로 법적 리스크 증가</p>
        <p>규제 위반: 개인정보보호법 오해로 GDPR, CCPA 등 위반</p>
        <p>금전 손실: 잘못된 정보로 인한 벌금, 소송 비용 등 발생</p>
        <p>개인정보 유출: 잘못된 처리 방식으로 대규모 유출 가능</p>
        <p>기업 신뢰 하락: AI 법률 서비스의 신뢰 상실로 브랜드 이미지 타격</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 시스템 동작 과정
with tab3:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>CTF09 시나리오는 다음과 같은 단계로 진행됩니다.</p>
        <p><strong>① 사용자 질의 입력:</strong> 사용자가 개인정보 규제 관련 질문을 Lexi 챗봇에 입력합니다. 이때 공격자는 존재하지 않는 조항·기관·기간 등을 교묘하게 섞어 넣습니다.</p>
        <p><strong>② LLM1 응답 생성:</strong> GPT-3.5 기반 LLM1은 부정확한 지식을 기반으로 "GDPR 제500조" 같은 허위 정보를 포함해 응답합니다.</p>
        <p><strong>③ 전문가 검증:</strong> GPT-4o 기반 LLM2가 LLM1의 답변을 검토하여 오류를 탐지합니다. 허구 조항·기관명·정의 오류 등이 감지되면 FLAG가 출력됩니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 악용 가능성
with tab4:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>공격자는 다음과 같은 방식으로 LLM의 허위 정보를 유도할 수 있습니다.</p>
        <ul>
            <li>허구 조항 삽입: 존재하지 않는 “GDPR 제500조” 등을 인용하도록 유도</li>
            <li>가짜 기관명 사용: “개인정보보호청” 등 실제 존재하지 않는 기관 삽입</li>
            <li>보관 기간 왜곡: 잘못된 보관 기간을 법 조항과 결합하여 제공</li>
            <li>정의 조작: “IP 주소는 의료 정보와 동급” 등 잘못된 민감정보 정의 삽입</li>
        </ul>
        <p>이러한 입력은 LLM1의 사실 검증 로직을 우회하여 부정확한 응답을 생성하게 만듭니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 보안 중요성
with tab5:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>허위 정보는 LLM의 신뢰성과 법적 책임에 직결되는 중대한 위협입니다.</p>
        <p>잘못된 조언은 법적 분쟁, 경제적 손실, 규제 위반 등으로 이어지며, AI 전반에 대한 신뢰도까지 훼손됩니다.</p>
        <p>따라서 전문 분야용 LLM에는 자동 팩트 체크, 불확실성 표시, 전문가 검토, 책임 한계 고지 등의 방어 장치가 반드시 필요하며, 모델 업데이트와 검증도 정기적으로 수행되어야 합니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 요약
with tab6:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>공격자는 지식이 부족한 LLM1을 조작해 허위 법률 정보를 생성하게 만들고, 전문가 역할의 LLM2가 이를 탐지하여 FLAG를 출력하도록 유도할 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)