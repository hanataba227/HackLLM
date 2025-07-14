import streamlit as st
import pandas as pd
from utils.auth import get_admin_client_direct
from utils.ui import render_sidebar_menu

st.set_page_config(page_title="전체 유저 랭킹", page_icon="🏆")

render_sidebar_menu()

st.header("🏆 전체 유저 랭킹")

supabase = get_admin_client_direct()

# scores 테이블 불러오기
score_rows = supabase.table("scores").select("user_id, score").execute().data
df_scores = pd.DataFrame(score_rows)

# profiles 테이블 불러오기
user_rows = supabase.table("profiles").select("id, username").execute().data
df_users = pd.DataFrame(user_rows).rename(columns={"id": "user_id"})

# 유저 정보 병합
if df_scores.empty or df_users.empty:
    st.warning("데이터가 충분하지 않습니다.")
else:
    df = pd.merge(df_scores, df_users, on="user_id", how="left")
    df_grouped = (
        df.groupby(["user_id", "username"], as_index=False)["score"]
        .sum()
        .sort_values("score", ascending=False)
    )
    df_grouped["순위"] = range(1, len(df_grouped) + 1)

    df_display = df_grouped[["순위", "username", "score"]].rename(
        columns={"username": "닉네임", "score": "총점"}
    )

    st.dataframe(df_display, use_container_width=True)