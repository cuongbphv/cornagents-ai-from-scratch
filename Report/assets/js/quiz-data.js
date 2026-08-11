/* Sinh tự động bởi scripts/generate_quiz.py — KHÔNG sửa tay.
   Nguồn: scripts/quiz_bank.json */
window.QUIZ_DATA = {
  "meta": {
    "title": "Quiz Bank — LLM From Scratch",
    "language": "vi",
    "version": "2.0",
    "note": "Nguồn chân lý cho quiz từng tuần. Chạy scripts/generate_quiz.py để sinh Week-XX/quiz.md, Week-XX/quiz_solution.md và Report/assets/js/quiz-data.js. type=mcq dùng choices+answer(index từ 0); type=open dùng answer(văn bản mẫu). Toán viết dạng plain-text cho dễ bảo trì."
  },
  "weeks": [
    {
      "week": 1,
      "title": "Toán nền tảng + PyTorch",
      "questions": [
        {
          "id": "w1q1",
          "type": "mcq",
          "q": "Một nn.Linear(in, out) thực chất tính gì?",
          "choices": [
            "y = x @ W + b với W có shape (in, out)",
            "y = x @ W^T + b với W lưu shape (out, in)",
            "y = W @ x luôn luôn, không có bias",
            "y = softmax(x @ W)"
          ],
          "answer": 1,
          "explain": "PyTorch lưu weight shape (out, in), nên forward là y = x @ W^T + b. Đây là khối tuyến tính cơ bản lặp lại khắp transformer."
        },
        {
          "id": "w1q2",
          "type": "mcq",
          "q": "Mục đích chính của softmax là gì?",
          "choices": [
            "Chuẩn hoá vector về độ dài 1",
            "Biến một vector logits thành phân phối xác suất (mọi phần tử dương, tổng = 1)",
            "Loại bỏ giá trị âm như ReLU",
            "Tính gradient của cross-entropy"
          ],
          "answer": 1,
          "explain": "softmax(z)_i = e^{z_i} / sum_j e^{z_j}: mũ hoá làm mọi giá trị dương, chia tổng làm chúng cộng lại bằng 1 → phân phối xác suất trên các lớp/token."
        },
        {
          "id": "w1q3",
          "type": "open",
          "q": "Chain rule liên quan thế nào tới backpropagation?",
          "answer": "Backprop = áp dụng chain rule lan ngược qua đồ thị tính toán. Đạo hàm của loss theo một tham số ở lớp sâu = tích các đạo hàm cục bộ dọc đường đi: dL/dw = dL/dg · dg/dw. Mỗi lớp chỉ cần biết đạo hàm cục bộ của nó và nhận gradient từ lớp sau, nhân vào, rồi truyền tiếp về trước.",
          "explain": "Đây là toàn bộ ý tưởng của autograd: lưu đồ thị forward, rồi nhân dồn đạo hàm cục bộ theo chiều ngược lại."
        },
        {
          "id": "w1q4",
          "type": "mcq",
          "q": "Cross-entropy loss L_CE = -sum_i y_i log(y_hat_i) đo điều gì?",
          "choices": [
            "Khoảng cách Euclid giữa dự đoán và nhãn",
            "Độ 'bất ngờ' của phân phối dự đoán so với nhãn thật — phạt nặng khi gán xác suất thấp cho lớp đúng",
            "Số token dự đoán sai",
            "Phương sai của logits"
          ],
          "answer": 1,
          "explain": "Với nhãn one-hot, L_CE = -log(xác suất gán cho lớp đúng). Gán xác suất gần 1 cho lớp đúng → loss ~0; gần 0 → loss rất lớn."
        },
        {
          "id": "w1q5",
          "type": "mcq",
          "q": "Cộng tensor shape (B, 1, D) với (1, T, D) bằng broadcasting cho ra shape nào?",
          "choices": [
            "(B, T, D)",
            "(B, 1, D)",
            "Lỗi — không broadcast được",
            "(B, T, 1)"
          ],
          "answer": 0,
          "explain": "Broadcasting căn phải các chiều; chiều bằng 1 được 'kéo dài'. (B,1,D) và (1,T,D) → (B,T,D). Hiểu broadcasting là chìa khoá đọc code attention."
        },
        {
          "id": "w1q6",
          "type": "open",
          "q": "torch.no_grad() và requires_grad khác nhau thế nào, dùng khi nào?",
          "answer": "requires_grad=True đánh dấu một tensor cần theo dõi để tính gradient (tham số train được). torch.no_grad() là context tắt việc xây đồ thị autograd cho mọi phép tính bên trong — dùng khi inference/đánh giá hoặc cập nhật tham số thủ công, để tiết kiệm bộ nhớ và tránh tính gradient thừa.",
          "explain": "Quên no_grad() khi eval/generate là lỗi VRAM phổ biến, nhất là trên card 8GB."
        },
        {
          "id": "w1q7",
          "type": "mcq",
          "q": "Dot product giữa hai vector đo điều gì (ý nghĩa cho attention)?",
          "choices": [
            "Luôn là khoảng cách giữa hai điểm",
            "Độ 'cùng hướng' / tương đồng — lớn khi hai vector cùng hướng",
            "Góc tuyệt đối tính bằng độ",
            "Tổng bình phương các phần tử"
          ],
          "answer": 1,
          "explain": "a·b = |a||b|cosθ. Trong attention, query·key chính là điểm tương đồng dùng để quyết định token nào 'chú ý' tới token nào."
        }
      ]
    },
    {
      "week": 2,
      "title": "Backprop từ đầu + mental model Transformer",
      "questions": [
        {
          "id": "w2q1",
          "type": "open",
          "q": "Trong micrograd, mỗi đối tượng Value lưu những gì và làm gì khi backward()?",
          "answer": "Mỗi Value lưu: data (giá trị forward), grad (đạo hàm của output cuối theo nó, khởi tạo 0), và một hàm _backward() biết cách đẩy gradient về các 'cha' của nó. Forward dựng đồ thị; backward() sắp xếp topo các node, set grad của output = 1, rồi gọi _backward() theo thứ tự ngược để nhân dồn chain rule.",
          "explain": "Đây là lõi của mọi autograd engine (kể cả PyTorch), chỉ khác quy mô."
        },
        {
          "id": "w2q2",
          "type": "mcq",
          "q": "backward() duyệt đồ thị theo thứ tự nào?",
          "choices": [
            "Thứ tự ngẫu nhiên",
            "Thứ tự topo NGƯỢC (từ output về input)",
            "Theo thứ tự khởi tạo biến",
            "Theo độ lớn của grad"
          ],
          "answer": 1,
          "explain": "Phải xử lý một node sau khi đã cộng xong mọi gradient đến từ các node phía sau nó → duyệt topo ngược."
        },
        {
          "id": "w2q3",
          "type": "open",
          "q": "Vì sao self-attention là 'permutation-equivariant' và điều đó buộc ta phải thêm gì?",
          "answer": "Score giữa token i và j chỉ là q_i·k_j, không chứa thông tin vị trí; W_Q, W_K, W_V dùng chung cho mọi vị trí. Nếu hoán vị thứ tự token đầu vào, đầu ra hoán vị y hệt — model không phân biệt 'chó cắn người' với 'người cắn chó'. Vì vậy phải thêm positional encoding (absolute learned ở GPT-2, hoặc RoPE ở model hiện đại) để đưa thông tin thứ tự vào.",
          "explain": "Đây là lý do tồn tại của positional embedding — không có nó, transformer mù thứ tự."
        },
        {
          "id": "w2q4",
          "type": "mcq",
          "q": "Đạo hàm của tanh(x) là gì (hay gặp khi tự code backward)?",
          "choices": [
            "tanh(x)",
            "1 - tanh^2(x)",
            "x(1-x)",
            "e^x / (1+e^x)"
          ],
          "answer": 1,
          "explain": "tanh'(x) = 1 - tanh^2(x). Tự viết local gradient cho tanh/relu/exp là bài tập cốt lõi của micrograd."
        },
        {
          "id": "w2q5",
          "type": "mcq",
          "q": "Khi một biến được dùng ở NHIỀU nhánh của đồ thị, gradient của nó được xử lý thế nào?",
          "choices": [
            "Lấy gradient lớn nhất",
            "Cộng dồn (+=) gradient từ tất cả các nhánh",
            "Ghi đè bằng gradient cuối cùng",
            "Lấy trung bình"
          ],
          "answer": 1,
          "explain": "Theo quy tắc tổng của chain rule, gradient từ các đường khác nhau phải CỘNG dồn. Quên += (dùng =) là bug micrograd kinh điển."
        },
        {
          "id": "w2q6",
          "type": "open",
          "q": "Bigram model trong makemore làm gì, và liên hệ thế nào với một mạng neural 1 lớp?",
          "answer": "Bigram dự đoán ký tự tiếp theo chỉ dựa trên ký tự hiện tại. Bản 'đếm' xây ma trận tần suất (c_i → c_{i+1}) rồi chuẩn hoá thành xác suất. Bản neural tương đương: one-hot ký tự đầu vào @ một ma trận trọng số → logits → softmax; train bằng cross-entropy sẽ hội tụ về cùng phân phối với bản đếm. Đây là cầu nối từ thống kê đếm sang học bằng gradient.",
          "explain": "Karpathy dùng bigram để cho thấy 'neural net' chỉ là cách tổng quát hoá của đếm tần suất."
        }
      ]
    },
    {
      "week": 3,
      "title": "Tokenization, embeddings, attention từ đầu",
      "questions": [
        {
          "id": "w3q1",
          "type": "mcq",
          "q": "Vì sao trong scaled dot-product attention ta chia cho sqrt(d_k)?",
          "choices": [
            "Để tiết kiệm bộ nhớ",
            "Để chuẩn hoá vector về độ dài 1",
            "Để giữ phương sai của score ổn định, tránh softmax bão hoà làm gradient triệt tiêu",
            "Để score luôn dương"
          ],
          "answer": 2,
          "explain": "Dot product của hai vector d_k chiều có phương sai ~d_k; không chia, score quá lớn đẩy softmax về one-hot → gradient ~0, khó học."
        },
        {
          "id": "w3q2",
          "type": "open",
          "q": "Causal mask làm gì và cài đặt thế nào?",
          "answer": "Causal (masked) attention đảm bảo token chỉ 'nhìn' về quá khứ, không thấy token tương lai — bắt buộc cho mô hình tự hồi quy. Cài đặt: đặt phần tam giác TRÊN của ma trận score = -vô cực (hoặc -1e9) TRƯỚC khi softmax; sau softmax các vị trí đó thành ~0, nên token i không attend tới token j>i.",
          "explain": "Nếu để token thấy tương lai, model 'gian lận' lúc train và vô dụng lúc generate."
        },
        {
          "id": "w3q3",
          "type": "mcq",
          "q": "Token embedding và positional embedding được kết hợp thế nào trong GPT-2?",
          "choices": [
            "Nối (concatenate) lại",
            "Cộng vào nhau (cùng chiều d_model)",
            "Nhân element-wise",
            "Chỉ dùng token embedding"
          ],
          "answer": 1,
          "explain": "GPT-2 cộng token embedding và positional embedding (cùng shape) → một vector vừa mang nghĩa token vừa mang vị trí."
        },
        {
          "id": "w3q4",
          "type": "mcq",
          "q": "Ma trận attention scores (trước khi nhân V) có shape nào với input (batch, seq, d)?",
          "choices": [
            "(batch, seq, d)",
            "(batch, seq, seq)",
            "(batch, d, d)",
            "(seq, seq)"
          ],
          "answer": 1,
          "explain": "Score[i,j] = q_i·k_j cho mọi cặp token → (batch, seq, seq). Chính shape (seq×seq) này gây độ phức tạp O(n^2)."
        },
        {
          "id": "w3q5",
          "type": "open",
          "q": "[Nâng cao] RoPE khác với positional embedding tuyệt đối của GPT-2 thế nào?",
          "answer": "GPT-2 CỘNG một vector vị trí học được vào embedding. RoPE thay vào đó XOAY các cặp chiều của Q và K một góc tỉ lệ với vị trí token, áp dụng ngay trong attention (không lên V). Hệ quả: tích q_m·k_n chỉ phụ thuộc khoảng cách tương đối (m-n), không phụ thuộc vị trí tuyệt đối → tổng quát hoá tốt hơn ra ngoài độ dài đã train và là nền cho mở rộng context (NTK/YaRN). Llama 3, Qwen3 dùng RoPE.",
          "explain": "Xem mục A1 trong advanced_topics_vi.md."
        },
        {
          "id": "w3q6",
          "type": "mcq",
          "q": "[Nâng cao] Mục đích chính của Grouped-Query Attention (GQA) so với Multi-Head Attention?",
          "choices": [
            "Tăng số head để chính xác hơn",
            "Cho các nhóm head chia sẻ chung K,V để GIẢM kích thước KV cache khi inference",
            "Bỏ hoàn toàn key và value",
            "Thay softmax bằng sigmoid"
          ],
          "answer": 1,
          "explain": "GQA gom head thành nhóm dùng chung K,V → KV cache nhỏ hơn → sinh text dài rẻ hơn về bộ nhớ; trung dung giữa MHA và MQA."
        },
        {
          "id": "w3q7",
          "type": "mcq",
          "q": "[Nâng cao] Độ phức tạp bộ nhớ/tính toán của self-attention thường (full) theo độ dài seq n là?",
          "choices": [
            "O(n)",
            "O(n log n)",
            "O(n^2)",
            "O(1)"
          ],
          "answer": 2,
          "explain": "Ma trận score n×n → O(n^2). Đây là động lực cho sliding-window, MLA, và FlashAttention (tiling, không vật chất hoá ma trận n×n)."
        }
      ]
    },
    {
      "week": 4,
      "title": "Lắp ráp & chạy mô hình GPT",
      "questions": [
        {
          "id": "w4q1",
          "type": "mcq",
          "q": "LayerNorm trong transformer chuẩn hoá theo chiều nào?",
          "choices": [
            "Theo chiều batch (như BatchNorm)",
            "Theo chiều feature/embedding của từng token (last dim)",
            "Theo chiều sequence",
            "Theo toàn bộ tensor"
          ],
          "answer": 1,
          "explain": "LayerNorm chuẩn hoá theo feature của mỗi token độc lập (không phụ thuộc batch) → ổn định, hợp với độ dài chuỗi thay đổi."
        },
        {
          "id": "w4q2",
          "type": "open",
          "q": "Pre-LN + residual: x = x + Sublayer(LN(x)). Vì sao thiết kế này giúp train mạng sâu?",
          "answer": "Residual tạo một 'đường cao tốc' để gradient chảy thẳng về các lớp đầu mà không bị nhân nhỏ dần qua nhiều lớp (chống vanishing gradient). Đặt LayerNorm TRƯỚC sublayer (pre-LN) giữ đầu vào mỗi sublayer ở thang đo ổn định, làm việc xếp chồng hàng chục block ổn định hơn so với post-LN. Nhờ vậy có thể train transformer rất sâu.",
          "explain": "Ngoài vai trò shortcut gradient, residual còn cho phép mỗi block tinh chỉnh dần biểu diễn (residual stream)."
        },
        {
          "id": "w4q3",
          "type": "mcq",
          "q": "Feed-forward network (FFN) trong block GPT-2 mở rộng chiều ẩn lên khoảng mấy lần d_model?",
          "choices": [
            "2 lần",
            "4 lần",
            "8 lần",
            "Không mở rộng"
          ],
          "answer": 1,
          "explain": "FFN: Linear(d → 4d) → GELU → Linear(4d → d). Hệ số 4× là chuẩn của GPT-2."
        },
        {
          "id": "w4q4",
          "type": "mcq",
          "q": "GPT-2 small có khoảng bao nhiêu tham số (với emb_dim=768, n_layers=12, n_heads=12)?",
          "choices": [
            "~50M",
            "~124M",
            "~350M",
            "~1.5B"
          ],
          "answer": 1,
          "explain": "~124M. Verify số tham số là cách kiểm tra nhanh kiến trúc đã ghép đúng."
        },
        {
          "id": "w4q5",
          "type": "open",
          "q": "[Nâng cao] RMSNorm khác LayerNorm ở điểm nào, vì sao model hiện đại chuộng nó?",
          "answer": "RMSNorm bỏ bước trừ mean và bỏ bias β; chỉ chia cho căn của trung bình bình phương rồi nhân γ: x / sqrt(mean(x^2) + eps) · γ. Ít phép tính hơn LayerNorm nhưng ổn định tương đương, nên Llama/Qwen dùng để rẻ và nhanh hơn ở quy mô lớn.",
          "explain": "Xem mục A2 trong advanced_topics_vi.md."
        },
        {
          "id": "w4q6",
          "type": "mcq",
          "q": "[Nâng cao] SwiGLU FFN của Llama/Qwen thay thế phần nào của GPT-2?",
          "choices": [
            "Thay attention",
            "Thay FFN GELU-4× bằng một FFN có cổng (gated) dùng SiLU, ~2/3·4d chiều ẩn",
            "Thay LayerNorm",
            "Thay positional embedding"
          ],
          "answer": 1,
          "explain": "SwiGLU = (SiLU(x W_gate) ⊙ x W_up) W_down; có 3 ma trận nên giảm chiều ẩn để giữ số tham số tương đương."
        },
        {
          "id": "w4q7",
          "type": "mcq",
          "q": "[Nâng cao] Trong một lớp Mixture-of-Experts (MoE), 'router' làm gì?",
          "choices": [
            "Chọn top-k expert (FFN con) cho mỗi token, chỉ kích hoạt số ít expert",
            "Định tuyến gradient ngược",
            "Chọn GPU để chạy",
            "Sắp xếp token theo độ dài"
          ],
          "answer": 0,
          "explain": "Router gán mỗi token cho top-k experts → tổng tham số lớn nhưng tham số active mỗi token nhỏ; cần lo load balancing. Qwen3-MoE, gpt-oss, DeepSeek dùng MoE."
        }
      ]
    },
    {
      "week": 5,
      "title": "Pretraining: training loop + 1 lần chạy GPT-2 thật",
      "questions": [
        {
          "id": "w5q1",
          "type": "mcq",
          "q": "Quan hệ giữa cross-entropy loss L và perplexity (PPL)?",
          "choices": [
            "PPL = L^2",
            "PPL = e^L",
            "PPL = log(L)",
            "PPL = 1/L"
          ],
          "answer": 1,
          "explain": "PPL = e^L. Trực giác: perplexity ~ số lựa chọn 'trung bình' model còn phân vân; thấp hơn = dự đoán chắc hơn."
        },
        {
          "id": "w5q2",
          "type": "open",
          "q": "Gradient accumulation là gì và vì sao quan trọng với GPU 8GB?",
          "answer": "Thay vì cập nhật trọng số sau mỗi micro-batch nhỏ, ta cộng dồn gradient qua N micro-batch rồi mới step một lần → mô phỏng một 'effective batch' lớn (micro_batch × N) mà không cần chứa toàn bộ batch lớn trong VRAM. Với 3070 Ti 8GB chỉ vừa batch 1-2, gradient accumulation là cách đạt effective batch ~0.5M token/update kiểu Karpathy mà vẫn không OOM.",
          "explain": "Xem cách nanoGPT/train.py implement gradient_accumulation_steps."
        },
        {
          "id": "w5q3",
          "type": "mcq",
          "q": "Lịch learning rate điển hình khi pretrain LLM là gì?",
          "choices": [
            "Giữ LR cố định suốt",
            "Warmup tuyến tính tăng dần → rồi cosine decay giảm dần",
            "Tăng dần đều tới cuối",
            "Giảm rồi tăng (chữ V)"
          ],
          "answer": 1,
          "explain": "Warmup tránh sốc gradient lúc đầu (trọng số ngẫu nhiên); cosine decay giúp hội tụ mượt về cuối."
        },
        {
          "id": "w5q4",
          "type": "open",
          "q": "[Nâng cao] Vì sao các repo pretraining hiện đại (vd. nanoGPT config mặc định) đặt dropout = 0?",
          "answer": "Dropout là regularizer chống overfit, hữu ích khi fine-tune trên data nhỏ; nhưng pretraining chạy ~1 epoch trên lượng data khổng lồ thì gần như không overfit, nên dropout chỉ làm 'nhiễu' quá trình học. Vì vậy pretraining hiện đại thường bỏ dropout (nanoGPT để dropout=0.0 cho pretrain, gợi ý 0.1+ khi fine-tune).",
          "explain": "Bài học: kỹ thuật 'tốt' phụ thuộc bối cảnh (data lớn 1-epoch vs data nhỏ nhiều epoch)."
        },
        {
          "id": "w5q5",
          "type": "mcq",
          "q": "[Nâng cao] Vì sao 'bits-per-byte' (bpb) tốt hơn perplexity khi so sánh các model có tokenizer khác nhau?",
          "choices": [
            "bpb chạy nhanh hơn",
            "bpb chuẩn hoá loss về mức byte nên không phụ thuộc vocab/tokenizer → so sánh chéo được",
            "bpb luôn nhỏ hơn perplexity",
            "bpb không cần dữ liệu validation"
          ],
          "answer": 1,
          "explain": "Perplexity phụ thuộc cách chia token; bpb quy về byte → công bằng giữa các tokenizer. nanochat dùng val_bpb làm chỉ số chính."
        },
        {
          "id": "w5q6",
          "type": "mcq",
          "q": "[Nâng cao] Optimizer Muon (nanochat) áp dụng cho loại tham số nào?",
          "choices": [
            "Mọi tham số, thay hẳn AdamW",
            "Các ma trận trọng số 2D (orthogonalize update bằng Newton-Schulz); embedding/head vẫn dùng AdamW",
            "Chỉ embedding",
            "Chỉ bias"
          ],
          "answer": 1,
          "explain": "Muon orthogonalize bản cập nhật cho ma trận 2D → hội tụ pretraining nhanh hơn; là một yếu tố giúp nanochat 'speedrun' GPT-2."
        },
        {
          "id": "w5q7",
          "type": "mcq",
          "q": "Mixed precision (bf16) lợi gì khi train?",
          "choices": [
            "Tăng độ chính xác số học tuyệt đối",
            "Giảm VRAM và tăng tốc tính toán với mất chất lượng không đáng kể",
            "Loại bỏ nhu cầu gradient",
            "Làm loss luôn giảm"
          ],
          "answer": 1,
          "explain": "bf16 dùng nửa bộ nhớ, tận dụng tensor core; bf16 có dải mũ rộng nên ổn định hơn fp16 (fp16 cần GradScaler)."
        },
        {
          "id": "w5q8",
          "type": "open",
          "q": "[Nâng cao] DistributedDataParallel (DDP) hoạt động thế nào?",
          "answer": "DDP nhân bản toàn bộ model lên mỗi GPU; mỗi GPU xử lý một phần khác nhau của batch (data parallel), tính gradient cục bộ, rồi all-reduce (cộng và chia trung bình) gradient qua tất cả GPU trước khi mỗi bản sao cùng step. Kết quả tương đương train với batch lớn hơn N lần. Đây là cách nanoGPT/llm.c train trên node 8×A100 qua torchrun.",
          "explain": "DDP là mức song song đầu tiên cần biết; TP/PP/FSDP cho model không vừa 1 GPU."
        }
      ]
    },
    {
      "week": 6,
      "title": "Instruction fine-tuning (classification + instruction-following + LoRA)",
      "questions": [
        {
          "id": "w6q1",
          "type": "mcq",
          "q": "Ý tưởng cốt lõi của LoRA?",
          "choices": [
            "Lượng tử hoá trọng số xuống 4-bit",
            "Đóng băng W, học thêm hai ma trận thấp hạng B,A sao cho W' = W + BA với rank r ≪ d",
            "Tăng learning rate cho lớp cuối",
            "Cắt tỉa (prune) trọng số nhỏ"
          ],
          "answer": 1,
          "explain": "LoRA chỉ train BA (ít tham số) thay vì toàn bộ W → tiết kiệm VRAM lớn, là nền của QLoRA (Tuần 8)."
        },
        {
          "id": "w6q2",
          "type": "mcq",
          "q": "Để fine-tune GPT cho classification, thay đổi kiến trúc nào là cốt lõi?",
          "choices": [
            "Thêm một transformer block mới",
            "Thay output head (vocab_size) bằng một head nhỏ số lớp = số nhãn, thường chỉ train head + vài layer cuối",
            "Bỏ positional embedding",
            "Tăng gấp đôi số attention head"
          ],
          "answer": 1,
          "explain": "Classification không cần dự đoán token: thay head 50257 chiều bằng Linear ra num_classes (vd. spam/ham), dùng hidden state của token cuối. Đóng băng phần lớn model giúp train nhanh, ít overfit."
        },
        {
          "id": "w6q3",
          "type": "open",
          "q": "Trong instruction fine-tuning, vì sao thường mask phần prompt/instruction khỏi loss (chỉ tính loss trên phần response)?",
          "answer": "Mục tiêu là dạy model SINH phản hồi tốt, không phải học thuộc lại đề bài. Nếu tính loss trên cả instruction, gradient bị pha loãng bởi việc dự đoán lại phần text đã cho sẵn — model tối ưu cho việc lặp lại prompt thay vì chất lượng response. Mask (đặt label = -100 trong PyTorch) các token thuộc prompt để cross-entropy chỉ chấm phần model phải tự sinh.",
          "explain": "Đây là chi tiết dễ bỏ sót khi tự viết collate function cho instruction dataset."
        },
        {
          "id": "w6q4",
          "type": "mcq",
          "q": "Instruction fine-tuning khác pretraining ở điểm nào về DỮ LIỆU và MỤC TIÊU?",
          "choices": [
            "Khác thuật toán tối ưu hoàn toàn (không dùng cross-entropy)",
            "Pretraining: text thô, học dự đoán token kế; instruction FT: cặp (instruction, response) có cấu trúc, học làm theo yêu cầu — cùng loss cross-entropy nhưng phân phối dữ liệu và hành vi đích khác",
            "Instruction FT không cần gradient",
            "Pretraining chỉ dùng cho model nhỏ"
          ],
          "answer": 1,
          "explain": "Cơ chế học giống nhau (next-token prediction); thứ thay đổi là dữ liệu (template Alpaca-style) và hành vi mà ta muốn model hội tụ về (làm theo instruction thay vì tiếp tục văn bản)."
        }
      ]
    },
    {
      "week": 7,
      "title": "Nhập môn alignment: SFT → Reward Model → DPO/PPO → GRPO",
      "questions": [
        {
          "id": "w7q1",
          "type": "open",
          "q": "Phân biệt SFT, DPO và GRPO.",
          "answer": "SFT (Supervised Fine-Tuning): học bắt chước các phản hồi tốt bằng cross-entropy trên cặp (prompt, response chuẩn). DPO (Direct Preference Optimization): tối ưu trực tiếp từ cặp (chosen, rejected) bằng một loss dạng logistic, BỎ QUA reward model và PPO → đơn giản, ổn định. GRPO (Group Relative Policy Optimization): RL bỏ critic, lấy nhiều sample cho cùng prompt và chuẩn hoá reward theo nhóm; hợp với reward kiểm chứng được (RLVR) → nền của reasoning models.",
          "explain": "Thứ tự thường gặp: SFT → (RM) → DPO hoặc PPO → GRPO. Xem mục G advanced_topics_vi.md."
        },
        {
          "id": "w7q2",
          "type": "mcq",
          "q": "Reward Model (RM) trong RLHF học để làm gì?",
          "choices": [
            "Sinh phản hồi cuối cùng cho người dùng",
            "Chấm điểm/so sánh mức ưu tiên giữa các output để hướng dẫn RL",
            "Tokenize dữ liệu",
            "Lưu KV cache"
          ],
          "answer": 1,
          "explain": "RM học từ nhãn ưu tiên của con người, xuất ra điểm scalar; PPO dùng điểm này làm reward. FareedKhan implement RM from scratch."
        },
        {
          "id": "w7q3",
          "type": "mcq",
          "q": "So với PPO/RLHF kinh điển, DPO bỏ được thành phần nào?",
          "choices": [
            "Bỏ dữ liệu ưu tiên (preference)",
            "Bỏ việc train reward model riêng và vòng lặp PPO — tối ưu thẳng từ cặp ưu tiên",
            "Bỏ model tham chiếu (reference)",
            "Bỏ tokenizer"
          ],
          "answer": 1,
          "explain": "DPO biến bài toán RLHF thành một loss phân loại trực tiếp trên cặp (chosen, rejected), vẫn dùng policy tham chiếu nhưng không cần RM/PPO."
        },
        {
          "id": "w7q4",
          "type": "open",
          "q": "[Nâng cao] RLVR (Reinforcement Learning from Verifiable Rewards) là gì, vì sao hợp với reasoning?",
          "answer": "RLVR dùng reward KIỂM CHỨNG ĐƯỢC một cách khách quan: đáp án toán đúng/sai, unit test code pass/fail, thay vì điểm chủ quan từ reward model. Vì tín hiệu thưởng chính xác và không bị 'hack', model có thể tự khám phá chuỗi suy luận (chain-of-thought) dẫn tới đáp án đúng. Đây là cơ chế đứng sau các reasoning model kiểu o1/R1; thường kết hợp với GRPO.",
          "explain": "Xem nanochat chat_rl.py (tasks gsm8k, spellingbee) và paper DeepSeekMath/GRPO (arXiv 2402.03300)."
        },
        {
          "id": "w7q5",
          "type": "mcq",
          "q": "[Nâng cao] Bước 'midtrain' (nanochat) nằm ở đâu trong pipeline?",
          "choices": [
            "Trước pretrain",
            "Giữa pretrain và SFT — dạy format hội thoại, special tokens, tool use",
            "Sau GRPO",
            "Thay thế SFT"
          ],
          "answer": 1,
          "explain": "Midtrain là khái niệm KHÔNG có trong pipeline GPT-2 kinh điển; nó chuẩn bị base model cho giai đoạn chat/SFT."
        },
        {
          "id": "w7q6",
          "type": "open",
          "q": "Trong RLHF/DPO, thành phần KL divergence (hoặc reference policy) đóng vai trò gì?",
          "answer": "Nó giữ policy mới không trôi quá xa khỏi model tham chiếu (thường là bản SFT). Không có ràng buộc này, RL có thể 'hack' reward: sinh văn bản kỳ dị đạt điểm cao từ reward model nhưng mất khả năng ngôn ngữ chung (reward hacking / catastrophic drift). Trong PPO nó là phạt KL trong reward; trong DPO nó nằm ngay trong loss qua tỉ số log-prob với pi_ref và hệ số beta.",
          "explain": "Đây là lý do mọi công thức DPO đều chứa pi_theta/pi_ref — không phải chi tiết trang trí."
        }
      ]
    },
    {
      "week": 8,
      "title": "QLoRA fine-tuning thực tế (Unsloth)",
      "questions": [
        {
          "id": "w8q1",
          "type": "mcq",
          "q": "QLoRA = ?",
          "choices": [
            "LoRA chạy trên nhiều GPU",
            "Quantize base model xuống 4-bit (NF4, đóng băng) + chỉ train adapter LoRA ở bf16",
            "Lượng tử hoá cả adapter xuống 4-bit",
            "LoRA cho mô hình vision"
          ],
          "answer": 1,
          "explain": "QLoRA nén base xuống NF4 4-bit để giảm VRAM, gradient chỉ chảy qua adapter LoRA → fine-tune 7B vừa ~5GB."
        },
        {
          "id": "w8q2",
          "type": "mcq",
          "q": "Theo bảng VRAM của Unsloth, QLoRA một model 7B cần khoảng bao nhiêu VRAM?",
          "choices": [
            "~2GB",
            "~5GB",
            "~12GB",
            "~24GB"
          ],
          "answer": 1,
          "explain": "~5GB (8B ≈ 6GB) → vừa thoải mái trên 3070 Ti 8GB. 14B ≈ 8.5GB thì vượt 8GB."
        },
        {
          "id": "w8q3",
          "type": "open",
          "q": "Liệt kê config QLoRA hợp lý cho GPU 8GB.",
          "answer": "load_in_4bit=True; batch_size 1-2; sequence length ≤ 1024; gradient_checkpointing=True; LoRA r=16, lora_alpha=16; target tất cả projection của attention + MLP. Nếu vẫn sát giới hạn: giảm seq len, tăng gradient accumulation, hoặc dùng Colab T4 15GB.",
          "explain": "Threshold: nếu OOM ở batch 1 hoặc run >24h → chuyển 4090/A100 thuê."
        },
        {
          "id": "w8q4",
          "type": "mcq",
          "q": "[Nâng cao] NF4 (trong QLoRA) là gì?",
          "choices": [
            "Một định dạng file model",
            "Kiểu lượng tử hoá 4-bit 'normal float', phân bố các mức tối ưu cho trọng số gần Gaussian",
            "Một optimizer",
            "Một loại attention"
          ],
          "answer": 1,
          "explain": "NF4 đặt các mức lượng tử theo phân vị của phân phối chuẩn → ít sai số hơn int4 đều cho trọng số ~Gaussian."
        },
        {
          "id": "w8q5",
          "type": "mcq",
          "q": "[Nâng cao] GGUF là gì?",
          "choices": [
            "Một thuật toán lượng tử hoá mới",
            "Một ĐỊNH DẠNG FILE của llama.cpp (chứa weight + metadata, các k-quant như Q4_K_M) mà Ollama/LM Studio load",
            "Một benchmark",
            "Một kiểu attention"
          ],
          "answer": 1,
          "explain": "GGUF là định dạng đóng gói, không phải thuật toán; nhầm lẫn này rất phổ biến. Tuần 9 sẽ load GGUF qua Ollama."
        },
        {
          "id": "w8q6",
          "type": "open",
          "q": "Khi nào nên ngừng fine-tune local và chuyển lên cloud (4090/A100)?",
          "answer": "Khi một lần fine-tune dự kiến chạy >24h ở local, hoặc khi OOM ngay cả ở batch size 1 (sau khi đã bật 4-bit, gradient checkpointing, giảm seq len). Lúc đó thuê RTX 4090/A100 sẽ rẻ hơn nhiều về thời gian.",
          "explain": "Đây là 'ngưỡng kích hoạt cloud' của roadmap; verify bằng smoke test ngắn trước khi cam kết run dài."
        }
      ]
    },
    {
      "week": 9,
      "title": "Fine-tuning Mac/MLX + local inference stack",
      "questions": [
        {
          "id": "w9q1",
          "type": "mcq",
          "q": "Vì sao MacBook 24GB có thể fine-tune model lớn hơn RTX 3070 Ti 8GB?",
          "choices": [
            "CPU Mac nhanh hơn GPU",
            "Unified memory 24GB dùng chung cho cả 'GPU', cho phép chứa model 13-14B (đổi lại chậm hơn ~2-4×)",
            "MLX nén model xuống 1-bit",
            "Mac có nhiều GPU hơn"
          ],
          "answer": 1,
          "explain": "Unified memory là lợi thế của Apple Silicon: dung lượng lớn hơn VRAM rời 8GB, dù thông lượng thấp hơn NVIDIA."
        },
        {
          "id": "w9q2",
          "type": "open",
          "q": "Mô tả luồng fine-tune → phục vụ bằng MLX trên Mac.",
          "answer": "1) mlx_lm.lora --model ... --train --data ... --iters 500 để train adapter LoRA. 2) mlx_lm.fuse --model ... --adapter-path ... để gộp adapter vào base. 3) Phục vụ qua Ollama (tạo Modelfile) hoặc LM Studio (load GGUF/MLX) để chat. Với 24GB có thể LoRA/QLoRA tới ~13-14B.",
          "explain": "Mac dùng định dạng MLX (mlx-community/...); Ollama/LM Studio là lớp serving."
        },
        {
          "id": "w9q3",
          "type": "mcq",
          "q": "Ollama và LM Studio đóng vai trò gì?",
          "choices": [
            "Train model from scratch",
            "Lớp inference/serving local — tải, quản lý và chat với model (GGUF/MLX) qua API/GUI",
            "Vector database cho RAG",
            "Tokenizer"
          ],
          "answer": 1,
          "explain": "Chúng giúp chạy model local dễ dàng; Ollama có API kiểu OpenAI tiện cắm vào RAG/agents."
        },
        {
          "id": "w9q4",
          "type": "open",
          "q": "Tóm tắt phân vai 3070 Ti vs Mac 24GB vs Cloud.",
          "answer": "3070 Ti (8GB): code from-scratch, train nhỏ/validate loop, QLoRA 7B-8B nhanh. Mac 24GB: chứa & fine-tune model 13-14B, chạy yên tĩnh local, inference quantized. Cloud (RunPod/Lambda): lần pretrain GPT-2 một lần (~$15-35), full fine-tune, iterate nhanh khi local quá chậm/OOM.",
          "explain": "Đây là nội dung deliverable hardware_decision.md."
        }
      ]
    },
    {
      "week": 10,
      "title": "Xây dựng RAG pipeline end-to-end",
      "questions": [
        {
          "id": "w10q1",
          "type": "mcq",
          "q": "Thứ tự đúng của một pipeline RAG cơ bản?",
          "choices": [
            "Generate → retrieve → embed → chunk",
            "Load → chunk → embed → vector store → retrieve top-k → generate",
            "Embed → generate → chunk → store",
            "Retrieve → generate → embed"
          ],
          "answer": 1,
          "explain": "Load tài liệu → cắt chunk → embed → lưu vector store → khi hỏi: embed query, retrieve top-k, ghép context vào prompt → generate."
        },
        {
          "id": "w10q2",
          "type": "open",
          "q": "Vì sao khi chunking cần 'overlap' giữa các đoạn?",
          "answer": "Overlap (vd. ~100 ký tự/token) giữ phần đầu/cuối câu liền mạch giữa hai chunk, tránh cắt đứt một ý/định nghĩa ngay ranh giới chunk khiến retrieval bỏ sót ngữ cảnh cần thiết. Với chunk ~800 và overlap ~100, một thông tin nằm ở mép vẫn xuất hiện trọn trong ít nhất một chunk.",
          "explain": "Chunk quá nhỏ mất ngữ cảnh; quá lớn loãng tín hiệu retrieval. Overlap là cân bằng."
        },
        {
          "id": "w10q3",
          "type": "mcq",
          "q": "Retrieval trong RAG thường xếp hạng tài liệu bằng độ đo nào?",
          "choices": [
            "Khoảng cách Hamming",
            "Cosine similarity giữa embedding của query và document",
            "Số ký tự trùng",
            "Thứ tự alphabet"
          ],
          "answer": 1,
          "explain": "sim(q,d) = (q·d)/(|q||d|). Tài liệu có embedding gần (cosine cao) với query được lấy ra trước."
        },
        {
          "id": "w10q4",
          "type": "mcq",
          "q": "Chroma đóng vai trò gì trong pipeline?",
          "choices": [
            "Mô hình sinh text",
            "Vector store (lưu & truy vấn nearest-neighbor các embedding) — tốt cho dev",
            "Tokenizer",
            "Reranker"
          ],
          "answer": 1,
          "explain": "Chroma là vector DB nhẹ cho dev; production có thể chuyển pgvector/Qdrant/Weaviate."
        },
        {
          "id": "w10q5",
          "type": "open",
          "q": "Vì sao RAG giúp giảm hallucination so với hỏi LLM trực tiếp?",
          "answer": "RAG 'grounding' câu trả lời vào các đoạn tài liệu thật được retrieve và đưa vào prompt, nên model trả lời dựa trên bằng chứng cụ thể thay vì chỉ dựa vào trí nhớ tham số (dễ bịa). Ngoài ra có thể trích dẫn nguồn để kiểm chứng. Nó cũng cập nhật được kiến thức mới mà không cần train lại.",
          "explain": "Anchor của roadmap: corpus là tài liệu nghiệp vụ Finance Banking của bạn."
        },
        {
          "id": "w10q6",
          "type": "mcq",
          "q": "Embedding model làm gì?",
          "choices": [
            "Sinh câu trả lời cuối",
            "Biến văn bản thành vector số nắm bắt ngữ nghĩa, để so sánh tương đồng",
            "Cắt tài liệu thành chunk",
            "Lượng tử hoá model"
          ],
          "answer": 1,
          "explain": "Embedding (BGE/e5/nomic...) ánh xạ text → vector; văn bản gần nghĩa → vector gần nhau."
        }
      ]
    },
    {
      "week": 11,
      "title": "Advanced RAG + đánh giá (RAGAS)",
      "questions": [
        {
          "id": "w11q1",
          "type": "mcq",
          "q": "Hybrid retrieval kết hợp BM25 và vector search; chúng thường được trộn bằng kỹ thuật nào?",
          "choices": [
            "Lấy trung bình embedding",
            "Reciprocal Rank Fusion (RRF) — hợp nhất thứ hạng từ hai bộ retrieve",
            "Nối kết quả ngẫu nhiên",
            "Chỉ lấy BM25"
          ],
          "answer": 1,
          "explain": "BM25 (lexical) bắt từ khoá chính xác; vector (semantic) bắt ý nghĩa; RRF hợp nhất để bù điểm yếu của nhau."
        },
        {
          "id": "w11q2",
          "type": "open",
          "q": "Cross-encoder reranker khác bi-encoder (embedding) thế nào, dùng khi nào?",
          "answer": "Bi-encoder mã hoá query và document RIÊNG thành vector rồi so cosine — nhanh, scale tốt, dùng để retrieve top-N từ kho lớn. Cross-encoder đưa CẢ cặp (query, document) qua model cùng lúc → chấm điểm liên quan chính xác hơn nhưng chậm, không scale cho toàn kho. Quy trình: bi-encoder lấy top-N (vd. 50), rồi cross-encoder rerank lại để chọn top-k tinh (vd. 5).",
          "explain": "BGE cross-encoder (mã nguồn mở) là lựa chọn phổ biến."
        },
        {
          "id": "w11q3",
          "type": "mcq",
          "q": "Trong RAGAS, 'faithfulness' đo điều gì?",
          "choices": [
            "Câu trả lời có bám/được hỗ trợ bởi context retrieve hay không (chống bịa)",
            "Tốc độ trả lời",
            "Độ dài câu trả lời",
            "Số token dùng"
          ],
          "answer": 0,
          "explain": "Faithfulness kiểm tra các khẳng định trong câu trả lời có truy được về context không → thước đo chống hallucination."
        },
        {
          "id": "w11q4",
          "type": "mcq",
          "q": "'Context precision' và 'context recall' trong RAGAS đánh giá khâu nào?",
          "choices": [
            "Khâu generate",
            "Chất lượng RETRIEVAL — đoạn lấy ra có liên quan (precision) và có đủ thông tin cần (recall) không",
            "Tốc độ embedding",
            "Chi phí API"
          ],
          "answer": 1,
          "explain": "Hai chỉ số này tách bạch lỗi do retrieval kém với lỗi do generation kém."
        },
        {
          "id": "w11q5",
          "type": "open",
          "q": "Vì sao cần eval set + cẩn trọng với LLM-as-judge?",
          "answer": "Cần một eval set (cặp câu hỏi + ground-truth) để đo before/after một cách định lượng thay vì cảm tính. LLM-as-judge (dùng một LLM mạnh chấm output) tiện nhưng nhiều bẫy đã được ghi nhận trong nghiên cứu (arXiv 2306.05685): thiên vị độ dài, thiên vị vị trí, tự khen model cùng họ. Loss thấp hơn KHÔNG tự động nghĩa là hữu ích hơn trong thực tế → đừng tin một chỉ số duy nhất; kết hợp metric tự động + kiểm tra thủ công.",
          "explain": "Đo lường tốt là điều phân biệt 'nghịch' với 'kỹ thuật'."
        },
        {
          "id": "w11q6",
          "type": "mcq",
          "q": "Langfuse/LangSmith dùng để làm gì?",
          "choices": [
            "Train embedding",
            "Tracing/observability: ghi lại từng bước retrieve → generate, chạy eval, LLM-as-judge",
            "Lưu vector",
            "Lượng tử hoá model"
          ],
          "answer": 1,
          "explain": "Tracing giúp gỡ lỗi pipeline (đoạn nào retrieve sai, prompt nào hỏng) và đo chất lượng có hệ thống."
        }
      ]
    },
    {
      "week": 12,
      "title": "Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP",
      "questions": [
        {
          "id": "w12q1",
          "type": "open",
          "q": "Mô tả 'agent loop' cơ bản.",
          "answer": "perceive (nhận input/trạng thái) → reason (LLM suy luận, quyết định bước tiếp) → chọn tool → execute tool → quan sát kết quả → lặp lại cho tới khi đạt mục tiêu, rồi trả về structured output. Khác với một lần gọi LLM, agent có vòng lặp nhiều bước có dùng công cụ và trạng thái.",
          "explain": "Đây là khung chung của Claude Agent SDK và mọi agent framework."
        },
        {
          "id": "w12q2",
          "type": "mcq",
          "q": "MCP (Model Context Protocol) là gì?",
          "choices": [
            "Một model ngôn ngữ",
            "Một chuẩn mở để kết nối model với tool/nguồn dữ liệu qua server/client (GitHub, Postgres, Slack, filesystem...)",
            "Một thuật toán RL",
            "Một định dạng file"
          ],
          "answer": 1,
          "explain": "MCP tách 'bộ não' khỏi nguồn dữ liệu/tool, cho phép tái sử dụng các server tool chuẩn hoá."
        },
        {
          "id": "w12q3",
          "type": "mcq",
          "q": "Khác biệt chính giữa LangGraph và CrewAI?",
          "choices": [
            "LangGraph chỉ cho vision, CrewAI cho text",
            "LangGraph: graph có trạng thái, tường minh, auditable; CrewAI: crew theo vai (role) prototype nhanh",
            "Cả hai giống hệt nhau",
            "CrewAI không hỗ trợ tool"
          ],
          "answer": 1,
          "explain": "LangGraph hợp workflow cần kiểm soát/audit (tài chính có quy định); CrewAI nhanh để dựng nhóm agent theo vai."
        },
        {
          "id": "w12q4",
          "type": "open",
          "q": "Vì sao workflow tài chính có quy định nên ưu tiên LangGraph?",
          "answer": "Vì LangGraph cho phép định nghĩa trạng thái và luồng chuyển tiếp một cách tường minh, có thể kiểm tra/ghi vết (auditable) từng bước, và chèn các human-in-the-loop gate rõ ràng. Trong domain tài chính bị ràng buộc quy định, khả năng giải trình 'vì sao agent ra quyết định này' và kiểm soát chặt từng chuyển tiếp quan trọng hơn tốc độ prototype.",
          "explain": "CrewAI tiện cho thử nghiệm nhanh nhưng kém minh bạch hơn về luồng trạng thái."
        },
        {
          "id": "w12q5",
          "type": "mcq",
          "q": "Human-in-the-loop (HITL) gate nghĩa là gì?",
          "choices": [
            "Agent chạy hoàn toàn tự động không cần người",
            "Điểm dừng yêu cầu con người phê duyệt/sửa trước khi agent đi tiếp",
            "Một loại tool",
            "Cách tính token"
          ],
          "answer": 1,
          "explain": "HITL gate đặt giữa các stage rủi ro để con người kiểm soát; thiết kế least-privilege + HITL ngay từ đầu."
        },
        {
          "id": "w12q6",
          "type": "mcq",
          "q": "Mô hình 5 tầng engineering (docs/5-layers-multi-agent.jpg) xếp theo thứ tự nào, từ trong ra ngoài?",
          "choices": [
            "Prompt → Harness → Context → Graph → Loop",
            "Prompt → Context → Harness → Loop → Graph",
            "Context → Prompt → Loop → Harness → Graph",
            "Loop → Prompt → Context → Graph → Harness"
          ],
          "answer": 1,
          "explain": "Prompt (the message) → Context (the memory) → Harness (the machine: gather-act-verify) → Loop (the system: run-check-decide) → Graph (the organization: nhiều agent + shared memory). Mỗi tầng bọc tầng trước; model là commodity, hệ thống quanh nó là engineering."
        },
        {
          "id": "w12q7",
          "type": "open",
          "q": "Bốn điều kiện nào làm loop autoresearch của Karpathy chạy được, và vì sao thiếu một cái là loop hỏng?",
          "answer": "(1) Output verifiable — có metric đo được (val_bpb), không thì agent tối ưu thứ sai; (2) Action reversible — git reset về commit giữ lại được, thất bại không phá state; (3) Horizon ngắn — run ~5 phút cho feedback dày; (4) Environment bounded — repo giới hạn không gian hành động. Thiếu verify thì không biết giữ hay bỏ thay đổi; thiếu reversible thì một lỗi phá cả quá trình; horizon dài làm tín hiệu học thưa; environment mở làm không gian tìm kiếm nổ.",
          "explain": "Đây là checklist trước khi cho agent chạy tự động bất kỳ việc gì — kể cả trong CornAgents.AI."
        }
      ]
    },
    {
      "week": 13,
      "title": "Map LLM vào SDLC; build agent graph CornAgents.AI",
      "questions": [
        {
          "id": "w13q1",
          "type": "open",
          "q": "Cho ví dụ map agent ↔ stage SDLC (ít nhất 3 agent).",
          "answer": "Requirements Analyst agent: biến feature request Finance Banking thành user story + acceptance criteria, grounded bởi RAG (Tuần 10-11) trên tài liệu nghiệp vụ nội bộ. Code Review agent: đọc diff/PR, flag bug/security/style. Test-Generation agent: từ story/code sinh test case. Có thể thêm Design và Docs agent. Mỗi agent có I/O contract rõ ràng và nối thành graph.",
          "explain": "Requirements Analyst tận dụng đúng thế mạnh BA của bạn."
        },
        {
          "id": "w13q2",
          "type": "mcq",
          "q": "Nguyên tắc 'least-privilege' cho agent nghĩa là gì?",
          "choices": [
            "Mỗi agent được mọi quyền để linh hoạt",
            "Mỗi agent chỉ được cấp quyền/tool tối thiểu cần cho nhiệm vụ của nó",
            "Chỉ một agent có quyền",
            "Không agent nào dùng tool"
          ],
          "answer": 1,
          "explain": "Giới hạn quyền giảm rủi ro khi agent lỗi/bị lạm dụng — đặc biệt quan trọng với hệ thống tài chính."
        },
        {
          "id": "w13q3",
          "type": "open",
          "q": "Requirements Analyst agent dùng RAG để làm gì?",
          "answer": "Dùng RAG để 'grounding' việc sinh user story/acceptance criteria vào tài liệu nguồn thật — ví dụ quy định nghiệp vụ và spec nội bộ — thay vì bịa. Khi nhận một feature request, agent retrieve các quy định/định nghĩa liên quan, đưa vào context, rồi sinh story bám đúng ràng buộc nghiệp vụ và có thể trích dẫn nguồn.",
          "explain": "Đây là điểm nối Phase 2 (RAG) vào Phase 3 (agents)."
        },
        {
          "id": "w13q4",
          "type": "mcq",
          "q": "Trong workflow multi-agent có quy định, human approval gate nên đặt ở đâu?",
          "choices": [
            "Không cần",
            "Giữa các stage quan trọng (vd. trước khi chốt requirement, trước khi merge) để người duyệt",
            "Chỉ ở cuối cùng",
            "Chỉ ở đầu"
          ],
          "answer": 1,
          "explain": "Đặt gate giữa các stage cho phép bắt lỗi sớm và giữ con người kiểm soát các quyết định rủi ro."
        },
        {
          "id": "w13q5",
          "type": "mcq",
          "q": "Vì sao cần 'I/O contract' rõ ràng giữa các agent?",
          "choices": [
            "Để agent chạy nhanh hơn",
            "Để output của agent này là input có cấu trúc, dự đoán được cho agent kế — dễ ghép graph, test và audit",
            "Để giảm token",
            "Để mã hoá dữ liệu"
          ],
          "answer": 1,
          "explain": "Contract (schema state trong LangGraph) làm hệ thống mô-đun và kiểm thử được từng mắt xích."
        },
        {
          "id": "w13q6",
          "type": "mcq",
          "q": "Ghép đúng 5 workflow patterns của Anthropic với mô tả?",
          "choices": [
            "Prompt Chaining = nhiều model bỏ phiếu; Routing = chạy tuần tự",
            "Prompt Chaining = các bước cố định nối tiếp; Routing = phân loại input rồi gửi tới prompt/model chuyên biệt; Parallelization = các call độc lập chạy song song; Orchestrator–Workers = model trung tâm phân rã & giao việc; Evaluator–Optimizer = một bên sinh, một bên chấm theo tiêu chí, lặp",
            "Orchestrator–Workers = không có model trung tâm; Evaluator–Optimizer = chỉ chạy 1 lần",
            "Cả 5 pattern đều cần knowledge graph"
          ],
          "answer": 1,
          "explain": "Lời khuyên gốc của Anthropic: 'simple, composable patterns rather than complex frameworks' — chọn pattern theo bài toán, đừng bê nguyên framework nặng."
        },
        {
          "id": "w13q7",
          "type": "open",
          "q": "'Artifact contract' giữa các agent là gì và vì sao reviewer nên trả 'criterion-level defects' thay vì 'looks good'?",
          "answer": "Artifact contract = mỗi handoff giữa hai agent là một artifact có schema rõ (user story JSON, defect list, test file) thay vì đoạn văn tự do — giúp validate tự động, test từng mắt xích, và audit. Reviewer trả defect theo từng tiêu chí (đúng/sai ở tiêu chí nào, bằng chứng gì) vì 'looks good' không cho downstream agent hay con người thông tin hành động được; defect có cấu trúc thì gate được (đếm, chặn, escalate) và đo được chất lượng review theo thời gian.",
          "explain": "Từ mục VI.D của Karpathy-Loop PDF: 'Every handoff should be an artifact contract. A reviewer returns criterion-level defects, not looks-good.'"
        }
      ]
    },
    {
      "week": 14,
      "title": "Graph Engineering: Knowledge Graph làm shared memory cho multi-agent",
      "questions": [
        {
          "id": "w14q1",
          "type": "mcq",
          "q": "Bốn stage của knowledge graph pipeline (Anthropic Playbook) theo đúng thứ tự?",
          "choices": [
            "Querying → Assembly → Resolution → Extraction",
            "Extraction (Haiku, structured outputs) → Resolution (Sonnet, cluster) → Assembly (NetworkX graph) → Querying (subgraph + grounded answer)",
            "Embedding → Chunking → Retrieval → Generation",
            "Extraction → Querying → Resolution → Assembly"
          ],
          "answer": 1,
          "explain": "Mỗi stage là một prompt/model call: Haiku extract entities+relations theo Pydantic schema; Sonnet resolve surface forms; NetworkX MultiDiGraph lắp graph với provenance; Sonnet trả lời trên subgraph đã serialize."
        },
        {
          "id": "w14q2",
          "type": "open",
          "q": "RAG và Knowledge Graph khác nhau thế nào, khi nào cần cái nào?",
          "answer": "RAG retrieve chunk theo tương đồng ngữ nghĩa với câu hỏi — tốt cho câu hỏi single-hop (đáp án nằm trong một đoạn). Nó thất bại với multi-hop: khi đáp án phải NỐI facts từ nhiều tài liệu không giống nhau về mặt lexical/semantic. Knowledge graph biến entity chung thành node tường minh có edge sang cả hai tài liệu — graph traversal tìm ra kết nối bất kể surface form. Hai cách bổ trợ: RAG rẻ cho direct retrieval, KG cho structural reasoning; thực tế dùng cùng nhau.",
          "explain": "Quy tắc: cần CHAIN facts xuyên nguồn / SHARE structured state / GROUND phán xét → graph. Chỉ cần retrieve/classify → RAG hoặc đơn giản hơn là đủ."
        },
        {
          "id": "w14q3",
          "type": "mcq",
          "q": "Vì sao extraction prompt yêu cầu viết 'one-sentence description grounded in this document' cho mỗi entity?",
          "choices": [
            "Để hiển thị đẹp trong UI",
            "Description là tín hiệu ngữ nghĩa cho stage RESOLUTION — thiếu nó resolver chỉ thấy tên và phải đoán; 'Armstrong — phi hành gia' và 'Armstrong — nghệ sĩ jazz' trùng tên nhưng không được merge",
            "Để giảm token",
            "Để thay thế cho embeddings"
          ],
          "answer": 1,
          "explain": "Description không phải metadata mà là input hạng nhất cho resolution — nó thay thứ mà trained classifier phải học từ labeled data theo domain."
        },
        {
          "id": "w14q4",
          "type": "mcq",
          "q": "Vì sao với knowledge graph, PRECISION của extraction thường quan trọng hơn RECALL?",
          "choices": [
            "Vì recall không đo được",
            "Vì một entity SAI sinh ra các quan hệ sai và lan truyền qua multi-hop reasoning (graph chủ động gây nhiễu), còn entity THIẾU chỉ làm graph không đầy đủ nhưng vẫn đúng",
            "Vì precision rẻ hơn để tính",
            "Vì Haiku không thể đạt recall cao"
          ],
          "answer": 1,
          "explain": "Kết quả trên Apollo corpus: precision 1.00, recall 0.38–0.55 — extractor bảo thủ là trade-off ĐÚNG cho production; evaluation harness giúp bạn chỉnh trade-off này có chủ đích."
        },
        {
          "id": "w14q5",
          "type": "open",
          "q": "Nêu 3 vai trò của knowledge graph trong kiến trúc multi-agent (theo Playbook).",
          "answer": "(1) Shared memory cho orchestrator–workers: worker đọc/ghi graph trực tiếp thay vì đẩy summary qua context window của orchestrator — window của orchestrator không phình theo số worker. (2) Grounding layer cho evaluator–optimizer: evaluator kiểm tra từng claim theo edge có provenance ('triple X không tồn tại; graph chứa Y từ document Z') — fact-check thay vì cảm giác. (3) Persistent world model cho loop chạy dài: context window bị flush thì graph vẫn còn — 'the agent forgets, the graph does not'.",
          "explain": "Đây là 3 chỗ cắm graph vào CornAgents.AI: workers ghi, evaluator check, loop qua đêm không mất trí nhớ."
        },
        {
          "id": "w14q6",
          "type": "mcq",
          "q": "'Grounded answer' khác 'ungrounded answer' thế nào khi query graph?",
          "choices": [
            "Grounded chạy nhanh hơn",
            "Grounded bị ràng buộc 'answer using ONLY the graph, cite edges' — trả lời truy vết được về triples có provenance và nói rõ graph KHÔNG chứa gì; ungrounded dựa vào pretraining nên nghe hợp lý nhưng trên private corpus thì không kiểm chứng được",
            "Ungrounded luôn sai",
            "Grounded không cần model"
          ],
          "answer": 1,
          "explain": "Trên corpus riêng (tài liệu Finance Banking nội bộ) model không có kiến thức pretraining — chỉ grounded answer là dùng được, và citation kiểm tra được bằng string matching."
        },
        {
          "id": "w14q7",
          "type": "open",
          "q": "Evaluation feedback loop của KG pipeline hoạt động thế nào và vì sao nó 'cùng hình dạng' với ratchet loop của Karpathy autoresearch?",
          "answer": "Lập gold set (entities/relations tự label từ 2+ tài liệu đại diện) → chạy extraction → scorer đo precision/recall/F1 → đổi extraction prompt/schema → chạy lại → giữ thay đổi nếu F1 tăng, revert nếu giảm. Cùng hình dạng với autoresearch: act (extract) → observe (score) → learn (tune prompt) → repeat; chỉ khác artifact được tối ưu không phải train.py mà là prompt/ontology/resolution policy — 'graph autoresearch'. Không có harness này, không biết thay đổi prompt làm chất lượng tốt lên hay tệ đi, và drift theo corpus không ai bắt được.",
          "explain": "Trí tuệ của loop nằm ở chất lượng environmental feedback, không nằm trong model."
        }
      ]
    },
    {
      "week": 15,
      "title": "Capstone + evaluation/observability",
      "questions": [
        {
          "id": "w15q1",
          "type": "open",
          "q": "Use case capstone khuyến nghị và 3 thành phần kỹ thuật của nó?",
          "answer": "Use case: spec-to-stories + automated review cho một feature Finance Banking (nghiệp vụ Finance Banking tổng quát). Ba thành phần: (1) RAG — grounding vào tài liệu domain; (2) Agents — workflow multi-agent (requirements → review → test) với HITL gate; (3) tùy chọn model fine-tuned local (Tuần 8/9) cho một sub-task phân loại nghiệp vụ hẹp. Gắn tracing và viết eval rubric.",
          "explain": "Đây là nơi hội tụ cả 3 phase của roadmap."
        },
        {
          "id": "w15q2",
          "type": "mcq",
          "q": "Bộ ba metric đánh giá capstone agentic gồm?",
          "choices": [
            "Loss, perplexity, BLEU",
            "Success rate, human-override rate, groundedness",
            "FPS, latency, throughput",
            "Precision, recall, F1 (chỉ vậy)"
          ],
          "answer": 1,
          "explain": "Success rate (hoàn thành đúng), human-override rate (tần suất người phải sửa — đo độ tin), groundedness (bám tài liệu nguồn — chống bịa)."
        },
        {
          "id": "w15q3",
          "type": "open",
          "q": "Vì sao chiến lược 'Claude làm brain + model 7B fine-tuned cho sub-task' lại hợp lý?",
          "answer": "Claude (model mạnh) làm bộ điều phối/suy luận chính cho các bước mở, cần năng lực rộng. Nhưng một sub-task hẹp, lặp lại nhiều (vd. phân loại văn bản nghiệp vụ thành các nhãn cố định) thì một model 7B fine-tuned local làm tốt với chi phí và độ trễ thấp hơn nhiều, lại chạy offline. Phối hợp tối ưu chi phí/độ trễ mà vẫn giữ chất lượng ở khâu khó.",
          "explain": "Hiểu internals Phase 1 giúp lập luận lựa chọn model này có cơ sở."
        },
        {
          "id": "w15q4",
          "type": "mcq",
          "q": "'Groundedness' đo điều gì?",
          "choices": [
            "Tốc độ agent",
            "Mức độ output bám vào/được hỗ trợ bởi tài liệu nguồn (chống bịa)",
            "Số agent dùng",
            "Chi phí token"
          ],
          "answer": 1,
          "explain": "Tương tự faithfulness trong RAGAS, áp cho output cuối của workflow — quan trọng trong domain tài chính."
        },
        {
          "id": "w15q5",
          "type": "open",
          "q": "Viết retrospective 'nối về Phase 1' nghĩa là gì?",
          "answer": "Sau khi ship capstone, nhìn lại và giải thích VÌ SAO các lựa chọn kỹ thuật hoạt động, dựa trên hiểu biết internals từ Phase 1: vì sao một model nhỏ fine-tuned đủ cho sub-task, vì sao context dài tốn KV cache, vì sao quantization 4-bit chấp nhận được, vì sao RAG cần grounding... Mục tiêu là khép vòng học: từ 'biết dùng' sang 'hiểu tại sao', biến cả roadmap thành kiến thức nền vững chứ không chỉ là làm theo công thức.",
          "explain": "Đây là deliverable retrospective.md — mục tiêu thật sự của toàn lộ trình."
        }
      ]
    }
  ]
};
