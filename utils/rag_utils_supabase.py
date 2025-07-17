# utils/rag_utils_supabase.py
import os
import uuid
import numpy as np
import vecs                        
from supabase import create_client
from sentence_transformers import SentenceTransformer
from typing import List

PG_URI = (
    os.getenv("SUPABASE_DB_URL")             
)
if not PG_URI:
    raise RuntimeError("❌ 데이터베이스 접속 문자열(SUPABASE_DB_URL)이 없습니다.")

class SupabaseRAG:
    def __init__(self, table: str, dim: int = 384):
        self.sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

        # 클라이언트 생성
        self.vx  = vecs.create_client(PG_URI)    

        # 테이블 준비
        self.col = self.vx.get_or_create_collection(name=table, dimension=dim)

        # 로컬 임베딩 모델
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    # numpy 타입을 Python 기본형으로 변환
    def sanitize_meta(self, meta: dict) -> dict:
        clean = {}
        for k, v in meta.items():
            if hasattr(v, "item"):
                clean[k] = v.item()  # numpy.bool_ 등 처리
            else:
                clean[k] = v
        return clean

    # 문서 추가
    def add(self, docs: List[str], metas: List[dict] | None = None):
        embeds = self.encoder.encode(docs).tolist()
        recs = []

        for i, (d, e) in enumerate(zip(docs, embeds)):
            raw_meta = (metas or [{}])[i]
            merged = {"content": d, **raw_meta}
            sanitized = self.sanitize_meta(merged)
            recs.append((str(uuid.uuid4()), e, sanitized))

        self.col.upsert(records=recs)

    # 질의
    def query(self, q: str, k: int = 5):
        q_emb = self.encoder.encode([q]).tolist()[0]
        records = self.col.query(
            data=q_emb,
            limit=k,
            include_metadata=True,   
            include_value=False  
        )

        return [
            (r[-1] or {}).get("content", "")
            for r in records
            if r and isinstance(r[-1], dict) and r[-1].get("content")
        ]

    def query_collection(self, table: str, query: str, top_k: int = 5):
        return self.query(query, k=top_k)