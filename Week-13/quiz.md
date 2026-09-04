# Tuần 13, Quiz: Xây dựng RAG pipeline end-to-end

> Tự kiểm tra **trước** khi xem solution. Tổng **17** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
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

## Câu 8 (Trắc nghiệm)

IR-book dùng ví dụ hai từ try và insurance trong tập Reuters để giải thích vì sao idf dựa trên document frequency (df) thay vì collection frequency (cf). Lập luận là gì?

- **A.** cf phụ thuộc vào độ dài tài liệu nên phải chuẩn hóa trước khi dùng, còn df thì độc lập với độ dài tài liệu
- **B.** cf của hai từ gần bằng nhau nhưng df khác nhau nhiều; ta muốn số ít tài liệu chứa insurance được tăng điểm hơn số đông tài liệu chứa try
- **C.** cf của hai từ khác nhau nhiều nhưng df gần bằng nhau, nên df là thống kê ổn định hơn để chuẩn hóa trọng số
- **D.** df dễ tính hơn cf vì chỉ cần đọc inverted index một lần, không cần đếm số lần xuất hiện của từng term trong tài liệu

## Câu 9 (Trắc nghiệm)

IR-book tóm tắt trọng số tf-idf của term t trong tài liệu d bằng ba tính chất. Trường hợp nào cho trọng số cao nhất?

- **A.** Term xuất hiện đúng một lần trong hầu hết tài liệu của collection
- **B.** Term xuất hiện ít lần trong d nhưng có mặt ở rất nhiều tài liệu khác
- **C.** Term xuất hiện nhiều lần trong một số ít tài liệu của collection
- **D.** Term xuất hiện nhiều lần trong gần như mọi tài liệu của collection

## Câu 10 (Trắc nghiệm)

IR-book cân nhắc dùng độ lớn của hiệu hai vector tài liệu làm độ tương đồng rồi bác bỏ. Lý do và cách khắc phục là gì?

- **A.** Hiệu vector tốn bộ nhớ vì phải lưu ma trận hiệu cho mọi cặp tài liệu trong collection; khắc phục bằng inverted index để chỉ so các tài liệu có chung ít nhất một term
- **B.** Hai tài liệu nội dung rất giống nhau vẫn có hiệu vector lớn chỉ vì một tài liệu dài hơn nhiều; khắc phục bằng cosine similarity, tức dot product của hai vector đã chuẩn hóa độ dài
- **C.** Hiệu vector không xác định khi hai tài liệu có từ vựng khác nhau, vì các term vắng mặt không có tọa độ; khắc phục bằng cách thêm smoothing cho mọi term trong từ điển trước khi trừ
- **D.** Hiệu vector nhạy với thứ tự từ trong tài liệu nên hai câu đảo trật tự cho kết quả khác nhau; khắc phục bằng cách chuyển sang biểu diễn bag-of-words rồi mới tính hiệu

## Câu 11 (Trắc nghiệm)

SLP3 trình bày hai kiến trúc dense retrieval: encoder chung cho query và document (Fig. 11.11a) và bi-encoder (Fig. 11.11b). Vì sao kiến trúc chung hầu như chỉ dùng để rerank?

- **A.** Vì mỗi query đến phải đưa toàn bộ tài liệu trong collection qua encoder cùng với query, quá tốn kém; bi-encoder mã hóa tài liệu trước một lần rồi chỉ tính dot product
- **B.** Vì nó bị giới hạn 512 token nên không xử lý được tài liệu dài hơn một passage, còn bi-encoder mã hóa từng phần tài liệu riêng nên không có giới hạn độ dài đầu vào
- **C.** Vì nó cần dữ liệu huấn luyện có nhãn relevance cho từng cặp query và document, còn bi-encoder có thể học không giám sát trực tiếp từ corpus tài liệu mà không cần nhãn
- **D.** Vì điểm số của nó là softmax nên không so sánh được giữa các query khác nhau, còn bi-encoder cho điểm dot product có thể so sánh và sắp hạng trên toàn collection

## Câu 12 (Trắc nghiệm)

SLP3 nói retrieval thường không chạy trên cả tài liệu. Cách chia và ràng buộc độ dài được mô tả là gì?

- **A.** Chia tài liệu thành các passage cố định không chồng lấn, ví dụ 100 token; query và document phải cùng nằm gọn trong cửa sổ 512 token của BERT, ví dụ cắt query còn 64 token
- **B.** Chia theo câu rồi gộp lại thành passage tối đa 512 token; query giữ nguyên độ dài và được nối vào sau passage bằng token [SEP]
- **C.** Chia theo đoạn văn tự nhiên với 50 token chồng lấn giữa hai passage liền kề; query cắt còn 128 token để chừa chỗ cho passage
- **D.** Không chia tài liệu thành passage; tài liệu dài được tóm tắt bằng một LLM xuống dưới 512 token rồi mới mã hóa cùng query trong một cửa sổ BERT duy nhất

## Câu 13 (Trắc nghiệm)

SLP3 mô tả thuật toán RAG cơ bản gồm ba bước và nhấn mạnh một đặc điểm của phiên bản này. Đặc điểm đó là gì?

- **A.** Nó để LLM tự quyết định khi nào cần gọi retrieval và gọi vào collection nào tùy nhu cầu người dùng
- **B.** Nó yêu cầu instruction-tune LLM trên bộ câu hỏi kèm passage để LLM học cách chọn passage hữu ích
- **C.** Nó không cần huấn luyện gì: dùng LLM có sẵn, đưa passage và prompt vào rồi kỳ vọng LLM tự nhận ra passage hữu ích
- **D.** Nó luôn có bước rerank passage trước khi tạo prompt để xử lý nhiễu trong kết quả retrieval

## Câu 14 (Tự luận)

SLP3 dùng 1 + log10 count(t, d) thay cho số đếm thô khi tính tf, và idf bằng 0 cho các từ như good hoặc sweet trong corpus Shakespeare. Hãy giải thích trực giác của hai lựa chọn này và hệ quả cho việc xếp hạng chunk trong RAG pipeline dùng tf-idf.

## Câu 15 (Tự luận)

Ngoài RAG cơ bản, SLP3 nêu các hướng cải thiện khi passage được truy hồi có nhiễu hoặc retriever không được tối ưu cho RAG. Hãy nêu ít nhất ba hướng và giải thích "mismatch" mà SLP3 chỉ ra ở phía IR engine.

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
