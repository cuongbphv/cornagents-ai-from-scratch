# Tuần 14, Quiz: Advanced RAG + đánh giá (RAGAS)

> Tự kiểm tra **trước** khi xem solution. Tổng **17** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
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

## Câu 8 (Trắc nghiệm)

Trong công thức BM25 (IR-book, phương trình 11.32), nếu bạn đặt tham số k1 = 0 cho tầng sparse retrieval của hệ hybrid search, điểm số của mỗi term thay đổi thế nào?

- **A.** Không còn phụ thuộc vào tần suất term trong tài liệu, mô hình trở về dạng nhị phân chỉ còn trọng số idf
- **B.** Không còn chuẩn hóa theo độ dài tài liệu, mọi chunk dài hay ngắn đều được tính điểm như nhau
- **C.** Không còn thành phần idf, mọi term hiếm hay phổ biến đều đóng góp một lượng bằng nhau
- **D.** Không còn trọng số cho term trong query, mọi term của câu hỏi được coi là xuất hiện một lần

## Câu 9 (Trắc nghiệm)

Bộ chunk của bạn ở Tuần 13 có độ dài rất chênh lệch (một số chunk dài gấp năm lần trung bình). Theo IR-book, tham số nào của BM25 kiểm soát mức phạt theo độ dài tài liệu, và hai giá trị biên của nó có ý nghĩa gì?

- **A.** b trong khoảng 0 đến 1; b = 0 là không chuẩn hóa độ dài, b = 1 là chuẩn hóa hoàn toàn theo độ dài
- **B.** k1 trong khoảng 0 đến vô cùng; k1 = 0 là không chuẩn hóa độ dài, k1 lớn là chuẩn hóa hoàn toàn
- **C.** Lave, độ dài trung bình; Lave = 0 là không chuẩn hóa độ dài, Lave lớn là chuẩn hóa hoàn toàn
- **D.** k3 trong khoảng 0 đến vô cùng; k3 = 0 là không chuẩn hóa độ dài, k3 lớn là chuẩn hóa hoàn toàn

## Câu 10 (Tự luận)

Khi xây eval set cho RAG, một đồng nghiệp đề xuất đo retriever bằng accuracy (tỷ lệ chunk được phân loại đúng là liên quan hoặc không liên quan). IR-book phản đối cách này vì lý do gì, và điều đó áp dụng thế nào cho corpus của bạn?

## Câu 11 (Trắc nghiệm)

Vì sao IR-book định nghĩa F measure bằng trung bình điều hòa (harmonic mean) của precision và recall thay vì trung bình cộng?

- **A.** Vì trung bình điều hòa cho phép cộng trực tiếp điểm F của nhiều query thành một điểm tổng, còn trung bình cộng phải chuẩn hóa theo số tài liệu trả về
- **B.** Vì trung bình điều hòa luôn lớn hơn trung bình cộng nên điểm F cao hơn, giúp so sánh hai hệ thống có precision và recall cùng thấp dễ dàng hơn
- **C.** Vì trung bình cộng chỉ định nghĩa được khi precision và recall cùng khác không, còn trung bình điều hòa xử lý được cả trường hợp một trong hai bằng không
- **D.** Vì trả về toàn bộ tài liệu cho mọi query luôn đạt recall 100% và do đó trung bình cộng đạt 50%, trong khi trung bình điều hòa gần với giá trị nhỏ hơn trong hai số

## Câu 12 (Trắc nghiệm)

RAG của bạn lấy top 5 chunk cho mỗi câu hỏi, nhưng nhiều câu trong eval set chỉ có đúng 1 chunk liên quan nên precision at 5 không bao giờ vượt 0,2. IR-book nêu độ đo nào để xử lý đúng vấn đề này, và vì sao?

- **A.** Precision at k với k nhỏ hơn, vì IR-book cho rằng đây là độ đo ổn định nhất và không cần biết số tài liệu liên quan
- **B.** 11-point interpolated average precision, vì nó thay số tài liệu liên quan bằng 11 mức recall cố định
- **C.** Recall at k, vì độ đo này không đổi theo số tài liệu liên quan và hệ thống hoàn hảo luôn đạt 1 với mọi k
- **D.** R-precision, vì nó tính precision trên đúng |Rel| kết quả đầu nên hệ thống hoàn hảo có thể đạt 1 cho mọi query

## Câu 13 (Tự luận)

SLP3 tính average precision (AP) cho một query như thế nào, và vì sao AP phản ánh chất lượng xếp hạng tốt hơn precision at k? Dùng ví dụ Fig. 11.7 (25 tài liệu, 9 liên quan) để minh họa con số sách đưa ra.

## Câu 14 (Trắc nghiệm)

IR-book định nghĩa interpolated precision tại mức recall r là precision cao nhất tìm được ở bất kỳ mức recall r' >= r (phương trình 8.7). Sách biện minh định nghĩa này bằng lập luận nào?

- **A.** Vì MAP được định nghĩa dựa trên interpolated precision nên hai độ đo phải dùng cùng một quy ước làm trơn
- **B.** Vì precision tại recall bằng 0 không xác định được, nên phải mượn giá trị từ các mức recall cao hơn để vẽ đủ 11 điểm
- **C.** Vì gần như ai cũng sẵn sàng xem thêm vài tài liệu nếu điều đó làm tăng tỷ lệ tài liệu liên quan trong tập đã xem
- **D.** Vì đường precision-recall của các hệ thống khác nhau chỉ so sánh được khi chúng đơn điệu giảm trên cùng trục recall

## Câu 15 (Tự luận)

Bạn cần chọn k1 và b cho BM25 trên corpus văn bản pháp luật ngân hàng tiếng Việt. IR-book khuyến nghị quy trình nào để đặt hai tham số này, và nếu chưa có tập phát triển thì dùng giá trị nào?

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
