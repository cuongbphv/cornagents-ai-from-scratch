# Tuần 8, Quiz: Pretraining: training loop + 1 lần chạy GPT-2 thật

> Tự kiểm tra **trước** khi xem solution. Tổng **20** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Quan hệ giữa cross-entropy loss L và perplexity (PPL)?

- **A.** PPL = e^L
- **B.** PPL = 1/L
- **C.** PPL = log(L)
- **D.** PPL = L^2

## Câu 2 (Tự luận)

Gradient accumulation là gì và vì sao quan trọng với GPU 8GB?

## Câu 3 (Trắc nghiệm)

Lịch learning rate điển hình khi pretrain LLM là gì?

- **A.** Warmup tuyến tính tăng dần → rồi cosine decay giảm dần
- **B.** Giữ LR cố định suốt
- **C.** Giảm rồi tăng (chữ V)
- **D.** Tăng dần đều tới cuối

## Câu 4 (Tự luận)

[Nâng cao] Vì sao các repo pretraining hiện đại (vd. nanoGPT config mặc định) đặt dropout = 0?

## Câu 5 (Trắc nghiệm)

[Nâng cao] Vì sao 'bits-per-byte' (bpb) tốt hơn perplexity khi so sánh các model có tokenizer khác nhau?

- **A.** bpb không cần dữ liệu validation
- **B.** bpb chuẩn hoá loss về mức byte nên không phụ thuộc vocab/tokenizer → so sánh chéo được
- **C.** bpb chạy nhanh hơn
- **D.** bpb luôn nhỏ hơn perplexity

## Câu 6 (Trắc nghiệm)

[Nâng cao] Optimizer Muon (nanochat) áp dụng cho loại tham số nào?

- **A.** Chỉ bias
- **B.** Chỉ embedding
- **C.** Mọi tham số, thay hẳn AdamW
- **D.** Các ma trận trọng số 2D (orthogonalize update bằng Newton-Schulz); embedding/head vẫn dùng AdamW

## Câu 7 (Trắc nghiệm)

Mixed precision (bf16) lợi gì khi train?

- **A.** Giảm VRAM và tăng tốc tính toán với mất chất lượng không đáng kể
- **B.** Loại bỏ nhu cầu gradient
- **C.** Làm loss luôn giảm
- **D.** Tăng độ chính xác số học tuyệt đối

## Câu 8 (Tự luận)

[Nâng cao] DistributedDataParallel (DDP) hoạt động thế nào?

## Câu 9 (Trắc nghiệm)

Vì sao Jurafsky và Martin (SLP3 mục 3.3) không dùng xác suất thô của tập test để đánh giá language model mà dùng perplexity?

- **A.** Vì xác suất của tập test giảm khi văn bản dài hơn, nên cần một số đo tính trên mỗi token, chuẩn hóa theo độ dài, để so được giữa các văn bản khác độ dài
- **B.** Vì xác suất thô chỉ định nghĩa được cho n-gram, không cho LLM
- **C.** Vì perplexity tính nhanh hơn xác suất
- **D.** Vì xác suất thô luôn bằng 1 với model đủ lớn

## Câu 10 (Trắc nghiệm)

SLP3 mục 3.3.1 xét language model B trên vocabulary 3 màu với P(red) = 0.8, P(green) = 0.1, P(blue) = 0.1 và tập test T = "red red red red blue". Perplexity của B trên T bằng bao nhiêu, và so với model A phân bố đều thì sao?

- **A.** Bằng 3, giống model A, vì perplexity chỉ phụ thuộc branching factor của ngôn ngữ và vocabulary vẫn có đúng 3 màu.
- **B.** Bằng 0.527, thấp hơn 3 của model A, vì perplexity là căn bậc năm của xác suất tập test theo model.
- **C.** Bằng 5, cao hơn 3 của model A, vì tập test có 5 token và mỗi token đóng góp một đơn vị vào perplexity.
- **D.** Bằng 1.89, thấp hơn 3 của model A, vì P_B(T) = 0.8^4 × 0.1 = 0.04096 và perplexity = 0.04096^(-1/5) = 0.527^(-1).

## Câu 11 (Trắc nghiệm)

SLP3 mục 7.7 nói một cửa sổ ngữ cảnh N token cho N ví dụ huấn luyện chỉ từ một lần forward. Điều gì làm được điều đó?

- **A.** Vì loss chỉ được tính ở token cuối cùng của cửa sổ nhưng được nhân với N để bù cho các vị trí còn lại chưa được chấm điểm trong lần forward đó.
- **B.** Vì đích w_{t+1} đã biết trước ở mọi vị trí và causal mask không cho mỗi vị trí attend tới đích của chính nó, nên N vị trí được chấm điểm cùng lúc.
- **C.** Vì mỗi vị trí được đưa qua model N lần với ngữ cảnh dài dần, rồi gradient của N lần đó được cộng dồn trước khi cập nhật.
- **D.** Vì ma trận embedding E được cập nhật N lần trong một bước tối ưu, mỗi lần cho một token trong cửa sổ ngữ cảnh, nên tương đương N ví dụ.

## Câu 12 (Trắc nghiệm)

FoLLM (mục 2.2.4) viết scaling law Chinchilla của Hoffmann et al. (2022) dưới dạng L(N, D) = 406.4/N^0.34 + 410.7/D^0.28 + 1.69. Khi N và D cùng tiến ra vô cùng, loss tiến về đâu và số hạng đó có ý nghĩa gì?

- **A.** Về 406.4 + 410.7 = 817.1, vì các mẫu số N^0.34 và D^0.28 tiến về 1 khi N và D đủ lớn so với các hệ số.
- **B.** Về 1.69, số hạng irreducible error: phần loss vẫn còn dù tăng tham số và dữ liệu vô hạn, do các yếu tố không mô hình hóa được.
- **C.** Về 0, vì cả hai số hạng lũy thừa đều triệt tiêu và model với đủ tham số và dữ liệu sẽ khớp hoàn hảo phân phối ngôn ngữ.
- **D.** Về 0.34 + 0.28 = 0.62, tổng hai số mũ, biểu thị độ dốc chung của power law theo cả số tham số và lượng dữ liệu.

## Câu 13 (Trắc nghiệm)

Fleuret (mục 3.7) nói test loss cải thiện theo lượng dữ liệu theo scaling law với một điều kiện đi kèm, và nêu yếu tố cho phép huấn luyện trên dataset lớn hơn bộ nhớ thiết bị nhiều bậc. Điều kiện và yếu tố đó là gì?

- **A.** Learning rate phải giảm tương ứng với lượng dữ liệu; mixed precision cho phép nạp toàn bộ dataset vào bộ nhớ GPU dưới dạng số 16 bit.
- **B.** Kích cỡ model phải tăng tương ứng; stochastic gradient descent chỉ cần một phần dữ liệu mỗi lần nên dataset có thể lớn hơn bộ nhớ thiết bị nhiều bậc.
- **C.** Số epoch phải tăng tương ứng với lượng dữ liệu; gradient accumulation cho phép batch hiệu dụng lớn hơn bộ nhớ của thiết bị.
- **D.** Độ dài ngữ cảnh phải tăng tương ứng với lượng dữ liệu; KV cache cho phép xử lý các chuỗi dài hơn nhiều so với bộ nhớ của thiết bị.

## Câu 14 (Trắc nghiệm)

UDL mục 9.2.2 suy ra hàm mất mát hiệu chỉnh L̃_SGD của stochastic gradient descent. So với gradient descent thường, SGD thêm một số hạng regularization ẩn tương ứng với đại lượng nào?

- **A.** Phương sai của gradient các loss theo batch, nên SGD ưu tiên vùng mà mọi batch đồng ý về độ dốc, nơi toàn bộ dữ liệu đều khớp tốt.
- **B.** Entropy của phân phối đầu ra model, khiến model tránh các dự đoán quá tự tin và nhờ đó tổng quát hóa tốt hơn.
- **C.** Bình phương chuẩn gradient của loss trên toàn bộ dữ liệu, khiến quỹ đạo bị đẩy khỏi những vùng mà mặt loss dốc.
- **D.** Chuẩn L2 của vector tham số, tương đương weight decay với hệ số α/4, khiến các trọng số nhỏ dần trong quá trình huấn luyện.

## Câu 15 (Trắc nghiệm)

SLP3 mục 3.3 nêu điều kiện để perplexity của hai language model có thể so sánh được và cảnh báo về tập test. Điều kiện đó là gì?

- **A.** Hai model phải dùng vocabulary giống hệt nhau, và model không được xây dựng với bất kỳ tri thức nào về tập test, nếu không perplexity thấp giả tạo.
- **B.** Hai model phải đạt cùng loss trên tập train trước khi đo, và tập test phải được tokenize lại theo tokenizer của model tốt hơn.
- **C.** Hai model phải có cùng số tham số và cùng độ dài ngữ cảnh, và tập test phải được lấy từ cùng nguồn văn bản với tập train của cả hai.
- **D.** Hai model phải được train cùng số epoch trên cùng phần cứng, và tập test phải có ít nhất một triệu token để ước lượng ổn định.

## Câu 16 (Tự luận)

SLP3 mục 3.7 định nghĩa cross-entropy H(p, m) của model m trên phân phối thật p (công thức 3.39) rồi rút gọn nhờ định lý Shannon-McMillan-Breiman. Vì sao có thể ước lượng cross-entropy từ một chuỗi test đủ dài thay vì tổng trên mọi chuỗi, và bất đẳng thức nào cho phép dùng H(p, m) để so hai model?

## Câu 17 (Tự luận)

FoLLM mục 2.2.1 liệt kê các vấn đề khi chuẩn bị dữ liệu pretraining. Hãy nêu ít nhất ba vấn đề, dẫn con số hay ví dụ cụ thể mà Xiao và Zhu đưa ra cho vấn đề chất lượng và vấn đề đa dạng, và liên hệ với việc bạn chọn corpus công khai cho lần pretrain 124M.

## Câu 18 (Tự luận)

SLP3 mục 7.7 gọi cách huấn luyện language model là self-supervised và mô tả teacher forcing. Hãy giải thích hai khái niệm này và chỉ ra chúng tương ứng với dòng nào trong training loop của bạn (cách tạo inputs và targets từ một chuỗi token).

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Vì sao nanochat báo val_bpb (bits per byte) trên leaderboard thay cho loss thô, theo lập luận của SLP3 về perplexity?

- **A.** Vì bpb là metric của MMLU
- **B.** Vì GPU tính byte nhanh hơn token
- **C.** Vì perplexity và loss tính trên token nên phụ thuộc tokenizer; chia lượng thông tin cho số byte thay cho số token cho phép so sánh chéo các model có vocab khác nhau
- **D.** Vì bpb luôn nhỏ hơn loss

## Nâng cao 2 (Tự luận)

Xiao và Zhu mô tả đường cong scaling law có ba pha theo lượng dữ liệu (Hestness et al. 2017). Ba pha đó là gì và lần pretrain 124M của bạn nằm ở đâu?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
