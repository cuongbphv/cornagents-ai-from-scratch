# Tuần 11 — Quiz: Advanced RAG + đánh giá (RAGAS)

> Tự kiểm tra **trước** khi xem solution. Tổng **6** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Hybrid retrieval kết hợp BM25 và vector search; chúng thường được trộn bằng kỹ thuật nào?

- **A.** Lấy trung bình embedding
- **B.** Reciprocal Rank Fusion (RRF) — hợp nhất thứ hạng từ hai bộ retrieve
- **C.** Nối kết quả ngẫu nhiên
- **D.** Chỉ lấy BM25

## Câu 2 (Tự luận)

Cross-encoder reranker khác bi-encoder (embedding) thế nào, dùng khi nào?

## Câu 3 (Trắc nghiệm)

Trong RAGAS, 'faithfulness' đo điều gì?

- **A.** Câu trả lời có bám/được hỗ trợ bởi context retrieve hay không (chống bịa)
- **B.** Tốc độ trả lời
- **C.** Độ dài câu trả lời
- **D.** Số token dùng

## Câu 4 (Trắc nghiệm)

'Context precision' và 'context recall' trong RAGAS đánh giá khâu nào?

- **A.** Khâu generate
- **B.** Chất lượng RETRIEVAL — đoạn lấy ra có liên quan (precision) và có đủ thông tin cần (recall) không
- **C.** Tốc độ embedding
- **D.** Chi phí API

## Câu 5 (Tự luận)

Vì sao cần eval set + cẩn trọng với LLM-as-judge?

## Câu 6 (Trắc nghiệm)

Langfuse/LangSmith dùng để làm gì?

- **A.** Train embedding
- **B.** Tracing/observability: ghi lại từng bước retrieve → generate, chạy eval, LLM-as-judge
- **C.** Lưu vector
- **D.** Lượng tử hoá model

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
