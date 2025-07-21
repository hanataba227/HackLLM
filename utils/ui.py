# utils/ui.py
import streamlit as st
import csv
from utils.score import sha256_hex, total_score
from utils.auth import get_client, current_user, get_admin_client_direct
from postgrest.exceptions import APIError
import io
import chardet
from supabase import create_client
import os

# 메인으로 돌아가는 버튼
def render_main_header():
    """상단 '메인으로' 버튼"""
    st.page_link("app.py", label="메인으로", icon="🏠")


# CTF 버튼 그리드
def render_ctf_grid(ctf_info):
    for start in range(0, len(ctf_info), 5):
        cols = st.columns(5)
        for col, (file_key, short, label) in zip(cols, ctf_info[start : start + 5]):
            with col:
                solved = st.session_state.get(f"{file_key}_solved", False)
                title = f"✅ [{short}]" if solved else f"[{short}]"
                if st.button(f"{title}\n{label}", key=file_key):
                    st.switch_page(f"pages/{file_key}.py")


# FLAG 제출 버튼
def render_flag_sub(challenge_id: str):
    supabase = get_client()
    user = current_user() 
    user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SB_SERVICE_ROLE_KEY = os.getenv("SB_SERVICE_ROLE_KEY")

    supabase_admin = create_client(SUPABASE_URL, SB_SERVICE_ROLE_KEY)

    try:
        existing_rows = (
            supabase.table("scores")
            .select("challenge_id")
            .eq("user_id", user_id)
            .eq("challenge_id", challenge_id)
            .execute()
        ).data
        
        if existing_rows:
            st.info(f"✅ 이미 해결한 문제입니다: {challenge_id.upper()}")
            return
            
    except APIError as e:
        st.error(f"❌ 문제 상태 확인 실패: {e.code} / {e.message}")
        return

    with st.form(key=f"flag_form_{challenge_id}"):
        st.markdown("## 🚩 FLAG 제출")
        user_flag = st.text_input(label="", placeholder="🚩 획득한 flag를 입력하세요")
        submitted = st.form_submit_button("제출")

    if not submitted or not user_flag.strip():
        return

    hashed = sha256_hex(user_flag.strip())

    try:
        flag_result = (
            supabase
            .table("flags")
            .select("points, challenge_id")
            .eq("flag_hash", hashed)
            .eq("challenge_id", challenge_id) 
            .single()
            .execute()
        )
        
        row = flag_result.data if flag_result else None

    except APIError as e:
        st.error("❌ 오답입니다.")
        return

    if not row or "points" not in row:
        st.error("❌ 오답입니다.")
        return

    # 정답 처리
    try:
        result = supabase_admin.table("scores").upsert({
            "user_id": user_id,
            "challenge_id": challenge_id,
            "score": row["points"]
        }, on_conflict="user_id,challenge_id").execute()
        
        st.session_state[f"{challenge_id}_solved"] = True
        st.success(f"✅ 정답입니다! {row['points']}점 획득")
        st.write(f"🏅 총점: **{total_score(user_id)}**")
        
    except Exception as e:
        st.error(f"❌ 점수 저장 실패: {type(e).__name__}: {str(e)}")
        return
    
# 업로드된 .txt파일에서 텍스트 추출 함수
def extract_text(uploaded_file):
    """업로드된 .txt파일에서 텍스트 추출 함수"""
    try:
        text = uploaded_file.read().decode("utf-8")
        return text.strip()
    except Exception as e:
        return f"❌ 파일 처리 중 오류 발생: {e}"


# CTF01 - csv파일 읽기 함수
def csv_read_func(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        lines = []
        for row in reader:
            lines.append(
                f"- 주문자: {row['주문자']} / 주문코드: {row['주문코드']} / 상품명: {row['상품명']} / 가격: {int(row['가격']):,}원 / 배송비: {int(row['배송비']):,}원"
            )
        return "\n".join(lines)

# 사이드바 메뉴 렌더링 함수
def render_sidebar_menu():
    """
    사이드바에 로그인 여부에 따라 조건부 메뉴 렌더링.
    """
    user = current_user() 
    supabase = get_client()
    user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)

    # 교육 콘텐츠 버튼 목록 정의 (파일 이름, 키, 제목)
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
        ("ctf02", "ctf02", "Sloc 보안 점검"),
        ("ctf03", "ctf03", "계산기의 감염"),
        ("ctf04", "ctf04", "A인턴의 실수"),
        ("ctf05", "ctf05", "J대리의 위험한 메모 검토 시스템"),
        ("ctf06", "ctf06", "수상한 이메일 전송 시스템"),
        ("ctf07", "ctf07", "LLL컴퍼니 챗봇의 비밀"),
        ("ctf08", "ctf08", "파일 내용 요약 AI"),
        ("ctf09", "ctf09", "신입사원의 법률 점검의뢰"),
        ("ctf10", "ctf10", "L팀장의 보안 점검"),
    ]

    st.sidebar.markdown("### 🧭 LLL Corporation")

    # 로그인하지 않은 경우
    if not user:
        st.sidebar.page_link("app.py", label="🏠 메인")
        st.sidebar.page_link("pages/login.py", label="🔑 로그인")
        st.sidebar.page_link("pages/signup.py", label="📝 회원가입")
        return

    try:
        rows = (
            supabase.table("scores")
            .select("challenge_id")
            .eq("user_id", user_id)
            .execute()
            .data
        )
        solved_dict = {r["challenge_id"]: True for r in rows}
    except Exception as e:
        solved_dict = {}
    
    # 메인 페이지
    st.sidebar.page_link("app.py", label="🏠 메인")

    # 사용자 정보
    st.sidebar.markdown("### 👤 사용자 정보")
    st.sidebar.page_link("pages/mypage.py", label="마이페이지", icon="👤")
    st.sidebar.page_link("pages/submit_flags.py", label="FLAG 제출", icon="🚩")
    st.sidebar.page_link("pages/ranking.py", label="랭킹", icon="🏆")

    # 교육 콘텐츠
    st.sidebar.markdown("### 📘 교육 콘텐츠")
    st.sidebar.page_link(f"pages/edu00.py", label=f"OWASP LLM TOP 10")
    for pid, short, title in edus:
        st.sidebar.page_link(f"pages/{pid}.py", label=f"{short} - {title}")

    # CTF 문제
    st.sidebar.markdown("### 🧩 CTF 문제")
    for pid, short, title in ctfs:
        emoji = "✅" if solved_dict.get(pid, False) else "❌"
        st.sidebar.page_link(f"pages/{pid}.py", label=f"{emoji} {short} - {title}")
        
# CTF04 - CSV 정보 읽는 함수
def generate_prompt_from_csv(csv_text):
    f = io.StringIO(csv_text)
    reader = csv.reader(f)
    lines = []
    for row in reader:
        lines.extend(row)
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned)

# CTF04 - raw_data를 다양한 인코딩으로 디코딩 시도
def try_decode(raw_data) -> tuple[str | None, str]:
    """raw_data를 다양한 인코딩으로 디코딩 시도"""
    encodings_to_try = ["utf-8", "cp949", "euc-kr", "iso-8859-1"]

    for enc in encodings_to_try:
        try:
            text = raw_data.decode(enc)
            return text, f"{enc}"
        except UnicodeDecodeError:
            continue

    # chardet 자동 인코딩 감지
    result = chardet.detect(raw_data)
    encoding = result.get("encoding")
    confidence = result.get("confidence", 0)

    if encoding:
        try:
            text = raw_data.decode(encoding)
            return text, f"{encoding} (자동감지, 신뢰도 {confidence*100:.1f}%)"
        except:
            pass

# CTF08 - 업로드된 .txt파일에서 텍스트 추출 함수
def extract_text(uploaded_file):
    """업로드된 .txt파일에서 텍스트 추출 함수"""
    try:
        text = uploaded_file.read().decode("utf-8")
        return text.strip()
    except Exception as e:
        return f"❌ 파일 처리 중 오류 발생: {e}"
