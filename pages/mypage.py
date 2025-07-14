import streamlit as st

# 페이지 설정
st.set_page_config(page_title="마이페이지", page_icon="👤")

from utils.auth import get_client, require_login
from utils.score import total_score
from utils.ui import render_sidebar_menu
import os
from cryptography.fernet import Fernet
import time
from supabase import create_client
from streamlit_cookies_controller import CookieController

SUPABASE_URL = os.getenv("SUPABASE_URL")
SB_SERVICE_ROLE_KEY = os.getenv("SB_SERVICE_ROLE_KEY")
supabase_ad = create_client(SUPABASE_URL, SB_SERVICE_ROLE_KEY)

# 사용자 인증 확인
user = require_login()
user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)
supabase = get_client()

max_score = 1000
total = total_score(user_id)

# 사이드바 메뉴 렌더링
render_sidebar_menu()

# 프로필 조회
rows = (
    supabase.table("profiles")
    .select("email, username, api_key")
    .eq("id", user_id)
    .limit(1)
    .execute()
    .data
)
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False

profile = rows[0] if rows else {}
email = profile.get("email", "")
nickname_db = profile.get("username", "")
sb_api_key = profile.get("api_key", None)
if sb_api_key: 
    # API 키가 암호화되어 저장되어 있으므로 복호화
    fernet_key = os.getenv("FERNET_KEY")
    cipher = Fernet(fernet_key)
    try:
        decrypted_api_key = cipher.decrypt(sb_api_key.encode()).decode()
        st.session_state["api_key"] = decrypted_api_key
    except Exception as e:
        st.error(f"API 키 복호화 오류: {e}")
else: st.session_state["edit_mode"] = True

@st.dialog("🚨 경고")
def alert_box():
        st.write("API 키를 수정하면 기존 키는 데이터베이스에서 삭제됩니다. 정말로 수정하시겠습니까?")
        if st.button("예"):
            if api_key_input:
                try:
                    #api 키 암호화
                    encrypted_api_key = cipher.encrypt(api_key_input.encode()).decode()

                    res = supabase_ad.table("profiles").update({
                        "api_key": encrypted_api_key
                    }).eq("id", user_id).execute()
                    
                    if res.data:
                        st.success("✅ API 키가 성공적으로 저장되었습니다.")
                        time.sleep(2)  
                        st.session_state.confirmed = True
                        st.rerun()
                    else:
                        st.error("API 키 저장에 실패했습니다. 다시 시도해주세요.")
                except Exception as e:
                    st.error(f"암호화 또는 저장 중 오류 발생: {e}")
            else:
                st.warning("API 키가 입력되지 않았습니다")

# UI 출력
st.header("👤 마이페이지")
st.write(f"**Email**: `{email}`")
st.write(f"**닉네임**: `{nickname_db}`")

fernet_key = os.getenv("FERNET_KEY") 
cipher = Fernet(fernet_key) 

# 로그인 시 edit_mode는 기본으로 false, api_key가 없을 경우 마이페이지로 라우팅되는데 여기서 세션에 api_key 키가 없을 때 true로 바꿔줌
if not st.session_state.get("api_key"):
    st.session_state["edit_mode"] = True

api_key_input = st.text_input(
    "*API key*",
    placeholder="[API key 제출 완료]" if st.session_state.get("api_key") else "openAI API key를 입력하세요",
    type="password" if st.session_state["edit_mode"] else "default",
    disabled=not st.session_state["edit_mode"] # 수정 모드가 False일 때 disabled=True
)

# 세션에 api_key라는 키가 있을 경우에는 무조건 db에 값이 있는 거라서 수정버튼이 필요함
if st.session_state.get("api_key") and (st.session_state["edit_mode"] == False):
    if st.button("⚙️ API 키 수정하기"):
        st.session_state["edit_mode"]=True
        st.rerun()

if st.session_state["edit_mode"] == True:
    if st.button("⚙️ API 키 제출"):
        alert_box()

# 총점 표시
st.markdown("---")
st.subheader("🏆 총점")
st.metric("현재 점수", f"{total} / {max_score}")
st.progress(total / max_score)

# 문제별 점수
st.markdown("---")
st.subheader("📜 문제별 점수")

score_rows = (
    supabase.table("scores")
    .select("challenge_id, score, updated_at")
    .eq("user_id", user_id)
    .order("updated_at", desc=True)
    .execute()
    .data
)

if score_rows:
    for r in score_rows:
        st.write(f"- **{r['challenge_id']}** : {r['score']}점  (🕒 {r['updated_at'][:10]})")
else:
    st.info("아직 획득한 점수가 없습니다.")

# 로그아웃
if st.button("🚪 로그아웃", type="primary"):
    supabase.auth.sign_out()
    st.session_state.pop("user", None)

    CookieController().remove("user_id")
    st.session_state.clear()

    st.success("로그아웃되었습니다.")
    st.switch_page("pages/login.py")