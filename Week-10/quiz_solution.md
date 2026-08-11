# Tuần 10 — Đáp án & Giải thích: Xây dựng RAG pipeline end-to-end

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Thứ tự đúng của một pipeline RAG cơ bản?

- **A.** Generate → retrieve → embed → chunk
- **B.** Load → chunk → embed → vector store → retrieve top-k → generate ✅
- **C.** Embed → generate → chunk → store
- **D.** Retrieve → generate → embed

**Đáp án: B**

**Giải thích:** Load tài liệu → cắt chunk → embed → lưu vector store → khi hỏi: embed query, retrieve top-k, ghép context vào prompt → generate.

## Câu 2 (Tự luận)

Vì sao khi chunking cần 'overlap' giữa các đoạn?

**Trả lời mẫu:** Overlap (vd. ~100 ký tự/token) giữ phần đầu/cuối câu liền mạch giữa hai chunk, tránh cắt đứt một ý/định nghĩa ngay ranh giới chunk khiến retrieval bỏ sót ngữ cảnh cần thiết. Với chunk ~800 và overlap ~100, một thông tin nằm ở mép vẫn xuất hiện trọn trong ít nhất một chunk.

**Giải thích:** Chunk quá nhỏ mất ngữ cảnh; quá lớn loãng tín hiệu retrieval. Overlap là cân bằng.

## Câu 3 (Trắc nghiệm)

Retrieval trong RAG thường xếp hạng tài liệu bằng độ đo nào?

- **A.** Khoảng cách Hamming
- **B.** Cosine similarity giữa embedding của query và document ✅
- **C.** Số ký tự trùng
- **D.** Thứ tự alphabet

**Đáp án: B**

**Giải thích:** sim(q,d) = (q·d)/(|q||d|). Tài liệu có embedding gần (cosine cao) với query được lấy ra trước.

## Câu 4 (Trắc nghiệm)

Chroma đóng vai trò gì trong pipeline?

- **A.** Mô hình sinh text
- **B.** Vector store (lưu & truy vấn nearest-neighbor các embedding) — tốt cho dev ✅
- **C.** Tokenizer
- **D.** Reranker

**Đáp án: B**

**Giải thích:** Chroma là vector DB nhẹ cho dev; production có thể chuyển pgvector/Qdrant/Weaviate.

## Câu 5 (Tự luận)

Vì sao RAG giúp giảm hallucination so với hỏi LLM trực tiếp?

**Trả lời mẫu:** RAG 'grounding' câu trả lời vào các đoạn tài liệu thật được retrieve và đưa vào prompt, nên model trả lời dựa trên bằng chứng cụ thể thay vì chỉ dựa vào trí nhớ tham số (dễ bịa). Ngoài ra có thể trích dẫn nguồn để kiểm chứng. Nó cũng cập nhật được kiến thức mới mà không cần train lại.

**Giải thích:** Anchor của roadmap: corpus là tài liệu nghiệp vụ Finance Banking của bạn.

## Câu 6 (Trắc nghiệm)

Embedding model làm gì?

- **A.** Sinh câu trả lời cuối
- **B.** Biến văn bản thành vector số nắm bắt ngữ nghĩa, để so sánh tương đồng ✅
- **C.** Cắt tài liệu thành chunk
- **D.** Lượng tử hoá model

**Đáp án: B**

**Giải thích:** Embedding (BGE/e5/nomic...) ánh xạ text → vector; văn bản gần nghĩa → vector gần nhau.
