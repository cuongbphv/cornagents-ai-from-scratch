# Tuần 10 — Xây dựng RAG pipeline end-to-end

> Phase 2 — Applied. Chunking → embeddings → vector store → retrieval → generation, trên tài liệu Finance Banking của bạn.

## Mục tiêu

Build baseline RAG đầy đủ trên corpus tài liệu nghiệp vụ Finance Banking của bạn.

## Nguồn học

- DeepLearning.AI — **"Retrieval Augmented Generation"** (audit free) và/hoặc freeCodeCamp **"RAG from Scratch"**.
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

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `rag_pipeline.py` | Starter RAG (load→chunk→embed→store→retrieve→generate) |
| `data/` | (bạn tự thêm) PDF/tài liệu Finance Banking |

> Anchor: corpus, dataset fine-tune và capstone NÊN đều là tài liệu nghiệp vụ Finance Banking (giữ tổng quát) — đây là điểm khác biệt của bạn.
