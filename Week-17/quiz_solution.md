# Tuần 17, Đáp án & Giải thích: Graph Engineering: Knowledge Graph làm shared memory cho multi-agent

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Bốn stage của knowledge graph pipeline (Anthropic Playbook) theo đúng thứ tự?

- **A.** Querying → Assembly → Resolution → Extraction
- **B.** Embedding → Chunking → Retrieval → Generation
- **C.** Extraction (Haiku, structured outputs) → Resolution (Sonnet, cluster) → Assembly (NetworkX graph) → Querying (subgraph + grounded answer) (đáp án đúng)
- **D.** Extraction → Querying → Resolution → Assembly

**Đáp án: C**

**Giải thích:** Mỗi stage là một prompt/model call: Haiku extract entities+relations theo Pydantic schema; Sonnet resolve surface forms; NetworkX MultiDiGraph lắp graph với provenance; Sonnet trả lời trên subgraph đã serialize.

## Câu 2 (Tự luận)

RAG và Knowledge Graph khác nhau thế nào, khi nào cần cái nào?

**Trả lời mẫu:** RAG có thể retrieval lặp và tổng hợp nhiều nguồn để xử lý multi-hop. Graph giúp biểu diễn và truy vấn quan hệ tường minh, nhưng extraction/resolution có thể lỗi. Chọn bằng đối chứng retrieval không graph dưới cùng ngân sách.

**Giải thích:** Theo tài liệu chương trình mục 1.1 và 6.5; không dùng quy tắc single-hop/multi-hop để bắt buộc graph.

## Câu 3 (Trắc nghiệm)

Vì sao extraction prompt yêu cầu viết 'one-sentence description grounded in this document' cho mỗi entity?

- **A.** Để hiển thị đẹp trong UI
- **B.** Description là tín hiệu ngữ nghĩa cho stage RESOLUTION, thiếu nó resolver chỉ thấy tên và phải đoán; 'Armstrong, phi hành gia' và 'Armstrong, nghệ sĩ jazz' trùng tên nhưng không được merge (đáp án đúng)
- **C.** Để giảm token
- **D.** Để thay thế cho embeddings

**Đáp án: B**

**Giải thích:** Description không phải metadata mà là input hạng nhất cho resolution, nó thay thứ mà trained classifier phải học từ labeled data theo domain.

## Câu 4 (Trắc nghiệm)

Vì sao với knowledge graph, PRECISION của extraction thường quan trọng hơn RECALL?

- **A.** Vì Haiku không thể đạt recall cao
- **B.** Vì precision rẻ hơn để tính
- **C.** Vì một entity SAI sinh ra các quan hệ sai và lan truyền qua multi-hop reasoning (graph chủ động gây nhiễu), còn entity THIẾU chỉ làm graph không đầy đủ nhưng vẫn đúng (đáp án đúng)
- **D.** Vì recall không đo được

**Đáp án: C**

**Giải thích:** Quan hệ sai có thể lan truyền; thực thể thiếu cũng có thể làm mất đáp án. Đo cả precision/recall theo task và corpus, không lấy một ngưỡng phổ quát cho production.

## Câu 5 (Tự luận)

Nêu 3 vai trò của knowledge graph trong kiến trúc multi-agent (theo Playbook).

**Trả lời mẫu:** (1) Shared memory cho orchestrator-workers: worker đọc/ghi graph trực tiếp thay vì đẩy summary qua context window của orchestrator, window của orchestrator không phình theo số worker. (2) Grounding layer cho evaluator-optimizer: evaluator kiểm tra từng claim theo edge có provenance ('triple X không tồn tại; graph chứa Y từ document Z'): fact-check thay vì cảm giác. (3) Persistent world model cho loop chạy dài: context window bị flush thì graph vẫn còn, 'the agent forgets, the graph does not'.

**Giải thích:** Đây là 3 chỗ cắm graph vào CornAgents.AI: workers ghi, evaluator check, loop qua đêm không mất trí nhớ.

## Câu 6 (Trắc nghiệm)

'Grounded answer' khác 'ungrounded answer' thế nào khi query graph?

- **A.** Grounded bị ràng buộc 'answer using ONLY the graph, cite edges', trả lời truy vết được về triples có provenance và nói rõ graph KHÔNG chứa gì; ungrounded dựa vào pretraining nên nghe hợp lý nhưng trên private corpus thì không kiểm chứng được (đáp án đúng)
- **B.** Grounded chạy nhanh hơn
- **C.** Ungrounded luôn sai
- **D.** Grounded không cần model

**Đáp án: A**

**Giải thích:** Trên corpus riêng (tài liệu Finance Banking nội bộ) model không có kiến thức pretraining, chỉ grounded answer là dùng được, và citation kiểm tra được bằng string matching.

## Câu 7 (Tự luận)

Evaluation feedback loop của KG pipeline hoạt động thế nào và vì sao nó 'cùng hình dạng' với ratchet loop của Karpathy autoresearch?

**Trả lời mẫu:** Lập gold set (entities/relations tự label từ 2+ tài liệu đại diện) → chạy extraction → scorer đo precision/recall/F1 → đổi extraction prompt/schema → chạy lại → giữ thay đổi nếu F1 tăng, revert nếu giảm. Cùng hình dạng với autoresearch: act (extract) → observe (score) → learn (tune prompt) → repeat; chỉ khác artifact được tối ưu không phải train.py mà là prompt/ontology/resolution policy, 'graph autoresearch'. Không có harness này, không biết thay đổi prompt làm chất lượng tốt lên hay tệ đi, và drift theo corpus không ai bắt được.

**Giải thích:** Trí tuệ của loop nằm ở chất lượng environmental feedback, không nằm trong model.

## Câu 8 (Trắc nghiệm)

Bạn muốn biết giữa hai thực thể trong knowledge graph có bao nhiêu đường đi độ dài 2 (ví dụ cùng chịu một văn bản pháp luật). Theo Ma và Tang (Theorem 2.14), đại lượng nào cho con số đó?

- **A.** Phần tử (i, j) của ma trận Laplacian L = D - A, vì nó trừ số cạnh trực tiếp khỏi bậc của nút
- **B.** Phần tử (i, j) của (I - αA)^-1, vì chuỗi lũy thừa của A đếm walk mọi độ dài có trọng số
- **C.** Phần tử (i, j) của ma trận D^2, vì bậc bình phương đếm số cặp láng giềng có thể nối hai nút
- **D.** Phần tử (i, j) của A^2, vì phần tử (i, j) của A^n bằng số walk độ dài n từ v_i đến v_j (đáp án đúng)

**Đáp án: D**

**Giải thích:** Theorem 2.14: "we use A^n to denote the n-th power of the adjacency matrix. The i, j-th element of the matrix A^n equals to the number of v_i-v_j walks of length n." Chứng minh bằng quy nạp qua phương trình 2.2. Lưu ý sách định nghĩa walk có thể lặp nút, khác path (Definition 2.10 và 2.12). (Ma và Tang mục 2.3.2, tr. 21)

## Câu 9 (Trắc nghiệm)

Trong ví dụ đồ thị 5 nút của Ma và Tang (Figure 2.1), ba nút v2, v3, v4 đều có degree 2 nhưng eigenvector centrality của v4 (0,806) cao hơn v2 và v3 (0,675). Điều này minh họa điểm gì khi bạn xếp hạng thực thể quan trọng trong knowledge graph?

- **A.** Eigenvector centrality đo khoảng cách trung bình tới các nút khác, nên nút gần trung tâm hình học được xếp cao hơn
- **B.** Eigenvector centrality tăng theo số shortest path đi qua nút, nên nút nằm giữa hai cụm được xếp cao hơn
- **C.** Eigenvector centrality bị lệch bởi hằng số β cộng thêm cho mỗi nút, nên cần chuẩn hóa lại theo degree
- **D.** Eigenvector centrality không coi mọi láng giềng ngang nhau; nối với láng giềng có centrality cao thì chính nút đó cũng cao hơn (đáp án đúng)

**Đáp án: D**

**Giải thích:** Ma và Tang: degree centrality "treats all the neighbors equally. However, the neighbors themselves can have different importance". Eigenvector centrality định nghĩa c_e = (1/λ) A c_e (phương trình 2.3), chọn λ là trị riêng lớn nhất theo Perron-Frobenius. Example 2.25: trị riêng lớn nhất 2,481, vector riêng [1, 0,675, 0,675, 0,806, 1]; v4 cao hơn "as it directly connects to nodes v1 and v5 whose eigenvector centrality is high." Đếm shortest path là betweenness, hằng số β là Katz. (Ma và Tang mục 2.3.3, tr. 24)

## Câu 10 (Tự luận)

Betweenness centrality theo Ma và Tang được định nghĩa và chuẩn hóa thế nào, vì sao cần chuẩn hóa, và độ đo này giúp gì khi bạn tìm thực thể cầu nối giữa các cụm trong knowledge graph của multi-agent?

**Trả lời mẫu:** Betweenness của nút v_i là tổng trên mọi cặp (v_s, v_t) của tỷ số σ_st(v_i)/σ_st, trong đó σ_st là số shortest path từ v_s tới v_t và σ_st(v_i) là số path trong đó đi qua v_i (phương trình 2.6). Vì tổng lấy trên mọi cặp nút nên giá trị tăng theo kích thước đồ thị; để so sánh giữa các đồ thị, sách chia cho giá trị lớn nhất có thể là (N-1)(N-2)/2 (số cặp nút trong đồ thị vô hướng), thu được normalized betweenness. Trong Example 2.27, v1 và v5 có betweenness 3/2 (chuẩn hóa 1/4), v4 có betweenness 0. Với knowledge graph, nút có betweenness cao là nút mà nhiều đường đi ngắn nhất giữa các thực thể khác phải đi qua, tức thực thể cầu nối mà agent nên ưu tiên giữ chính xác khi extraction.

**Giải thích:** Ma và Tang: "if there are many paths passing through a node, it is at an important position in the graph", định nghĩa c_b(v_i) = Σ σ_st(v_i)/σ_st (phương trình 2.6, tr. 25). Về chuẩn hóa: "the magnitude of the betweenness centrality score scales as the size of graph scales ... There are, in total, (N-1)(N-2)/2 pairs of nodes in an undirected graph. Hence, the maximum betweenness centrality score is (N-1)(N-2)/2." (Ma và Tang mục 2.3.3, tr. 26)

## Câu 11 (Trắc nghiệm)

Sau bước entity resolution, bạn nghi knowledge graph bị tách thành nhiều cụm rời nhau. Theo Ma và Tang (Theorem 2.31), đại lượng phổ nào cho biết đúng số connected component?

- **A.** Bội của trị riêng 0 của ma trận Laplacian L bằng đúng số connected component của đồ thị (đáp án đúng)
- **B.** Trị riêng lớn nhất của ma trận kề A, làm tròn xuống, bằng đúng số connected component của đồ thị
- **C.** Số trị riêng âm của ma trận Laplacian L bằng đúng số connected component của đồ thị
- **D.** Hạng của ma trận bậc D trừ hạng của ma trận kề A bằng đúng số connected component của đồ thị

**Đáp án: A**

**Giải thích:** Theorem 2.31: "the number of 0 eigenvalues of its Laplacian matrix L (the multiplicity of the 0 eigenvalue) equals to the number of connected components in the graph." Chứng minh dựng K vector chỉ báo của K thành phần, mỗi vector là vector riêng ứng với 0 và trực giao nhau. Theorem 2.30 cho biết mọi trị riêng của L đều không âm nên phương án về trị riêng âm sai. (Ma và Tang mục 2.4.2, tr. 28)

## Câu 12 (Trắc nghiệm)

Ma và Tang định nghĩa knowledge graph là G = (V, E, R) với mỗi cạnh là bộ ba (s, r, t). Sách nói khác biệt lớn nhất so với đồ thị đơn là gì, và có hai hướng nào để đưa GNN lên knowledge graph?

- **A.** Khác biệt là số nút rất lớn; hai hướng là lấy mẫu láng giềng khi tính filter, hoặc gộp các nút cùng loại thực thể thành siêu nút để thu nhỏ đồ thị trước khi học
- **B.** Khác biệt là thuộc tính trên nút; hai hướng là học embedding riêng cho từng loại thuộc tính, hoặc nối thuộc tính vào vector đặc trưng nút rồi dùng filter cho đồ thị đơn
- **C.** Khác biệt là thông tin quan hệ trên cạnh; hai hướng là đưa thông tin quan hệ vào thiết kế graph filter, hoặc biến knowledge graph thành đồ thị đơn vô hướng có giữ thông tin quan hệ (đáp án đúng)
- **D.** Khác biệt là đồ thị có hướng; hai hướng là bỏ chiều của mọi cạnh để dùng filter thường, hoặc thêm cạnh ngược cho mọi cạnh gốc rồi học tham số riêng cho hai chiều

**Đáp án: C**

**Giải thích:** Ma và Tang: "The major difference between the knowledge graphs and simple graphs is the relational information, which is important to consider when designing graph neural networks for knowledge graphs." và "there are majorly two ways to deal with the relational edges in knowledge graphs: 1) incorporating the relational information of the edges into the design of graph filters; and 2) transforming the relational knowledge graph into a simple undirected graph by capturing the relational information." (Ma và Tang mục 10.7, tr. 216)

## Câu 13 (Tự luận)

Katz centrality khác eigenvector centrality ở điểm nào, khi nào hai độ đo trùng nhau, và Ma và Tang cảnh báo gì về việc chọn tham số α?

**Trả lời mẫu:** Katz centrality thêm một hằng số β cho chính nút đang xét: c_k(v_i) = α Σ_j A_ij c_k(v_j) + β (phương trình 2.4), dạng ma trận (I - αA) c_k = β. Nó trùng eigenvector centrality khi α = 1/λ_max và β = 0. Về α: α lớn có thể làm ma trận I - αA ill-conditioned, α nhỏ làm mọi nút nhận điểm gần bằng β nên vô dụng; thực tế thường chọn α < 1/λ_max để I - αA khả nghịch và tính c_k = (I - αA)^-1 β. Trong Example 2.26 với β = 1, α = 1/5, v1 và v5 được 2,16, v2 và v3 được 1,79, v4 được 1,87.

**Giải thích:** Ma và Tang: "The Katz centrality is a variant of the eigenvector centrality, which not only considers the centrality scores of the neighbors but also includes a small constant for the central node itself"; "the Katz centrality is equivalent to the eigenvector centrality if we set α = 1/λ_max and β = 0"; "a large α may make the matrix I - α·A ill-conditioned while a small α may make the centrality scores useless since it will assign very similar scores close to β to all nodes." (Ma và Tang mục 2.3.3, tr. 25)

## Câu 14 (Trắc nghiệm)

Ma và Tang chứng minh f^T L f = (1/2) Σ_{v_i} Σ_{v_j ∈ N(v_i)} (f[i] - f[j])^2 (phương trình 2.10). Nếu f là một điểm số gán cho từng thực thể trong knowledge graph, đại lượng này đo điều gì và suy ra tính chất nào của L?

- **A.** Đo tổng bậc có trọng số f của các nút, suy ra định thức của L bằng tích các bậc nút
- **B.** Đo khoảng cách từ f tới vector hằng, nên L khả nghịch khi f không phải là vector hằng
- **C.** Đo mức khác biệt giữa giá trị của các nút kề nhau, luôn không âm nên L là nửa xác định dương (đáp án đúng)
- **D.** Đo số walk độ dài 2 có trọng số f giữa các nút, suy ra L có cùng phổ trị riêng với A^2

**Đáp án: C**

**Giải thích:** Ma và Tang: "f^T L f is the sum of the squares of the differences between adjacent nodes. In other words, it measures how different the values of adjacent nodes are. It is easy to verify that f^T L f is always non-negative for any possible choice of a real vector f, which indicates that the Laplacian matrix is positive semi-definite." Ở mục 2.5 sách gọi giá trị này là độ trơn (smoothness) của tín hiệu đồ thị. L không khả nghịch vì luôn có trị riêng 0 (tr. 28). (Ma và Tang mục 2.4.1, tr. 27)

## Câu 15 (Trắc nghiệm)

Knowledge graph của bạn thiếu nhiều liên kết vì extraction ưu tiên precision. Ma và Tang mô tả bài toán knowledge graph completion và hàm chấm điểm DistMult thế nào?

- **A.** Dự đoán quan hệ giữa hai nút bằng so khớp văn bản mô tả; điểm là token F1 giữa hai mô tả thực thể, huấn luyện bằng các cặp mô tả đã gán nhãn cùng quan hệ
- **B.** Dự đoán bộ ba (s, r, t) có thật hay không; điểm f(s, r, t) = F_s^T R_r F_t với R_r là ma trận chéo của quan hệ r, huấn luyện bằng negative sampling (đáp án đúng)
- **C.** Dự đoán nút bị thiếu trong một connected component; điểm là số walk độ dài 2 giữa hai nút theo A^2, huấn luyện bằng cách che ngẫu nhiên một số nút trong đồ thị
- **D.** Dự đoán nhãn loại thực thể cho nút mới xuất hiện; điểm là cosine giữa embedding nút và embedding trung bình của các nút cùng loại, huấn luyện bằng cross-entropy

**Đáp án: B**

**Giải thích:** Ma và Tang: "Knowledge graph completion, which aims to predict the relation between a pair of disconnected entities ... the task is to predict whether a given triplet (s, r, t) is a real relation or not." DistMult: f(s, r, t) = F_s^(L)T R_r F_t^(L), với R_r "a diagonal matrix corresponding to the relation r to be learned during training"; huấn luyện bằng cross-entropy với k mẫu âm sinh bằng cách "randomly replacing either its subject or object with another entity." (Ma và Tang mục 10.7.3, tr. 218)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Playbook Graph Engineering dùng blocking trước resolution. Blocking là gì và nguyên tắc chung nào nó minh họa?

- **A.** Gom ứng viên bằng tín hiệu rẻ (trùng token tên, Jaccard, quy tắc) thành block 50-100 rồi chỉ để model phân xử trong block; nguyên tắc: model cho phần cần phán xét, logic tất định cho phần còn lại (đáp án đúng)
- **B.** Chia tài liệu thành chunk cố định 512 token
- **C.** Chặn model không được đọc tài liệu dài
- **D.** Xóa mọi thực thể xuất hiện một lần

**Đáp án: A**

**Giải thích:** Playbook (docs/Graph-Engineering-Athropic-Playbook.pdf) ghi pipeline 'works unchanged on blocks of 50-100' và mô tả 'blocking plus expensive LLM arbitration within blocks'.

## Nâng cao 2 (Tự luận)

Ma và Tang định nghĩa ma trận kề A ∈ {0,1}^{N×N}. Vì sao knowledge graph của bạn không biểu diễn được bằng một ma trận như vậy, và hệ quả lên precision ở bước extraction là gì?

**Trả lời mẫu:** KG có cạnh có hướng và nhiều loại quan hệ, nên mỗi loại quan hệ cần một ma trận kề riêng, tức một tensor N×N×R; đây là suy luận từ Definition 2.2 (Deep Learning on Graphs, trang 18), sách chương 2 chỉ xét đồ thị đơn. Vì truy vấn k-hop là chuỗi phép nhân trên các ma trận này, một entry sai lan qua mọi bước, nên Playbook và ghi chú Tuần 17 đặt precision cao hơn recall ở extraction.

**Giải thích:** Playbook cũng nhắc precision 1.00 chưa chắc tốt: 'Perfect precision (1.00) means the extractor is conservative'.
