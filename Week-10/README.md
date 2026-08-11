# Tuần 10 — Xây dựng RAG pipeline end-to-end

> Phase 2 — Applied. Chunking → embeddings → vector store → retrieval → generation, trên tài liệu Finance Banking của bạn.

## Mục tiêu

Build baseline RAG đầy đủ trên corpus tài liệu nghiệp vụ Finance Banking của bạn.

## Nguồn học

- Paper gốc RAG (arXiv 2005.11401) — nền lý thuyết; tutorial RAG chính thức trong docs LlamaIndex/LangChain.
- **LlamaIndex** + **LangChain** docs.
- GitHub: **NirDiamant/RAG_Techniques**, sosanzma/rag-techniques-handbook.

## Nhiệm vụ (Task)

Load PDFs → `RecursiveCharacterTextSplitter` (chunk ~800, overlap ~100) → embed → **Chroma** (dev) → retrieve top-k → generate bằng Ollama local hoặc Claude. Dùng **pgvector/Qdrant** nếu muốn production-grade.

## Deliverable

App RAG trả lời được câu hỏi trên tài liệu Finance Banking của bạn.

## Thời lượng

~12 giờ.

## Phần cứng

Mac hoặc 3070 Ti cho embeddings/inference local; embeddings nhẹ.

---

## Checklist tiến độ

- [ ] Thu thập corpus (PDF tài liệu nghiệp vụ nội bộ) vào `data/`
- [ ] Load + parse PDF (PyPDF / Unstructured)
- [ ] Chunk: RecursiveCharacterTextSplitter (size ~800, overlap ~100)
- [ ] Chọn embedding model (BGE / e5 / OpenAI / nomic) — local được
- [ ] Index vào Chroma (persist xuống đĩa)
- [ ] Retrieve top-k + lắp prompt context
- [ ] Generate bằng Ollama (Tuần 9) hoặc Claude
- [ ] Test 10 câu hỏi domain → kiểm tra câu trả lời có grounding
- [ ] (Chuẩn bị Tuần 11) lưu lại baseline để so sánh sau khi thêm rerank

## 🚀 Bổ sung nâng cao (sampling quyết định độ "bịa")

Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **B2 Sampling**:

Cùng một context retrieve được, `temperature` và `top-p` vẫn quyết định câu trả lời bám nguồn hay bắt đầu suy diễn. Với RAG trên tài liệu nghiệp vụ, mặc định nên **hạ temperature** (≤0.3) và giữ top-p vừa phải — ưu tiên groundedness hơn sự "mượt".

> ➡️ Tuần 11 sẽ đọc mục **H** đầy đủ để biết cách *đo* điều này thay vì cảm nhận.

## 📦 Dữ liệu cho tuần này

Xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md) — mục **1** (nguồn quy định tiếng Việt) và mục **9** (chọn embedding model).

Corpus khuyến nghị: `th1nhng0/vietnamese-legal-documents` (CC BY 4.0, 171k văn bản scrape từ **vbpl.vn** của Bộ Tư pháp) → **filter riêng phần NHNN**. Chọn embedding model tham chiếu **VN-MTEB**.

> ⚠️ Đọc mục **6** về pháp lý trước khi tải: ưu tiên nguồn chính thức (vbpl.vn) hơn aggregator thương mại có paywall; và giữ lại metadata nguồn + ngày hiệu lực của từng văn bản — bạn sẽ cần chúng làm provenance ở Tuần 14.

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `rag_pipeline.py` | Starter RAG (load→chunk→embed→store→retrieve→generate) |
| `data/` | (bạn tự thêm) PDF/tài liệu Finance Banking |

> Anchor: corpus, dataset fine-tune và capstone NÊN đều là tài liệu nghiệp vụ Finance Banking (giữ tổng quát) — đây là điểm khác biệt của bạn.
