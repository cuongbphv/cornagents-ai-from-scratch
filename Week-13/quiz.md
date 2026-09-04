# Tuần 13, Quiz: Xây dựng RAG pipeline end-to-end

> Tự kiểm tra **trước** khi xem solution. Tổng **9** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Thứ tự đúng của một pipeline RAG cơ bản?

- **A.** Retrieve → generate → embed
- **B.** Generate → retrieve → embed → chunk
- **C.** Embed → generate → chunk → store
- **D.** Load → chunk → embed → vector store → retrieve top-k → generate

## Câu 2 (Tự luận)

Vì sao khi chunking cần 'overlap' giữa các đoạn?

## Câu 3 (Trắc nghiệm)

Retrieval trong RAG thường xếp hạng tài liệu bằng độ đo nào?

- **A.** Số ký tự trùng
- **B.** Khoảng cách Hamming
- **C.** Cosine similarity giữa embedding của query và document
- **D.** Thứ tự alphabet

## Câu 4 (Trắc nghiệm)

Chroma đóng vai trò gì trong pipeline?

- **A.** Vector store (lưu & truy vấn nearest-neighbor các embedding): tốt cho dev
- **B.** Mô hình sinh text
- **C.** Tokenizer
- **D.** Reranker

## Câu 5 (Tự luận)

Vì sao RAG giúp giảm hallucination so với hỏi LLM trực tiếp?

## Câu 6 (Trắc nghiệm)

Embedding model làm gì?

- **A.** Lượng tử hoá model
- **B.** Sinh câu trả lời cuối
- **C.** Biến văn bản thành vector số nắm bắt ngữ nghĩa, để so sánh tương đồng
- **D.** Cắt tài liệu thành chunk

## Câu 7 (Trắc nghiệm)

Jurafsky và Martin gọi khiếm khuyết cốt lõi của tf-idf và BM25 là 'vocabulary mismatch problem'. Khiếm khuyết đó là gì và dense retrieval giải quyết ra sao?

- **A.** tf-idf và BM25 không chấm được tài liệu dài; dense retrieval cắt chunk
- **B.** tf-idf và BM25 chỉ hoạt động khi query và tài liệu dùng chung đúng từ, nên người hỏi phải đoán từ người viết đã dùng; dense embedding xử lý được từ đồng nghĩa vì so nghĩa thay vì so chuỗi ký tự
- **C.** tf-idf và BM25 quá chậm với corpus lớn; dense retrieval nhanh hơn nhờ GPU
- **D.** tf-idf và BM25 cần nhãn huấn luyện; dense retrieval thì không

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Jurafsky và Martin gọi khiếm khuyết của tf-idf và BM25 là 'vocabulary mismatch problem'. Trong hybrid search ở Tuần 14, vì sao vẫn giữ BM25 dù đã có dense retrieval?

- **A.** Vì RAGAS bắt buộc dùng BM25
- **B.** Vì BM25 nhanh hơn nên thay được embedding
- **C.** Vì embedding không chạy được trên CPU
- **D.** Vì dense bắt đồng nghĩa nhưng có thể trượt các chuỗi cần khớp chính xác như số hiệu văn bản hay mã điều khoản, thứ BM25 làm tốt; hai nhánh bù khuyết cho nhau rồi gộp bằng RRF

## Nâng cao 2 (Tự luận)

Theo SLP3, RAG có hai thành phần chính và ba mục tiêu. Hãy nêu chúng và chỉ ra mục tiêu nào trùng với lý do repo chọn RAG cho kiến thức quy định.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
