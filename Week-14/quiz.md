# Tuần 14, Quiz: Advanced RAG + đánh giá (RAGAS)

> Tự kiểm tra **trước** khi xem solution. Tổng **9** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Hybrid retrieval kết hợp BM25 và vector search; chúng thường được trộn bằng kỹ thuật nào?

- **A.** Chỉ lấy BM25
- **B.** Lấy trung bình embedding
- **C.** Nối kết quả ngẫu nhiên
- **D.** Reciprocal Rank Fusion (RRF): hợp nhất thứ hạng từ hai bộ retrieve

## Câu 2 (Tự luận)

Cross-encoder reranker khác bi-encoder (embedding) thế nào, dùng khi nào?

## Câu 3 (Trắc nghiệm)

Trong RAGAS, 'faithfulness' đo điều gì?

- **A.** Số token dùng
- **B.** Tốc độ trả lời
- **C.** Độ dài câu trả lời
- **D.** Câu trả lời có bám/được hỗ trợ bởi context retrieve hay không (chống bịa)

## Câu 4 (Trắc nghiệm)

'Context precision' và 'context recall' trong RAGAS đánh giá khâu nào?

- **A.** Chất lượng RETRIEVAL, đoạn lấy ra có liên quan (precision) và có đủ thông tin cần (recall) không
- **B.** Chi phí API
- **C.** Khâu generate
- **D.** Tốc độ embedding

## Câu 5 (Tự luận)

Vì sao cần eval set + cẩn trọng với LLM-as-judge?

## Câu 6 (Trắc nghiệm)

Langfuse/LangSmith dùng để làm gì?

- **A.** Tracing/observability: ghi lại từng bước retrieve → generate, chạy eval, LLM-as-judge
- **B.** Train embedding
- **C.** Lượng tử hoá model
- **D.** Lưu vector

## Câu 7 (Tự luận)

Theo IR-book mục 11.4.3, BM25 được thiết kế để mô hình xác suất nhạy với hai đại lượng nào mà mô hình nhị phân độc lập bỏ qua, và điều đó liên quan gì đến cách bạn chunk tài liệu ở Tuần 13?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Zheng et al. (arXiv 2306.05685) nêu những thiên vị nào của LLM-as-judge, và bạn kiểm position bias bằng cách nào trong rubric RAGAS?

- **A.** Chỉ có self-enhancement; kiểm bằng dùng model khác
- **B.** Position bias, verbosity bias, self-enhancement bias, và limited reasoning ability; kiểm position bias bằng cách đảo thứ tự hai câu trả lời và xem phán quyết có đổi không
- **C.** Chỉ có thiên vị độ dài; kiểm bằng cách cắt câu trả lời
- **D.** Không có thiên vị nào đáng kể vì agreement trên 80%

## Nâng cao 2 (Tự luận)

IR-book nói precision-recall curve của kết quả xếp hạng có hình răng cưa. Vì sao, và context precision của RAGAS liên quan thế nào?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
