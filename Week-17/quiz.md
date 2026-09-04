# Tuần 17, Quiz: Graph Engineering: Knowledge Graph làm shared memory cho multi-agent

> Tự kiểm tra **trước** khi xem solution. Tổng **17** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Bốn stage của knowledge graph pipeline (Anthropic Playbook) theo đúng thứ tự?

- **A.** Querying → Assembly → Resolution → Extraction
- **B.** Embedding → Chunking → Retrieval → Generation
- **C.** Extraction (Haiku, structured outputs) → Resolution (Sonnet, cluster) → Assembly (NetworkX graph) → Querying (subgraph + grounded answer)
- **D.** Extraction → Querying → Resolution → Assembly

## Câu 2 (Tự luận)

RAG và Knowledge Graph khác nhau thế nào, khi nào cần cái nào?

## Câu 3 (Trắc nghiệm)

Vì sao extraction prompt yêu cầu viết 'one-sentence description grounded in this document' cho mỗi entity?

- **A.** Để hiển thị đẹp trong UI
- **B.** Description là tín hiệu ngữ nghĩa cho stage RESOLUTION, thiếu nó resolver chỉ thấy tên và phải đoán; 'Armstrong, phi hành gia' và 'Armstrong, nghệ sĩ jazz' trùng tên nhưng không được merge
- **C.** Để giảm token
- **D.** Để thay thế cho embeddings

## Câu 4 (Trắc nghiệm)

Vì sao với knowledge graph, PRECISION của extraction thường quan trọng hơn RECALL?

- **A.** Vì Haiku không thể đạt recall cao
- **B.** Vì precision rẻ hơn để tính
- **C.** Vì một entity SAI sinh ra các quan hệ sai và lan truyền qua multi-hop reasoning (graph chủ động gây nhiễu), còn entity THIẾU chỉ làm graph không đầy đủ nhưng vẫn đúng
- **D.** Vì recall không đo được

## Câu 5 (Tự luận)

Nêu 3 vai trò của knowledge graph trong kiến trúc multi-agent (theo Playbook).

## Câu 6 (Trắc nghiệm)

'Grounded answer' khác 'ungrounded answer' thế nào khi query graph?

- **A.** Grounded bị ràng buộc 'answer using ONLY the graph, cite edges', trả lời truy vết được về triples có provenance và nói rõ graph KHÔNG chứa gì; ungrounded dựa vào pretraining nên nghe hợp lý nhưng trên private corpus thì không kiểm chứng được
- **B.** Grounded chạy nhanh hơn
- **C.** Ungrounded luôn sai
- **D.** Grounded không cần model

## Câu 7 (Tự luận)

Evaluation feedback loop của KG pipeline hoạt động thế nào và vì sao nó 'cùng hình dạng' với ratchet loop của Karpathy autoresearch?

## Câu 8 (Trắc nghiệm)

Bạn muốn biết giữa hai thực thể trong knowledge graph có bao nhiêu đường đi độ dài 2 (ví dụ cùng chịu một văn bản pháp luật). Theo Ma và Tang (Theorem 2.14), đại lượng nào cho con số đó?

- **A.** Phần tử (i, j) của ma trận Laplacian L = D - A, vì nó trừ số cạnh trực tiếp khỏi bậc của nút
- **B.** Phần tử (i, j) của (I - αA)^-1, vì chuỗi lũy thừa của A đếm walk mọi độ dài có trọng số
- **C.** Phần tử (i, j) của ma trận D^2, vì bậc bình phương đếm số cặp láng giềng có thể nối hai nút
- **D.** Phần tử (i, j) của A^2, vì phần tử (i, j) của A^n bằng số walk độ dài n từ v_i đến v_j

## Câu 9 (Trắc nghiệm)

Trong ví dụ đồ thị 5 nút của Ma và Tang (Figure 2.1), ba nút v2, v3, v4 đều có degree 2 nhưng eigenvector centrality của v4 (0,806) cao hơn v2 và v3 (0,675). Điều này minh họa điểm gì khi bạn xếp hạng thực thể quan trọng trong knowledge graph?

- **A.** Eigenvector centrality đo khoảng cách trung bình tới các nút khác, nên nút gần trung tâm hình học được xếp cao hơn
- **B.** Eigenvector centrality tăng theo số shortest path đi qua nút, nên nút nằm giữa hai cụm được xếp cao hơn
- **C.** Eigenvector centrality bị lệch bởi hằng số β cộng thêm cho mỗi nút, nên cần chuẩn hóa lại theo degree
- **D.** Eigenvector centrality không coi mọi láng giềng ngang nhau; nối với láng giềng có centrality cao thì chính nút đó cũng cao hơn

## Câu 10 (Tự luận)

Betweenness centrality theo Ma và Tang được định nghĩa và chuẩn hóa thế nào, vì sao cần chuẩn hóa, và độ đo này giúp gì khi bạn tìm thực thể cầu nối giữa các cụm trong knowledge graph của multi-agent?

## Câu 11 (Trắc nghiệm)

Sau bước entity resolution, bạn nghi knowledge graph bị tách thành nhiều cụm rời nhau. Theo Ma và Tang (Theorem 2.31), đại lượng phổ nào cho biết đúng số connected component?

- **A.** Bội của trị riêng 0 của ma trận Laplacian L bằng đúng số connected component của đồ thị
- **B.** Trị riêng lớn nhất của ma trận kề A, làm tròn xuống, bằng đúng số connected component của đồ thị
- **C.** Số trị riêng âm của ma trận Laplacian L bằng đúng số connected component của đồ thị
- **D.** Hạng của ma trận bậc D trừ hạng của ma trận kề A bằng đúng số connected component của đồ thị

## Câu 12 (Trắc nghiệm)

Ma và Tang định nghĩa knowledge graph là G = (V, E, R) với mỗi cạnh là bộ ba (s, r, t). Sách nói khác biệt lớn nhất so với đồ thị đơn là gì, và có hai hướng nào để đưa GNN lên knowledge graph?

- **A.** Khác biệt là số nút rất lớn; hai hướng là lấy mẫu láng giềng khi tính filter, hoặc gộp các nút cùng loại thực thể thành siêu nút để thu nhỏ đồ thị trước khi học
- **B.** Khác biệt là thuộc tính trên nút; hai hướng là học embedding riêng cho từng loại thuộc tính, hoặc nối thuộc tính vào vector đặc trưng nút rồi dùng filter cho đồ thị đơn
- **C.** Khác biệt là thông tin quan hệ trên cạnh; hai hướng là đưa thông tin quan hệ vào thiết kế graph filter, hoặc biến knowledge graph thành đồ thị đơn vô hướng có giữ thông tin quan hệ
- **D.** Khác biệt là đồ thị có hướng; hai hướng là bỏ chiều của mọi cạnh để dùng filter thường, hoặc thêm cạnh ngược cho mọi cạnh gốc rồi học tham số riêng cho hai chiều

## Câu 13 (Tự luận)

Katz centrality khác eigenvector centrality ở điểm nào, khi nào hai độ đo trùng nhau, và Ma và Tang cảnh báo gì về việc chọn tham số α?

## Câu 14 (Trắc nghiệm)

Ma và Tang chứng minh f^T L f = (1/2) Σ_{v_i} Σ_{v_j ∈ N(v_i)} (f[i] - f[j])^2 (phương trình 2.10). Nếu f là một điểm số gán cho từng thực thể trong knowledge graph, đại lượng này đo điều gì và suy ra tính chất nào của L?

- **A.** Đo tổng bậc có trọng số f của các nút, suy ra định thức của L bằng tích các bậc nút
- **B.** Đo khoảng cách từ f tới vector hằng, nên L khả nghịch khi f không phải là vector hằng
- **C.** Đo mức khác biệt giữa giá trị của các nút kề nhau, luôn không âm nên L là nửa xác định dương
- **D.** Đo số walk độ dài 2 có trọng số f giữa các nút, suy ra L có cùng phổ trị riêng với A^2

## Câu 15 (Trắc nghiệm)

Knowledge graph của bạn thiếu nhiều liên kết vì extraction ưu tiên precision. Ma và Tang mô tả bài toán knowledge graph completion và hàm chấm điểm DistMult thế nào?

- **A.** Dự đoán quan hệ giữa hai nút bằng so khớp văn bản mô tả; điểm là token F1 giữa hai mô tả thực thể, huấn luyện bằng các cặp mô tả đã gán nhãn cùng quan hệ
- **B.** Dự đoán bộ ba (s, r, t) có thật hay không; điểm f(s, r, t) = F_s^T R_r F_t với R_r là ma trận chéo của quan hệ r, huấn luyện bằng negative sampling
- **C.** Dự đoán nút bị thiếu trong một connected component; điểm là số walk độ dài 2 giữa hai nút theo A^2, huấn luyện bằng cách che ngẫu nhiên một số nút trong đồ thị
- **D.** Dự đoán nhãn loại thực thể cho nút mới xuất hiện; điểm là cosine giữa embedding nút và embedding trung bình của các nút cùng loại, huấn luyện bằng cross-entropy

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Playbook Graph Engineering dùng blocking trước resolution. Blocking là gì và nguyên tắc chung nào nó minh họa?

- **A.** Gom ứng viên bằng tín hiệu rẻ (trùng token tên, Jaccard, quy tắc) thành block 50-100 rồi chỉ để model phân xử trong block; nguyên tắc: model cho phần cần phán xét, logic tất định cho phần còn lại
- **B.** Chia tài liệu thành chunk cố định 512 token
- **C.** Chặn model không được đọc tài liệu dài
- **D.** Xóa mọi thực thể xuất hiện một lần

## Nâng cao 2 (Tự luận)

Ma và Tang định nghĩa ma trận kề A ∈ {0,1}^{N×N}. Vì sao knowledge graph của bạn không biểu diễn được bằng một ma trận như vậy, và hệ quả lên precision ở bước extraction là gì?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
