# Tuần 11 — Advanced RAG + đánh giá

> Phase 2 — Applied. Thêm hybrid search, reranking, và đánh giá nghiêm túc; học observability.

## Mục tiêu

- Thêm **hybrid search** (BM25 + vector) và **reranker**.
- Đánh giá định lượng với **RAGAS**; wire **tracing** (Langfuse/LangSmith).

## Nguồn học

- **RAGAS** docs (context precision/recall, faithfulness, answer relevancy).
- **LangSmith** + **Langfuse** (tracing, LLM-as-judge).
- **BGE cross-encoder** reranker (mã nguồn mở).
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
- [ ] Thêm reranker (BGE cross-encoder) trên top-N
- [ ] Tạo eval set: ~20–30 cặp (câu hỏi, câu trả lời/ground-truth)
- [ ] Đo RAGAS: context precision/recall, faithfulness, answer relevancy
- [ ] So sánh baseline (Tuần 10) vs hybrid+rerank → bảng số
- [ ] Wire Langfuse/LangSmith tracing → xem từng bước retrieval/generate
- [ ] Viết `ragas_report.md`

## 🚀 Bổ sung nâng cao (đo lường cho đúng)

Tuần này bạn bắt đầu tin vào số, nên đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **H — đầy đủ**:

- **LLM-as-judge có nhiều bẫy** đã được ghi nhận trong nghiên cứu (arXiv 2306.05685): thiên vị độ dài, thiên vị vị trí, tự khen model cùng họ. RAGAS dùng LLM để chấm faithfulness/relevancy → những bẫy này áp trực tiếp vào báo cáo của bạn.
- **Loss thấp hơn KHÔNG tự động nghĩa là hữu ích hơn** trong thực tế → đừng tin một chỉ số duy nhất; kết hợp metric tự động + kiểm tra thủ công một mẫu nhỏ.
- **Perplexity phụ thuộc tokenizer**, `bits-per-byte` mới so chéo được — cần khi bạn so nhiều model backend khác nhau.

> Nguyên tắc mang sang Phase 3: một pipeline có scorer tốt thì tự cải thiện; pipeline không có thì âm thầm trôi.

## 📦 Dữ liệu cho tuần này

Xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md) — mục **1** (`YuITC/Vietnamese-Legal-Documents`, MIT — benchmark retrieval để đo retriever của bạn), mục **4** (các bộ chỉ-dùng-để-eval), mục **9** (benchmark tiếng Việt).

> Không benchmark công khai nào đo được "model trả lời đúng quy định của bạn hay chưa" — tự xây eval set ~50–100 câu nghiệp vụ thật, mỗi câu kèm điều khoản dẫn nguồn.

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `advanced_rag_notes.md` | Hướng dẫn hybrid + rerank + tracing (code mẫu) |
| `ragas_report.md` | Template báo cáo eval before/after (deliverable) |
