# Tuần 12, Đáp án & Giải thích: Fine-tuning Mac/MLX + local inference stack

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Vì sao MacBook 24GB có thể fine-tune model lớn hơn RTX 3070 Ti 8GB?

- **A.** Mac có nhiều GPU hơn
- **B.** Unified memory 24GB dùng chung cho cả 'GPU', cho phép chứa model 13-14B (đổi lại chậm hơn ~2-4×) (đáp án đúng)
- **C.** MLX nén model xuống 1-bit
- **D.** CPU Mac nhanh hơn GPU

**Đáp án: B**

**Giải thích:** Unified memory là lợi thế của Apple Silicon: dung lượng lớn hơn VRAM rời 8GB, dù thông lượng thấp hơn NVIDIA.

## Câu 2 (Tự luận)

Mô tả luồng fine-tune → phục vụ bằng MLX trên Mac.

**Trả lời mẫu:** 1) mlx_lm.lora --model ... --train --data ... --iters 500 để train adapter LoRA. 2) mlx_lm.fuse --model ... --adapter-path ... để gộp adapter vào base. 3) Phục vụ qua Ollama (tạo Modelfile) hoặc LM Studio (load GGUF/MLX) để chat. Với 24GB có thể LoRA/QLoRA tới ~13-14B.

**Giải thích:** Mac dùng định dạng MLX (mlx-community/...); Ollama/LM Studio là lớp serving.

## Câu 3 (Trắc nghiệm)

Ollama và LM Studio đóng vai trò gì?

- **A.** Lớp inference/serving local, tải, quản lý và chat với model (GGUF/MLX) qua API/GUI (đáp án đúng)
- **B.** Train model from scratch
- **C.** Vector database cho RAG
- **D.** Tokenizer

**Đáp án: A**

**Giải thích:** Chúng giúp chạy model local dễ dàng; Ollama có API kiểu OpenAI tiện cắm vào RAG/agents.

## Câu 4 (Tự luận)

Tóm tắt phân vai 3070 Ti vs Mac 24GB vs Cloud.

**Trả lời mẫu:** 3070 Ti (8GB): code from-scratch, train nhỏ/validate loop, QLoRA 7B-8B nhanh. Mac 24GB: chứa & fine-tune model 13-14B, chạy yên tĩnh local, inference quantized. Cloud (RunPod/Lambda): lần pretrain GPT-2 một lần (~$15-35), full fine-tune, iterate nhanh khi local quá chậm/OOM.

**Giải thích:** Đây là nội dung deliverable 03_hardware_decision.md.

## Câu 5 (Trắc nghiệm)

Theo Ilharco et al. 2022 (task arithmetic, mục 7 theory notes), 'task vector' là gì và cộng/trừ nó dùng để làm gì?

- **A.** Gradient trung bình của batch cuối cùng khi train
- **B.** Một hàng của ma trận LoRA A
- **C.** τ = W_finetuned − W_base, 'hướng' fine-tune đã đẩy model tới trong không gian trọng số; CỘNG nhiều τ để ghép nhiều kỹ năng vào một model, PHỦ ĐỊNH (−τ) để giảm một hành vi mà ít ảnh hưởng task khác (đáp án đúng)
- **D.** Vector embedding của mô tả task, dùng để retrieve adapter phù hợp

**Đáp án: C**

**Giải thích:** Mục 7 của 01_theory_notes.md (arXiv 2212.04089): LoRA adapter merge về được dạng ΔW nên cũng quy về khung task vector. Caveat của repo: merging là kỹ thuật THỰC NGHIỆM, merge xong bắt buộc chạy lại bộ 10 prompt song ngữ + eval nghiệp vụ, chỉ giữ bản merge khi số đo không tụt.

## Câu 6 (Tự luận)

Mô tả quy trình kiểm tra catastrophic forgetting song ngữ bắt buộc của repo (mục 5 theory notes) và làm gì khi phát hiện suy giảm.

**Trả lời mẫu:** 1) TRƯỚC khi fine-tune: chốt bộ 10 prompt cố định (5 tiếng Việt + 5 tiếng Anh, có cả nghiệp vụ lẫn thường thức), sinh và lưu output của base. 2) SAU fine-tune: chạy đúng 10 prompt đó ở temperature 0, so từng cặp output. 3) Nếu suy giảm rõ ở tiếng Anh: giảm tỷ lệ data một chiều, trộn thêm data tiếng Anh rồi train lại. Bộ 10 prompt giữ cố định vĩnh viễn, là 'bài kiểm tra sức khỏe song ngữ' cho mọi model sau này của dự án (kể cả mọi bản merge ở mục 7).

**Giải thích:** Mục 5 của 01_theory_notes.md. Chỗ dựa từ paper: Biderman et al. 2024 (arXiv 2405.09673) đo được full fine-tuning quên kiến thức ngoài domain đích nhiều hơn hẳn LoRA, mức quên PHỤ THUỘC cách fine-tune, nên chỉ có đo mới biết mình ở đâu trên trade-off.

## Câu 7 (Trắc nghiệm)

Theo FoLLM, vì sao prefilling được coi là compute-bound còn decoding là memory-bound?

- **A.** Prefilling xử lý cả chuỗi x trong một lần self-attention song song nên nút thắt là năng lực tính toán; decoding sinh từng token và truy cập KV cache liên tục nên nút thắt là bộ nhớ (đáp án đúng)
- **B.** Prefilling chạy trên CPU để chuẩn bị embedding và mask cho toàn bộ prompt; decoding chạy trên GPU nơi dung lượng bộ nhớ là giới hạn chính của hệ thống
- **C.** Prefilling không dùng KV cache nên phải tính lại attention cho mọi cặp token; decoding lưu toàn bộ activation của mọi layer nên bộ nhớ tăng theo số token sinh ra
- **D.** Prefilling phải tính softmax trên toàn bộ vocabulary cho mọi vị trí của prompt nên nặng về tính toán; decoding chỉ tính một softmax mỗi bước nên phần còn lại là chi phí đọc trọng số

**Đáp án: A**

**Giải thích:** FoLLM: "since the entire sequence x is input into the model all at once, all queries can be packed together and the self-attention operation is performed on x in parallel ... the prefilling process is considered compute-bound." và "the decoding process is memory-bound due to its frequent access to the KV cache." Table 5.1 tóm tắt Resource Limitation: Compute-bound so với Memory-bound. (FoLLM mục 5.1.2, tr. 209-211)

## Câu 8 (Trắc nghiệm)

FoLLM so sánh giai đoạn prefilling với BERT. Điểm giống và điểm khác là gì?

- **A.** Giống ở việc mã hóa chuỗi đầu vào thành biểu diễn ngữ cảnh (ở đây là KV cache) thay vì sinh token; khác ở việc prefilling là một chiều (đáp án đúng)
- **B.** Giống ở việc dùng masked language modeling để học biểu diễn; khác ở việc prefilling không có lớp softmax đầu ra
- **C.** Giống ở việc dùng một encoder riêng cho input; khác ở việc prefilling chia sẻ tham số với decoder sinh token
- **D.** Giống ở việc xử lý toàn bộ chuỗi song song trên GPU; khác ở việc BERT không dùng self-attention nhân quả

**Đáp án: A**

**Giải thích:** FoLLM: "it can be considered an encoding process. This is because our goal is not to generate tokens, but to build a context representation (i.e., the KV cache) ... it is similar to BERT ... On the other hand, unlike BERT which generates bidirectional sequence representations, prefilling is based on standard language modeling tasks, and is thus unidirectional." Mask trong eq. 5.13 đặt −∞ cho các vị trí tương lai. (FoLLM mục 5.1.2, tr. 209)

## Câu 9 (Trắc nghiệm)

Khi benchmark inference trên Mac và trên 3070 Ti, metric nào của FoLLM phản ánh chủ yếu chi phí prefilling, và metric nào phản ánh hiệu quả decoding?

- **A.** Tokens Per Second phản ánh prefilling; Resource Utilization phản ánh decoding
- **B.** Request Latency phản ánh prefilling; Throughput phản ánh decoding
- **C.** Throughput phản ánh prefilling; Request Latency phản ánh decoding
- **D.** Time to First Token phản ánh prefilling; Inter-token Latency phản ánh decoding (đáp án đúng)

**Đáp án: D**

**Giải thích:** FoLLM: "If data transmission does not consume too much time, then TTFT is mainly the time for prefilling and predicting the first token." và ITL "refers to the time taken to generate each subsequent token after the first one. It reflects the efficiency of the decoding process." (FoLLM mục 5.1.4, tr. 222)

## Câu 10 (Trắc nghiệm)

Trong mục 2.3.3.1, FoLLM nêu các cách làm KV cache có kích thước cố định. Cách nào chỉ cần lưu một cặp key-value duy nhất trong lúc suy luận?

- **A.** Trung bình động có trọng số của nc cặp gần nhất với các hệ số β tăng dần theo vị trí
- **B.** Trung bình cộng dồn của toàn bộ key và value tới vị trí hiện tại, cập nhật theo công thức đệ quy (đáp án đúng)
- **C.** Một mạng neural làm bộ nhớ, nhận đầu ra bộ nhớ trước và trạng thái hiện tại để sinh đầu ra mới
- **D.** Cửa sổ trượt gồm nc cặp key-value gần nhất, được xem là một dạng local attention

**Đáp án: B**

**Giải thích:** Với cumulative average, Mem_i = ((k_i, v_i) + i · Mem_{i−1}) / (i + 1) (eq. 2.57); FoLLM: "An advantage of this model is that we only need to store a single key-value pair during inference, rather than storing all the key-value pairs." Cửa sổ nc cặp (eq. 2.53) vẫn phải lưu nc cặp và "can be seen as a type of local attention model". (FoLLM mục 2.3.3.1, tr. 72-73)

## Câu 11 (Trắc nghiệm)

FoLLM mô tả trade-off khi chọn batch size trong inference. Phát biểu nào đúng?

- **A.** Batch nhỏ cho throughput cao hơn vì ít padding hơn; batch lớn cho latency thấp hơn nhờ các chuỗi chia sẻ chung một KV cache
- **B.** Batch nhỏ cho latency thấp hơn nhưng để GPU nhàn rỗi; batch lớn tận dụng song song tốt hơn nhưng phải padding và chờ chuỗi dài nhất xong (đáp án đúng)
- **C.** Batch nhỏ và batch lớn cho cùng throughput trên GPU; khác biệt chỉ nằm ở lượng VRAM dành cho KV cache của mỗi chuỗi
- **D.** Batch lớn luôn tốt hơn về cả latency và throughput miễn là còn đủ VRAM; batch nhỏ chỉ dùng khi hết bộ nhớ

**Đáp án: B**

**Giải thích:** FoLLM: "If we choose a smaller batch size, the latency would be lower ... However, this low-latency advantage comes at the cost of underutilizing parallel computing resources, as the parallelism of GPUs remains largely idle during sequential processing." Với batch 4, chuỗi ngắn được left padding và "the generation process continues until the longest sequence reaches completion". (FoLLM mục 5.2.2, tr. 224-225)

## Câu 12 (Trắc nghiệm)

Hệ thống của bạn dùng một system prompt dài giống nhau cho mọi request. Kỹ thuật nào trong FoLLM mục 5.2.1 giúp tránh tính lại phần này, và nó hoạt động thế nào?

- **A.** Continuous batching: gộp các request có cùng system prompt vào một batch để tính attention chung một lần
- **B.** Fixed-size KV cache: cắt bỏ phần system prompt khỏi cache ngay sau khi prefilling xong để tiết kiệm bộ nhớ
- **C.** Prefix cache: lưu KV cache của các tiền tố; request mới có chung tiền tố x<k thì khởi tạo KV cache bằng cache<k và chỉ tính các token còn lại (đáp án đúng)
- **D.** Sequence-level cache: lưu cặp query-response, có tác dụng khi input mới trùng khớp chính xác với một query đã lưu

**Đáp án: C**

**Giải thích:** FoLLM: "if a new input x′ has x′<k = x<k for some k ≤ m, we can initialize the KV cache with cache<k and only compute the hidden states for the remaining tokens x′≥k." Tra cứu bằng hash của các token tiền tố; hệ thống thực tế thường dùng LRU để cân bằng bộ nhớ. Sequence-level cache chỉ dùng được khi input "exactly matches a cached query". (FoLLM mục 5.2.1, tr. 223)

## Câu 13 (Tự luận)

FoLLM viết log Pr(y|x) = log Pr([x, y]) − log Pr(x) rồi nói trong cài đặt thực tế người ta tính trực tiếp theo cách khác. Hãy nêu cách tính trực tiếp đó và hai bài toán con mà FoLLM tách ra từ bài toán inference.

**Trả lời mẫu:** Trong cài đặt thông thường không cần tính log-xác suất của input; ta tính thẳng log Pr(y|x) bằng tổng từ i = 1 đến n của log Pr(yi | x, y<i), trong đó [x, y<i] là ngữ cảnh để dự đoán yi (eq. 5.4). Hai bài toán con là Model Computation, tức mô hình hóa và tính Pr(yi | x, y<i) hiệu quả bằng Transformer decoder với softmax chỉ lấy tại vị trí m + i, và Search, tức tìm chuỗi output tối ưu hoặc gần tối ưu theo log Pr(y|x) bằng các thuật toán decoding ở mục 5.1.3.

**Giải thích:** FoLLM eq. 5.2 đến 5.4 và đoạn: "Now, we have two sub-problems in addressing the inference issue described in Eq. (5.1): Model Computation: we model Pr(yi|x, y<i) and compute it in an efficient manner. Search: we find the optimal (or sub-optimal) output sequence in terms of log Pr(y|x)." (FoLLM mục 5.1.1, tr. 204-205)

## Câu 14 (Tự luận)

So sánh request-level scheduling và continuous batching theo FoLLM. Vì sao continuous batching giảm lãng phí khi các response trong batch có độ dài rất khác nhau?

**Trả lời mẫu:** Với request-level scheduling, khi một batch đã được gửi vào inference engine thì không thể ngắt; scheduler phải chờ cả batch xong mới xử lý batch tiếp theo. Continuous batching (dùng trong hệ thống Orca) là iteration-based scheduling: một iteration là toàn bộ prefilling hoặc một bước decoding, và batch có thể được điều chỉnh giữa các iteration, thêm chuỗi mới hoặc bỏ chuỗi đã hoàn thành ngay cả khi batch chưa xong. Nhờ đó chuỗi ngắn kết thúc sớm nhường chỗ cho request mới, thay vì GPU tiếp tục tính cho các vị trí vô nghĩa cho tới khi chuỗi dài nhất hoàn tất như trong batching tĩnh.

**Giải thích:** FoLLM: "once a batch is filled and sent to the engine, the processing of the entire batch cannot be interrupted." và "In this method, an iteration refers to either the entire prefilling procedure or a single decoding step ... we can either add a new input sequence to the batch, or remove a complete sequence from the batch at some iteration, even if the batch processing is not yet finished." (FoLLM mục 5.2.2.1-5.2.2.2, tr. 225-226)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Rolling buffer cache của Mistral 7B hoạt động thế nào và cho tiết kiệm bao nhiêu theo paper?

- **A.** Cache chỉ giữ token đầu tiên
- **B.** Cache có kích thước cố định W; cặp K, V ở bước i ghi vào ô i mod W nên khi i vượt W cache ghi đè và không lớn thêm; ở chuỗi 32k paper báo giảm 8 lần bộ nhớ cache mà không ảnh hưởng chất lượng (đáp án đúng)
- **C.** Cache lưu toàn bộ K, V nhưng nén 8 bit
- **D.** Cache lưu trên CPU

**Đáp án: B**

**Giải thích:** Mistral 7B mục 2 (arXiv 2310.06825), Rolling Buffer Cache. FoLLM mục 2.3.3.1 gọi cùng ý là fixed-size KV cache.

## Nâng cao 2 (Tự luận)

Khi đo tốc độ inference trên Mac và trên 3070 Ti, vì sao nên tách tốc độ prefill và tốc độ decode thay vì báo một con số tokens mỗi giây?

**Trả lời mẫu:** Inference gồm hai pha (FoLLM mục 5.1.2, trang 207): prefill xử lý cả prompt trong một lượt nên gom nhiều token vào một lần nhân ma trận, còn decode sinh từng token và mỗi bước đọc lại toàn bộ trọng số và KV cache, bị giới hạn bởi băng thông bộ nhớ (Fleuret mục 8.2; Leviathan et al. mục 1). Hai pha có nút thắt khác nhau nên một con số gộp che mất việc máy nào mạnh ở pha nào; prompt dài với câu trả lời ngắn và ngược lại cho cảm giác rất khác.

**Giải thích:** Ghi tách hai số cho mỗi máy vào 03_hardware_decision.md.
