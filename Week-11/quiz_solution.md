# Tuần 11 — Đáp án & Giải thích: Advanced RAG + đánh giá (RAGAS)

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Hybrid retrieval kết hợp BM25 và vector search; chúng thường được trộn bằng kỹ thuật nào?

- **A.** Lấy trung bình embedding
- **B.** Reciprocal Rank Fusion (RRF) — hợp nhất thứ hạng từ hai bộ retrieve ✅
- **C.** Nối kết quả ngẫu nhiên
- **D.** Chỉ lấy BM25

**Đáp án: B**

**Giải thích:** BM25 (lexical) bắt từ khoá chính xác; vector (semantic) bắt ý nghĩa; RRF hợp nhất để bù điểm yếu của nhau.

## Câu 2 (Tự luận)

Cross-encoder reranker khác bi-encoder (embedding) thế nào, dùng khi nào?

**Trả lời mẫu:** Bi-encoder mã hoá query và document RIÊNG thành vector rồi so cosine — nhanh, scale tốt, dùng để retrieve top-N từ kho lớn. Cross-encoder đưa CẢ cặp (query, document) qua model cùng lúc → chấm điểm liên quan chính xác hơn nhưng chậm, không scale cho toàn kho. Quy trình: bi-encoder lấy top-N (vd. 50), rồi cross-encoder rerank lại để chọn top-k tinh (vd. 5).

**Giải thích:** BGE cross-encoder hoặc Cohere Rerank là lựa chọn phổ biến.

## Câu 3 (Trắc nghiệm)

Trong RAGAS, 'faithfulness' đo điều gì?

- **A.** Câu trả lời có bám/được hỗ trợ bởi context retrieve hay không (chống bịa) ✅
- **B.** Tốc độ trả lời
- **C.** Độ dài câu trả lời
- **D.** Số token dùng

**Đáp án: A**

**Giải thích:** Faithfulness kiểm tra các khẳng định trong câu trả lời có truy được về context không → thước đo chống hallucination.

## Câu 4 (Trắc nghiệm)

'Context precision' và 'context recall' trong RAGAS đánh giá khâu nào?

- **A.** Khâu generate
- **B.** Chất lượng RETRIEVAL — đoạn lấy ra có liên quan (precision) và có đủ thông tin cần (recall) không ✅
- **C.** Tốc độ embedding
- **D.** Chi phí API

**Đáp án: B**

**Giải thích:** Hai chỉ số này tách bạch lỗi do retrieval kém với lỗi do generation kém.

## Câu 5 (Tự luận)

Vì sao cần eval set + cẩn trọng với LLM-as-judge (Giles part 30)?

**Trả lời mẫu:** Cần một eval set (cặp câu hỏi + ground-truth) để đo before/after một cách định lượng thay vì cảm tính. LLM-as-judge (dùng một LLM mạnh chấm output) tiện nhưng nhiều bẫy: thiên vị độ dài, thiên vị vị trí, tự khen model cùng họ. Giles còn cho thấy loss thấp hơn KHÔNG đảm bảo hữu ích hơn trong thực tế → đừng tin một chỉ số duy nhất; kết hợp metric tự động + kiểm tra thủ công.

**Giải thích:** Đo lường tốt là điều phân biệt 'nghịch' với 'kỹ thuật'.

## Câu 6 (Trắc nghiệm)

Langfuse/LangSmith dùng để làm gì?

- **A.** Train embedding
- **B.** Tracing/observability: ghi lại từng bước retrieve → generate, chạy eval, LLM-as-judge ✅
- **C.** Lưu vector
- **D.** Lượng tử hoá model

**Đáp án: B**

**Giải thích:** Tracing giúp gỡ lỗi pipeline (đoạn nào retrieve sai, prompt nào hỏng) và đo chất lượng có hệ thống.
