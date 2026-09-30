# Tuần 10, Quiz: Nhập môn alignment: SFT, DPO và các nhánh RL

> Tự kiểm tra **trước** khi xem solution. Tổng **18** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Phân biệt SFT, DPO và GRPO.

## Câu 2 (Trắc nghiệm)

Reward Model (RM) trong RLHF học để làm gì?

- **A.** Chấm điểm/so sánh mức ưu tiên giữa các output để hướng dẫn RL
- **B.** Tokenize dữ liệu
- **C.** Lưu KV cache
- **D.** Sinh phản hồi cuối cùng cho người dùng

## Câu 3 (Trắc nghiệm)

So với PPO/RLHF kinh điển, DPO bỏ được thành phần nào?

- **A.** Bỏ tokenizer
- **B.** Bỏ model tham chiếu (reference)
- **C.** Bỏ dữ liệu ưu tiên (preference)
- **D.** Bỏ việc train reward model riêng và vòng lặp PPO, tối ưu thẳng từ cặp ưu tiên

## Câu 4 (Tự luận)

[Nâng cao] RLVR (Reinforcement Learning from Verifiable Rewards) là gì, vì sao hợp với reasoning?

## Câu 5 (Trắc nghiệm)

[Nâng cao] Bước 'midtrain' (nanochat) nằm ở đâu trong pipeline?

- **A.** Trước pretrain
- **B.** Sau GRPO
- **C.** Thay thế SFT
- **D.** Giữa pretrain và SFT, dạy format hội thoại, special tokens, tool use

## Câu 6 (Tự luận)

Trong RLHF/DPO, thành phần KL divergence (hoặc reference policy) đóng vai trò gì?

## Câu 7 (Tự luận)

Jurafsky và Martin viết rằng các phương pháp alignment bằng dữ liệu ưu tiên hiện nay đứng trên khung reinforcement learning của Sutton và Barto. Hãy đặt tên từng thành phần của khung đó (agent, environment, action, reward, policy) vào bài toán alignment một LLM.

## Câu 8 (Trắc nghiệm)

Dataset HH-RLHF (Bai et al. 2022) bạn dùng tuần này viết tắt của gì, và điều đó nói gì về nội dung các cặp chosen/rejected?

- **A.** 'Human-Human RLHF', data do hai người chat với nhau
- **B.** 'Helpful Hints for RLHF', bộ hướng dẫn gán nhãn
- **C.** 'High-quality Human RLHF', data đã lọc chất lượng cao
- **D.** 'Helpful and Harmless', một phần các cặp chosen/rejected không so 'câu nào hay hơn' mà so 'câu nào AN TOÀN hơn'

## Câu 9 (Tự luận)

Vì sao nói 'refusal là hành vi được HUẤN LUYỆN, không phải bản năng', và vì sao RM/DPO/GRPO không tự đem lại harmlessness?

## Câu 10 (Trắc nghiệm)

Trong mô hình Bradley-Terry mà SLP3 dùng để mô hình hóa preference, nếu hai output có reward gần bằng nhau thì P(oi ≻ oj | x) xấp xỉ bao nhiêu và điều đó phản ánh gì?

- **A.** Xấp xỉ 0.5, phản ánh preference yếu hoặc không có preference giữa hai output
- **B.** Xấp xỉ 1, phản ánh rằng model luôn phải chọn ra một bên thắng rõ ràng trong mỗi cặp
- **C.** Không xác định, vì Bradley-Terry chỉ được định nghĩa khi hai reward khác nhau rõ rệt
- **D.** Xấp xỉ 0, phản ánh rằng cặp dữ liệu này bị coi là nhiễu và không đóng góp vào loss

## Câu 11 (Trắc nghiệm)

Jurafsky và Martin nêu hai khác biệt then chốt giữa RL truyền thống và RL dùng cho alignment LLM. Cặp nào đúng?

- **A.** Không gian hành động là liên tục thay vì rời rạc, và mỗi episode chỉ có đúng một bước quyết định
- **B.** Reward model chỉ là surrogate nhiễu của reward thật, và học bắt đầu từ model đã mạnh nên chỉ cần đẩy nhẹ hành vi
- **C.** Không cần hàm giá trị vì reward cho cả chuỗi, và trajectory ngắn hơn nhiều so với các bài toán game
- **D.** Reward đến từ môi trường và phản ánh sự thật quan sát được, và policy được học từ khởi tạo ngẫu nhiên

## Câu 12 (Trắc nghiệm)

Theo SLP3, DPO phải duy trì bao nhiêu model trong lúc huấn luyện so với PPO, và điều này có ý nghĩa gì khi bạn chạy alignment trên GPU 8GB?

- **A.** 3 model so với 5 của PPO; chênh lệch nhỏ nên VRAM không phải lý do chính để chọn DPO
- **B.** 1 model so với 3 của PPO; nhờ vậy DPO chạy được cả khi không có reference policy trong bộ nhớ
- **C.** 2 model so với 2 của PPO; khác biệt chỉ nằm ở hàm loss chứ không nằm ở bộ nhớ
- **D.** 2 model so với 4 của PPO; ít model hơn và không cần sampling online nên nhẹ hơn về bộ nhớ và tính toán

## Câu 13 (Trắc nghiệm)

Trong cập nhật REINFORCE θ ← θ + α G ∇π(A|S,θ) / π(A|S,θ), Sutton và Barto giải thích vì sao phải chia cho xác suất hành động π(A|S,θ)?

- **A.** Để các hành động được chọn thường xuyên không có lợi thế chỉ vì được cập nhật theo hướng của chúng nhiều lần hơn
- **B.** Để cập nhật hội tụ về policy xác định, vì hành động có xác suất nhỏ sẽ bị đẩy về 0 nhanh hơn
- **C.** Để biến return G thành advantage, loại bỏ phần phương sai do thiếu baseline gây ra trong ước lượng
- **D.** Để chuẩn hóa gradient về độ dài đơn vị, giúp step size α không phụ thuộc vào thang đo của bài toán

## Câu 14 (Trắc nghiệm)

Sutton và Barto nêu một lợi thế của policy softmax theo action preferences (eq. 13.2) so với chọn hành động ε-greedy trên action value. Lợi thế đó là gì?

- **A.** Policy softmax luôn khám phá nhiều hơn vì mọi hành động đều giữ một xác suất tối thiểu bằng ε
- **B.** Policy softmax có thể tiến tới policy xác định, còn ε-greedy luôn giữ xác suất ε chọn hành động ngẫu nhiên
- **C.** Policy softmax hội tụ nhanh hơn vì action preferences tiến về đúng giá trị thật của action value
- **D.** Policy softmax cần ít tham số hơn vì không phải ước lượng action value riêng cho từng hành động

## Câu 15 (Tự luận)

FoLLM mô tả DPO là một dạng offline RL còn PPO là online RL. Hãy nêu lợi ích mà FoLLM gán cho mỗi bên và cho biết vì sao online RL vẫn được xem là có giá trị với LLM dù DPO đơn giản hơn.

## Câu 16 (Tự luận)

Sutton và Barto đưa ra quy tắc chung để vẽ ranh giới giữa agent và environment, và nói riêng về việc tính reward. Hãy nêu quy tắc đó và giải thích vì sao trong RLHF reward model phải được coi là phần của environment chứ không phải của policy.

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

GRPO (DeepSeekMath, arXiv 2402.03300) khác PPO ở điểm cốt lõi nào?

- **A.** GRPO chỉ dùng cho code
- **B.** GRPO không dùng KL
- **C.** GRPO bỏ critic (value network), ước lượng baseline từ điểm của một nhóm output sinh cho cùng prompt
- **D.** GRPO không cần reward

## Nâng cao 2 (Tự luận)

Hãy nối softmax policy của Sutton và Barto (eq. 13.2) với logits của LLM, và chỉ ra vì sao alignment bằng RL không cần thêm lớp nào mới vào model.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
