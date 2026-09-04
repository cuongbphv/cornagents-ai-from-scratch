# Tuần 13, Đáp án & Giải thích: Xây dựng RAG pipeline end-to-end

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Thứ tự đúng của một pipeline RAG cơ bản?

- **A.** Retrieve → generate → embed
- **B.** Generate → retrieve → embed → chunk
- **C.** Embed → generate → chunk → store
- **D.** Load → chunk → embed → vector store → retrieve top-k → generate (đáp án đúng)

**Đáp án: D**

**Giải thích:** Load tài liệu → cắt chunk → embed → lưu vector store → khi hỏi: embed query, retrieve top-k, ghép context vào prompt → generate.

## Câu 2 (Tự luận)

Vì sao khi chunking cần 'overlap' giữa các đoạn?

**Trả lời mẫu:** Overlap (vd. ~100 ký tự/token) giữ phần đầu/cuối câu liền mạch giữa hai chunk, tránh cắt đứt một ý/định nghĩa ngay ranh giới chunk khiến retrieval bỏ sót ngữ cảnh cần thiết. Với chunk ~800 và overlap ~100, một thông tin nằm ở mép vẫn xuất hiện trọn trong ít nhất một chunk.

**Giải thích:** Chunk quá nhỏ mất ngữ cảnh; quá lớn loãng tín hiệu retrieval. Overlap là cân bằng.

## Câu 3 (Trắc nghiệm)

Retrieval trong RAG thường xếp hạng tài liệu bằng độ đo nào?

- **A.** Số ký tự trùng
- **B.** Khoảng cách Hamming
- **C.** Cosine similarity giữa embedding của query và document (đáp án đúng)
- **D.** Thứ tự alphabet

**Đáp án: C**

**Giải thích:** sim(q,d) = (q·d)/(|q||d|). Tài liệu có embedding gần (cosine cao) với query được lấy ra trước.

## Câu 4 (Trắc nghiệm)

Chroma đóng vai trò gì trong pipeline?

- **A.** Vector store (lưu & truy vấn nearest-neighbor các embedding): tốt cho dev (đáp án đúng)
- **B.** Mô hình sinh text
- **C.** Tokenizer
- **D.** Reranker

**Đáp án: A**

**Giải thích:** Chroma là vector DB nhẹ cho dev; production có thể chuyển pgvector/Qdrant/Weaviate.

## Câu 5 (Tự luận)

Vì sao RAG giúp giảm hallucination so với hỏi LLM trực tiếp?

**Trả lời mẫu:** RAG 'grounding' câu trả lời vào các đoạn tài liệu thật được retrieve và đưa vào prompt, nên model trả lời dựa trên bằng chứng cụ thể thay vì chỉ dựa vào trí nhớ tham số (dễ bịa). Ngoài ra có thể trích dẫn nguồn để kiểm chứng. Nó cũng cập nhật được kiến thức mới mà không cần train lại.

**Giải thích:** Anchor của roadmap: corpus là tài liệu nghiệp vụ Finance Banking của bạn.

## Câu 6 (Trắc nghiệm)

Embedding model làm gì?

- **A.** Lượng tử hoá model
- **B.** Sinh câu trả lời cuối
- **C.** Biến văn bản thành vector số nắm bắt ngữ nghĩa, để so sánh tương đồng (đáp án đúng)
- **D.** Cắt tài liệu thành chunk

**Đáp án: C**

**Giải thích:** Embedding (BGE/e5/nomic...) ánh xạ text → vector; văn bản gần nghĩa → vector gần nhau.

## Câu 7 (Trắc nghiệm)

Jurafsky và Martin gọi khiếm khuyết cốt lõi của tf-idf và BM25 là 'vocabulary mismatch problem'. Khiếm khuyết đó là gì và dense retrieval giải quyết ra sao?

- **A.** tf-idf và BM25 không chấm được tài liệu dài; dense retrieval cắt chunk
- **B.** tf-idf và BM25 chỉ hoạt động khi query và tài liệu dùng chung đúng từ, nên người hỏi phải đoán từ người viết đã dùng; dense embedding xử lý được từ đồng nghĩa vì so nghĩa thay vì so chuỗi ký tự (đáp án đúng)
- **C.** tf-idf và BM25 quá chậm với corpus lớn; dense retrieval nhanh hơn nhờ GPU
- **D.** tf-idf và BM25 cần nhãn huấn luyện; dense retrieval thì không

**Đáp án: B**

**Giải thích:** SLP3 mục 11.3 trang 264: 'they work only if there is exact overlap of words between the query and document'. Vì thế Tuần 14 dùng cả hai trong hybrid search: BM25 bắt từ khóa chính xác, dense bắt đồng nghĩa.

## Câu 8 (Trắc nghiệm)

IR-book dùng ví dụ hai từ try và insurance trong tập Reuters để giải thích vì sao idf dựa trên document frequency (df) thay vì collection frequency (cf). Lập luận là gì?

- **A.** cf phụ thuộc vào độ dài tài liệu nên phải chuẩn hóa trước khi dùng, còn df thì độc lập với độ dài tài liệu
- **B.** cf của hai từ gần bằng nhau nhưng df khác nhau nhiều; ta muốn số ít tài liệu chứa insurance được tăng điểm hơn số đông tài liệu chứa try (đáp án đúng)
- **C.** cf của hai từ khác nhau nhiều nhưng df gần bằng nhau, nên df là thống kê ổn định hơn để chuẩn hóa trọng số
- **D.** df dễ tính hơn cf vì chỉ cần đọc inverted index một lần, không cần đếm số lần xuất hiện của từng term trong tài liệu

**Đáp án: B**

**Giải thích:** Figure 6.7: try có cf 10422 và df 8760; insurance có cf 10440 và df 3997. IR-book: "the cf values for both try and insurance are roughly equal, but their df values differ significantly. Intuitively, we want the few documents that contain insurance to get a higher boost for a query on insurance than the many documents containing try get from a query on try." Từ đó idf_t = log(N/df_t) (eq. 6.7). (IR-book mục 6.2.1, tr. 118)

## Câu 9 (Trắc nghiệm)

IR-book tóm tắt trọng số tf-idf của term t trong tài liệu d bằng ba tính chất. Trường hợp nào cho trọng số cao nhất?

- **A.** Term xuất hiện đúng một lần trong hầu hết tài liệu của collection
- **B.** Term xuất hiện ít lần trong d nhưng có mặt ở rất nhiều tài liệu khác
- **C.** Term xuất hiện nhiều lần trong một số ít tài liệu của collection (đáp án đúng)
- **D.** Term xuất hiện nhiều lần trong gần như mọi tài liệu của collection

**Đáp án: C**

**Giải thích:** IR-book: tf-idf_{t,d} là "1. highest when t occurs many times within a small number of documents (thus lending high discriminating power to those documents); 2. lower when the term occurs fewer times in a document, or occurs in many documents (thus offering a less pronounced relevance signal); 3. lowest when the term occurs in virtually all documents." (IR-book mục 6.2.2, tr. 119)

## Câu 10 (Trắc nghiệm)

IR-book cân nhắc dùng độ lớn của hiệu hai vector tài liệu làm độ tương đồng rồi bác bỏ. Lý do và cách khắc phục là gì?

- **A.** Hiệu vector tốn bộ nhớ vì phải lưu ma trận hiệu cho mọi cặp tài liệu trong collection; khắc phục bằng inverted index để chỉ so các tài liệu có chung ít nhất một term
- **B.** Hai tài liệu nội dung rất giống nhau vẫn có hiệu vector lớn chỉ vì một tài liệu dài hơn nhiều; khắc phục bằng cosine similarity, tức dot product của hai vector đã chuẩn hóa độ dài (đáp án đúng)
- **C.** Hiệu vector không xác định khi hai tài liệu có từ vựng khác nhau, vì các term vắng mặt không có tọa độ; khắc phục bằng cách thêm smoothing cho mọi term trong từ điển trước khi trừ
- **D.** Hiệu vector nhạy với thứ tự từ trong tài liệu nên hai câu đảo trật tự cho kết quả khác nhau; khắc phục bằng cách chuyển sang biểu diễn bag-of-words rồi mới tính hiệu

**Đáp án: B**

**Giải thích:** IR-book: "two documents with very similar content can have a significant vector difference simply because one is much longer than the other ... To compensate for the effect of document length, the standard way of quantifying the similarity between two documents d1 and d2 is to compute the cosine similarity" sim(d1, d2) = V(d1)·V(d2) / (|V(d1)| |V(d2)|) (eq. 6.10); mẫu số length-normalize hai vector về vector đơn vị. (IR-book mục 6.3.1, tr. 121)

## Câu 11 (Trắc nghiệm)

SLP3 trình bày hai kiến trúc dense retrieval: encoder chung cho query và document (Fig. 11.11a) và bi-encoder (Fig. 11.11b). Vì sao kiến trúc chung hầu như chỉ dùng để rerank?

- **A.** Vì mỗi query đến phải đưa toàn bộ tài liệu trong collection qua encoder cùng với query, quá tốn kém; bi-encoder mã hóa tài liệu trước một lần rồi chỉ tính dot product (đáp án đúng)
- **B.** Vì nó bị giới hạn 512 token nên không xử lý được tài liệu dài hơn một passage, còn bi-encoder mã hóa từng phần tài liệu riêng nên không có giới hạn độ dài đầu vào
- **C.** Vì nó cần dữ liệu huấn luyện có nhãn relevance cho từng cặp query và document, còn bi-encoder có thể học không giám sát trực tiếp từ corpus tài liệu mà không cần nhãn
- **D.** Vì điểm số của nó là softmax nên không so sánh được giữa các query khác nhau, còn bi-encoder cho điểm dot product có thể so sánh và sắp hạng trên toàn collection

**Đáp án: A**

**Giải thích:** SLP3: "every time we get a query, we have to pass every single document in our entire collection through a BERT encoder jointly with the new query! This enormous use of resources is impractical for real cases." Bi-encoder "encode the documents in the collection only one time", điểm là zq · zd (eq. 11.19), rẻ hơn nhưng kém chính xác hơn vì không thấy tương tác giữa token của query và document. (SLP3 mục 11.3, tr. 265)

## Câu 12 (Trắc nghiệm)

SLP3 nói retrieval thường không chạy trên cả tài liệu. Cách chia và ràng buộc độ dài được mô tả là gì?

- **A.** Chia tài liệu thành các passage cố định không chồng lấn, ví dụ 100 token; query và document phải cùng nằm gọn trong cửa sổ 512 token của BERT, ví dụ cắt query còn 64 token (đáp án đúng)
- **B.** Chia theo câu rồi gộp lại thành passage tối đa 512 token; query giữ nguyên độ dài và được nối vào sau passage bằng token [SEP]
- **C.** Chia theo đoạn văn tự nhiên với 50 token chồng lấn giữa hai passage liền kề; query cắt còn 128 token để chừa chỗ cho passage
- **D.** Không chia tài liệu thành passage; tài liệu dài được tóm tắt bằng một LLM xuống dưới 512 token rồi mới mã hóa cùng query trong một cửa sổ BERT duy nhất

**Đáp án: A**

**Giải thích:** SLP3: "documents are broken up into smaller passages, such as non-overlapping fixed-length chunks of say 100 tokens ... The query and document have to be made to fit in the BERT 512-token window, for example by truncating the query to 64 tokens and truncating the document if necessary so that it, the query, [CLS], and [SEP] fit in 512 tokens." (SLP3 mục 11.3, tr. 264)

## Câu 13 (Trắc nghiệm)

SLP3 mô tả thuật toán RAG cơ bản gồm ba bước và nhấn mạnh một đặc điểm của phiên bản này. Đặc điểm đó là gì?

- **A.** Nó để LLM tự quyết định khi nào cần gọi retrieval và gọi vào collection nào tùy nhu cầu người dùng
- **B.** Nó yêu cầu instruction-tune LLM trên bộ câu hỏi kèm passage để LLM học cách chọn passage hữu ích
- **C.** Nó không cần huấn luyện gì: dùng LLM có sẵn, đưa passage và prompt vào rồi kỳ vọng LLM tự nhận ra passage hữu ích (đáp án đúng)
- **D.** Nó luôn có bước rerank passage trước khi tạo prompt để xử lý nhiễu trong kết quả retrieval

**Đáp án: C**

**Giải thích:** Ba bước: gọi retriever trả về top-k passage R(q), tạo prompt gồm q và các passage, gọi LLM. SLP3: "The basic version of RAG described above involves no training; we take an off-the-shelf LLM, and give it the passages and a prompt and hope that it will correctly figure out which passages are useful or relevant in generating the answer." Reranker, agent-based RAG và instruction-tuning cho RAG là các mở rộng. (SLP3 mục 11.4, tr. 268-269)

## Câu 14 (Tự luận)

SLP3 dùng 1 + log10 count(t, d) thay cho số đếm thô khi tính tf, và idf bằng 0 cho các từ như good hoặc sweet trong corpus Shakespeare. Hãy giải thích trực giác của hai lựa chọn này và hệ quả cho việc xếp hạng chunk trong RAG pipeline dùng tf-idf.

**Trả lời mẫu:** Về tf, SLP3 lập luận rằng một từ xuất hiện 100 lần không làm nó có khả năng liên quan gấp 100 lần, nên dùng log để nén: 1 lần cho tf = 1, 10 lần cho tf = 2, 100 lần cho tf = 3, và count 0 cho tf = 0 vì không lấy được log của 0. Về idf, idf_t = log10(N/df_t) nên từ xuất hiện trong mọi tài liệu (df = N, như good và sweet có mặt trong cả 37 vở) nhận trọng số 0, vì từ có mặt khắp collection không giúp phân biệt tài liệu. Hệ quả cho RAG: từ lặp lại nhiều trong một chunk không được thưởng tuyến tính, và từ có mặt trong mọi chunk của corpus (ví dụ tên tổ chức xuất hiện ở mọi văn bản) gần như không đóng góp vào điểm tf-idf dù có trong query.

**Giải thích:** SLP3: "The intuition is that a word appearing 100 times in a document doesn't make that word 100 times more likely to be relevant to the meaning of the document." (eq. 11.4); "The fewer documents in which a term occurs, the higher this weight; the lowest weight of 0 is assigned to terms that occur in every document." với bảng từ Romeo df 1 idf 1.57 tới good và sweet df 37 idf 0. (SLP3 mục 11.1.2, tr. 257)

## Câu 15 (Tự luận)

Ngoài RAG cơ bản, SLP3 nêu các hướng cải thiện khi passage được truy hồi có nhiễu hoặc retriever không được tối ưu cho RAG. Hãy nêu ít nhất ba hướng và giải thích "mismatch" mà SLP3 chỉ ra ở phía IR engine.

**Trả lời mẫu:** SLP3 nêu: thêm reranker để sắp lại passage sau retrieval; kiến trúc multi-hop dùng kết quả truy hồi lần một nối vào query để truy hồi lần hai; instruction-tune LLM trên dataset câu hỏi kèm passage và đáp án đúng; dùng test-time compute để LLM vừa trả lời vừa sinh reflection về passage nào hữu ích; và huấn luyện end-to-end cả IR engine cùng LLM. Mismatch là IR engine thường chưa được huấn luyện, hoặc chỉ được huấn luyện cho IR đơn giản hay factoid QA, không phải cho kịch bản RAG nơi passage truy hồi được một LLM khác dùng để sinh văn bản; huấn luyện end-to-end trên tập câu hỏi và đáp án là cách SLP3 đề xuất để khép khoảng cách này. SLP3 cũng khuyến nghị đưa knowledge citation (URL hoặc tham chiếu) vào output, cách đơn giản nhất là yêu cầu ngay trong prompt.

**Giải thích:** SLP3: "the IR engine itself has not been optimized for the RAG scenario. It might not have been trained, or if it was, it was likely trained for simple IR or factoid question-answering tasks, not for the RAG scenario where the retrieved passages are specifically to be used by another LLM for generating texts. We can address this mismatch for trainable IR algorithms by doing end-to-end training of the entire architecture on some set of questions and answers". (SLP3 mục 11.4, tr. 269)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Jurafsky và Martin gọi khiếm khuyết của tf-idf và BM25 là 'vocabulary mismatch problem'. Trong hybrid search ở Tuần 14, vì sao vẫn giữ BM25 dù đã có dense retrieval?

- **A.** Vì RAGAS bắt buộc dùng BM25
- **B.** Vì BM25 nhanh hơn nên thay được embedding
- **C.** Vì embedding không chạy được trên CPU
- **D.** Vì dense bắt đồng nghĩa nhưng có thể trượt các chuỗi cần khớp chính xác như số hiệu văn bản hay mã điều khoản, thứ BM25 làm tốt; hai nhánh bù khuyết cho nhau rồi gộp bằng RRF (đáp án đúng)

**Đáp án: D**

**Giải thích:** SLP3 mục 11.3 (trang 264) nêu khiếm khuyết của sparse; phần lý giải vì sao vẫn giữ BM25 là suy luận thực hành của người viết cho corpus pháp lý.

## Nâng cao 2 (Tự luận)

Theo SLP3, RAG có hai thành phần chính và ba mục tiêu. Hãy nêu chúng và chỉ ra mục tiêu nào trùng với lý do repo chọn RAG cho kiến thức quy định.

**Trả lời mẫu:** Hai thành phần: retriever và generator (đôi khi gọi reader). Ba mục tiêu: giảm hallucination bằng tập tài liệu đáng tin, sinh text đúng về dữ liệu riêng như tài liệu nội bộ hay pháp lý, và xử lý kiến thức thay đổi theo thời gian (SLP3 mục 11.4, trang 267). Cả ba trùng với lý do của repo: văn bản pháp luật thay đổi, cần dẫn nguồn, và không được bịa.

**Giải thích:** Paper 'Does Fine-Tuning on New Knowledge Encourage Hallucinations?' trong kệ paper là bằng chứng thực nghiệm cho việc không nhét kiến thức quy định vào trọng số.
