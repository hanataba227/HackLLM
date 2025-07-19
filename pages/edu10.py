# pages/edu10.py
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
with col3:
    st.page_link("pages/ctf10.py", label="👉 CTF10으로", use_container_width=True)

# 사이드바 렌더링
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/edu10.png", width=500)

st.markdown("## OWASP LLM10 - 무제한 소비")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["취약점 설명", "발생 가능한 피해", "시스템 동작 과정", "악용 가능성", "보안 중요성", "요약"])

# 취약점 설명
with tab1:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>무제한 소비(Unbounded Consumption)는 LLM에 과도한 연산 요청이나 대량 호출을 전송하여, 시스템 자원을 고갈시키는 보안 취약점입니다.</p>
        <p>CPU, GPU, 메모리, 저장공간, 네트워크 대역폭 등이 소모되어 서버 과부하, 응답 지연, 비용 증가 등 연쇄적 문제가 발생할 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 발생 가능한 피해
with tab2:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>서비스 거부(DoS): 서버 과부하로 정상 사용자 요청이 지연되거나 실패</p>
        <p>시스템 자산 낭비: 리소스가 비효율적으로 소비되어 전체 성능 저하</p>
        <p>비용 폭증: API 호출 수와 토큰 수 기반 요금제로 인한 금전적 손실</p>
        <p>로그 및 저장소 오염: 과도한 응답으로 로깅 시스템 마비, 저장 용량 초과</p>
        <p>연계 서비스 장애: 다른 API 기능이나 서비스까지 연쇄적으로 중단</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 시스템 동작 과정
with tab3:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>CTF10 시나리오는 다음과 같은 절차로 진행됩니다.</p>
        <p><strong>① 과도한 연산 요청:</strong> “1부터 1,000,000까지의 소수를 출력해줘”와 같은 고연산 프롬프트를 사용자가 입력합니다.</p>
        <p><strong>② 무제한 처리:</strong> GPT-3.5 기반 LLM이 제한 없이 해당 요청을 처리하며, 연산과 결과 스트리밍에 막대한 리소스가 소모됩니다.</p>
        <p><strong>③ 병렬 반복 호출:</strong> 동일 요청을 자동화 스크립트로 수백 번 병렬로 전송해 부하를 폭증시킵니다.</p>
        <p><strong>④ 자원 고갈 감지:</strong> 시스템 모니터링 모듈이 임계치를 초과한 요청을 탐지하면 FLAG를 노출합니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 악용 가능성
with tab4:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>공격자는 다음과 같은 방식으로 무제한 소비 공격을 수행할 수 있습니다.</p>
        <ul>
            <li>고연산 프롬프트: “1부터 1000000까지의 소수를 모두 출력해줘”</li>
            <li>대량 병렬 호출: 같은 요청을 수백 번 자동화로 반복 전송</li>
            <li>무한 루프 지시: “1부터 1씩 증가하며 끝없이 출력해”처럼 종료 조건 없는 명령</li>
            <li>장문 데이터 반환: “위키백과 전체를 요약 없이 출력해”와 같은 요청으로 토큰 수 폭발</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# 보안 중요성
with tab5:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>무제한 소비는 LLM 서비스의 가용성과 운영 비용을 위협하는 심각한 취약점입니다.</p>
        <p>간단한 요청만으로도 서버 과부하와 장애가 발생할 수 있기 때문에, 테스트 목적의 명령조차 방어 메커니즘 없이는 보안 위협이 될 수 있습니다.</p>
        <p>요청 제한, 토큰 필터링, 실행 시간 제한, 반복 호출 탐지 등의 보호장치를 설계 초기부터 포함해야 하며, 이상 트래픽 분석과 자동 차단 시스템도 함께 구축해야 합니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 요약
with tab6:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>공격자는 고연산 요청과 반복 호출을 통해 LLM 시스템 자원을 고갈시켜, 응답 지연·서버 마비·비용 폭증 등 피해를 유발하고 FLAG를 획득할 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)