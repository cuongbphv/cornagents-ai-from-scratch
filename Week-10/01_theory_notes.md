# Lý thuyết Tuần 10 — RAG pipeline end-to-end

> Đọc trước khi điền [`02_rag_pipeline.py`](02_rag_pipeline.py). Ví dụ số kiểm chứng bằng PyTorch 2.5.1 + tiktoken ngày 2026-08-11; nguồn cuối file.

---

## 1. Vì sao RAG — và vì sao không phải fine-tune

Nguyên tắc đã chốt từ Tuần 8: **fine-tune dạy hành vi, RAG cung cấp kiến thức.** Kiến thức quy định (thông tư, điều khoản) thay đổi liên tục và cần dẫn nguồn — nhét vào trọng số thì không cập nhật được, không trích dẫn được, và không kiểm chứng được. RAG (Lewis et al., arXiv 2005.11401) tách đôi: kiến thức nằm trong **kho tài liệu truy xuất được**, model chỉ làm việc đọc-hiểu-trả-lời trên context được đưa vào.

Pipeline baseline 6 khâu — hỏng khâu nào hỏng cả chuỗi:

```
Load PDF → Chunk → Embed → Vector store → Retrieve top-k → Generate (kèm context)
```

## 2. Embeddings + cosine similarity — thước đo "gần nghĩa"

Embedding model biến đoạn văn thành vector; hai đoạn gần nghĩa → vector gần nhau theo **cosine similarity**:

```
cos(a, b) = (a·b) / (|a||b|)     ∈ [−1, 1]
```

Kiểm chứng 2026-08-11: `cos(a, 2a) = 1.0` (cùng hướng tuyệt đối — cosine bỏ qua độ dài, chỉ đo hướng); hai vector lệch hướng cho 0.378. Retrieval = embed câu hỏi → tìm k chunk có cosine cao nhất trong store. Lưu ý nền từ Tuần 1: đây vẫn chỉ là dot product sau khi chuẩn hóa.

**Embedding model là quyết định chất lượng số 1 của RAG** — nó quyết định "gần nghĩa" nghĩa là gì. Chọn theo benchmark phù hợp ngôn ngữ của corpus (mục 6).

## 3. Chunking — cắt tài liệu không làm đứt nghĩa

- Baseline README: `RecursiveCharacterTextSplitter`, size ~800, overlap ~100. Splitter này đếm theo **ký tự** và ưu tiên cắt tại ranh giới tự nhiên (đoạn → câu → từ) theo thứ tự separator.
- **Ký tự ≠ token.** Đo thật trên một câu thông tư tiếng Việt (cl100k, 2026-08-11): 115 ký tự → 52 token, tức ~**2.2 ký tự/token** — chunk 800 ký tự tiếng Việt ≈ 360 token. Muốn kiểm soát ngân sách context chính xác thì đếm bằng token của đúng model bạn dùng, đừng áng chừng theo ký tự.
- Overlap tồn tại để câu nằm vắt qua ranh giới chunk không bị mất ngữ cảnh ở cả hai phía.
- Với văn bản pháp luật, ranh giới tự nhiên tốt nhất là **Điều/Khoản/Điểm** — cắt theo cấu trúc văn bản (semantic) luôn thắng cắt theo đếm ký tự mù; giữ số hiệu Điều trong metadata của chunk.

## 4. Vector store + metadata — chỗ provenance bắt đầu

- **Chroma** cho dev (persist xuống đĩa, không cần server); pgvector/Qdrant khi cần production.
- Mỗi chunk lưu kèm **metadata: tên văn bản, số hiệu, điều khoản, ngày hiệu lực** — Tuần 14 cần chúng làm provenance, và câu trả lời có dẫn nguồn cần chúng ngay tuần này. Mất metadata lúc ingest là mất vĩnh viễn.

## 5. Generate — grounding là mục tiêu, không phải văn hay

- Prompt template tối thiểu: *"Chỉ trả lời dựa trên context dưới đây. Không tìm thấy thông tin thì nói không tìm thấy."* + context top-k + câu hỏi.
- **Temperature ≤ 0.3** cho RAG nghiệp vụ (khuyến nghị trong README, mục nâng cao B2): cùng context đó, temperature cao làm model "suy diễn vượt nguồn" nhiều hơn.
- Test 10 câu hỏi domain: với mỗi câu trả lời, tự hỏi **"câu này dẫn về được chunk nào?"** — không dẫn được = chưa grounded, đánh dấu lại làm baseline cho Tuần 11 đo.

## 6. Tiếng Việt trong tuần này — 3 bẫy có bằng chứng

1. **Unicode NFC vs NFD** — bẫy âm thầm nhất. Kiểm chứng 2026-08-11: ký tự `ế` dạng NFC là **1 codepoint**, dạng NFD là **3 codepoint** (e + dấu mũ + dấu sắc), và hai chuỗi **không bằng nhau** khi so sánh trực tiếp. Corpus scrape từ nhiều nguồn có thể trộn cả hai dạng → cùng một từ thành hai chuỗi khác nhau khi match, đếm ký tự lệch, highlight sai. **Chuẩn hóa `unicodedata.normalize("NFC", text)` ngay tại bước load, trước mọi xử lý khác.**
2. **Embedding model phải hỗ trợ tiếng Việt thật** — model embedding train chủ yếu tiếng Anh cho cosine similarity kém nghĩa trên tiếng Việt. Chọn theo **VN-MTEB** (benchmark embedding tiếng Việt — mục 9 của [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md)); nghi ngờ thì tự test: 5 cặp câu nghiệp vụ đồng nghĩa + 5 cặp không liên quan, xem cosine có tách hai nhóm không.
3. **Ngân sách token tiếng Việt**: 2.2 ký tự/token (đo ở mục 3) — khi ước lượng "top-k chunk có vừa context window không", tính bằng token thật, nhất là khi generate bằng model local context ngắn.

Corpus khuyến nghị + lưu ý pháp lý: xem mục 📦 trong [README.md](README.md) (nguồn vbpl.vn, giữ metadata ngày hiệu lực).

## 7. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| Lewis et al. 2020 — RAG | https://arxiv.org/abs/2005.11401 | 1 |

(LlamaIndex/LangChain docs, NirDiamant/RAG_Techniques: link trong README nguồn học — API đổi theo version, đọc docs đúng version bạn cài.)

## Sau khi đọc xong

1. Thu thập corpus vào `data/`, **normalize NFC ngay khi load**.
2. Điền [`02_rag_pipeline.py`](02_rag_pipeline.py) theo 6 khâu; chunk giữ metadata điều khoản.
3. Test 10 câu hỏi domain, ghi lại câu nào grounded/câu nào không — đây là baseline Tuần 11.
4. Làm [`quiz.md`](quiz.md).
