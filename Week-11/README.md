# Tuần 11 — Advanced RAG + đánh giá

> Phase 2 — Applied. Thêm hybrid search, reranking, và đánh giá nghiêm túc; học observability.

## Mục tiêu

- Thêm **hybrid search** (BM25 + vector) và **reranker**.
- Đánh giá định lượng với **RAGAS**; wire **tracing** (Langfuse/LangSmith).

## Nguồn học

- **RAGAS** docs (context precision/recall, faithfulness, answer relevancy).
- **LangSmith** + **Langfuse** (tracing, LLM-as-judge).
- **Cohere Rerank** hoặc **BGE cross-encoder** reranker.
- Tùy chọn nâng cao: **GraphRAG** (Microsoft).

## Nhiệm vụ (Task)

Nâng cấp pipeline Tuần 10: retrieval hybrid (BM25 + vector) + reranker; đo before/after bằng RAGAS; wire Langfuse/LangSmith.

## Deliverable

- Báo cáo eval RAGAS cho thấy **cải thiện relevancy đo được** nhờ reranking.
- Pipeline đã được trace.

## Thời lượng

~10–12 giờ.

## Phần cứng

Local; cross-encoder reranker chạy ổn trên Mac/3070 Ti.

---

## Checklist tiến độ

- [ ] Thêm BM25 retriever (rank_bm25) song song vector retriever
- [ ] Kết hợp kết quả (EnsembleRetriever / reciprocal rank fusion)
- [ ] Thêm reranker (BGE cross-encoder hoặc Cohere Rerank) trên top-N
- [ ] Tạo eval set: ~20–30 cặp (câu hỏi, câu trả lời/ground-truth)
- [ ] Đo RAGAS: context precision/recall, faithfulness, answer relevancy
- [ ] So sánh baseline (Tuần 10) vs hybrid+rerank → bảng số
- [ ] Wire Langfuse/LangSmith tracing → xem từng bước retrieval/generate
- [ ] Viết `ragas_report.md`

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `advanced_rag_notes.md` | Hướng dẫn hybrid + rerank + tracing (code mẫu) |
| `ragas_report.md` | Template báo cáo eval before/after (deliverable) |
