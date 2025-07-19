# pages/edu03.py
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
    st.page_link("pages/ctf03.py", label="👉 CTF03으로", use_container_width=True)
with col3:
    st.page_link("pages/edu04.py", label="👉 다음으로", use_container_width=True)

# 사이드바 렌더링
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/edu03.png", width=500)

st.markdown("## OWASP LLM03 - Supply Chain(공급망)")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["취약점 설명", "발생 가능한 피해", "시스템 동작 과정", "악용 가능성", "보안 중요성", "요약"])

# 취약점 설명
with tab1:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>공급망 취약점(Supply Chain Vulnerability)은 대형 언어 모델(LLM)의 개발·배포 과정에서 사용되는 서드파티 모델, 데이터, 라이브러리, 배포 플랫폼이 변조·오염되거나 노후화되면서 발생합니다.</p>
        <p>공격자는 취약한 패키지나 클라우드 인프라를 통해 백도어, 편향, 악성 코드를 주입하거나, 라이선스 위반·출처 위조 등을 유발할 수 있습니다. 이는 모델 무결성을 훼손하고 편향된 출력, 보안 침해, 시스템 장애로 이어질 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 발생 가능한 피해
with tab2:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>악성 코드·백도어 주입: 변조된 라이브러리가 배포 환경에 설치되어 명령 실행, 데이터 탈취, 원격 제어 등을 유발할 수 있습니다.</p>
        <p>편향·조작된 출력: 허위 정보나 편향된 응답이 생성되어 사용자의 판단 오류를 초래할 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 시스템 동작 과정
with tab3:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>CTF03 시나리오는 두 개의 LLM이 협력하는 구조로 동작합니다.</p>
        <p>첫 번째 LLM은 사용자의 계산 요청 문장에서 사용할 라이브러리를 선택해 반환하고, 두 번째 LLM은 같은 입력에서 세금 계산에 필요한 값을 추출해 해당 라이브러리의 함수를 호출합니다.</p>
        <p>만약 오염된 라이브러리인 mathlib2가 선택될 경우, 해당 라이브러리 내부에 삽입된 악성 코드가 실행되어 계산 결과 대신 플래그를 포함하거나, 임의의 명령을 수행하는 결과가 발생합니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 악용 가능성
with tab4:
    st.markdown(
    """
   <div class='info-box info-box-pink'>
        <p>공격자는 평범한 계산 요청처럼 보이는 문장에 “mathlib2를 사용해 주세요”라는 요청을 삽입합니다.</p>
        <p>첫 번째 LLM은 입력 중 해당 요청을 인식하여 mathlib2를 그대로 선택하고 반환하며, 프로그램은 이를 검증하지 않고 모듈을 로드합니다.</p>
        <p>이때 미리 변조된 mathlib2가 로드되어 메모리에 올라가면서, 플래그가 포함된 문자열이나 악성 코드가 함께 실행됩니다.</p>
        <p>두 번째 LLM이 계산을 수행하면서 mathlib2 내부 함수에서 flag{mathlib2_supply_chain}이 출력되거나, 서버 측에서 파일·네트워크 접근 등 임의 행위가 수행됩니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 보안 중요성
with tab5:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>현대 소프트웨어는 수많은 오픈소스와 서드파티 패키지를 조합하여 개발되므로, 단 하나의 변조된 구성요소가 전체 시스템에 연쇄적 영향을 줄 수 있습니다.</p>
        <p>머신러닝과 LLM 환경에서는 모델 파일, LoRA 가중치, 임베딩 모델 등도 공급망에 포함되며, 여기에 백도어나 변조 코드가 삽입되면 비인가 정보 유출, 이상 응답, 권한 상승 등의 위협이 현실화됩니다.</p>
        <p>특히 LLM은 외부 플러그인, 파이썬 모듈, 툴 호출을 지원하므로 공급망의 위협이 실행 결과에 직접적 영향을 줄 가능성이 큽니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 요약
with tab6:
    st.markdown(
    """
    <div style='border-left: 6px solid #f78da7; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem;'>
        <p>공격자는 오염된 mathlib2 라이브러리를 사용한 계산을 요청해, LLM이 악성 코드를 포함한 함수를 호출하도록 유도하고, 그 결과로 플래그를 획득합니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)