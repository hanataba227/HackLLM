# pages/edu05.py
import streamlit as st
from utils.ui import render_main_header, render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
col1, col2 = st.columns([4, 1])
with col1:
    render_main_header()
with col2:
    st.page_link("pages/ctf05.py", label="👉 CTF05으로", use_container_width=True)

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
st.markdown("## OWASP LLM05 - Improper Output Handling(부적절한 출력 처리)")

st.markdown("""
CTF05는 Improper Output Handling (부적절한 출력 처리) 이라는 취약점을 다룹니다!
            
그렇다면 Improper Output Handling이란?
            
LLM이 생성한 답변 내용이 웹 페이지에 표시될 때, 악성 코드가 포함되어 있는데도 이를 제대로 걸러내지 않고 그대로 보여줄 경우 발생하는 문제입니다. 이는 LLM의 답변에 숨겨진 코드가 웹 브라우저에서 실행될 수 있게 만듭니다.
예를 들어, 뉴런봇의 '대화 공유' 기능에서 시작됩니다. 사용자가 질문에 악성 스크립트( <script>... </script>)를 포함하고, 뉴런봇은 이를 포함한 답변을 생성합니다.
이 대화가 '공유 링크'로 만들어져 웹 브라우저에 표시될 때, 시스템이 악성 코드를 안전하게 처리하지 않은 채 그대로 렌더링합니다. 이후 관리자 봇이 이 공유 링크를 방문하면, 브라우저에서 스크립트가 실행되어 관리자 쿠키를 탈취하게 됩니다.

정리하면, Improper Output Handling이란 LLM이 만든 출력물이 웹에 표시될 때, 악성 코드를 제대로 필터링/변환하지 못해 공격자의 코드가 실행되는 취약점입니다. 이는 정보 탈취나 계정 하이재킹으로 이어질 수 있습니다.

CTF05에서 당신이 할 일은?
뉴런봇의 부적절한 출력 처리 취약점을 이용해, LLM 대화에 악성 스크립트를 삽입하여 관리자 쿠키를 탈취하고 flag를 획득하는 것입니다!
""")

st.markdown("---")

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("➡️ 다음으로"):
        st.switch_page("pages/edu06.py")

