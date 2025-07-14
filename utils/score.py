# utils/score.py
import hashlib
from utils.auth import get_client

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def submit_flag(user_id: str, chall: str, flag: str) -> bool:
    supabase = get_client()
    h = sha256_hex(flag.strip())

    row = (supabase.table("flags")
           .select("points")
           .eq("challenge_id", chall)
           .eq("flag_hash", h)
           .single()
           .execute()
           .data)
    if not row:
        return False

    supabase.table("scores").upsert(
        {"user_id": user_id, "challenge_id": chall, "score": row["points"]}
    ).execute()
    return True

def total_score(user_id: str) -> int:
    supabase = get_client()
    rows = (supabase.table("scores")
            .select("score")
            .eq("user_id", user_id)
            .execute()
            .data)
    return sum(r["score"] for r in rows)
