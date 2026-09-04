# Tuần 14, Đáp án & Giải thích: Advanced RAG + đánh giá (RAGAS)

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Hybrid retrieval kết hợp BM25 và vector search; chúng thường được trộn bằng kỹ thuật nào?

- **A.** Lấy trung bình embedding
- **B.** Reciprocal Rank Fusion (RRF): hợp nhất thứ hạng từ hai bộ retrieve ✅
- **C.** Nối kết quả ngẫu nhiên
- **D.** Chỉ lấy BM25

**Đáp án: B**

**Giải thích:** BM25 (lexical) bắt từ khoá chính xác; vector (semantic) bắt ý nghĩa; RRF hợp nhất để bù điểm yếu của nhau.

## Câu 2 (Tự luận)

Cross-encoder reranker khác bi-encoder (embedding) thế nào, dùng khi nào?

**Trả lời mẫu:** Bi-encoder mã hoá query và document RIÊNG thành vector rồi so cosine, nhanh, scale tốt, dùng để retrieve top-N từ kho lớn. Cross-encoder đưa CẢ cặp (query, document) qua model cùng lúc → chấm điểm liên quan chính xác hơn nhưng chậm, không scale cho toàn kho. Quy trình: bi-encoder lấy top-N (vd. 50), rồi cross-encoder rerank lại để chọn top-k tinh (vd. 5).

**Giải thích:** BGE cross-encoder (mã nguồn mở) là lựa chọn phổ biến.

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
- **B.** Chất lượng RETRIEVAL, đoạn lấy ra có liên quan (precision) và có đủ thông tin cần (recall) không ✅
- **C.** Tốc độ embedding
- **D.** Chi phí API

**Đáp án: B**

**Giải thích:** Hai chỉ số này tách bạch lỗi do retrieval kém với lỗi do generation kém.

## Câu 5 (Tự luận)

Vì sao cần eval set + cẩn trọng với LLM-as-judge?

**Trả lời mẫu:** Cần một eval set (cặp câu hỏi + ground-truth) để đo before/after một cách định lượng thay vì cảm tính. LLM-as-judge (dùng một LLM mạnh chấm output) tiện nhưng nhiều bẫy đã được ghi nhận trong nghiên cứu (arXiv 2306.05685): thiên vị độ dài, thiên vị vị trí, tự khen model cùng họ. Loss thấp hơn KHÔNG tự động nghĩa là hữu ích hơn trong thực tế → đừng tin một chỉ số duy nhất; kết hợp metric tự động + kiểm tra thủ công.

**Giải thích:** Đo lường tốt là điều phân biệt 'nghịch' với 'kỹ thuật'.

## Câu 6 (Trắc nghiệm)

Langfuse/LangSmith dùng để làm gì?

- **A.** Train embedding
- **B.** Tracing/observability: ghi lại từng bước retrieve → generate, chạy eval, LLM-as-judge ✅
- **C.** Lưu vector
- **D.** Lượng tử hoá model

**Đáp án: B**

**Giải thích:** Tracing giúp gỡ lỗi pipeline (đoạn nào retrieve sai, prompt nào hỏng) và đo chất lượng có hệ thống.

## Câu 7 (Tự luận)

Theo IR-book mục 11.4.3, BM25 được thiết kế để mô hình xác suất nhạy với hai đại lượng nào mà mô hình nhị phân độc lập bỏ qua, và điều đó liên quan gì đến cách bạn chunk tài liệu ở Tuần 13?

**Trả lời mẫu:** Hai đại lượng là tần suất từ trong tài liệu (term frequency) và độ dài tài liệu (document length); BM25 chuẩn hóa điểm theo độ dài bằng tham số b và bão hòa tần suất bằng tham số k₁. Chunk dài ngắn không đều sẽ bị chuẩn hóa độ dài kéo điểm lên xuống, nên khi dùng BM25 trong hybrid search cần chunk tương đối đều hoặc hiểu rõ ảnh hưởng của b.

**Giải thích:** IR-book trang 232 nói BM25 'sensitive to these quantities while not introducing too many additional parameters'. Hiểu hai tham số này giúp bạn không coi rank_bm25 là hộp đen khi đo lại RAGAS.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Zheng et al. (arXiv 2306.05685) nêu những thiên vị nào của LLM-as-judge, và bạn kiểm position bias bằng cách nào trong rubric RAGAS?

- **A.** Chỉ có thiên vị độ dài; kiểm bằng cách cắt câu trả lời
- **B.** Position bias, verbosity bias, self-enhancement bias, và limited reasoning ability; kiểm position bias bằng cách đảo thứ tự hai câu trả lời và xem phán quyết có đổi không ✅
- **C.** Chỉ có self-enhancement; kiểm bằng dùng model khác
- **D.** Không có thiên vị nào đáng kể vì agreement trên 80%

**Đáp án: B**

**Giải thích:** Abstract của paper liệt kê bốn hạn chế và báo judge mạnh đạt 'over 80% agreement' với người. Hai điều cùng đúng: dùng được, nhưng phải kiểm.

## Nâng cao 2 (Tự luận)

IR-book nói precision-recall curve của kết quả xếp hạng có hình răng cưa. Vì sao, và context precision của RAGAS liên quan thế nào?

**Trả lời mẫu:** Với kết quả xếp hạng, precision và recall tính trên top-k; khi tài liệu thứ k+1 không liên quan thì recall giữ nguyên còn precision giảm, khi liên quan thì cả hai tăng, nên đường cong nhảy lên xuống (IR-book mục 8.4, trang 158). Context precision của RAGAS là phiên bản dùng LLM phán liên quan của precision trên top-k, nên nó kế thừa cả định nghĩa lẫn cách đọc răng cưa này khi bạn đổi k.

**Giải thích:** Khi so baseline với hybrid và rerank, giữ cùng k để hai số đo so được với nhau.
