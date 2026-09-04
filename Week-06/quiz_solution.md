# Tuần 6, Đáp án & Giải thích: Tokenization, embeddings, attention từ đầu

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Vì sao trong scaled dot-product attention ta chia cho sqrt(d_k)?

- **A.** Để score luôn dương
- **B.** Để chuẩn hoá vector về độ dài 1
- **C.** Để tiết kiệm bộ nhớ
- **D.** Để giữ phương sai của score ổn định, tránh softmax bão hoà làm gradient triệt tiêu (đáp án đúng)

**Đáp án: D**

**Giải thích:** Dot product của hai vector d_k chiều có phương sai ~d_k; không chia, score quá lớn đẩy softmax về one-hot → gradient ~0, khó học.

## Câu 2 (Tự luận)

Causal mask làm gì và cài đặt thế nào?

**Trả lời mẫu:** Causal (masked) attention làm cho token chỉ 'nhìn' về quá khứ, không thấy token tương lai, bắt buộc cho mô hình tự hồi quy. Cài đặt: đặt phần tam giác TRÊN của ma trận score = -vô cực (hoặc -1e9) TRƯỚC khi softmax; sau softmax các vị trí đó thành ~0, nên token i không attend tới token j>i.

**Giải thích:** Nếu để token thấy tương lai, model 'gian lận' lúc train và vô dụng lúc generate.

## Câu 3 (Trắc nghiệm)

Token embedding và positional embedding được kết hợp thế nào trong GPT-2?

- **A.** Nhân element-wise
- **B.** Chỉ dùng token embedding
- **C.** Nối (concatenate) lại
- **D.** Cộng vào nhau (cùng chiều d_model) (đáp án đúng)

**Đáp án: D**

**Giải thích:** GPT-2 cộng token embedding và positional embedding (cùng shape) → một vector vừa mang nghĩa token vừa mang vị trí.

## Câu 4 (Trắc nghiệm)

Ma trận attention scores (trước khi nhân V) có shape nào với input (batch, seq, d)?

- **A.** (batch, d, d)
- **B.** (seq, seq)
- **C.** (batch, seq, d)
- **D.** (batch, seq, seq) (đáp án đúng)

**Đáp án: D**

**Giải thích:** Score[i,j] = q_i·k_j cho mọi cặp token → (batch, seq, seq). Chính shape (seq×seq) này gây độ phức tạp O(n^2).

## Câu 5 (Tự luận)

[Nâng cao] RoPE khác với positional embedding tuyệt đối của GPT-2 thế nào?

**Trả lời mẫu:** GPT-2 CỘNG một vector vị trí học được vào embedding. RoPE thay vào đó XOAY các cặp chiều của Q và K một góc tỉ lệ với vị trí token, áp dụng ngay trong attention (không lên V). Hệ quả: tích q_m·k_n chỉ phụ thuộc khoảng cách tương đối (m-n), không phụ thuộc vị trí tuyệt đối → tổng quát hoá tốt hơn ra ngoài độ dài đã train và là nền cho mở rộng context (NTK/YaRN). Llama 3, Qwen3 dùng RoPE.

**Giải thích:** Xem mục A1 trong advanced_topics_vi.md.

## Câu 6 (Trắc nghiệm)

[Nâng cao] Mục đích chính của Grouped-Query Attention (GQA) so với Multi-Head Attention?

- **A.** Thay softmax bằng sigmoid
- **B.** Tăng số head để chính xác hơn
- **C.** Bỏ hoàn toàn key và value
- **D.** Cho các nhóm head chia sẻ chung K,V để GIẢM kích thước KV cache khi inference (đáp án đúng)

**Đáp án: D**

**Giải thích:** GQA gom head thành nhóm dùng chung K,V → KV cache nhỏ hơn → sinh text dài rẻ hơn về bộ nhớ; trung dung giữa MHA và MQA.

## Câu 7 (Trắc nghiệm)

[Nâng cao] Độ phức tạp bộ nhớ/tính toán của self-attention thường (full) theo độ dài seq n là?

- **A.** O(1)
- **B.** O(n)
- **C.** O(n log n)
- **D.** O(n^2) (đáp án đúng)

**Đáp án: D**

**Giải thích:** Ma trận score n×n → O(n^2). Đây là động lực cho sliding-window, MLA, và FlashAttention (tiling, không vật chất hoá ma trận n×n).

## Câu 8 (Tự luận)

Jurafsky và Martin (SLP3 mục 2.4) nói từ và morpheme có nghĩa ổn định nhưng khó định nghĩa hình thức, còn ký tự thì dễ định nghĩa nhưng quá nhỏ. BPE giải quyết mâu thuẫn này bằng cách nào, và vì sao việc chuẩn hóa đơn vị token lại cần cho perplexity?

**Trả lời mẫu:** BPE học đơn vị token từ dữ liệu bằng cách gộp dần các cặp ký tự hay đi cùng nhau, nên đơn vị thu được thường cỡ morpheme hoặc từ với từ phổ biến, và rơi về ký tự với từ hiếm. Chuẩn hóa đơn vị cần vì perplexity tính trên mỗi token, chuẩn hóa theo độ dài chuỗi; hai model tokenize khác nhau thì số token khác nhau và perplexity không so được với nhau.

**Giải thích:** SLP3 trang 42 nói rõ tokenization là để 'different algorithms and systems can agree on simple questions' như độ dài văn bản, và perplexity 'assume that all texts have a fixed' đơn vị. Đây là lý do mục H nâng cao đề xuất bits per byte để so model khác tokenizer.

## Câu 9 (Trắc nghiệm)

Theo SLP3 mục 2.4.2, khi BPE encoder tách một câu mới (test) thành token, nó quyết định các phép merge dựa trên gì?

- **A.** Chọn ngẫu nhiên một trong các cách phân đoạn hợp lệ theo vocabulary để tăng tính đa dạng của dữ liệu đưa vào model khi huấn luyện.
- **B.** Đếm lại tần suất các cặp ký hiệu kề nhau trong chính câu mới, rồi merge cặp phổ biến nhất của câu đó cho tới khi hết cặp lặp lại.
- **C.** Áp dụng lần lượt các merge đã học theo đúng thứ tự học từ tập train (cặp phổ biến nhất trước); tần suất trong dữ liệu test không có vai trò gì. (đáp án đúng)
- **D.** Tìm cách phân đoạn cho ra ít token nhất bằng quy hoạch động trên toàn bộ vocabulary đã học, không cần quan tâm thứ tự merge.

**Đáp án: C**

**Giải thích:** SLP3 viết encoder "just runs on the test data the merges we have learned from the training data. It runs them in the order we learned them (i.e., greedily, meaning starting from the most frequent in the training data). The frequencies in the test data don't play a role, just the frequencies in the training data." Vì vậy tokenizer của bạn chỉ cần lưu danh sách merge có thứ tự; encode là lặp lại danh sách đó. (SLP3 mục 2.4.2, tr. 45)

## Câu 10 (Trắc nghiệm)

SLP3 mục 2.4.1 minh họa BPE trên corpus 10 ký tự "A B D C A B E C A B" với vocabulary ban đầu {A, B, C, D, E}. Sau hai lần merge (tạo AB rồi CAB), độ dài corpus và kích cỡ vocabulary là bao nhiêu?

- **A.** Corpus dài 5 token, vocabulary có 6 token.
- **B.** Corpus dài 8 token, vocabulary có 7 token.
- **C.** Corpus dài 7 token, vocabulary có 6 token.
- **D.** Corpus dài 5 token, vocabulary có 7 token. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Sau merge thứ nhất corpus thành "AB D C AB E C AB": vocabulary 6 token {A, B, C, D, E, AB}, corpus dài 7. Cặp phổ biến nhất tiếp theo là "C AB", merge thành CAB cho corpus "AB D CAB E CAB": vocabulary 7 token và "the corpus has length 5". Ví dụ này cho thấy mỗi merge làm vocabulary tăng đúng 1 và corpus ngắn đi, đó là cách vocab_size của bạn tăng theo số merge k. (SLP3 mục 2.4.1, tr. 43)

## Câu 11 (Trắc nghiệm)

SLP3 mục 5.4 giải thích vì sao không dùng dot product thô làm độ đo tương đồng giữa hai vector từ mà chuẩn hóa thành cosine. Lý do là gì?

- **A.** Vì dot product thô tốn O(N²) phép nhân với N chiều, còn cosine tính được trong O(N) nhờ chuẩn hóa vector trước khi so sánh.
- **B.** Vì dot product thô thiên về vector dài, mà từ xuất hiện nhiều có vector dài hơn; chia cho độ dài hai vector loại bỏ ảnh hưởng của tần suất. (đáp án đúng)
- **C.** Vì dot product thô chỉ định nghĩa được cho vector thưa đếm từ, còn cosine mới áp dụng được cho embedding dày đặc học từ mạng neural.
- **D.** Vì dot product thô có thể âm trong khi độ tương đồng phải luôn không âm để có thể so sánh và xếp hạng giữa các cặp từ trong vocabulary.

**Đáp án: B**

**Giải thích:** SLP3 viết "This raw dot product, however, has a problem as a similarity metric: it favors long vectors" và "More frequent words have longer vectors, since they tend to co-occur with more words"; ta muốn độ đo cho biết hai từ giống nhau đến đâu "regardless of their frequency", nên chia dot product cho tích độ dài, chính là cos θ (công thức 5.9, 5.10). Với unit vector, dot product và cosine trùng nhau, đó là lý do các hệ RAG chuẩn hóa embedding trước khi so. (SLP3 mục 5.4, tr. 135)

## Câu 12 (Trắc nghiệm)

Theo UDL mục 12.2.1, số attention weight a[x_m, x_n] trong một khối self-attention phụ thuộc thế nào vào độ dài chuỗi N và chiều mỗi input D?

- **A.** Tuyến tính theo N và bậc hai theo D, giống một lớp fully connected nối toàn bộ DN đầu vào với DN đầu ra.
- **B.** Bậc hai theo D và độc lập với N, vì ma trận Ω_v có kích cỡ D × D được dùng chung cho mọi vị trí trong chuỗi.
- **C.** Tuyến tính theo N và tuyến tính theo D, vì mỗi cặp input cần D trọng số riêng để so từng chiều với nhau.
- **D.** Bậc hai theo N và độc lập với D, vì chỉ có một trọng số cho mỗi cặp có thứ tự (x_m, x_n) bất kể kích cỡ của các input. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Prince viết các attention weight "are also sparse since there is only one weight for each ordered pair of inputs (x_m, x_n), regardless of the size of these inputs (figure 12.2c). It follows that the number of attention weights has a quadratic dependence on the sequence length N, but is independent of the length D of each input." Ngược lại, phép tính value với Ω_v chia sẻ tham số nên chỉ tăng tuyến tính theo N. Đây là gốc của ma trận N × N trong code attention của bạn. (UDL mục 12.2.1, tr. 209)

## Câu 13 (Trắc nghiệm)

UDL mục 12.2.3 nói self-attention không có hàm kích hoạt như ReLU, nhưng toàn bộ phép tính vẫn phi tuyến. Tính phi tuyến đó đến từ đâu?

- **A.** Từ ReLU ẩn trong phép tính query và key, giống lớp fully connected chuẩn f[x] = ReLU[β + Ωx] mà Prince nêu ở đầu mục 12.2.
- **B.** Từ dot product query-key rồi softmax khi tính attention weight; các trọng số này là hàm phi tuyến của input, một dạng hypernetwork. (đáp án đúng)
- **C.** Từ LayerNorm được áp dụng lên các value trước khi lấy tổng có trọng số, vì phép chuẩn hóa chia cho độ lệch chuẩn là phi tuyến.
- **D.** Từ positional encoding được cộng vào input, vì các hàm sin và cos dùng để mã hóa vị trí là hàm phi tuyến của chỉ số vị trí.

**Đáp án: B**

**Giải thích:** Prince tóm tắt: "There is no activation function, but the mechanism is nonlinear due to the dot-product and a softmax operation used to compute the attention weights." Ở mục 12.2.2 ông gọi đây là ví dụ của hypernetwork, "where one network branch computes the weights of another". Value chỉ là biến đổi tuyến tính của input; phi tuyến nằm ở cách các value được trộn. (UDL mục 12.2.3, tr. 209-211)

## Câu 14 (Trắc nghiệm)

Fleuret (mục 4.8) nêu tính chất của attention operator đối với hoán vị đầu vào khi không dùng mask. Tính chất đó là gì?

- **A.** Đẳng biến với mọi hoán vị của cả ba tensor, nghĩa là đổi chỗ bất kỳ đầu vào nào cũng đổi chỗ đầu ra tương ứng.
- **B.** Bất biến với hoán vị của key và value, và đẳng biến với hoán vị của query vì tensor kết quả bị hoán vị theo cùng cách. (đáp án đúng)
- **C.** Bất biến với mọi hoán vị của cả query, key và value, nên bắt buộc phải cộng positional encoding thì mới phân biệt được vị trí.
- **D.** Bất biến với hoán vị của query và đẳng biến với hoán vị của key và value, vì thứ tự query không ảnh hưởng tới điểm attention.

**Đáp án: B**

**Giải thích:** Fleuret viết attention operator, và do đó multi-head attention layer khi không có mask, "is invariant to a permutation of the keys and values, and equivariant to a permutation of the queries, as it would permute the resulting tensor similarly." Đổi chỗ các key/value chỉ đổi thứ tự cộng trong Σ_k A_{q,k} V_k nên Y_q không đổi; đổi chỗ query thì các hàng của Y đổi chỗ theo. Đây là lý do cần positional encoding (mục 4.10). (Fleuret mục 4.8, tr. 97)

## Câu 15 (Tự luận)

SLP3 mục 7.1 mở đầu bằng hai câu "The chicken didn't cross the road because it was too tired" và "... because it was too wide", rồi xét tình huống model causal mới đọc tới từ "it". Dùng ví dụ này để giải thích vì sao static embedding không đủ, và attention xây biểu diễn cho "it" như thế nào ở lớp k+1.

**Trả lời mẫu:** Với static embedding như word2vec, từ "it" luôn có cùng một vector dù nó chỉ con gà (câu 1) hay con đường (câu 2). Khi model causal mới đọc tới "it" thì chưa biết nó sẽ chỉ gì, nên biểu diễn hợp lý phải mang đặc điểm của cả chicken và road. Attention làm điều đó: khi tính biểu diễn cho "it" ở lớp k+1, nó gán trọng số cao cho cột chicken và road ở lớp k (Figure 7.3) và tổng hợp biểu diễn của các token đó, tạo ra contextual embedding thay đổi theo ngữ cảnh và có thể lấy thông tin từ những từ ở xa.

**Giải thích:** SLP3 viết với static embedding "the representation of a word's meaning is always the same vector irrespective of the context"; ở câu (7.3) dừng tại "it", "a representation of it at this point might have aspects of both chicken and road" (tr. 179). Attention là cơ chế "weighs and combines the representations from appropriate other tokens in the context from layer k to build the representation for tokens in layer k + 1", và Figure 7.3 cho thấy chicken và road nhận attention weight cao. (SLP3 mục 7.1, tr. 180)

## Câu 16 (Tự luận)

SLP3 mục 7.4 mô tả việc lấy token embedding như một phép nhân ma trận và nêu một hạn chế của absolute positional embedding học được. Hãy giải thích vì sao nn.Embedding tương đương nhân vector one-hot với E, nêu shape của E và E_pos, và mô tả hạn chế đó.

**Trả lời mẫu:** E có shape [|V| × d], mỗi hàng là embedding của một token. Nhân vector one-hot [1 × |V|] (chỉ có 1 tại chỉ số token) với E cho ra đúng hàng tương ứng, nên lookup theo chỉ số của nn.Embedding và phép nhân one-hot × E cho cùng kết quả; cả chuỗi N token là ma trận one-hot [N × |V|] nhân E cho [N × d]. Positional embedding tuyệt đối được lưu trong E_pos shape [N × d] và cộng vào token embedding. Hạn chế: các vị trí đầu chuỗi có rất nhiều ví dụ huấn luyện còn các vị trí gần giới hạn độ dài có ít, nên embedding của các vị trí cuối có thể được huấn luyện kém và tổng quát hóa không tốt; sinusoidal hay RoPE là các lựa chọn thay thế.

**Giải thích:** SLP3: E "has a row for each of the |V| tokens" với shape [|V| × d]; "Multiplying by a one-hot vector that has only one non-zero element x_i = 1 simply selects out the relevant row vector for word i" (Figure 7.12, 7.13, tr. 192). Positional embedding học được lưu trong E_pos shape [N × d]; hạn chế: "there will be plenty of training examples for the initial positions in our inputs and correspondingly fewer at the outer length limits. These latter embeddings may be poorly trained and may not generalize well during testing." (SLP3 mục 7.4, tr. 193)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

GQA (arXiv 2305.13245) là gì, và vì sao nó làm giảm KV cache nhưng không làm giảm số phép nhân trong QKᵀ?

- **A.** GQA chia query head thành g nhóm cùng chia sẻ một cặp K, V; cache chỉ lưu n_kv_head cặp nên nhỏ hơn, nhưng mỗi query head vẫn tính điểm với toàn bộ K của nhóm nên số phép nhân điểm attention không đổi (đáp án đúng)
- **B.** GQA chỉ áp dụng khi train, không khi inference
- **C.** GQA bỏ hẳn value
- **D.** GQA giảm số query head

**Đáp án: A**

**Giải thích:** Paper mô tả GQA là 'an interpolation between multi-head and multi-query attention with single key and value heads per subgroup of query heads'. Llama 3 dùng 8 KV head (arXiv 2407.21783 mục 3.2).

## Nâng cao 2 (Tự luận)

FlashAttention được gọi là exact attention. Nó thay đổi điều gì và không thay đổi điều gì so với cách bạn cài attention ở tuần này?

**Trả lời mẫu:** Nó không đổi kết quả toán học: cùng softmax(QKᵀ/√d)V. Nó đổi cách dùng bộ nhớ: chia Q, K, V thành khối (tiling), tính softmax theo kiểu streaming trong SRAM của GPU, không vật chất hóa ma trận n×n trong HBM, nên giảm số lần đọc ghi bộ nhớ (Dao et al., arXiv 2205.14135, abstract: 'an IO-aware exact attention algorithm that uses tiling'). Trong PyTorch, F.scaled_dot_product_attention chọn backend flash khi đủ điều kiện.

**Giải thích:** Kiểm bằng cách so output attention thủ công của bạn với F.scaled_dot_product_attention trên cùng input, sai lệch phải ở mức sai số số học.
