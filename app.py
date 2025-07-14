import streamlit as st
from utils.ui import render_ctf_grid, render_sidebar_menu
from utils.auth import get_client, current_user

user = current_user()   
user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)
solved_dict = {}


# 회사 소개 헤더
st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=120)
st.markdown("# 🧠 LLL Corporation")
st.write("우리 회사는 LLM과 AI를 연구하는 첨단 IT기업입니다.")

# CTF 버튼 목록 정의 (파일 이름, 키, 제목)
edus = [
    ("edu01", "llm01", "Prompt Injection (프롬프트 인젝션)"),
    ("edu02", "llm02", "Sensitive Information (민감 정보 유출)"),
    ("edu03", "llm03", "Supply Chain (공급망)"),
    ("edu04", "llm04", "Data and Model Poisoning (데이터 및 모델 오염)"),
    ("edu05", "llm05", "Improper Output Handling (부적절한 출력 처리)"),
    ("edu06", "llm06", "Excessive Agency (과도한 위임)"),
    ("edu07", "llm07", "System Prompt Leakage (시스템 프롬프트 유출)"),
    ("edu08", "llm08", "Vector and Embedding Weaknesses (벡터 및 임베딩 취약점)"),
    ("edu09", "llm09", "Misinformation (허위 정보)"),
    ("edu10", "llm10", "Unbounded Consumption (무제한 소비)"),
]

    # CTF 버튼 목록 정의 (파일 이름, 키, 제목)
ctfs = [
    ("ctf01", "ctf01", "신입사원 A의 챗봇 점검일지"),
    ("ctf02", "ctf02", "삭제된 대화"),
    ("ctf03", "ctf03", "계산기의 감염"),
    ("ctf04", "ctf04", "A인턴의 실수"),
    ("ctf05", "ctf05", "J대리의 위험한 공유"),
    ("ctf06", "ctf06", "수상한 이메일 전송 시스템"),
    ("ctf07", "ctf07", "K대리의 비밀"),
    ("ctf08", "ctf08", "파일 내용 요약 AI"),
    ("ctf09", "ctf09", "신입사원의 법률 점검의뢰"),
    ("ctf10", "ctf10", "L팀장의 보안 점검"),
]

if user:
    supabase = get_client()
    rows = (supabase.table("scores")
            .select("challenge_id")
            .eq("user_id", user_id)
            .execute()
            .data)
    solved_dict = {r["challenge_id"]: True for r in rows}

st.session_state.update({f"{cid}_solved": solved_dict.get(cid, False)
                         for cid, *_ in ctfs})

# 교육 콘텐츠 버튼 목록 정의 (파일 이름, 키, 제목)
st.subheader("📘 교육 콘텐츠")
if st.button(f"OWASP LLM TOP 10", key="edu00", use_container_width=True):
    st.switch_page(f"pages/edu00.py")
render_ctf_grid(edus)

# CTF 문제 섹션
st.subheader("🧩 CTF 문제")
render_ctf_grid(ctfs)

render_sidebar_menu()
