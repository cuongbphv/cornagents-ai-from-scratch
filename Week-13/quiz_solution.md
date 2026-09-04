# Tuần 13, Đáp án & Giải thích: Xây dựng RAG pipeline end-to-end

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Thứ tự đúng của một pipeline RAG cơ bản?

- **A.** Generate → retrieve → embed → chunk
- **B.** Load → chunk → embed → vector store → retrieve top-k → generate (đáp án đúng)
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
- **B.** Cosine similarity giữa embedding của query và document (đáp án đúng)
- **C.** Số ký tự trùng
- **D.** Thứ tự alphabet

**Đáp án: B**

**Giải thích:** sim(q,d) = (q·d)/(|q||d|). Tài liệu có embedding gần (cosine cao) với query được lấy ra trước.

## Câu 4 (Trắc nghiệm)

Chroma đóng vai trò gì trong pipeline?

- **A.** Mô hình sinh text
- **B.** Vector store (lưu & truy vấn nearest-neighbor các embedding): tốt cho dev (đáp án đúng)
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
- **B.** Biến văn bản thành vector số nắm bắt ngữ nghĩa, để so sánh tương đồng (đáp án đúng)
- **C.** Cắt tài liệu thành chunk
- **D.** Lượng tử hoá model

**Đáp án: B**

**Giải thích:** Embedding (BGE/e5/nomic...) ánh xạ text → vector; văn bản gần nghĩa → vector gần nhau.

## Câu 7 (Trắc nghiệm)

Jurafsky và Martin gọi khiếm khuyết cốt lõi của tf-idf và BM25 là 'vocabulary mismatch problem'. Khiếm khuyết đó là gì và dense retrieval giải quyết ra sao?

- **A.** tf-idf và BM25 quá chậm với corpus lớn; dense retrieval nhanh hơn nhờ GPU
- **B.** tf-idf và BM25 chỉ hoạt động khi query và tài liệu dùng chung đúng từ, nên người hỏi phải đoán từ người viết đã dùng; dense embedding xử lý được từ đồng nghĩa vì so nghĩa thay vì so chuỗi ký tự (đáp án đúng)
- **C.** tf-idf và BM25 không chấm được tài liệu dài; dense retrieval cắt chunk
- **D.** tf-idf và BM25 cần nhãn huấn luyện; dense retrieval thì không

**Đáp án: B**

**Giải thích:** SLP3 mục 11.3 trang 264: 'they work only if there is exact overlap of words between the query and document'. Vì thế Tuần 14 dùng cả hai trong hybrid search: BM25 bắt từ khóa chính xác, dense bắt đồng nghĩa.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Jurafsky và Martin gọi khiếm khuyết của tf-idf và BM25 là 'vocabulary mismatch problem'. Trong hybrid search ở Tuần 14, vì sao vẫn giữ BM25 dù đã có dense retrieval?

- **A.** Vì BM25 nhanh hơn nên thay được embedding
- **B.** Vì dense bắt đồng nghĩa nhưng có thể trượt các chuỗi cần khớp chính xác như số hiệu văn bản hay mã điều khoản, thứ BM25 làm tốt; hai nhánh bù khuyết cho nhau rồi gộp bằng RRF (đáp án đúng)
- **C.** Vì embedding không chạy được trên CPU
- **D.** Vì RAGAS bắt buộc dùng BM25

**Đáp án: B**

**Giải thích:** SLP3 mục 11.3 (trang 264) nêu khiếm khuyết của sparse; phần lý giải vì sao vẫn giữ BM25 là suy luận thực hành của người viết cho corpus pháp lý.

## Nâng cao 2 (Tự luận)

Theo SLP3, RAG có hai thành phần chính và ba mục tiêu. Hãy nêu chúng và chỉ ra mục tiêu nào trùng với lý do repo chọn RAG cho kiến thức quy định.

**Trả lời mẫu:** Hai thành phần: retriever và generator (đôi khi gọi reader). Ba mục tiêu: giảm hallucination bằng tập tài liệu đáng tin, sinh text đúng về dữ liệu riêng như tài liệu nội bộ hay pháp lý, và xử lý kiến thức thay đổi theo thời gian (SLP3 mục 11.4, trang 267). Cả ba trùng với lý do của repo: văn bản pháp luật thay đổi, cần dẫn nguồn, và không được bịa.

**Giải thích:** Paper 'Does Fine-Tuning on New Knowledge Encourage Hallucinations?' trong kệ paper là bằng chứng thực nghiệm cho việc không nhét kiến thức quy định vào trọng số.
