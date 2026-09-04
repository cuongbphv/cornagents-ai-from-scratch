# Tuần 4, Đáp án & Giải thích: PyTorch core: từ NumPy sang tensor, autograd, training loop

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Một nn.Linear(in, out) thực chất tính gì?

- **A.** y = W @ x luôn luôn, không có bias
- **B.** y = x @ W + b với W có shape (in, out)
- **C.** y = softmax(x @ W)
- **D.** y = x @ W^T + b với W lưu shape (out, in) (đáp án đúng)

**Đáp án: D**

**Giải thích:** PyTorch lưu weight shape (out, in), nên forward là y = x @ W^T + b. Đây là khối tuyến tính cơ bản lặp lại khắp transformer.

## Câu 2 (Trắc nghiệm)

Mục đích chính của softmax là gì?

- **A.** Tính gradient của cross-entropy
- **B.** Biến một vector logits thành phân phối xác suất (mọi phần tử dương, tổng = 1) (đáp án đúng)
- **C.** Loại bỏ giá trị âm như ReLU
- **D.** Chuẩn hoá vector về độ dài 1

**Đáp án: B**

**Giải thích:** softmax(z)_i = e^{z_i} / sum_j e^{z_j}: mũ hoá làm mọi giá trị dương, chia tổng làm chúng cộng lại bằng 1 → phân phối xác suất trên các lớp/token.

## Câu 3 (Tự luận)

Chain rule liên quan thế nào tới backpropagation?

**Trả lời mẫu:** Backprop = áp dụng chain rule lan ngược qua đồ thị tính toán. Đạo hàm của loss theo một tham số ở lớp sâu = tích các đạo hàm cục bộ dọc đường đi: dL/dw = dL/dg · dg/dw. Mỗi lớp chỉ cần biết đạo hàm cục bộ của nó và nhận gradient từ lớp sau, nhân vào, rồi truyền tiếp về trước.

**Giải thích:** Đây là toàn bộ ý tưởng của autograd: lưu đồ thị forward, rồi nhân dồn đạo hàm cục bộ theo chiều ngược lại.

## Câu 4 (Trắc nghiệm)

Cross-entropy loss L_CE = -sum_i y_i log(y_hat_i) đo điều gì?

- **A.** Phương sai của logits
- **B.** Số token dự đoán sai
- **C.** Độ 'bất ngờ' của phân phối dự đoán so với nhãn thật, phạt nặng khi gán xác suất thấp cho lớp đúng (đáp án đúng)
- **D.** Khoảng cách Euclid giữa dự đoán và nhãn

**Đáp án: C**

**Giải thích:** Với nhãn one-hot, L_CE = -log(xác suất gán cho lớp đúng). Gán xác suất gần 1 cho lớp đúng → loss ~0; gần 0 → loss rất lớn.

## Câu 5 (Trắc nghiệm)

Cộng tensor shape (B, 1, D) với (1, T, D) bằng broadcasting cho ra shape nào?

- **A.** (B, 1, D)
- **B.** (B, T, 1)
- **C.** (B, T, D) (đáp án đúng)
- **D.** Lỗi, không broadcast được

**Đáp án: C**

**Giải thích:** Broadcasting căn phải các chiều; chiều bằng 1 được 'kéo dài'. (B,1,D) và (1,T,D) → (B,T,D). Hiểu broadcasting là chìa khoá đọc code attention.

## Câu 6 (Tự luận)

torch.no_grad() và requires_grad khác nhau thế nào, dùng khi nào?

**Trả lời mẫu:** requires_grad=True đánh dấu một tensor cần theo dõi để tính gradient (tham số train được). torch.no_grad() là context tắt việc xây đồ thị autograd cho mọi phép tính bên trong, dùng khi inference/đánh giá hoặc cập nhật tham số thủ công, để tiết kiệm bộ nhớ và tránh tính gradient thừa.

**Giải thích:** Quên no_grad() khi eval/generate là lỗi VRAM phổ biến, nhất là trên card 8GB.

## Câu 7 (Trắc nghiệm)

Dot product giữa hai vector đo điều gì (ý nghĩa cho attention)?

- **A.** Độ 'cùng hướng' / tương đồng, lớn khi hai vector cùng hướng (đáp án đúng)
- **B.** Góc tuyệt đối tính bằng độ
- **C.** Tổng bình phương các phần tử
- **D.** Luôn là khoảng cách giữa hai điểm

**Đáp án: A**

**Giải thích:** a·b = |a||b|cosθ. Trong attention, query·key chính là điểm tương đồng dùng để quyết định token nào 'chú ý' tới token nào.

## Câu 8 (Tự luận)

Ở Tuần 3 bạn viết logistic regression bằng NumPy với hàm grad tự tính và kiểm bằng sai phân. Khi viết lại bằng PyTorch, dòng nào thay cho hàm grad, dòng nào thay cho phép cập nhật w -= lr * grad, và vì sao xuất hiện thêm bước zero_grad() mà vòng lặp NumPy không cần?

**Trả lời mẫu:** loss.backward() thay cho hàm grad: autograd áp chain rule ngược trên đồ thị tính toán và điền vào .grad của từng tham số. optimizer.step() thay cho w -= lr * grad, với lr là step size. Bước zero_grad() cần vì PyTorch cộng dồn gradient vào .grad qua các lần backward (thiết kế phục vụ gradient accumulation); vòng lặp NumPy tính gradient mới mỗi lần nên không có gì để xóa. Cách kiểm bằng sai phân của Tuần 2 vẫn dùng được để đối chiếu .grad.

**Giải thích:** Đây là toàn bộ 'phần mới' của Tuần 4: đổi công cụ, không đổi toán. Nếu bạn chỉ ra được ba dòng này thì đã nối xong Phase 0 với PyTorch.

## Câu 9 (Trắc nghiệm)

UDL mục 5.1.3 chuyển từ cực đại likelihood (tích các Pr(y_i|f[x_i, ϕ])) sang cực đại log-likelihood (tổng các log). Lý do thực tế mà Prince nêu là gì, và vì sao phép chuyển này không làm đổi nghiệm tối ưu?

- **A.** Vì logarit đổi dấu các số hạng, biến bài toán cực đại thành cực tiểu mà không cần nhân thêm hệ số âm nào, nên hai bài toán trùng nghiệm.
- **B.** Vì logarit biến tích thành tổng, tránh tích của nhiều xác suất nhỏ khó biểu diễn bằng số học độ chính xác hữu hạn, mà vị trí cực đại vẫn giữ nguyên do log đơn điệu tăng. (đáp án đúng)
- **C.** Vì logarit làm hàm mất mát trở thành lồi, nên gradient descent luôn tìm được cực tiểu toàn cục bất kể điểm khởi đầu, và nghiệm vì thế không đổi.
- **D.** Vì logarit làm giảm phương sai của gradient qua các minibatch, nên SGD hội tụ nhanh hơn về cùng một nghiệm so với dùng likelihood thô.

**Đáp án: B**

**Giải thích:** Prince viết mỗi số hạng Pr(y_i|f[x_i, ϕ]) có thể rất nhỏ nên tích của nhiều số hạng "can be tiny" và khó biểu diễn với finite precision arithmetic; log là hàm đơn điệu tăng nên cực đại của g[z] và log[g[z]] ở cùng vị trí (Figure 5.2), và tổng thay cho tích thì biểu diễn số không còn là vấn đề. Đây cũng là lý do trong code bạn luôn cộng log-prob thay vì nhân xác suất. (UDL mục 5.1.3, tr. 59)

## Câu 10 (Trắc nghiệm)

UDL mục 5.7 xuất phát từ việc cực tiểu KL divergence giữa phân phối thực nghiệm q(y) (tổng các hàm delta Dirac tại các điểm dữ liệu) và phân phối model Pr(y|θ). Số hạng nào trong KL biến mất khi tối ưu theo θ, và kết quả cuối cùng là gì?

- **A.** Hệ số 1/I biến mất vì phân phối thực nghiệm đã được chuẩn hóa; nhờ đó KL trở thành entropy của model và trùng với negative log-likelihood.
- **B.** Số hạng tích phân q log Pr(y|θ) biến mất vì các delta Dirac tích phân về 0; phần còn lại là entropy của dữ liệu và trùng với negative log-likelihood.
- **C.** Không số hạng nào biến mất; KL được giữ nguyên rồi xấp xỉ bằng khai triển Taylor bậc một quanh θ để thu được negative log-likelihood.
- **D.** Số hạng tích phân q log q biến mất vì không phụ thuộc θ; phần còn lại là cross-entropy, và sau khi thay q bằng tổng các delta Dirac thì đúng bằng negative log-likelihood. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Trong công thức 5.29, số hạng thứ nhất của KL (tích phân q(y) log q(y)) "disappears, as it has no dependence on θ"; số hạng còn lại là cross-entropy. Thay q(y) = (1/I) Σ δ[y - y_i] vào cho tổng -Σ log Pr(y_i|θ) (công thức 5.30, hệ số 1/I bị bỏ vì không đổi vị trí cực tiểu), chính là tiêu chí negative log-likelihood của mục 5.2. Vì vậy loss cross-entropy mà bạn gọi trong PyTorch và NLL là một. (UDL mục 5.7, tr. 72)

## Câu 11 (Trắc nghiệm)

Trong phần "Engineering the loss", Fleuret giải thích vì sao bài toán phân loại được huấn luyện bằng cross-entropy dù chỉ số ta thực sự quan tâm là tỉ lệ lỗi phân loại. Lý do đó là gì?

- **A.** Vì tỉ lệ lỗi phân loại không có gradient mang thông tin, còn cross-entropy là một proxy dễ tối ưu hơn mà vẫn hướng model về cùng mục tiêu. (đáp án đúng)
- **B.** Vì tỉ lệ lỗi phân loại cần nhãn dạng one-hot, còn cross-entropy chỉ cần logit chưa chuẩn hóa của model, tiết kiệm bộ nhớ khi batch lớn.
- **C.** Vì tỉ lệ lỗi phân loại chỉ tính được trên tập test còn cross-entropy tính được trên tập train, nên chỉ cross-entropy mới dùng được để cập nhật tham số.
- **D.** Vì cross-entropy luôn cho giá trị nhỏ hơn tỉ lệ lỗi nên đường cong loss trông mượt hơn, thuận tiện khi theo dõi quá trình huấn luyện.

**Đáp án: A**

**Giải thích:** Fleuret viết loss được cực tiểu khi train thường không phải đại lượng ta muốn tối ưu sau cùng mà là một proxy dễ tìm tham số hơn: cross-entropy là loss chuẩn cho phân loại "even though the actual performance measure is a classification error rate, because the latter has no informative gradient". Điều này giải thích vì sao trong training loop bạn theo dõi cross-entropy nhưng khi đánh giá lại nhìn accuracy hay perplexity. (Fleuret mục 3.1, tr. 28)

## Câu 12 (Trắc nghiệm)

UDL mục 6.2.1 đưa ra một cách diễn giải khác về stochastic gradient descent so với cách nhìn "thêm nhiễu vào gradient". Cách diễn giải đó là gì?

- **A.** SGD chọn ngẫu nhiên một tập con tham số để cập nhật ở mỗi bước, nên tính trung bình theo thời gian mọi tham số đều được cập nhật giống gradient descent.
- **B.** SGD tính gradient chính xác trên toàn bộ dữ liệu rồi cộng thêm nhiễu Gaussian có phương sai tỉ lệ với learning rate để thoát khỏi cực tiểu địa phương.
- **C.** SGD thực hiện gradient descent xác định trên một hàm mất mát thay đổi theo từng batch, nhưng kỳ vọng của loss và của gradient tại mọi điểm vẫn bằng của gradient descent thường. (đáp án đúng)
- **D.** SGD tính gradient của cùng một hàm mất mát nhưng làm tròn về độ chính xác thấp hơn ở mỗi bước, và chính sai số làm tròn đó đóng vai trò nhiễu ngẫu nhiên.

**Đáp án: C**

**Giải thích:** Prince viết SGD có thể xem như tính gradient của một hàm mất mát khác ở mỗi vòng lặp vì loss phụ thuộc cả model và batch được chọn; theo cách nhìn này "SGD performs deterministic gradient descent on a constantly changing loss function" (Figure 6.6), song "the expected loss and expected gradients at any point remain the same as for gradient descent". Đây là lý do mỗi batch trong training loop của bạn cho một hướng khác nhau nhưng trung bình vẫn đi xuống. (UDL mục 6.2.1, tr. 85)

## Câu 13 (Trắc nghiệm)

Trong Adam (UDL mục 6.4), sau khi tính m_{t+1} và v_{t+1} bằng momentum, Prince hiệu chỉnh chúng thành m̃ = m/(1 - β^{t+1}) và ṽ = v/(1 - γ^{t+1}) (công thức 6.16). Vì sao cần bước này?

- **A.** Vì gradient ở các lớp sâu có độ lớn khác nhau, cần chia cho một hệ số phụ thuộc thời gian để cân bằng mức cập nhật giữa các lớp trong mạng.
- **B.** Vì learning rate α cần giảm dần theo lịch, và phép chia này chính là cách Adam cài sẵn lịch giảm learning rate mà không cần scheduler ngoài.
- **C.** Vì ở đầu quá trình các phép đo trước đó thực chất bằng 0, khiến ước lượng trung bình có trọng số nhỏ một cách phi thực tế; hiệu chỉnh giảm dần tác dụng khi t tăng. (đáp án đúng)
- **D.** Vì ε trong mẫu số quá nhỏ ở các bước đầu, nên phải phóng đại m và v để phép chia cho căn bậc hai không bị tràn số về 0 ở những bước cập nhật đầu tiên.

**Đáp án: C**

**Giải thích:** Prince giải thích dùng momentum tương đương lấy trung bình có trọng số theo lịch sử; "At the start of the procedure, all the previous measurements are effectively zero, resulting in unrealistically small estimates", nên phải chia cho 1 - β^{t+1} và 1 - γ^{t+1}. Vì β, γ thuộc [0, 1) nên các lũy thừa nhỏ dần, mẫu số tiến về 1 và "this modification has a diminishing effect". Các lựa chọn về cân bằng lớp hay lịch learning rate mô tả tác dụng khác của Adam, không phải lý do của bước hiệu chỉnh này. (UDL mục 6.4, tr. 90)

## Câu 14 (Trắc nghiệm)

Theo UDL mục 6.3, việc thêm momentum m_{t+1} = β m_t + (1 - β) Σ ∂ℓ_i/∂ϕ ảnh hưởng thế nào đến độ lớn bước đi hiệu dụng của SGD?

- **A.** Bước hiệu dụng tăng khi các gradient liên tiếp cùng hướng, và giảm khi hướng gradient đổi liên tục vì các số hạng trong tổng triệt tiêu lẫn nhau. (đáp án đúng)
- **B.** Bước hiệu dụng luôn nhỏ hơn α vì hệ số (1 - β) làm co gradient hiện tại trước khi cộng vào, nên momentum chủ yếu làm chậm quá trình học.
- **C.** Bước hiệu dụng không đổi so với SGD thường; momentum chỉ xoay hướng đi về phía gradient trung bình mà không đổi độ dài mỗi bước.
- **D.** Bước hiệu dụng luôn lớn hơn α vì momentum cộng dồn mọi gradient trước đó với trọng số bằng nhau, làm quỹ đạo dài hơn ở mọi bước.

**Đáp án: A**

**Giải thích:** Prince viết công thức đệ quy làm bước gradient trở thành tổng có trọng số vô hạn của mọi gradient trước đó với trọng số giảm dần về quá khứ: "The effective learning rate increases if all these gradients are aligned over multiple iterations but decreases if the gradient direction repeatedly changes as the terms in the sum cancel out." Kết quả là quỹ đạo mượt hơn và ít dao động trong các thung lũng (Figure 6.7). (UDL mục 6.3, tr. 86)

## Câu 15 (Tự luận)

UDL mục 5.2 tóm tắt "recipe" bốn bước để xây dựng hàm mất mát theo maximum likelihood. Hãy ánh xạ từng bước vào bài toán dự đoán token kế tiếp trong GPT mà bạn tự cài: phân phối nào được chọn, phần nào của mạng tính tham số phân phối, loss nào được cực tiểu, và khi generate bạn trả về gì?

**Trả lời mẫu:** Bước 1: chọn một phân phối xác suất rời rạc trên |V| token của vocabulary. Bước 2: mạng f[x, ϕ] (các block transformer rồi lm_head) tính tham số của phân phối đó, tức logits rồi softmax thành Pr(token|ngữ cảnh). Bước 3: tìm ϕ cực tiểu negative log-likelihood -Σ log Pr(y_i|f[x_i, ϕ]) trên các cặp (ngữ cảnh, token đúng), chính là cross-entropy loss trong training loop. Bước 4: khi sinh văn bản trả về hoặc cả phân phối (để sample) hoặc giá trị làm phân phối cực đại (greedy).

**Giải thích:** Prince liệt kê bốn bước: (1) chọn phân phối Pr(y|θ) trên miền đầu ra, (2) cho model dự đoán tham số θ = f[x, ϕ], (3) cực tiểu negative log-likelihood -Σ log Pr(y_i|f[x_i, ϕ]) (công thức 5.6), (4) khi suy luận trả về "either the full distribution Pr(y|f[x, ϕ̂]) or the value where this distribution is maximized". Mục 5.7 sau đó chỉ ra tiêu chí này trùng với cross-entropy. (UDL mục 5.2, tr. 60)

## Câu 16 (Tự luận)

UDL mục 6.1.3 mô tả saddle point trên mặt loss của Gabor model. Vì sao tiêu chí dừng "gradient đủ nhỏ" trong training loop có thể đánh lừa bạn ở gần saddle point, và mục 6.2.2 nói SGD giúp gì trong tình huống này?

**Trả lời mẫu:** Tại saddle point gradient bằng 0 nhưng hàm tăng theo hướng này và giảm theo hướng khác, và mặt loss quanh đó rất phẳng; nếu dừng khi gradient nhỏ ta có thể tưởng đã hội tụ trong khi mới chỉ ở gần saddle point. SGD giảm khả năng kẹt ở đó vì gradient được tính trên từng batch khác nhau, và nhiều khả năng ít nhất một số batch có gradient đáng kể tại điểm đó, đẩy tham số đi tiếp.

**Giải thích:** Prince viết về saddle point: "the surface near the saddle point is flat, so it's hard to be sure that training hasn't converged; if we terminate the algorithm when the gradient is small, we may erroneously stop near a saddle point" (mục 6.1.3, tr. 83). Trong danh sách ưu điểm của SGD ở mục 6.2.2, điểm thứ năm là nó giảm khả năng kẹt gần saddle point vì "at least some of the possible batches will have a significant gradient at any point on the loss function". (UDL mục 6.2.2, tr. 83-86)

## Câu 17 (Tự luận)

Fleuret định nghĩa cross-entropy trực tiếp từ logit f(x;w)_y. Hãy viết lại công thức ước lượng P̂(Y = y | X = x) và ℒ_ce(w) theo Fleuret, rồi giải thích vì sao hàm loss trong code của bạn nhận logit thô chứ không phải xác suất đã qua softmax.

**Trả lời mẫu:** Mỗi thành phần f(x;w)_y được hiểu là log của một xác suất chưa chuẩn hóa (logit). Xác suất hậu nghiệm là P̂(Y = y | X = x) = exp f(x;w)_y / Σ_z exp f(x;w)_z, tức softmax (Fleuret gọi chính xác hơn là softargmax). Cross-entropy là ℒ_ce(w) = -(1/N) Σ_n log P̂(Y = y_n | X = x_n) = (1/N) Σ_n [-log(exp f(x_n;w)_{y_n} / Σ_z exp f(x_n;w)_z)]. Vì công thức loss đã chứa sẵn bước chuẩn hóa softmax bên trong, đầu vào tự nhiên của nó là vector logit; đưa xác suất đã softmax vào sẽ là áp softmax hai lần và sai công thức.

**Giải thích:** Fleuret: đầu ra model là vector có một thành phần f(x;w)_y cho mỗi lớp, "interpreted as the logarithm of a non-normalized probability, or logit"; từ đó P̂(Y = y | X = x) = exp f(x;w)_y / Σ_z exp f(x;w)_z (tr. 26) và ℒ_ce(w) = -(1/N) Σ log P̂(Y = y_n | X = x_n), với số hạng bên trong ký hiệu L_ce(f(x_n;w), y_n) (tr. 27). (Fleuret mục 3.1, tr. 26)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

nanoGPT đặt dropout = 0.0 cho pretraining với comment 'for pretraining 0 is good, for finetuning try 0.1+'. Khung nào của Tuần 3 giải thích lựa chọn này?

- **A.** Dropout chỉ hoạt động với LayerNorm
- **B.** Dropout không tương thích với bf16
- **C.** Dropout làm chậm GPU nên bỏ khi có nhiều dữ liệu
- **D.** Pretraining chạy trên dữ liệu rất lớn, thường dưới một epoch, nên estimation error nhỏ và regularization kiểu dropout ít cần; fine-tune trên dữ liệu nhỏ dễ overfit nên cần regularization hơn (đáp án đúng)

**Đáp án: D**

**Giải thích:** Giá trị đọc từ nanoGPT/train.py ngày 2026-09-04. Lý giải theo error decomposition của UML mục 5.2 là suy luận của người viết dựa trên khung lý thuyết, không phải kết luận trong code.

## Nâng cao 2 (Tự luận)

Vì sao PyTorch cộng dồn gradient vào .grad thay vì ghi đè, và kỹ thuật nào trong nanoGPT dựa trực tiếp vào hành vi đó?

**Trả lời mẫu:** Cộng dồn cho phép gọi backward nhiều lần trên nhiều micro-batch rồi mới step một lần, tức gradient accumulation; nanoGPT có gradient_accumulation_steps = 5 * 8 với comment 'used to simulate larger batch sizes'. Hệ quả là mỗi lần bắt đầu tích lũy phải zero_grad, còn micrograd Tuần 5 cũng phải dùng += trong _backward vì một node có thể được dùng ở nhiều nhánh.

**Giải thích:** Trên card 8GB, gradient accumulation là cách duy nhất đạt effective batch lớn; hiểu cơ chế cộng dồn giúp tránh lỗi quên zero_grad.
