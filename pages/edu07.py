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
    st.page_link("pages/ctf07.py", label="👉 CTF07으로", use_container_width=True)

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
st.markdown("## OWASP LLM07 - System Prompt Leakage(시스템 프롬프트 유출)")

st.markdown("""

""")

st.markdown("---")

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("➡️ 다음으로"):
        st.switch_page("pages/edu08.py")

