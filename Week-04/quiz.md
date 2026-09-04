# Tuần 4, Quiz: PyTorch core: từ NumPy sang tensor, autograd, training loop

> Tự kiểm tra **trước** khi xem solution. Tổng **19** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Một nn.Linear(in, out) thực chất tính gì?

- **A.** y = W @ x luôn luôn, không có bias
- **B.** y = x @ W + b với W có shape (in, out)
- **C.** y = softmax(x @ W)
- **D.** y = x @ W^T + b với W lưu shape (out, in)

## Câu 2 (Trắc nghiệm)

Mục đích chính của softmax là gì?

- **A.** Tính gradient của cross-entropy
- **B.** Biến một vector logits thành phân phối xác suất (mọi phần tử dương, tổng = 1)
- **C.** Loại bỏ giá trị âm như ReLU
- **D.** Chuẩn hoá vector về độ dài 1

## Câu 3 (Tự luận)

Chain rule liên quan thế nào tới backpropagation?

## Câu 4 (Trắc nghiệm)

Cross-entropy loss L_CE = -sum_i y_i log(y_hat_i) đo điều gì?

- **A.** Phương sai của logits
- **B.** Số token dự đoán sai
- **C.** Độ 'bất ngờ' của phân phối dự đoán so với nhãn thật, phạt nặng khi gán xác suất thấp cho lớp đúng
- **D.** Khoảng cách Euclid giữa dự đoán và nhãn

## Câu 5 (Trắc nghiệm)

Cộng tensor shape (B, 1, D) với (1, T, D) bằng broadcasting cho ra shape nào?

- **A.** (B, 1, D)
- **B.** (B, T, 1)
- **C.** (B, T, D)
- **D.** Lỗi, không broadcast được

## Câu 6 (Tự luận)

torch.no_grad() và requires_grad khác nhau thế nào, dùng khi nào?

## Câu 7 (Trắc nghiệm)

Dot product giữa hai vector đo điều gì (ý nghĩa cho attention)?

- **A.** Độ 'cùng hướng' / tương đồng, lớn khi hai vector cùng hướng
- **B.** Góc tuyệt đối tính bằng độ
- **C.** Tổng bình phương các phần tử
- **D.** Luôn là khoảng cách giữa hai điểm

## Câu 8 (Tự luận)

Ở Tuần 3 bạn viết logistic regression bằng NumPy với hàm grad tự tính và kiểm bằng sai phân. Khi viết lại bằng PyTorch, dòng nào thay cho hàm grad, dòng nào thay cho phép cập nhật w -= lr * grad, và vì sao xuất hiện thêm bước zero_grad() mà vòng lặp NumPy không cần?

## Câu 9 (Trắc nghiệm)

UDL mục 5.1.3 chuyển từ cực đại likelihood (tích các Pr(y_i|f[x_i, ϕ])) sang cực đại log-likelihood (tổng các log). Lý do thực tế mà Prince nêu là gì, và vì sao phép chuyển này không làm đổi nghiệm tối ưu?

- **A.** Vì logarit đổi dấu các số hạng, biến bài toán cực đại thành cực tiểu mà không cần nhân thêm hệ số âm nào, nên hai bài toán trùng nghiệm.
- **B.** Vì logarit biến tích thành tổng, tránh tích của nhiều xác suất nhỏ khó biểu diễn bằng số học độ chính xác hữu hạn, mà vị trí cực đại vẫn giữ nguyên do log đơn điệu tăng.
- **C.** Vì logarit làm hàm mất mát trở thành lồi, nên gradient descent luôn tìm được cực tiểu toàn cục bất kể điểm khởi đầu, và nghiệm vì thế không đổi.
- **D.** Vì logarit làm giảm phương sai của gradient qua các minibatch, nên SGD hội tụ nhanh hơn về cùng một nghiệm so với dùng likelihood thô.

## Câu 10 (Trắc nghiệm)

UDL mục 5.7 xuất phát từ việc cực tiểu KL divergence giữa phân phối thực nghiệm q(y) (tổng các hàm delta Dirac tại các điểm dữ liệu) và phân phối model Pr(y|θ). Số hạng nào trong KL biến mất khi tối ưu theo θ, và kết quả cuối cùng là gì?

- **A.** Hệ số 1/I biến mất vì phân phối thực nghiệm đã được chuẩn hóa; nhờ đó KL trở thành entropy của model và trùng với negative log-likelihood.
- **B.** Số hạng tích phân q log Pr(y|θ) biến mất vì các delta Dirac tích phân về 0; phần còn lại là entropy của dữ liệu và trùng với negative log-likelihood.
- **C.** Không số hạng nào biến mất; KL được giữ nguyên rồi xấp xỉ bằng khai triển Taylor bậc một quanh θ để thu được negative log-likelihood.
- **D.** Số hạng tích phân q log q biến mất vì không phụ thuộc θ; phần còn lại là cross-entropy, và sau khi thay q bằng tổng các delta Dirac thì đúng bằng negative log-likelihood.

## Câu 11 (Trắc nghiệm)

Trong phần "Engineering the loss", Fleuret giải thích vì sao bài toán phân loại được huấn luyện bằng cross-entropy dù chỉ số ta thực sự quan tâm là tỉ lệ lỗi phân loại. Lý do đó là gì?

- **A.** Vì tỉ lệ lỗi phân loại không có gradient mang thông tin, còn cross-entropy là một proxy dễ tối ưu hơn mà vẫn hướng model về cùng mục tiêu.
- **B.** Vì tỉ lệ lỗi phân loại cần nhãn dạng one-hot, còn cross-entropy chỉ cần logit chưa chuẩn hóa của model, tiết kiệm bộ nhớ khi batch lớn.
- **C.** Vì tỉ lệ lỗi phân loại chỉ tính được trên tập test còn cross-entropy tính được trên tập train, nên chỉ cross-entropy mới dùng được để cập nhật tham số.
- **D.** Vì cross-entropy luôn cho giá trị nhỏ hơn tỉ lệ lỗi nên đường cong loss trông mượt hơn, thuận tiện khi theo dõi quá trình huấn luyện.

## Câu 12 (Trắc nghiệm)

UDL mục 6.2.1 đưa ra một cách diễn giải khác về stochastic gradient descent so với cách nhìn "thêm nhiễu vào gradient". Cách diễn giải đó là gì?

- **A.** SGD chọn ngẫu nhiên một tập con tham số để cập nhật ở mỗi bước, nên tính trung bình theo thời gian mọi tham số đều được cập nhật giống gradient descent.
- **B.** SGD tính gradient chính xác trên toàn bộ dữ liệu rồi cộng thêm nhiễu Gaussian có phương sai tỉ lệ với learning rate để thoát khỏi cực tiểu địa phương.
- **C.** SGD thực hiện gradient descent xác định trên một hàm mất mát thay đổi theo từng batch, nhưng kỳ vọng của loss và của gradient tại mọi điểm vẫn bằng của gradient descent thường.
- **D.** SGD tính gradient của cùng một hàm mất mát nhưng làm tròn về độ chính xác thấp hơn ở mỗi bước, và chính sai số làm tròn đó đóng vai trò nhiễu ngẫu nhiên.

## Câu 13 (Trắc nghiệm)

Trong Adam (UDL mục 6.4), sau khi tính m_{t+1} và v_{t+1} bằng momentum, Prince hiệu chỉnh chúng thành m̃ = m/(1 - β^{t+1}) và ṽ = v/(1 - γ^{t+1}) (công thức 6.16). Vì sao cần bước này?

- **A.** Vì gradient ở các lớp sâu có độ lớn khác nhau, cần chia cho một hệ số phụ thuộc thời gian để cân bằng mức cập nhật giữa các lớp trong mạng.
- **B.** Vì learning rate α cần giảm dần theo lịch, và phép chia này chính là cách Adam cài sẵn lịch giảm learning rate mà không cần scheduler ngoài.
- **C.** Vì ở đầu quá trình các phép đo trước đó thực chất bằng 0, khiến ước lượng trung bình có trọng số nhỏ một cách phi thực tế; hiệu chỉnh giảm dần tác dụng khi t tăng.
- **D.** Vì ε trong mẫu số quá nhỏ ở các bước đầu, nên phải phóng đại m và v để phép chia cho căn bậc hai không bị tràn số về 0 ở những bước cập nhật đầu tiên.

## Câu 14 (Trắc nghiệm)

Theo UDL mục 6.3, việc thêm momentum m_{t+1} = β m_t + (1 - β) Σ ∂ℓ_i/∂ϕ ảnh hưởng thế nào đến độ lớn bước đi hiệu dụng của SGD?

- **A.** Bước hiệu dụng tăng khi các gradient liên tiếp cùng hướng, và giảm khi hướng gradient đổi liên tục vì các số hạng trong tổng triệt tiêu lẫn nhau.
- **B.** Bước hiệu dụng luôn nhỏ hơn α vì hệ số (1 - β) làm co gradient hiện tại trước khi cộng vào, nên momentum chủ yếu làm chậm quá trình học.
- **C.** Bước hiệu dụng không đổi so với SGD thường; momentum chỉ xoay hướng đi về phía gradient trung bình mà không đổi độ dài mỗi bước.
- **D.** Bước hiệu dụng luôn lớn hơn α vì momentum cộng dồn mọi gradient trước đó với trọng số bằng nhau, làm quỹ đạo dài hơn ở mọi bước.

## Câu 15 (Tự luận)

UDL mục 5.2 tóm tắt "recipe" bốn bước để xây dựng hàm mất mát theo maximum likelihood. Hãy ánh xạ từng bước vào bài toán dự đoán token kế tiếp trong GPT mà bạn tự cài: phân phối nào được chọn, phần nào của mạng tính tham số phân phối, loss nào được cực tiểu, và khi generate bạn trả về gì?

## Câu 16 (Tự luận)

UDL mục 6.1.3 mô tả saddle point trên mặt loss của Gabor model. Vì sao tiêu chí dừng "gradient đủ nhỏ" trong training loop có thể đánh lừa bạn ở gần saddle point, và mục 6.2.2 nói SGD giúp gì trong tình huống này?

## Câu 17 (Tự luận)

Fleuret định nghĩa cross-entropy trực tiếp từ logit f(x;w)_y. Hãy viết lại công thức ước lượng P̂(Y = y | X = x) và ℒ_ce(w) theo Fleuret, rồi giải thích vì sao hàm loss trong code của bạn nhận logit thô chứ không phải xác suất đã qua softmax.

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

nanoGPT đặt dropout = 0.0 cho pretraining với comment 'for pretraining 0 is good, for finetuning try 0.1+'. Khung nào của Tuần 3 giải thích lựa chọn này?

- **A.** Dropout chỉ hoạt động với LayerNorm
- **B.** Dropout không tương thích với bf16
- **C.** Dropout làm chậm GPU nên bỏ khi có nhiều dữ liệu
- **D.** Pretraining chạy trên dữ liệu rất lớn, thường dưới một epoch, nên estimation error nhỏ và regularization kiểu dropout ít cần; fine-tune trên dữ liệu nhỏ dễ overfit nên cần regularization hơn

## Nâng cao 2 (Tự luận)

Vì sao PyTorch cộng dồn gradient vào .grad thay vì ghi đè, và kỹ thuật nào trong nanoGPT dựa trực tiếp vào hành vi đó?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
