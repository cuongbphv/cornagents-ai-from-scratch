# Tuần 14, Đáp án & Giải thích: Advanced RAG + đánh giá (RAGAS)

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Hybrid retrieval kết hợp BM25 và vector search; chúng thường được trộn bằng kỹ thuật nào?

- **A.** Chỉ lấy BM25
- **B.** Lấy trung bình embedding
- **C.** Nối kết quả ngẫu nhiên
- **D.** Reciprocal Rank Fusion (RRF): hợp nhất thứ hạng từ hai bộ retrieve (đáp án đúng)

**Đáp án: D**

**Giải thích:** BM25 (lexical) bắt từ khoá chính xác; vector (semantic) bắt ý nghĩa; RRF hợp nhất để bù điểm yếu của nhau.

## Câu 2 (Tự luận)

Cross-encoder reranker khác bi-encoder (embedding) thế nào, dùng khi nào?

**Trả lời mẫu:** Bi-encoder mã hoá query và document RIÊNG thành vector rồi so cosine, nhanh, scale tốt, dùng để retrieve top-N từ kho lớn. Cross-encoder đưa CẢ cặp (query, document) qua model cùng lúc → chấm điểm liên quan chính xác hơn nhưng chậm, không scale cho toàn kho. Quy trình: bi-encoder lấy top-N (vd. 50), rồi cross-encoder rerank lại để chọn top-k tinh (vd. 5).

**Giải thích:** BGE cross-encoder (mã nguồn mở) là lựa chọn phổ biến.

## Câu 3 (Trắc nghiệm)

Trong RAGAS, 'faithfulness' đo điều gì?

- **A.** Số token dùng
- **B.** Tốc độ trả lời
- **C.** Độ dài câu trả lời
- **D.** Câu trả lời có bám/được hỗ trợ bởi context retrieve hay không (chống bịa) (đáp án đúng)

**Đáp án: D**

**Giải thích:** Faithfulness kiểm tra các khẳng định trong câu trả lời có truy được về context không → thước đo chống hallucination.

## Câu 4 (Trắc nghiệm)

'Context precision' và 'context recall' trong RAGAS đánh giá khâu nào?

- **A.** Chất lượng RETRIEVAL, đoạn lấy ra có liên quan (precision) và có đủ thông tin cần (recall) không (đáp án đúng)
- **B.** Chi phí API
- **C.** Khâu generate
- **D.** Tốc độ embedding

**Đáp án: A**

**Giải thích:** Hai chỉ số này tách bạch lỗi do retrieval kém với lỗi do generation kém.

## Câu 5 (Tự luận)

Vì sao cần eval set + cẩn trọng với LLM-as-judge?

**Trả lời mẫu:** Cần một eval set (cặp câu hỏi + ground-truth) để đo before/after một cách định lượng thay vì cảm tính. LLM-as-judge (dùng một LLM mạnh chấm output) tiện nhưng nhiều bẫy đã được ghi nhận trong nghiên cứu (arXiv 2306.05685): thiên vị độ dài, thiên vị vị trí, tự khen model cùng họ. Loss thấp hơn KHÔNG tự động nghĩa là hữu ích hơn trong thực tế → đừng tin một chỉ số duy nhất; kết hợp metric tự động + kiểm tra thủ công.

**Giải thích:** Đo lường tốt là điều phân biệt 'nghịch' với 'kỹ thuật'.

## Câu 6 (Trắc nghiệm)

Langfuse/LangSmith dùng để làm gì?

- **A.** Tracing/observability: ghi lại từng bước retrieve → generate, chạy eval, LLM-as-judge (đáp án đúng)
- **B.** Train embedding
- **C.** Lượng tử hoá model
- **D.** Lưu vector

**Đáp án: A**

**Giải thích:** Tracing giúp gỡ lỗi pipeline (đoạn nào retrieve sai, prompt nào hỏng) và đo chất lượng có hệ thống.

## Câu 7 (Tự luận)

Theo IR-book mục 11.4.3, BM25 được thiết kế để mô hình xác suất nhạy với hai đại lượng nào mà mô hình nhị phân độc lập bỏ qua, và điều đó liên quan gì đến cách bạn chunk tài liệu ở Tuần 13?

**Trả lời mẫu:** Hai đại lượng là tần suất từ trong tài liệu (term frequency) và độ dài tài liệu (document length); BM25 chuẩn hóa điểm theo độ dài bằng tham số b và bão hòa tần suất bằng tham số k₁. Chunk dài ngắn không đều sẽ bị chuẩn hóa độ dài kéo điểm lên xuống, nên khi dùng BM25 trong hybrid search cần chunk tương đối đều hoặc hiểu rõ ảnh hưởng của b.

**Giải thích:** IR-book trang 232 nói BM25 'sensitive to these quantities while not introducing too many additional parameters'. Hiểu hai tham số này giúp bạn không coi rank_bm25 là hộp đen khi đo lại RAGAS.

## Câu 8 (Trắc nghiệm)

Trong công thức BM25 (IR-book, phương trình 11.32), nếu bạn đặt tham số k1 = 0 cho tầng sparse retrieval của hệ hybrid search, điểm số của mỗi term thay đổi thế nào?

- **A.** Không còn phụ thuộc vào tần suất term trong tài liệu, mô hình trở về dạng nhị phân chỉ còn trọng số idf (đáp án đúng)
- **B.** Không còn chuẩn hóa theo độ dài tài liệu, mọi chunk dài hay ngắn đều được tính điểm như nhau
- **C.** Không còn thành phần idf, mọi term hiếm hay phổ biến đều đóng góp một lượng bằng nhau
- **D.** Không còn trọng số cho term trong query, mọi term của câu hỏi được coi là xuất hiện một lần

**Đáp án: A**

**Giải thích:** IR-book viết về k1 trong phương trình 11.32: "A k1 value of 0 corresponds to a binary model (no term frequency), and a large value corresponds to using raw term frequency." Chuẩn hóa độ dài do b điều khiển, trọng số term trong query do k3 điều khiển (phương trình 11.33), còn idf là thừa số log(N/df_t) độc lập với k1. (IR-book mục 11.4.3, tr. 233)

## Câu 9 (Trắc nghiệm)

Bộ chunk của bạn ở Tuần 13 có độ dài rất chênh lệch (một số chunk dài gấp năm lần trung bình). Theo IR-book, tham số nào của BM25 kiểm soát mức phạt theo độ dài tài liệu, và hai giá trị biên của nó có ý nghĩa gì?

- **A.** b trong khoảng 0 đến 1; b = 0 là không chuẩn hóa độ dài, b = 1 là chuẩn hóa hoàn toàn theo độ dài (đáp án đúng)
- **B.** k1 trong khoảng 0 đến vô cùng; k1 = 0 là không chuẩn hóa độ dài, k1 lớn là chuẩn hóa hoàn toàn
- **C.** Lave, độ dài trung bình; Lave = 0 là không chuẩn hóa độ dài, Lave lớn là chuẩn hóa hoàn toàn
- **D.** k3 trong khoảng 0 đến vô cùng; k3 = 0 là không chuẩn hóa độ dài, k3 lớn là chuẩn hóa hoàn toàn

**Đáp án: A**

**Giải thích:** IR-book: "b is another tuning parameter (0 ≤ b ≤ 1) which determines the scaling by document length: b = 1 corresponds to fully scaling the term weight by the document length, while b = 0 corresponds to no length normalization." Thừa số L_d/L_ave trong mẫu số nhân với b, nên khi chunk dài hơn trung bình, điểm tf bị giảm theo mức b chọn. (IR-book mục 11.4.3, tr. 233)

## Câu 10 (Tự luận)

Khi xây eval set cho RAG, một đồng nghiệp đề xuất đo retriever bằng accuracy (tỷ lệ chunk được phân loại đúng là liên quan hoặc không liên quan). IR-book phản đối cách này vì lý do gì, và điều đó áp dụng thế nào cho corpus của bạn?

**Trả lời mẫu:** IR-book chỉ ra dữ liệu IR cực kỳ lệch: thường trên 99,9% tài liệu là không liên quan, nên một hệ thống gán nhãn tất cả tài liệu là không liên quan vẫn đạt accuracy rất cao mà vô dụng với người dùng. Precision và recall tập trung vào true positives, hỏi bao nhiêu phần tài liệu liên quan đã tìm được và kèm bao nhiêu false positives. Với corpus hàng nghìn chunk mà mỗi câu hỏi chỉ có vài chunk liên quan, accuracy của retriever sẽ luôn gần 1 và không phân biệt được retriever tốt hay xấu, nên phải dùng precision, recall hoặc F.

**Giải thích:** Nguyên văn IR-book: "In almost all circumstances, the data is extremely skewed: normally over 99.9% of the documents are in the nonrelevant category. A system tuned to maximize accuracy can appear to perform well by simply deeming all documents nonrelevant to all queries." Accuracy được định nghĩa là (tp + tn)/(tp + fp + fn + tn), trong đó tn áp đảo. (IR-book mục 8.3, tr. 155)

## Câu 11 (Trắc nghiệm)

Vì sao IR-book định nghĩa F measure bằng trung bình điều hòa (harmonic mean) của precision và recall thay vì trung bình cộng?

- **A.** Vì trung bình điều hòa cho phép cộng trực tiếp điểm F của nhiều query thành một điểm tổng, còn trung bình cộng phải chuẩn hóa theo số tài liệu trả về
- **B.** Vì trung bình điều hòa luôn lớn hơn trung bình cộng nên điểm F cao hơn, giúp so sánh hai hệ thống có precision và recall cùng thấp dễ dàng hơn
- **C.** Vì trung bình cộng chỉ định nghĩa được khi precision và recall cùng khác không, còn trung bình điều hòa xử lý được cả trường hợp một trong hai bằng không
- **D.** Vì trả về toàn bộ tài liệu cho mọi query luôn đạt recall 100% và do đó trung bình cộng đạt 50%, trong khi trung bình điều hòa gần với giá trị nhỏ hơn trong hai số (đáp án đúng)

**Đáp án: D**

**Giải thích:** IR-book: trả về mọi tài liệu luôn đạt recall 100% nên trung bình cộng luôn có thể đạt 50%, "This strongly suggests that the arithmetic mean is an unsuitable measure to use." Với giả định 1 trong 10.000 tài liệu liên quan, trung bình điều hòa của chiến lược đó chỉ là 0,02%. "When the values of two numbers differ greatly, the harmonic mean is closer to their minimum than to their arithmetic mean." (IR-book mục 8.3, tr. 157)

## Câu 12 (Trắc nghiệm)

RAG của bạn lấy top 5 chunk cho mỗi câu hỏi, nhưng nhiều câu trong eval set chỉ có đúng 1 chunk liên quan nên precision at 5 không bao giờ vượt 0,2. IR-book nêu độ đo nào để xử lý đúng vấn đề này, và vì sao?

- **A.** Precision at k với k nhỏ hơn, vì IR-book cho rằng đây là độ đo ổn định nhất và không cần biết số tài liệu liên quan
- **B.** 11-point interpolated average precision, vì nó thay số tài liệu liên quan bằng 11 mức recall cố định
- **C.** Recall at k, vì độ đo này không đổi theo số tài liệu liên quan và hệ thống hoàn hảo luôn đạt 1 với mọi k
- **D.** R-precision, vì nó tính precision trên đúng |Rel| kết quả đầu nên hệ thống hoàn hảo có thể đạt 1 cho mọi query (đáp án đúng)

**Đáp án: D**

**Giải thích:** IR-book nói precision at k có nhược điểm "it is the least stable of the commonly used evaluation measures and that it does not average well, since the total number of relevant documents for a query has a strong influence on precision at k." R-precision "adjusts for the size of the set of relevant documents: A perfect system could score 1 on this metric for each query, whereas, even a perfect system could only achieve a precision at 20 of 0.4 if there were only 8 documents in the collection relevant". Sách cũng ghi R-precision trùng với break-even point và tương quan cao với MAP. (IR-book mục 8.4, tr. 161)

## Câu 13 (Tự luận)

SLP3 tính average precision (AP) cho một query như thế nào, và vì sao AP phản ánh chất lượng xếp hạng tốt hơn precision at k? Dùng ví dụ Fig. 11.7 (25 tài liệu, 9 liên quan) để minh họa con số sách đưa ra.

**Trả lời mẫu:** Theo SLP3, ta đi xuống danh sách xếp hạng và chỉ ghi lại precision tại những vị trí gặp tài liệu liên quan (ví dụ hạng 1, 3, 5, 6 nhưng không phải 2 hay 4), rồi lấy trung bình các giá trị đó trên tập tài liệu liên quan (phương trình 11.16). MAP là trung bình AP trên tập query (phương trình 11.17). Với Fig. 11.7, sách cho biết AP (cũng là MAP vì chỉ một query) bằng 0,6. AP thưởng cho hệ thống đưa tài liệu liên quan lên cao vì precision tại các vị trí đó lớn, còn precision at k chỉ nhìn một điểm cắt cố định và bỏ qua thứ tự bên trong top k.

**Giải thích:** SLP3: "we again descend through the ranked list of items, but now we note the precision only at those points where a relevant item has been encountered (for example at ranks 1, 3, 5, 6 but not 2 or 4 in Fig. 11.7)." và "The MAP for the single query (hence = AP) in Fig. 11.7 is 0.6." (SLP3 mục 11.2, tr. 263)

## Câu 14 (Trắc nghiệm)

IR-book định nghĩa interpolated precision tại mức recall r là precision cao nhất tìm được ở bất kỳ mức recall r' >= r (phương trình 8.7). Sách biện minh định nghĩa này bằng lập luận nào?

- **A.** Vì MAP được định nghĩa dựa trên interpolated precision nên hai độ đo phải dùng cùng một quy ước làm trơn
- **B.** Vì precision tại recall bằng 0 không xác định được, nên phải mượn giá trị từ các mức recall cao hơn để vẽ đủ 11 điểm
- **C.** Vì gần như ai cũng sẵn sàng xem thêm vài tài liệu nếu điều đó làm tăng tỷ lệ tài liệu liên quan trong tập đã xem (đáp án đúng)
- **D.** Vì đường precision-recall của các hệ thống khác nhau chỉ so sánh được khi chúng đơn điệu giảm trên cùng trục recall

**Đáp án: C**

**Giải thích:** IR-book: "The justification is that almost anyone would be prepared to look at a few more documents if it would increase the percentage of the viewed set that were relevant (that is, if the precision of the larger set is higher)." Sách cũng ghi MAP không dùng nội suy: "Using MAP, fixed recall levels are not chosen, and there is no interpolation." (tr. 160), nên phương án cuối sai. (IR-book mục 8.4, tr. 159)

## Câu 15 (Tự luận)

Bạn cần chọn k1 và b cho BM25 trên corpus văn bản pháp luật ngân hàng tiếng Việt. IR-book khuyến nghị quy trình nào để đặt hai tham số này, và nếu chưa có tập phát triển thì dùng giá trị nào?

**Trả lời mẫu:** IR-book nói các tham số nên được đặt bằng cách tối ưu hiệu năng trên một development test collection tách riêng (tìm thủ công hoặc bằng grid search hay phương pháp tối ưu khác), rồi mới dùng các giá trị đó trên test collection thật. Khi không có bước tối ưu như vậy, thực nghiệm cho thấy giá trị hợp lý là k1 và k3 trong khoảng 1,2 đến 2 và b = 0,75. Với eval set RAG của bạn, điều này nghĩa là phải tách một phần câu hỏi làm dev set để dò k1, b, không dò trực tiếp trên tập dùng để báo cáo kết quả.

**Giải thích:** Nguyên văn: "The tuning parameters of these formulas should ideally be set to optimize performance on a development test collection" và "In the absence of such optimization, experiments have shown reasonable values are to set k1 and k3 to a value between 1.2 and 2 and b = 0.75." (IR-book mục 11.4.3, tr. 233)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Zheng et al. (arXiv 2306.05685) nêu những thiên vị nào của LLM-as-judge, và bạn kiểm position bias bằng cách nào trong rubric RAGAS?

- **A.** Chỉ có self-enhancement; kiểm bằng dùng model khác
- **B.** Position bias, verbosity bias, self-enhancement bias, và limited reasoning ability; kiểm position bias bằng cách đảo thứ tự hai câu trả lời và xem phán quyết có đổi không (đáp án đúng)
- **C.** Chỉ có thiên vị độ dài; kiểm bằng cách cắt câu trả lời
- **D.** Không có thiên vị nào đáng kể vì agreement trên 80%

**Đáp án: B**

**Giải thích:** Abstract của paper liệt kê bốn hạn chế và báo judge mạnh đạt 'over 80% agreement' với người. Hai điều cùng đúng: dùng được, nhưng phải kiểm.

## Nâng cao 2 (Tự luận)

IR-book nói precision-recall curve của kết quả xếp hạng có hình răng cưa. Vì sao, và context precision của RAGAS liên quan thế nào?

**Trả lời mẫu:** Với kết quả xếp hạng, precision và recall tính trên top-k; khi tài liệu thứ k+1 không liên quan thì recall giữ nguyên còn precision giảm, khi liên quan thì cả hai tăng, nên đường cong nhảy lên xuống (IR-book mục 8.4, trang 158). Context precision của RAGAS là phiên bản dùng LLM phán liên quan của precision trên top-k, nên nó kế thừa cả định nghĩa lẫn cách đọc răng cưa này khi bạn đổi k.

**Giải thích:** Khi so baseline với hybrid và rerank, giữ cùng k để hai số đo so được với nhau.
