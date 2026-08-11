# Tuần 10 — Quiz: Xây dựng RAG pipeline end-to-end

> Tự kiểm tra **trước** khi xem solution. Tổng **6** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Thứ tự đúng của một pipeline RAG cơ bản?

- **A.** Generate → retrieve → embed → chunk
- **B.** Load → chunk → embed → vector store → retrieve top-k → generate
- **C.** Embed → generate → chunk → store
- **D.** Retrieve → generate → embed

## Câu 2 (Tự luận)

Vì sao khi chunking cần 'overlap' giữa các đoạn?

## Câu 3 (Trắc nghiệm)

Retrieval trong RAG thường xếp hạng tài liệu bằng độ đo nào?

- **A.** Khoảng cách Hamming
- **B.** Cosine similarity giữa embedding của query và document
- **C.** Số ký tự trùng
- **D.** Thứ tự alphabet

## Câu 4 (Trắc nghiệm)

Chroma đóng vai trò gì trong pipeline?

- **A.** Mô hình sinh text
- **B.** Vector store (lưu & truy vấn nearest-neighbor các embedding) — tốt cho dev
- **C.** Tokenizer
- **D.** Reranker

## Câu 5 (Tự luận)

Vì sao RAG giúp giảm hallucination so với hỏi LLM trực tiếp?

## Câu 6 (Trắc nghiệm)

Embedding model làm gì?

- **A.** Sinh câu trả lời cuối
- **B.** Biến văn bản thành vector số nắm bắt ngữ nghĩa, để so sánh tương đồng
- **C.** Cắt tài liệu thành chunk
- **D.** Lượng tử hoá model

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
