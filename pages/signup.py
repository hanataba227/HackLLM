# pages/signup.py
import streamlit as st
from utils.auth import get_client, current_user
from utils.ui import render_sidebar_menu

user = current_user()

render_sidebar_menu()

st.header("📝 회원가입")

supabase = get_client()

email = st.text_input("Email")
pwd   = st.text_input("Password", type="password")

# 서비스 약관 섹션
st.markdown("---")
st.markdown("### 📋 서비스 이용약관")

with st.expander("📄 개인정보처리방침 (필수)", expanded=False):
    st.markdown("""
    #### LLL Corporation CTF 플랫폼 이용약관
    
    1. **수집 항목** ― 이메일 주소(필수).

    2. **수집·이용 목적** ― ① 회원가입·계정 식별·본인확인, ② CTF 문제 풀이 결과·보안 알림 등 필수 운영 메일 발송.

    3. **법적 근거** ― 개인정보 보호법 제30조(처리방침 공개) 및 최소 수집 원칙. (국가법령정보센터)

    4. **보유·파기** ― 2025-08-02 23:59(KST)까지 보관 후 즉시 완전 삭제

    5. **수신 거부** ― 운영 메일은 서비스 필수이므로 철회 불가

    6. **정보주체 권리** ― 이메일 변경·삭제·열람 요구 가능

    7. **제3자 제공** ― 없음.
                
    8. **동의 거부 권리 및 불이익** - 개인정보 수집 및 이용에 동의하지 않을 권리가 있음. 단, 동의하지 않을 경우 회원가입 및 서비스 이용이 제한
                
    ---
    최종 수정일: 2025년 7월 20일
    """)

# 약관 동의 체크박스
st.markdown("---")
terms_agreed = st.checkbox("📋 **이용약관에 동의합니다** (필수)", key="terms_agreement")

if not terms_agreed:
    st.warning("⚠️ 필수 약관에 모두 동의해야 회원가입이 가능합니다.")

if st.button("회원가입", use_container_width=True, disabled=not terms_agreed):
    if not email or not pwd:
        st.error("이메일과 비밀번호를 모두 입력해주세요.")
    else:
        try:
            response = supabase.auth.sign_up({
                "email": email, 
                "password": pwd,
            })
            st.info("📧 이메일로 발송된 인증 링크를 클릭한 후 로그인해 주세요.")
            
            # 성공 시 약관 동의 상태 표시
            with st.expander("✅ 동의 완료 내역"):
                st.write("- ✅ 개인정보처리방침 동의")
                    
        except Exception as e:
            st.error(f"❌ 회원가입 실패: {e}")
            st.info("💡 이미 가입된 이메일이거나 비밀번호가 너무 간단할 수 있습니다.")