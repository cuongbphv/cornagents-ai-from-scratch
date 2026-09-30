# Tuần 10, Đáp án & Giải thích: Nhập môn alignment: SFT, DPO và các nhánh RL

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Phân biệt SFT, DPO và GRPO.

**Trả lời mẫu:** SFT (Supervised Fine-Tuning): học bắt chước các phản hồi tốt bằng cross-entropy trên cặp (prompt, response chuẩn). DPO (Direct Preference Optimization): tối ưu trực tiếp từ cặp (chosen, rejected) bằng một loss dạng logistic, BỎ QUA reward model và PPO → đơn giản, ổn định. GRPO (Group Relative Policy Optimization): RL bỏ critic, lấy nhiều sample cho cùng prompt và chuẩn hoá reward theo nhóm; hợp với reward kiểm chứng được (RLVR) → nền của reasoning models.

**Giải thích:** DPO không bắt buộc reward model riêng. RLHF dùng RM/PPO là nhánh khác; GRPO là thuật toán, RLVR mô tả loại reward. Theo tài liệu chương trình mục 6.3 và 11.

## Câu 2 (Trắc nghiệm)

Reward Model (RM) trong RLHF học để làm gì?

- **A.** Chấm điểm/so sánh mức ưu tiên giữa các output để hướng dẫn RL (đáp án đúng)
- **B.** Tokenize dữ liệu
- **C.** Lưu KV cache
- **D.** Sinh phản hồi cuối cùng cho người dùng

**Đáp án: A**

**Giải thích:** RM học từ nhãn ưu tiên của con người, xuất ra điểm scalar; PPO dùng điểm này làm reward. FareedKhan implement RM from scratch.

## Câu 3 (Trắc nghiệm)

So với PPO/RLHF kinh điển, DPO bỏ được thành phần nào?

- **A.** Bỏ tokenizer
- **B.** Bỏ model tham chiếu (reference)
- **C.** Bỏ dữ liệu ưu tiên (preference)
- **D.** Bỏ việc train reward model riêng và vòng lặp PPO, tối ưu thẳng từ cặp ưu tiên (đáp án đúng)

**Đáp án: D**

**Giải thích:** DPO biến bài toán RLHF thành một loss phân loại trực tiếp trên cặp (chosen, rejected), vẫn dùng policy tham chiếu nhưng không cần RM/PPO.

## Câu 4 (Tự luận)

[Nâng cao] RLVR (Reinforcement Learning from Verifiable Rewards) là gì, vì sao hợp với reasoning?

**Trả lời mẫu:** RLVR dùng reward KIỂM CHỨNG ĐƯỢC một cách khách quan: đáp án toán đúng/sai, unit test code pass/fail, thay vì điểm chủ quan từ reward model. Vì tín hiệu thưởng chính xác và không bị 'hack', model có thể tự khám phá chuỗi suy luận (chain-of-thought) dẫn tới đáp án đúng. Đây là cơ chế đứng sau các reasoning model kiểu o1/R1; thường kết hợp với GRPO.

**Giải thích:** Xem nanochat chat_rl.py (tasks gsm8k, spellingbee) và paper DeepSeekMath/GRPO (arXiv 2402.03300).

## Câu 5 (Trắc nghiệm)

[Nâng cao] Bước 'midtrain' (nanochat) nằm ở đâu trong pipeline?

- **A.** Trước pretrain
- **B.** Sau GRPO
- **C.** Thay thế SFT
- **D.** Giữa pretrain và SFT, dạy format hội thoại, special tokens, tool use (đáp án đúng)

**Đáp án: D**

**Giải thích:** Midtrain là khái niệm KHÔNG có trong pipeline GPT-2 kinh điển; nó chuẩn bị base model cho giai đoạn chat/SFT.

## Câu 6 (Tự luận)

Trong RLHF/DPO, thành phần KL divergence (hoặc reference policy) đóng vai trò gì?

**Trả lời mẫu:** Nó giữ policy mới không trôi quá xa khỏi model tham chiếu (thường là bản SFT). Không có ràng buộc này, RL có thể 'hack' reward: sinh văn bản kỳ dị đạt điểm cao từ reward model nhưng mất khả năng ngôn ngữ chung (reward hacking / catastrophic drift). Trong PPO nó là phạt KL trong reward; trong DPO nó nằm ngay trong loss qua tỉ số log-prob với pi_ref và hệ số beta.

**Giải thích:** Đây là lý do mọi công thức DPO đều chứa pi_theta/pi_ref, không phải chi tiết trang trí.

## Câu 7 (Tự luận)

Jurafsky và Martin viết rằng các phương pháp alignment bằng dữ liệu ưu tiên hiện nay đứng trên khung reinforcement learning của Sutton và Barto. Hãy đặt tên từng thành phần của khung đó (agent, environment, action, reward, policy) vào bài toán alignment một LLM.

**Trả lời mẫu:** Policy là chính LLM với tham số θ; action là token được sinh ở mỗi bước, hoặc cả chuỗi trả lời; state là prompt cộng các token đã sinh; environment là thứ trả về reward, ở đây là reward model học từ cặp ưu tiên của người; reward của cả chuỗi là hàm của reward từng bước. Mục tiêu là tối đa reward kỳ vọng, đồng thời giữ KL với model tham chiếu để policy không trôi xa.

**Giải thích:** SLP3 mục 8.4 trang 219 mô tả đúng khung này và dẫn Sutton và Barto 1998. Sutton và Barto 13.1 cho softmax policy trên preference h(s, a, θ), chính là softmax trên logits của LLM; PPO và GRPO là hậu duệ của REINFORCE ở mục 13.3.

## Câu 8 (Trắc nghiệm)

Dataset HH-RLHF (Bai et al. 2022) bạn dùng tuần này viết tắt của gì, và điều đó nói gì về nội dung các cặp chosen/rejected?

- **A.** 'Human-Human RLHF', data do hai người chat với nhau
- **B.** 'Helpful Hints for RLHF', bộ hướng dẫn gán nhãn
- **C.** 'High-quality Human RLHF', data đã lọc chất lượng cao
- **D.** 'Helpful and Harmless', một phần các cặp chosen/rejected không so 'câu nào hay hơn' mà so 'câu nào AN TOÀN hơn' (đáp án đúng)

**Đáp án: D**

**Giải thích:** Mục 7 của 01_theory_notes.md: cái tên đúng nghĩa đen 'Helpful and Harmless' (Bai et al. 2022, arXiv 2204.05862): harmlessness nằm ngay trong preference data. Bài tập cuối tuần: tự mở vài mẫu HH-RLHF và tìm một cặp khác nhau về AN TOÀN chứ không phải chất lượng.

## Câu 9 (Tự luận)

Vì sao nói 'refusal là hành vi được HUẤN LUYỆN, không phải bản năng', và vì sao RM/DPO/GRPO không tự đem lại harmlessness?

**Trả lời mẫu:** Base model chỉ dự đoán token, nó không 'biết từ chối'. Model từ chối yêu cầu độc hại vì trong preference data, câu từ chối được gán chosen còn câu tuân theo bị gán rejected, và RM/DPO/PPO đẩy policy về phía đó. RM/DPO/GRPO chỉ là máy tối ưu 'cái gì được ưa thích trong data': Bradley-Terry không biết 'an toàn' là gì, nó chỉ biết chosen và rejected, nếu preference data chỉ encode 'trả lời dài, lễ phép, đúng format' thì model học đúng và CHỈ những thứ đó. Harmlessness phải nằm sẵn trong data (như HH-RLHF) hoặc trong verifier; thuật toán không thêm được giá trị mà data không chứa. Hệ quả thực dụng: fine-tune tiếp trên data không có tín hiệu harmlessness thì hành vi từ chối có thể xói mòn, nó chỉ là trọng số như mọi hành vi khác.

**Giải thích:** Mục 7 của 01_theory_notes.md. Cùng bài học với 'metric bị game' (nâng cao I5): hệ tối ưu chỉ tối ưu cái nó thấy. Red-teaming (Ganguli et al. 2022, arXiv 2209.07858) là dạng eval cho trục an toàn, không đo thì không biết.

## Câu 10 (Trắc nghiệm)

Trong mô hình Bradley-Terry mà SLP3 dùng để mô hình hóa preference, nếu hai output có reward gần bằng nhau thì P(oi ≻ oj | x) xấp xỉ bao nhiêu và điều đó phản ánh gì?

- **A.** Xấp xỉ 0.5, phản ánh preference yếu hoặc không có preference giữa hai output (đáp án đúng)
- **B.** Xấp xỉ 1, phản ánh rằng model luôn phải chọn ra một bên thắng rõ ràng trong mỗi cặp
- **C.** Không xác định, vì Bradley-Terry chỉ được định nghĩa khi hai reward khác nhau rõ rệt
- **D.** Xấp xỉ 0, phản ánh rằng cặp dữ liệu này bị coi là nhiễu và không đóng góp vào loss

**Đáp án: A**

**Giải thích:** P(oi ≻ oj | x) = σ(zi − zj). SLP3: "very small differences in scores yield probabilities near 0.5, reflecting either weak or no preference between the items, larger differences rapidly approach values of 1 or 0". Đạo hàm của sigmoid cũng giúp học bằng binary cross-entropy. (SLP3 mục 8.3.2, tr. 218)

## Câu 11 (Trắc nghiệm)

Jurafsky và Martin nêu hai khác biệt then chốt giữa RL truyền thống và RL dùng cho alignment LLM. Cặp nào đúng?

- **A.** Không gian hành động là liên tục thay vì rời rạc, và mỗi episode chỉ có đúng một bước quyết định
- **B.** Reward model chỉ là surrogate nhiễu của reward thật, và học bắt đầu từ model đã mạnh nên chỉ cần đẩy nhẹ hành vi (đáp án đúng)
- **C.** Không cần hàm giá trị vì reward cho cả chuỗi, và trajectory ngắn hơn nhiều so với các bài toán game
- **D.** Reward đến từ môi trường và phản ánh sự thật quan sát được, và policy được học từ khởi tạo ngẫu nhiên

**Đáp án: B**

**Giải thích:** SLP3: "With preference learning, the learned reward model only serves as a noisy surrogate for a true reward model." và "Here, we begin with models that are already performing at a high level ... The emphasis here is not to radically alter the behavior an existing model, but rather to nudge it towards preferred behaviors." Lựa chọn đầu mô tả RL truyền thống, không phải alignment. (SLP3 mục 8.4, tr. 220-221)

## Câu 12 (Trắc nghiệm)

Theo SLP3, DPO phải duy trì bao nhiêu model trong lúc huấn luyện so với PPO, và điều này có ý nghĩa gì khi bạn chạy alignment trên GPU 8GB?

- **A.** 3 model so với 5 của PPO; chênh lệch nhỏ nên VRAM không phải lý do chính để chọn DPO
- **B.** 1 model so với 3 của PPO; nhờ vậy DPO chạy được cả khi không có reference policy trong bộ nhớ
- **C.** 2 model so với 2 của PPO; khác biệt chỉ nằm ở hàm loss chứ không nằm ở bộ nhớ
- **D.** 2 model so với 4 của PPO; ít model hơn và không cần sampling online nên nhẹ hơn về bộ nhớ và tính toán (đáp án đúng)

**Đáp án: D**

**Giải thích:** SLP3: "DPO only incurs the cost of maintaining 2 LLMs during training, as opposed to the 4 models needed for PPO." và "DPO learns directly from the preferences contained in D without the need for computationally expensive online sampling from πθ." Hai model của DPO là policy πθ và reference πref. (SLP3 mục 8.4.2, tr. 223)

## Câu 13 (Trắc nghiệm)

Trong cập nhật REINFORCE θ ← θ + α G ∇π(A|S,θ) / π(A|S,θ), Sutton và Barto giải thích vì sao phải chia cho xác suất hành động π(A|S,θ)?

- **A.** Để các hành động được chọn thường xuyên không có lợi thế chỉ vì được cập nhật theo hướng của chúng nhiều lần hơn (đáp án đúng)
- **B.** Để cập nhật hội tụ về policy xác định, vì hành động có xác suất nhỏ sẽ bị đẩy về 0 nhanh hơn
- **C.** Để biến return G thành advantage, loại bỏ phần phương sai do thiếu baseline gây ra trong ước lượng
- **D.** Để chuẩn hóa gradient về độ dài đơn vị, giúp step size α không phụ thuộc vào thang đo của bài toán

**Đáp án: A**

**Giải thích:** Sutton và Barto: "The latter makes sense because otherwise actions that are selected frequently are at an advantage (the updates will be more often in their direction) and might win out even if they do not yield the highest return." Vector ∇π/π tương đương ∇ln π(A|S,θ) và được gọi là eligibility vector. (Sutton và Barto mục 13.3, tr. 327-328)

## Câu 14 (Trắc nghiệm)

Sutton và Barto nêu một lợi thế của policy softmax theo action preferences (eq. 13.2) so với chọn hành động ε-greedy trên action value. Lợi thế đó là gì?

- **A.** Policy softmax luôn khám phá nhiều hơn vì mọi hành động đều giữ một xác suất tối thiểu bằng ε
- **B.** Policy softmax có thể tiến tới policy xác định, còn ε-greedy luôn giữ xác suất ε chọn hành động ngẫu nhiên (đáp án đúng)
- **C.** Policy softmax hội tụ nhanh hơn vì action preferences tiến về đúng giá trị thật của action value
- **D.** Policy softmax cần ít tham số hơn vì không phải ước lượng action value riêng cho từng hành động

**Đáp án: B**

**Giải thích:** Sutton và Barto: "One advantage of parameterizing policies according to the soft-max in action preferences is that the approximate policy can approach a deterministic policy, whereas with ε-greedy action selection over action values there is always an ε probability of selecting a random action." Action preferences không tiến về giá trị cụ thể mà được đẩy để sinh ra policy ngẫu nhiên tối ưu. (Sutton và Barto mục 13.1, tr. 322-323)

## Câu 15 (Tự luận)

FoLLM mô tả DPO là một dạng offline RL còn PPO là online RL. Hãy nêu lợi ích mà FoLLM gán cho mỗi bên và cho biết vì sao online RL vẫn được xem là có giá trị với LLM dù DPO đơn giản hơn.

**Trả lời mẫu:** DPO học từ một dataset preference cố định, không cần quá trình sampling tốn kém như PPO nên đơn giản và sample-efficient hơn, đồng thời bỏ được việc huấn luyện reward model riêng, vốn khó và có thể làm hỏng policy learning nếu reward model kém. Ngược lại, online RL như PPO khám phá trạng thái mới qua tương tác với môi trường (reward model làm proxy), không bị giới hạn bởi dữ liệu tĩnh, có thể tìm ra chiến lược giải quyết mới và bao phủ nhiều cặp state-action hơn. FoLLM cho rằng điểm cuối này giúp cải thiện generalization, một khía cạnh được coi là then chốt với LLM.

**Giải thích:** FoLLM: "DPO can broadly be viewed as an offline reinforcement learning method, where the training data is pre-collected and fixed, and there is no exploration." và "exploration can help the agent cover a wider range of state-action pairs, thus improving generalization. This could be an important advantage for LLMs". Về reward model: "a poorly trained reward model can greatly affect the outcome of policy learning". (FoLLM mục 4.4.2, tr. 193, 196)

## Câu 16 (Tự luận)

Sutton và Barto đưa ra quy tắc chung để vẽ ranh giới giữa agent và environment, và nói riêng về việc tính reward. Hãy nêu quy tắc đó và giải thích vì sao trong RLHF reward model phải được coi là phần của environment chứ không phải của policy.

**Trả lời mẫu:** Quy tắc là bất cứ thứ gì agent không thể thay đổi tùy ý thì nằm ngoài agent, tức thuộc environment; ranh giới này thường gần agent hơn ranh giới vật lý (motor và cảm biến của robot được coi là environment). Riêng reward luôn được coi là bên ngoài agent, kể cả khi agent biết cách reward được tính, vì reward định nghĩa nhiệm vụ nên phải nằm ngoài khả năng sửa đổi tùy ý của agent. Áp vào RLHF: nếu policy có thể sửa reward model thì nó sẽ tự chấm điểm cao thay vì học hành vi được ưa thích; vì vậy reward model được cố định và đóng vai trò môi trường chấm điểm, còn LLM là policy.

**Giải thích:** Sutton và Barto: "The general rule we follow is that anything that cannot be changed arbitrarily by the agent is considered to be outside of it and thus part of its environment." và "we always consider the reward computation to be external to the agent because it defines the task facing the agent and thus must be beyond its ability to change arbitrarily." FoLLM cũng viết environment trong LLM là khung mà LLM nhận feedback và học. (Sutton và Barto mục 3.1, tr. 50; FoLLM mục 4.3.1, tr. 174)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

GRPO (DeepSeekMath, arXiv 2402.03300) khác PPO ở điểm cốt lõi nào?

- **A.** GRPO chỉ dùng cho code
- **B.** GRPO không dùng KL
- **C.** GRPO bỏ critic (value network), ước lượng baseline từ điểm của một nhóm output sinh cho cùng prompt (đáp án đúng)
- **D.** GRPO không cần reward

**Đáp án: C**

**Giải thích:** Trích paper: 'GRPO foregoes the critic model, instead estimating the baseline from group scores, significantly reducing training resources'.

## Nâng cao 2 (Tự luận)

Hãy nối softmax policy của Sutton và Barto (eq. 13.2) với logits của LLM, và chỉ ra vì sao alignment bằng RL không cần thêm lớp nào mới vào model.

**Trả lời mẫu:** Sutton và Barto tham số hóa policy cho action rời rạc bằng preference h(s, a, θ) rồi lấy softmax: π(a|s, θ) = e^{h(s,a,θ)} / Σ_b e^{h(s,b,θ)} (mục 13.1, trang 322). Với LLM, h chính là logit của từng token trong vocab và softmax là lớp output có sẵn; state là prompt cộng token đã sinh, action là token kế. Vì thế RLHF chỉ đổi hàm mục tiêu và cách lấy reward, không đổi kiến trúc.

**Giải thích:** SLP3 mục 8.4 (trang 219) khẳng định các phương pháp alignment hiện nay đứng trên khung RL của Sutton và Barto.
