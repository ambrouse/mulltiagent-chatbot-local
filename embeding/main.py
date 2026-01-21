import os
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union, Dict, Any

# Import thư viện BAAI
from FlagEmbedding import BGEM3FlagModel, FlagReranker

app = FastAPI(title="Test BAAI Server SOTA")

# --- GLOBAL VARIABLES ---
embed_model = None
rerank_model = None

# --- CONFIG ---
if torch.cuda.is_available():
    DEVICE = "cuda"
    print(f"🔥 PHÁT HIỆN GPU: {torch.cuda.get_device_name(0)}")
else:
    DEVICE = "cpu"
    print("⚠️ CẢNH BÁO: Đang chạy bằng CPU!")

EMBED_MODEL_ID = "BAAI/bge-m3"
RERANK_MODEL_ID = "BAAI/bge-reranker-v2-m3"

@app.on_event("startup")
async def startup_event():
    global embed_model, rerank_model
    
    # 1. Load Embedding
    # use_fp16=True: Tăng tốc và giảm VRAM
    print(f"⏳ Đang tải Embedding: {EMBED_MODEL_ID} ...")
    embed_model = BGEM3FlagModel(EMBED_MODEL_ID, use_fp16=True, device=DEVICE)
    print("✅ Embedding Model OK!")
    
    # 2. Load Reranker
    print(f"⏳ Đang tải Reranker: {RERANK_MODEL_ID} ...")
    rerank_model = FlagReranker(RERANK_MODEL_ID, use_fp16=True, device=DEVICE)
    print("✅ Reranker Model OK!")

# --- REQUEST MODELS ---
class EmbedRequest(BaseModel):
    input: Union[str, List[str]]
    is_query: bool = False # <-- THÊM CỜ NÀY: Để phân biệt câu hỏi và tài liệu

class RerankRequest(BaseModel):
    query: str
    documents: List[str]

# --- ENDPOINTS ---

@app.post("/embed")
async def create_embedding(req: EmbedRequest):
    """
    Trả về cả Dense Vector (Ngữ nghĩa) và Sparse Vector (Từ khóa)
    """
    sentences = [req.input] if isinstance(req.input, str) else req.input
    
    # XỬ LÝ INSTRUCTION (QUAN TRỌNG CHO ĐỘ CHÍNH XÁC)
    # BGE-M3 hoạt động tốt nhất khi Query được thêm chỉ dẫn, còn Doc thì không
    if req.is_query:
        # Instruction chuẩn của BGE cho retrieval
        # Lưu ý: BGE-M3 thông minh hơn bản cũ, nhưng thêm instruction vẫn giúp định hướng tốt hơn
        # Tuy nhiên, thư viện FlagEmbedding thường tự xử lý nếu dùng hàm encode_queries
        # Ở đây ta dùng encode chung nên có thể giữ nguyên hoặc thêm prefix nếu cần thiết.
        # Với BGE-M3, việc phân biệt Query/Doc chủ yếu nằm ở cách ta dùng vector sau này.
        pass 

    # encode trả về dictionary chứa: dense_vecs, sparse_vecs, colbert_vecs
    output = embed_model.encode(
        sentences, 
        batch_size=12, 
        max_length=8192,
        return_dense=True,   # Lấy vector ngữ nghĩa
        return_sparse=True,  # <--- LẤY THÊM CÁI NÀY (Lexical Weights)
        return_colbert_vecs=False # Tắt cái này đi cho nhẹ (trừ khi bạn dùng ColBERT)
    )
    
    # Chuẩn bị kết quả trả về
    dense_data = output['dense_vecs'].tolist()
    
    # Sparse vector trả về dạng dictionary {token_id: weight}, ta cần xử lý chút để trả JSON
    # output['lexical_weights'] là list các dict
    sparse_data = output['lexical_weights'] 

    return {
        "object": "list",
        "data": [
            {
                "index": i,
                "embedding": dense_data[i], # Vector ngữ nghĩa (Dùng cho vector search)
                "sparse_embedding": sparse_data[i] # Vector từ khóa (Dùng cho keyword boosting)
            } 
            for i in range(len(dense_data))
        ]
    }

@app.post("/rerank")
async def rerank_docs(req: RerankRequest):
    if not req.documents: return {"results": []}
    
    # Reranker BGE-M3 tự động xử lý ngữ nghĩa và từ khóa bên trong nó
    pairs = [[req.query, doc] for doc in req.documents]
    
    scores = rerank_model.compute_score(pairs, batch_size=12, max_length=2048) # Tăng max_length nếu tài liệu dài
    
    if isinstance(scores, float): scores = [scores]
    
    results = [{"index": i, "score": s, "text": req.documents[i]} for i, s in enumerate(scores)]
    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": results}