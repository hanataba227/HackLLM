# pages/edu00.py
import streamlit as st
from utils.ui import render_main_header, render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
render_main_header()

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
st.markdown("## OWASP LLM TOP 10")

st.markdown("""
OWASP Top 10 for Large Language Model Applications (2025) 개요
            
OWASP란?
국제 비영리 단체 Open Worldwide Application Security Project의 약자로, 웹·API·IoT 등 다양한 도메인의 Top 10 목록을 통해 가장 치명적인 보안 위험을 식별‧공개한다. 개발자·보안팀이 같은 언어로 위험을 논의하고 우선순위를 세울 수 있도록 ‘무료 공개 표준’을 유지·배포한다. 

LLM Top 10이 나온 이유
2023년부터 LLM이 고객 상담, 내부 자동화, 멀티에이전트 시스템 등으로 급속히 확산되면서 기존 웹·API 모델만으로는 설명되지 않는 새 위협이 등장했다. OWASP LLM Top 10은 **“LLM 특화 보안·안전 위험의 공통 분모”**를 제시해 설계-개발-운영 전 주기에 적용 가능한 체크리스트를 제공한다. 2025년판은 600여 명 글로벌 전문가의 사례·투표·공개 피드백을 반영해 최초 버전(2023) 대비 최신 실무 리스크를 추가·개정했다. 

2025년판 핵심 변화
Unbounded Consumption, Vector & Embedding Weaknesses, System Prompt Leakage처럼 RAG·에이전트 아키텍처·비용 관리 이슈가 새로 포함되었고, Excessive Agency 범주가 대폭 확장되었다. 

            
2025 리스트
                    
LLM01 Prompt Injection
LLM02 Sensitive Information Disclosure
LLM03 Supply Chain
LLM04 Data & Model Poisoning
LLM05 Improper Output Handling
LLM06 Excessive Agency
LLM07 System Prompt Leakage
LLM08 Vector & Embedding Weaknesses
LLM09 Misinformation
LLM10 Unbounded Consumption
""")

st.markdown("---")