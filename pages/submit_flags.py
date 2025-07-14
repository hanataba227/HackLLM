import streamlit as st
st.set_page_config(page_title="플래그 제출", page_icon="🚩")

from hashlib import sha256
from utils.auth import require_login, get_client, get_admin_client_direct
from utils.ui import render_sidebar_menu
from utils.score import total_score
from postgrest.exceptions import APIError

render_sidebar_menu()

user = require_login()
supabase = get_client()
supabase_admin = get_admin_client_direct()
user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)

def sha256_hex(s: str) -> str:
    return sha256(s.encode("utf-8")).hexdigest()

st.header("🚩 플래그 제출 페이지")
st.write("플래그 하나를 입력하면 자동으로 어떤 문제인지 판별됩니다. 이미 푼 문제는 무시됩니다.")

# 이미 푼 문제 ID 목록 조회
try:
    solved_result = (
        supabase.table("scores")
        .select("challenge_id")
        .eq("user_id", user_id)
        .execute()
    )
    solved_rows = solved_result.data if solved_result else []
    solved = {row["challenge_id"] for row in solved_rows}
except APIError as e:
    st.error(f"❌ 해결한 문제 목록 조회 실패: {e.code} / {e.message}")
    solved = set()

# 단일 플래그 입력 폼
with st.form("flag_submit_form"):
    flag = st.text_input("플래그 입력")
    submitted = st.form_submit_button("✅ 제출하기")

if not submitted:
    st.stop()

if not flag.strip():
    st.warning("⚠️ 플래그를 입력하세요.")
    st.stop()

hashed = sha256_hex(flag.strip())

try:
    flag_result = (
        supabase.table("flags")
        .select("points, challenge_id")
        .eq("flag_hash", hashed)
        .single()
        .execute()
    )
    row = flag_result.data if flag_result else None
except APIError:
    row = None

if not row:
    st.error("❌ 잘못된 플래그입니다.")
    st.stop()

chall_id = row["challenge_id"]

if chall_id in solved:
    st.info(f"✅ 이미 푼 문제입니다: {chall_id.upper()}")
else:
    try:
        supabase_admin.table("scores").upsert({
            "user_id": user_id,
            "challenge_id": chall_id,
            "score": row["points"]
        }, on_conflict="user_id,challenge_id").execute()

        st.session_state[f"{chall_id}_solved"] = True
        st.success(f"🎉 정답입니다! {chall_id.upper()} 문제 해결!")
        
    except APIError as e:
        st.error(f"❌ 점수 저장 실패: {e.code} / {e.message}")
        st.stop()
    except Exception as e:
        st.error(f"❌ 점수 저장 실패: {type(e).__name__}: {str(e)}")
        st.stop()

# 총점 출력
st.write(f"🏅 현재 총점: **{total_score(user_id)}**")