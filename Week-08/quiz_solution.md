# Tuần 8, Đáp án & Giải thích: Pretraining: training loop + 1 lần chạy GPT-2 thật

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Quan hệ giữa cross-entropy loss L và perplexity (PPL)?

- **A.** PPL = e^L (đáp án đúng)
- **B.** PPL = 1/L
- **C.** PPL = log(L)
- **D.** PPL = L^2

**Đáp án: A**

**Giải thích:** PPL = e^L. Trực giác: perplexity ~ số lựa chọn 'trung bình' model còn phân vân; thấp hơn = dự đoán chắc hơn.

## Câu 2 (Tự luận)

Gradient accumulation là gì và vì sao quan trọng với GPU 8GB?

**Trả lời mẫu:** Thay vì cập nhật trọng số sau mỗi micro-batch nhỏ, ta cộng dồn gradient qua N micro-batch rồi mới step một lần → mô phỏng một 'effective batch' lớn (micro_batch × N) mà không cần chứa toàn bộ batch lớn trong VRAM. Với 3070 Ti 8GB chỉ vừa batch 1-2, gradient accumulation là cách đạt effective batch ~0.5M token/update kiểu Karpathy mà vẫn không OOM.

**Giải thích:** Xem cách nanoGPT/train.py implement gradient_accumulation_steps.

## Câu 3 (Trắc nghiệm)

Lịch learning rate điển hình khi pretrain LLM là gì?

- **A.** Warmup tuyến tính tăng dần → rồi cosine decay giảm dần (đáp án đúng)
- **B.** Giữ LR cố định suốt
- **C.** Giảm rồi tăng (chữ V)
- **D.** Tăng dần đều tới cuối

**Đáp án: A**

**Giải thích:** Warmup tránh sốc gradient lúc đầu (trọng số ngẫu nhiên); cosine decay giúp hội tụ mượt về cuối.

## Câu 4 (Tự luận)

[Nâng cao] Vì sao các repo pretraining hiện đại (vd. nanoGPT config mặc định) đặt dropout = 0?

**Trả lời mẫu:** Dropout là regularizer chống overfit, hữu ích khi fine-tune trên data nhỏ; nhưng pretraining chạy ~1 epoch trên lượng data khổng lồ thì gần như không overfit, nên dropout chỉ làm 'nhiễu' quá trình học. Vì vậy pretraining hiện đại thường bỏ dropout (nanoGPT để dropout=0.0 cho pretrain, gợi ý 0.1+ khi fine-tune).

**Giải thích:** Bài học: kỹ thuật 'tốt' phụ thuộc bối cảnh (data lớn 1-epoch vs data nhỏ nhiều epoch).

## Câu 5 (Trắc nghiệm)

[Nâng cao] Vì sao 'bits-per-byte' (bpb) tốt hơn perplexity khi so sánh các model có tokenizer khác nhau?

- **A.** bpb không cần dữ liệu validation
- **B.** bpb chuẩn hoá loss về mức byte nên không phụ thuộc vocab/tokenizer → so sánh chéo được (đáp án đúng)
- **C.** bpb chạy nhanh hơn
- **D.** bpb luôn nhỏ hơn perplexity

**Đáp án: B**

**Giải thích:** Perplexity phụ thuộc cách chia token; bpb quy về byte → công bằng giữa các tokenizer. nanochat dùng val_bpb làm chỉ số chính.

## Câu 6 (Trắc nghiệm)

[Nâng cao] Optimizer Muon (nanochat) áp dụng cho loại tham số nào?

- **A.** Chỉ bias
- **B.** Chỉ embedding
- **C.** Mọi tham số, thay hẳn AdamW
- **D.** Các ma trận trọng số 2D (orthogonalize update bằng Newton-Schulz); embedding/head vẫn dùng AdamW (đáp án đúng)

**Đáp án: D**

**Giải thích:** Muon orthogonalize bản cập nhật cho ma trận 2D → hội tụ pretraining nhanh hơn; là một yếu tố giúp nanochat 'speedrun' GPT-2.

## Câu 7 (Trắc nghiệm)

Mixed precision (bf16) lợi gì khi train?

- **A.** Giảm VRAM và tăng tốc tính toán với mất chất lượng không đáng kể (đáp án đúng)
- **B.** Loại bỏ nhu cầu gradient
- **C.** Làm loss luôn giảm
- **D.** Tăng độ chính xác số học tuyệt đối

**Đáp án: A**

**Giải thích:** bf16 dùng nửa bộ nhớ, tận dụng tensor core; bf16 có dải mũ rộng nên ổn định hơn fp16 (fp16 cần GradScaler).

## Câu 8 (Tự luận)

[Nâng cao] DistributedDataParallel (DDP) hoạt động thế nào?

**Trả lời mẫu:** DDP nhân bản toàn bộ model lên mỗi GPU; mỗi GPU xử lý một phần khác nhau của batch (data parallel), tính gradient cục bộ, rồi all-reduce (cộng và chia trung bình) gradient qua tất cả GPU trước khi mỗi bản sao cùng step. Kết quả tương đương train với batch lớn hơn N lần. Đây là cách nanoGPT/llm.c train trên node 8×A100 qua torchrun.

**Giải thích:** DDP là mức song song đầu tiên cần biết; TP/PP/FSDP cho model không vừa 1 GPU.

## Câu 9 (Trắc nghiệm)

Vì sao Jurafsky và Martin (SLP3 mục 3.3) không dùng xác suất thô của tập test để đánh giá language model mà dùng perplexity?

- **A.** Vì xác suất của tập test giảm khi văn bản dài hơn, nên cần một số đo tính trên mỗi token, chuẩn hóa theo độ dài, để so được giữa các văn bản khác độ dài (đáp án đúng)
- **B.** Vì xác suất thô chỉ định nghĩa được cho n-gram, không cho LLM
- **C.** Vì perplexity tính nhanh hơn xác suất
- **D.** Vì xác suất thô luôn bằng 1 với model đủ lớn

**Đáp án: A**

**Giải thích:** SLP3 trang 76: 'the probability of a test set gets smaller the longer the text. It's useful to have a metric that is per-word, normalized by length'. Perplexity là exp của cross-entropy trung bình trên token, đúng công thức ở mục lý thuyết của tuần.

## Câu 10 (Trắc nghiệm)

SLP3 mục 3.3.1 xét language model B trên vocabulary 3 màu với P(red) = 0.8, P(green) = 0.1, P(blue) = 0.1 và tập test T = "red red red red blue". Perplexity của B trên T bằng bao nhiêu, và so với model A phân bố đều thì sao?

- **A.** Bằng 3, giống model A, vì perplexity chỉ phụ thuộc branching factor của ngôn ngữ và vocabulary vẫn có đúng 3 màu.
- **B.** Bằng 0.527, thấp hơn 3 của model A, vì perplexity là căn bậc năm của xác suất tập test theo model.
- **C.** Bằng 5, cao hơn 3 của model A, vì tập test có 5 token và mỗi token đóng góp một đơn vị vào perplexity.
- **D.** Bằng 1.89, thấp hơn 3 của model A, vì P_B(T) = 0.8^4 × 0.1 = 0.04096 và perplexity = 0.04096^(-1/5) = 0.527^(-1). (đáp án đúng)

**Đáp án: D**

**Giải thích:** SLP3 tính perplexity_A(T) = (1/3)^(-1) = 3 (công thức 3.19) và perplexity_B(T) = P_B(red red red red blue)^(-1/5) = 0.04096^(-1/5) = 0.527^(-1) = 1.89 (công thức 3.21): tuy branching factor vẫn là 3, "the perplexity or weighted branching factor is smaller" vì red rất dễ đoán. Bài này cho thấy perplexity là số lựa chọn hiệu dụng có trọng số, chứ không phải kích cỡ vocabulary. (SLP3 mục 3.3.1, tr. 78)

## Câu 11 (Trắc nghiệm)

SLP3 mục 7.7 nói một cửa sổ ngữ cảnh N token cho N ví dụ huấn luyện chỉ từ một lần forward. Điều gì làm được điều đó?

- **A.** Vì loss chỉ được tính ở token cuối cùng của cửa sổ nhưng được nhân với N để bù cho các vị trí còn lại chưa được chấm điểm trong lần forward đó.
- **B.** Vì đích w_{t+1} đã biết trước ở mọi vị trí và causal mask không cho mỗi vị trí attend tới đích của chính nó, nên N vị trí được chấm điểm cùng lúc. (đáp án đúng)
- **C.** Vì mỗi vị trí được đưa qua model N lần với ngữ cảnh dài dần, rồi gradient của N lần đó được cộng dồn trước khi cập nhật.
- **D.** Vì ma trận embedding E được cập nhật N lần trong một bước tối ưu, mỗi lần cho một token trong cửa sổ ngữ cảnh, nên tương đương N ví dụ.

**Đáp án: B**

**Giải thích:** SLP3: "Parallelism is possible because we know in advance the desired output (w_{t+1}), and the causal mask prevents each position from attending to its own target, allowing the output for each token to be computed separately. This means that all N positions in the context window can be scored at once against their true next tokens, giving N training examples from one pass through the network." Loss của batch là trung bình -log ŷ_t[w_{t+1}] trên T vị trí (công thức 7.55). Đó là lý do target trong training loop của bạn là chuỗi dịch một token, không phải một token cuối. (SLP3 mục 7.7, tr. 202)

## Câu 12 (Trắc nghiệm)

FoLLM (mục 2.2.4) viết scaling law Chinchilla của Hoffmann et al. (2022) dưới dạng L(N, D) = 406.4/N^0.34 + 410.7/D^0.28 + 1.69. Khi N và D cùng tiến ra vô cùng, loss tiến về đâu và số hạng đó có ý nghĩa gì?

- **A.** Về 406.4 + 410.7 = 817.1, vì các mẫu số N^0.34 và D^0.28 tiến về 1 khi N và D đủ lớn so với các hệ số.
- **B.** Về 1.69, số hạng irreducible error: phần loss vẫn còn dù tăng tham số và dữ liệu vô hạn, do các yếu tố không mô hình hóa được. (đáp án đúng)
- **C.** Về 0, vì cả hai số hạng lũy thừa đều triệt tiêu và model với đủ tham số và dữ liệu sẽ khớp hoàn hảo phân phối ngôn ngữ.
- **D.** Về 0.34 + 0.28 = 0.62, tổng hai số mũ, biểu thị độ dốc chung của power law theo cả số tham số và lượng dữ liệu.

**Đáp án: B**

**Giải thích:** FoLLM viết dạng tổng quát L(x) = a x^b + ε_∞, "where ε_∞ is the irreducible error that accounts for the error due to unknown variables, which is present even as x → ∞" (công thức 2.37), và ghi rõ trong công thức 2.39 hai số hạng đầu là model scaling và dataset scaling, còn 1.69 là irreducible error. Khi so loss pretrain 124M của bạn với các con số này, hãy nhớ loss có sàn khác 0. (FoLLM mục 2.2.4, tr. 65)

## Câu 13 (Trắc nghiệm)

Fleuret (mục 3.7) nói test loss cải thiện theo lượng dữ liệu theo scaling law với một điều kiện đi kèm, và nêu yếu tố cho phép huấn luyện trên dataset lớn hơn bộ nhớ thiết bị nhiều bậc. Điều kiện và yếu tố đó là gì?

- **A.** Learning rate phải giảm tương ứng với lượng dữ liệu; mixed precision cho phép nạp toàn bộ dataset vào bộ nhớ GPU dưới dạng số 16 bit.
- **B.** Kích cỡ model phải tăng tương ứng; stochastic gradient descent chỉ cần một phần dữ liệu mỗi lần nên dataset có thể lớn hơn bộ nhớ thiết bị nhiều bậc. (đáp án đúng)
- **C.** Số epoch phải tăng tương ứng với lượng dữ liệu; gradient accumulation cho phép batch hiệu dụng lớn hơn bộ nhớ của thiết bị.
- **D.** Độ dài ngữ cảnh phải tăng tương ứng với lượng dữ liệu; KV cache cho phép xử lý các chuỗi dài hơn nhiều so với bộ nhớ của thiết bị.

**Đáp án: B**

**Giải thích:** Fleuret: hiệu năng "improves with the amount of data according to remarkable scaling laws, as long as the model size increases correspondingly [Kaplan et al., 2020]" (Figure 3.6). Việc khai thác được scaling law trong vùng hàng tỷ mẫu là nhờ cấu trúc model có thể mở rộng và "stochastic gradient descent, which requires only a fraction of the data at a time and can operate with datasets whose size is orders of magnitude greater than that of the computing device's memory." (Fleuret mục 3.7, tr. 52)

## Câu 14 (Trắc nghiệm)

UDL mục 9.2.2 suy ra hàm mất mát hiệu chỉnh L̃_SGD của stochastic gradient descent. So với gradient descent thường, SGD thêm một số hạng regularization ẩn tương ứng với đại lượng nào?

- **A.** Phương sai của gradient các loss theo batch, nên SGD ưu tiên vùng mà mọi batch đồng ý về độ dốc, nơi toàn bộ dữ liệu đều khớp tốt. (đáp án đúng)
- **B.** Entropy của phân phối đầu ra model, khiến model tránh các dự đoán quá tự tin và nhờ đó tổng quát hóa tốt hơn.
- **C.** Bình phương chuẩn gradient của loss trên toàn bộ dữ liệu, khiến quỹ đạo bị đẩy khỏi những vùng mà mặt loss dốc.
- **D.** Chuẩn L2 của vector tham số, tương đương weight decay với hệ số α/4, khiến các trọng số nhỏ dần trong quá trình huấn luyện.

**Đáp án: A**

**Giải thích:** Prince viết công thức 9.9 "reveals an extra regularization term, which corresponds to the variance of the gradients of the batch losses L_b. In other words, SGD implicitly favors places where the gradients are stable (where all the batches agree on the slope)." Số hạng bình phương chuẩn gradient (α/4)‖∂L/∂ϕ‖² là phần đã có sẵn ở gradient descent thường (công thức 9.8), không phải phần thêm của SGD. Đây là một lời giải thích vì sao batch nhỏ thường tổng quát hóa tốt hơn (Figure 9.5b). (UDL mục 9.2.2, tr. 143)

## Câu 15 (Trắc nghiệm)

SLP3 mục 3.3 nêu điều kiện để perplexity của hai language model có thể so sánh được và cảnh báo về tập test. Điều kiện đó là gì?

- **A.** Hai model phải dùng vocabulary giống hệt nhau, và model không được xây dựng với bất kỳ tri thức nào về tập test, nếu không perplexity thấp giả tạo. (đáp án đúng)
- **B.** Hai model phải đạt cùng loss trên tập train trước khi đo, và tập test phải được tokenize lại theo tokenizer của model tốt hơn.
- **C.** Hai model phải có cùng số tham số và cùng độ dài ngữ cảnh, và tập test phải được lấy từ cùng nguồn văn bản với tập train của cả hai.
- **D.** Hai model phải được train cùng số epoch trên cùng phần cứng, và tập test phải có ít nhất một triệu token để ước lượng ổn định.

**Đáp án: A**

**Giải thích:** SLP3: "in computing perplexities, the language model must be constructed without any knowledge of the test set, or else the perplexity will be artificially low. And the perplexity of two language models is only comparable if they use identical vocabularies." Ví dụ trong cùng mục: unigram, bigram, trigram train trên 38 triệu từ WSJ cho perplexity 962, 170, 109 trên cùng tập test 1.5 triệu từ. Khi so pretrain 124M của bạn với một baseline, hãy kiểm tra hai điều kiện này trước. (SLP3 mục 3.3, tr. 77)

## Câu 16 (Tự luận)

SLP3 mục 3.7 định nghĩa cross-entropy H(p, m) của model m trên phân phối thật p (công thức 3.39) rồi rút gọn nhờ định lý Shannon-McMillan-Breiman. Vì sao có thể ước lượng cross-entropy từ một chuỗi test đủ dài thay vì tổng trên mọi chuỗi, và bất đẳng thức nào cho phép dùng H(p, m) để so hai model?

**Trả lời mẫu:** Định nghĩa gốc lấy kỳ vọng theo p của -log m trên mọi chuỗi độ dài n rồi cho n ra vô cùng. Với quá trình dừng và ergodic, định lý Shannon-McMillan-Breiman cho H(p, m) = lim -(1/n) log m(w_1 ... w_n), tức chỉ cần một chuỗi đủ dài: chuỗi dài chứa nhiều chuỗi con lặp lại theo đúng xác suất của chúng. Vì vậy loss trung bình trên tập test dài chính là ước lượng cross-entropy. Bất đẳng thức H(p) ≤ H(p, m) nói cross-entropy luôn là cận trên của entropy thật; model càng chính xác thì H(p, m) càng gần H(p), nên model có cross-entropy (và perplexity) thấp hơn là model gần p hơn. Giả định dừng không đúng hoàn toàn với ngôn ngữ tự nhiên nên đây chỉ là xấp xỉ.

**Giải thích:** SLP3: "following the Shannon-McMillan-Breiman theorem, for a stationary ergodic process: H(p, m) = lim −(1/n) log m(w_1 w_2 ... w_n)" (công thức 3.40), nên "we can estimate the cross-entropy of a model m on some distribution p by taking a single sequence that is long enough"; "the cross-entropy H(p, m) is an upper bound on the entropy H(p)" (3.41) và "the difference between H(p, m) and H(p) is a measure of how accurate a model is". Cùng mục ghi ngôn ngữ tự nhiên không dừng nên các model chỉ xấp xỉ. (SLP3 mục 3.7, tr. 87)

## Câu 17 (Tự luận)

FoLLM mục 2.2.1 liệt kê các vấn đề khi chuẩn bị dữ liệu pretraining. Hãy nêu ít nhất ba vấn đề, dẫn con số hay ví dụ cụ thể mà Xiao và Zhu đưa ra cho vấn đề chất lượng và vấn đề đa dạng, và liên hệ với việc bạn chọn corpus công khai cho lần pretrain 124M.

**Trả lời mẫu:** Bốn vấn đề: chất lượng dữ liệu, đa dạng dữ liệu, thiên lệch trong dữ liệu, và quyền riêng tư. Về chất lượng: dữ liệu web thô chứa lỗi và nội dung không phù hợp, train trên dữ liệu chưa lọc là có hại (Raffel et al. 2020); Penedo et al. (2023) cho thấy sau các bước xử lý có thể loại bỏ 90% dữ liệu web đã thu thập. Về đa dạng: đưa mã nguồn vào dữ liệu train không chỉ cải thiện khả năng lập trình mà còn cải thiện suy luận cho bài toán phức tạp; đa dạng ngôn ngữ giúp một model xử lý nhiều ngôn ngữ nhưng chất lượng với ngôn ngữ ít tài nguyên phụ thuộc lượng và chất dữ liệu của ngôn ngữ đó. Với lần pretrain 124M, điều này nghĩa là ưu tiên corpus mở đã được lọc và trộn nhiều nguồn, kiểm tra license, và loại dữ liệu cá nhân trước khi train.

**Giải thích:** FoLLM: "A first issue is the quality of data ... Researchers have found that training LLMs on unfiltered data is harmful [Raffel et al., 2020] ... Penedo et al. [2023] show that by adopting a number of data processing techniques, 90% of their web-scraped data can be removed for LLM training" (tr. 56-57); "A second issue is the diversity of data ... incorporating programming code into training data has been found to be beneficial ... also in improving reasoning for complex problems"; "A third issue is the bias in training data"; "Another issue with collecting large-scale data is the privacy concern." (FoLLM mục 2.2.1, tr. 57)

## Câu 18 (Tự luận)

SLP3 mục 7.7 gọi cách huấn luyện language model là self-supervised và mô tả teacher forcing. Hãy giải thích hai khái niệm này và chỉ ra chúng tương ứng với dòng nào trong training loop của bạn (cách tạo inputs và targets từ một chuỗi token).

**Trả lời mẫu:** Self-supervised: không cần nhãn vàng do người gán; chuỗi từ tự nhiên là giám sát của chính nó, tại mỗi vị trí t model được yêu cầu dự đoán token kế tiếp và loss là -log ŷ_t[w_{t+1}]. Teacher forcing: khi chuyển sang vị trí t+1, ta bỏ qua token model vừa dự đoán và luôn đưa chuỗi đúng w_{1:t+1} vào để dự đoán w_{t+2}, tức model luôn nhận lịch sử đúng thay vì dự đoán của chính nó. Trong training loop, điều này tương ứng với inputs = tokens[:-1] và targets = tokens[1:] (hay x = buf[:-1], y = buf[1:]) rồi cross_entropy(logits, targets): inputs luôn là dữ liệu thật, không phải đầu ra được sinh ra.

**Giải thích:** SLP3: "We call such a model self-supervised because we don't have to add any special gold labels to the data; the natural sequence of words is its own supervision!"; loss tại vị trí t là L_CE = −log ŷ_t[w_{t+1}] (công thức 7.54); "we ignore what the model predicted for the next word and instead use the correct sequence of tokens w_{1:t+1} to get the model to estimate the probability of token w_{t+2}. This idea that we always give the model the correct history sequence to predict the next word ... is called teacher forcing." (SLP3 mục 7.7, tr. 201)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Vì sao nanochat báo val_bpb (bits per byte) trên leaderboard thay cho loss thô, theo lập luận của SLP3 về perplexity?

- **A.** Vì bpb là metric của MMLU
- **B.** Vì GPU tính byte nhanh hơn token
- **C.** Vì perplexity và loss tính trên token nên phụ thuộc tokenizer; chia lượng thông tin cho số byte thay cho số token cho phép so sánh chéo các model có vocab khác nhau (đáp án đúng)
- **D.** Vì bpb luôn nhỏ hơn loss

**Đáp án: C**

**Giải thích:** SLP3 mục 3.3 và 3.7 nối perplexity với cross-entropy và entropy tính bằng bit; leaderboard nanochat đọc ngày 2026-09-04 có cột val_bpb và CORE, GPT-2 gốc CORE 0.2565.

## Nâng cao 2 (Tự luận)

Xiao và Zhu mô tả đường cong scaling law có ba pha theo lượng dữ liệu (Hestness et al. 2017). Ba pha đó là gì và lần pretrain 124M của bạn nằm ở đâu?

**Trả lời mẫu:** Khi dữ liệu còn ít, hiệu năng cải thiện chậm; sau đó vào pha cải thiện nhanh theo dạng power-law; cuối cùng chậm lại khi thêm dữ liệu không còn tăng nhiều (FoLLM mục 2.2.4, trang 63). Lần chạy 124M trên một mẫu FineWeb-Edu nằm ở quy mô rất nhỏ so với các model trong paper; mục tiêu của nó là hiểu cơ chế và đọc loss curve, không phải đuổi số.

**Giải thích:** Fleuret mục 3.7 (trang 52) nói cùng ý và dẫn Kaplan et al. 2020; hai paper Scaling Laws và Chinchilla trong kệ paper là nguồn gốc con số.
