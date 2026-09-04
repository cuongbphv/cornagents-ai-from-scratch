# Tuần 6, Quiz: Tokenization, embeddings, attention từ đầu

> Tự kiểm tra **trước** khi xem solution. Tổng **18** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Vì sao trong scaled dot-product attention ta chia cho sqrt(d_k)?

- **A.** Để score luôn dương
- **B.** Để chuẩn hoá vector về độ dài 1
- **C.** Để tiết kiệm bộ nhớ
- **D.** Để giữ phương sai của score ổn định, tránh softmax bão hoà làm gradient triệt tiêu

## Câu 2 (Tự luận)

Causal mask làm gì và cài đặt thế nào?

## Câu 3 (Trắc nghiệm)

Token embedding và positional embedding được kết hợp thế nào trong GPT-2?

- **A.** Nhân element-wise
- **B.** Chỉ dùng token embedding
- **C.** Nối (concatenate) lại
- **D.** Cộng vào nhau (cùng chiều d_model)

## Câu 4 (Trắc nghiệm)

Ma trận attention scores (trước khi nhân V) có shape nào với input (batch, seq, d)?

- **A.** (batch, d, d)
- **B.** (seq, seq)
- **C.** (batch, seq, d)
- **D.** (batch, seq, seq)

## Câu 5 (Tự luận)

[Nâng cao] RoPE khác với positional embedding tuyệt đối của GPT-2 thế nào?

## Câu 6 (Trắc nghiệm)

[Nâng cao] Mục đích chính của Grouped-Query Attention (GQA) so với Multi-Head Attention?

- **A.** Thay softmax bằng sigmoid
- **B.** Tăng số head để chính xác hơn
- **C.** Bỏ hoàn toàn key và value
- **D.** Cho các nhóm head chia sẻ chung K,V để GIẢM kích thước KV cache khi inference

## Câu 7 (Trắc nghiệm)

[Nâng cao] Độ phức tạp bộ nhớ/tính toán của self-attention thường (full) theo độ dài seq n là?

- **A.** O(1)
- **B.** O(n)
- **C.** O(n log n)
- **D.** O(n^2)

## Câu 8 (Tự luận)

Jurafsky và Martin (SLP3 mục 2.4) nói từ và morpheme có nghĩa ổn định nhưng khó định nghĩa hình thức, còn ký tự thì dễ định nghĩa nhưng quá nhỏ. BPE giải quyết mâu thuẫn này bằng cách nào, và vì sao việc chuẩn hóa đơn vị token lại cần cho perplexity?

## Câu 9 (Trắc nghiệm)

Theo SLP3 mục 2.4.2, khi BPE encoder tách một câu mới (test) thành token, nó quyết định các phép merge dựa trên gì?

- **A.** Chọn ngẫu nhiên một trong các cách phân đoạn hợp lệ theo vocabulary để tăng tính đa dạng của dữ liệu đưa vào model khi huấn luyện.
- **B.** Đếm lại tần suất các cặp ký hiệu kề nhau trong chính câu mới, rồi merge cặp phổ biến nhất của câu đó cho tới khi hết cặp lặp lại.
- **C.** Áp dụng lần lượt các merge đã học theo đúng thứ tự học từ tập train (cặp phổ biến nhất trước); tần suất trong dữ liệu test không có vai trò gì.
- **D.** Tìm cách phân đoạn cho ra ít token nhất bằng quy hoạch động trên toàn bộ vocabulary đã học, không cần quan tâm thứ tự merge.

## Câu 10 (Trắc nghiệm)

SLP3 mục 2.4.1 minh họa BPE trên corpus 10 ký tự "A B D C A B E C A B" với vocabulary ban đầu {A, B, C, D, E}. Sau hai lần merge (tạo AB rồi CAB), độ dài corpus và kích cỡ vocabulary là bao nhiêu?

- **A.** Corpus dài 5 token, vocabulary có 6 token.
- **B.** Corpus dài 8 token, vocabulary có 7 token.
- **C.** Corpus dài 7 token, vocabulary có 6 token.
- **D.** Corpus dài 5 token, vocabulary có 7 token.

## Câu 11 (Trắc nghiệm)

SLP3 mục 5.4 giải thích vì sao không dùng dot product thô làm độ đo tương đồng giữa hai vector từ mà chuẩn hóa thành cosine. Lý do là gì?

- **A.** Vì dot product thô tốn O(N²) phép nhân với N chiều, còn cosine tính được trong O(N) nhờ chuẩn hóa vector trước khi so sánh.
- **B.** Vì dot product thô thiên về vector dài, mà từ xuất hiện nhiều có vector dài hơn; chia cho độ dài hai vector loại bỏ ảnh hưởng của tần suất.
- **C.** Vì dot product thô chỉ định nghĩa được cho vector thưa đếm từ, còn cosine mới áp dụng được cho embedding dày đặc học từ mạng neural.
- **D.** Vì dot product thô có thể âm trong khi độ tương đồng phải luôn không âm để có thể so sánh và xếp hạng giữa các cặp từ trong vocabulary.

## Câu 12 (Trắc nghiệm)

Theo UDL mục 12.2.1, số attention weight a[x_m, x_n] trong một khối self-attention phụ thuộc thế nào vào độ dài chuỗi N và chiều mỗi input D?

- **A.** Tuyến tính theo N và bậc hai theo D, giống một lớp fully connected nối toàn bộ DN đầu vào với DN đầu ra.
- **B.** Bậc hai theo D và độc lập với N, vì ma trận Ω_v có kích cỡ D × D được dùng chung cho mọi vị trí trong chuỗi.
- **C.** Tuyến tính theo N và tuyến tính theo D, vì mỗi cặp input cần D trọng số riêng để so từng chiều với nhau.
- **D.** Bậc hai theo N và độc lập với D, vì chỉ có một trọng số cho mỗi cặp có thứ tự (x_m, x_n) bất kể kích cỡ của các input.

## Câu 13 (Trắc nghiệm)

UDL mục 12.2.3 nói self-attention không có hàm kích hoạt như ReLU, nhưng toàn bộ phép tính vẫn phi tuyến. Tính phi tuyến đó đến từ đâu?

- **A.** Từ ReLU ẩn trong phép tính query và key, giống lớp fully connected chuẩn f[x] = ReLU[β + Ωx] mà Prince nêu ở đầu mục 12.2.
- **B.** Từ dot product query-key rồi softmax khi tính attention weight; các trọng số này là hàm phi tuyến của input, một dạng hypernetwork.
- **C.** Từ LayerNorm được áp dụng lên các value trước khi lấy tổng có trọng số, vì phép chuẩn hóa chia cho độ lệch chuẩn là phi tuyến.
- **D.** Từ positional encoding được cộng vào input, vì các hàm sin và cos dùng để mã hóa vị trí là hàm phi tuyến của chỉ số vị trí.

## Câu 14 (Trắc nghiệm)

Fleuret (mục 4.8) nêu tính chất của attention operator đối với hoán vị đầu vào khi không dùng mask. Tính chất đó là gì?

- **A.** Đẳng biến với mọi hoán vị của cả ba tensor, nghĩa là đổi chỗ bất kỳ đầu vào nào cũng đổi chỗ đầu ra tương ứng.
- **B.** Bất biến với hoán vị của key và value, và đẳng biến với hoán vị của query vì tensor kết quả bị hoán vị theo cùng cách.
- **C.** Bất biến với mọi hoán vị của cả query, key và value, nên bắt buộc phải cộng positional encoding thì mới phân biệt được vị trí.
- **D.** Bất biến với hoán vị của query và đẳng biến với hoán vị của key và value, vì thứ tự query không ảnh hưởng tới điểm attention.

## Câu 15 (Tự luận)

SLP3 mục 7.1 mở đầu bằng hai câu "The chicken didn't cross the road because it was too tired" và "... because it was too wide", rồi xét tình huống model causal mới đọc tới từ "it". Dùng ví dụ này để giải thích vì sao static embedding không đủ, và attention xây biểu diễn cho "it" như thế nào ở lớp k+1.

## Câu 16 (Tự luận)

SLP3 mục 7.4 mô tả việc lấy token embedding như một phép nhân ma trận và nêu một hạn chế của absolute positional embedding học được. Hãy giải thích vì sao nn.Embedding tương đương nhân vector one-hot với E, nêu shape của E và E_pos, và mô tả hạn chế đó.

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

GQA (arXiv 2305.13245) là gì, và vì sao nó làm giảm KV cache nhưng không làm giảm số phép nhân trong QKᵀ?

- **A.** GQA chia query head thành g nhóm cùng chia sẻ một cặp K, V; cache chỉ lưu n_kv_head cặp nên nhỏ hơn, nhưng mỗi query head vẫn tính điểm với toàn bộ K của nhóm nên số phép nhân điểm attention không đổi
- **B.** GQA chỉ áp dụng khi train, không khi inference
- **C.** GQA bỏ hẳn value
- **D.** GQA giảm số query head

## Nâng cao 2 (Tự luận)

FlashAttention được gọi là exact attention. Nó thay đổi điều gì và không thay đổi điều gì so với cách bạn cài attention ở tuần này?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
