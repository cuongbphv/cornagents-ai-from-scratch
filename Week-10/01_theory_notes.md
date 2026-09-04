# Lý thuyết Tuần 10: Alignment: SFT → Reward Model → PPO/DPO → GRPO

> Đọc trước khi chạy stage alignment và viết [`02_alignment_notes.md`](02_alignment_notes.md). Ví dụ số kiểm chứng bằng PyTorch 2.5.1 ngày 2026-08-11; nguồn cuối file.

---

## 1. Bản đồ pipeline: thuộc lòng trước, chi tiết sau

```
Pretrain → (Midtrain) → SFT → Reward Model → PPO / DPO → GRPO/RLVR
```

- **Pretrain**: đoán token kế (Tuần 8): biết *ngôn ngữ*, chưa biết *nghe lời*.
- **SFT**: instruction FT (Tuần 9): bắt chước demonstration.
- **RM → PPO** hoặc **DPO**: học từ *so sánh cặp* thay vì demonstration, vì "câu nào hay hơn" dễ gán nhãn hơn "viết câu hay".
- **GRPO/RLVR**: RL với reward kiểm chứng được (toán đúng/sai, test pass): nền của reasoning model.
- **Midtrain** (khái niệm nanochat, không có trong pipeline kinh điển): dạy format hội thoại/special token trước SFT.

## 2. Reward Model: chấm điểm bằng so sánh cặp

Data: `(prompt, chosen, rejected)`. RM là model + head scalar; loss Bradley-Terry:

```
L_RM = −log σ(r(x, y_chosen) − r(x, y_rejected))
```

Kiểm chứng: `r_chosen=2.0, r_rejected=1.0` → `−logsigmoid(1.0) = 0.3133`. Chênh lệch càng đúng chiều và càng lớn, loss càng nhỏ. RM chỉ học **thứ tự tương đối**: điểm tuyệt đối không có ý nghĩa.

## 3. PPO: RL trên reward đã học (mức khái niệm là đủ)

Policy (model đang train) sinh câu trả lời → RM chấm → cập nhật policy tăng reward, **kèm phanh KL** giữ policy không trôi xa model tham chiếu (xa quá = reward hacking: câu được RM khen nhưng thực chất tệ). Cồng kềnh: cần 4 model trong bộ nhớ (policy, reference, RM, critic): lý do DPO ra đời.

## 4. DPO: bỏ hẳn RM và RL loop

Insight của Rafailov et al. (arXiv 2305.18290, đúng như tựa đề *"Your Language Model is Secretly a Reward Model"*): bài toán RLHF-với-phanh-KL có nghiệm dạng đóng, cho phép viết reward **ẩn trong chính policy**, đưa về một loss supervised trên cặp preference:

```
L_DPO = −log σ( β·[ log πθ(y_w|x)/πref(y_w|x) − log πθ(y_l|x)/πref(y_l|x) ] )
```

Kiểm chứng toy: log-ratio chosen 0.5, rejected −0.3, β=0.1 → loss 0.6539. Đọc loss này bằng lời: **tăng xác suất câu được chọn, giảm câu bị loại, so tương đối với reference model, β điều phanh**. Chỉ cần 2 model (policy + reference đóng băng), train như supervised, vì thế DPO là stage được khuyến nghị chạy thử tuần này.

Một lời cảnh tỉnh đáng biết trước khi kết luận "DPO ăn đứt PPO": Xu et al. 2024 (arXiv [2404.10719](https://arxiv.org/abs/2404.10719), abstract tra 2026-08-12) chạy so sánh có kiểm soát và báo cáo "PPO is able to surpass other alignment methods in all cases and achieve state-of-the-art results in challenging code competitions", kèm nhận định DPO "may have fundamental limitations". Với tuần này DPO vẫn là lựa chọn đúng, rẻ, dễ chạy, đủ để hiểu cơ chế, nhưng đừng mang "DPO tốt hơn PPO" đi như chân lý.

## 5. GRPO: advantage tính theo nhóm, khỏi cần critic

DeepSeekMath (arXiv 2402.03300): với mỗi prompt, sample **một nhóm** G câu trả lời, advantage của từng câu = chuẩn hóa reward **trong nhóm đó**:

```
A_i = (r_i − mean(r_nhóm)) / std(r_nhóm)
```

Không cần critic model như PPO. Hợp **RLVR**: reward kiểm chứng được bằng máy (đáp số đúng/sai, test pass/fail): reward sạch, không sợ RM bị hack. Đổi lại, chỉ áp được cho task có verifier.

## 6. Chọn stage nào khi nào: khung cho `02_alignment_notes.md`

| | SFT | DPO | GRPO |
|---|-----|-----|------|
| Data cần | demonstration | cặp chosen/rejected | prompt + verifier |
| Số model lúc train | 1 | 2 (policy + ref) | 2 + verifier (không critic) |
| Dạy được gì | format, hành vi, miền | "gu", chọn giữa các câu khả dĩ | năng lực có thể chấm đúng/sai |
| Khi nào dùng | luôn là bước đầu | có preference data, muốn rẻ | toán/code/task verify được |

Viết lại bảng này **bằng lời mình** + trải nghiệm sau khi chạy một stage, đó là deliverable.

## 7. Safety & red-teaming: mặt còn lại của alignment

Tuần này dễ đọc alignment thành "làm model *hữu ích* hơn". Đó mới là một nửa; nửa kia là **harmlessness**: và nó không tự đến.

- **HH-RLHF, dataset bạn đang dùng tuần này, là dataset helpfulness + HARMLESSNESS**: cái tên viết tắt đúng nghĩa đen "Helpful and Harmless". Bai et al. 2022 (arXiv [2204.05862](https://arxiv.org/abs/2204.05862), abstract tra 2026-08-16): "We apply preference modeling and reinforcement learning from human feedback (RLHF) to finetune language models to act as helpful and harmless assistants." Nghĩa là ngay trong data preference bạn cầm trên tay, một phần các cặp chosen/rejected không so "câu nào hay hơn" mà so "câu nào *an toàn* hơn".
- **Refusal là hành vi được HUẤN LUYỆN, không phải bản năng**: base model dự đoán token, nó không "biết từ chối". Model từ chối yêu cầu độc hại vì trong preference data, câu từ chối được gán *chosen* còn câu tuân theo bị gán *rejected*, và RM/DPO/PPO đẩy policy về phía đó. Hệ quả thực dụng: fine-tune tiếp trên data không có tín hiệu harmlessness thì hành vi từ chối có thể xói mòn, nó chỉ là trọng số như mọi hành vi khác.
- **Red-teaming là gì**: chủ động tấn công model của chính mình để tìm output có hại *trước* khi người dùng tìm ra. Ganguli et al. 2022 (arXiv [2209.07858](https://arxiv.org/abs/2209.07858), abstract tra 2026-08-16) mô tả quy trình ở quy mô thật: cho red team tấn công các model nhiều cỡ, gồm cả model đã RLHF, để đo phương pháp huấn luyện nào chống chịu tốt hơn, và công bố data tấn công. Điểm phương pháp luận: red-teaming là một dạng *eval* (Tuần 8/H) cho trục an toàn, không đo thì không biết.
- **Vì sao mechanics KHÔNG tự cho harmlessness**: RM/DPO/GRPO chỉ là máy tối ưu "cái gì được ưa thích trong data". Bradley-Terry (mục 2) không biết "an toàn" là gì, nó chỉ biết `chosen` và `rejected`. Nếu preference data chỉ encode "trả lời dài, lễ phép, đúng format" thì model học đúng những thứ đó và *chỉ* những thứ đó. Harmlessness phải **nằm sẵn trong data** (như HH-RLHF) hoặc trong verifier; thuật toán không thêm được giá trị mà data không chứa. Đây là cùng bài học với "metric bị game" ở phần nâng cao I5: hệ tối ưu chỉ tối ưu cái nó thấy.

[Suy luận] Cho domain VN banking của dự án: nếu sau này làm DPO tiếng Việt (mục 8), tập preference phải cố ý chứa các cặp về hành vi từ chối đúng chỗ (tư vấn lách luật, lộ thông tin khách hàng): không có thì model nghiệp vụ giỏi đến đâu cũng thiếu hẳn trục an toàn.

## 8. Tiếng Việt trong tuần này

- Các dataset trong nguồn học tuần này (Alpaca, Dolly, HH-RLHF, UltraFeedback): **kiểm tra ngôn ngữ từng bộ trước khi dùng**; phần lớn thiên tiếng Anh. Stage bạn chạy tuần này nên làm tiếng Anh cho khớp base model nhỏ.
- Preference data tiếng Việt chất lượng cao hiếm và đắt (cần người gán "câu nào hơn", với văn bản nghiệp vụ là chuyên gia). [Suy luận] Với domain VN banking của dự án, thứ tự đầu tư hợp lý là SFT tiếng Việt + RAG trước, DPO tiếng Việt chỉ khi đã có nguồn preference thật, vì SFT/RAG giải quyết phần format + kiến thức, còn DPO cần data đắt nhất.
- RLVR là ngoại lệ thú vị: reward do máy chấm nên **không phụ thuộc ngôn ngữ**: bài toán tính toán nghiệp vụ (đối chiếu số liệu, tính lãi) về lý thuyết làm RLVR tiếng Việt được mà không cần người gán nhãn preference.

## 9. Nguồn (đã xác minh truy cập được ngày 2026-08-11, trừ dòng ghi ngày khác)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| Ouyang et al. 2022, InstructGPT (RLHF/PPO) | https://arxiv.org/abs/2203.02155 | 2, 3 |
| Rafailov et al. 2023, DPO (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2305.18290, PDF local: [`../docs/papers/2305.18290_dpo-direct-preference-optimization.pdf`](../docs/papers/2305.18290_dpo-direct-preference-optimization.pdf) | 4 |
| Shao et al. 2024, DeepSeekMath (GRPO) | https://arxiv.org/abs/2402.03300 | 5 |
| Xu et al. 2024, Is DPO Superior to PPO? (chỉ link, arXiv non-exclusive, kiểm 2026-08-12) | https://arxiv.org/abs/2404.10719 | 4 |
| Bai et al. 2022, Training a Helpful and Harmless Assistant with RLHF (chỉ link, abstract tra 2026-08-16) | https://arxiv.org/abs/2204.05862 | 7 |
| Ganguli et al. 2022, Red Teaming Language Models to Reduce Harms (chỉ link, abstract tra 2026-08-16) | https://arxiv.org/abs/2209.07858 | 7 |

(FareedKhan-dev/train-llm-from-scratch: link trong README, đọc `src/post_training/` để thấy cả 5 stage bằng PyTorch thuần.)

## Sau khi đọc xong

1. Vẽ lại pipeline mục 1 bằng tay, không nhìn tài liệu.
2. Đọc code FareedKhan `src/post_training/`: đối chiếu công thức mục 2/4/5 với code thật.
3. Chạy MỘT stage scaled-down (khuyến nghị DPO), lưu log/checkpoint làm bằng chứng.
4. Mở vài mẫu HH-RLHF, tự tìm ít nhất một cặp mà chosen/rejected khác nhau về *an toàn* chứ không phải *chất lượng*, để thấy tận mắt harmlessness nằm trong data (mục 7).
5. Viết [`02_alignment_notes.md`](02_alignment_notes.md) từ bảng mục 6; làm [`quiz.md`](quiz.md).

## 10. Khung RL cho alignment: từ agent và environment đến policy gradient

Pipeline SFT, reward model, PPO, DPO, GRPO ở các mục trên dùng từ vựng của reinforcement learning. Mục này dựng từ vựng đó từ sách gốc, để công thức PPO và GRPO trong code FareedKhan không còn là hộp đen.

**Agent và environment.** Sutton và Barto định nghĩa: "The learner and decision maker is called the agent. The thing it interacts with, comprising everything outside the agent, is called the environment" (*RL: An Introduction* mục 3.1, trang 47). Hai bên tương tác liên tục: agent chọn action, environment phản hồi bằng state mới và reward. Với LLM, SLP3 (mục 8.4, trang 219) map như sau: model chọn chuỗi action theo policy dựa trên state hiện tại, environment cho reward cho mỗi action, reward của cả chuỗi là hàm của reward từng bước, và mục tiêu là tối đa tổng reward. Cụ thể: policy là LLM với tham số θ, action là token, state là prompt cộng các token đã sinh, reward đến từ reward model học ở mục 4.

**Softmax policy.** Sutton và Barto (mục 13.1, trang 322) yêu cầu policy π(a|s, θ) khả vi theo θ và, để còn khám phá, không bao giờ trở thành xác định, tức π(a|s, θ) ∈ (0, 1). Cách tham số hóa phổ biến cho action rời rạc là tính một preference h(s, a, θ) cho từng cặp state và action rồi lấy softmax: π(a|s, θ) = e^{h(s,a,θ)} / Σ_b e^{h(s,b,θ)} (eq. 13.2). Đó chính là softmax trên logits của LLM, với h là logit và b chạy trên vocab. Nhìn thấy điều này, bạn hiểu vì sao alignment bằng RL không cần thêm lớp nào mới cho model.

**Policy gradient và REINFORCE.** Mục 13.3 (trang 326) đặt chiến lược chung là stochastic gradient ascent trên hiệu năng J(θ): cần một cách lấy mẫu sao cho kỳ vọng của gradient mẫu tỉ lệ với gradient thật; hằng số tỉ lệ không quan trọng vì được hấp thụ vào step size. Định lý policy gradient cho biểu thức ∇J(θ) tỉ lệ với Σ_s μ(s) Σ_a q_π(s, a) ∇π(a|s, θ), một tổng trên các state có trọng số là tần suất gặp state đó dưới policy π. Phiên bản "all-actions" cập nhật θ theo Σ_a q̂(S_t, a, w) ∇π(a|S_t, θ) (eq. 13.7). REINFORCE thay tổng trên mọi action bằng action đã thực sự lấy mẫu, nên gọi là Monte Carlo policy gradient.

**Từ REINFORCE đến PPO trong RLHF.** Xiao và Zhu (*Foundations of LLMs* mục 4.3.3, trang 182) viết hàm utility của một trajectory τ là U(τ; θ) = Σ_t log π_θ(a_t|s_t) A(s_t, a_t) (eq. 4.39), trong đó A là advantage của action a_t tại state s_t, ước lượng bằng TD error r_t + γV(s_{t+1}) − V(s_t), với value function V được train nhờ reward model. Loss là −E_τ[U(τ; θ)] (eq. 4.40). So với REINFORCE, advantage thay cho return thô, đúng ý tưởng baseline ở Sutton và Barto mục 13.4 REINFORCE with Baseline (trang 329); PPO thêm cơ chế kẹp tỉ số policy mới trên policy cũ (mục 5 ở trên). GRPO bỏ value function, dùng nhóm sample từ cùng prompt để ước lượng advantage (mục 6). DPO đi hướng khác hẳn: bỏ luôn reward model tường minh (FoLLM mục 4.4.2, trang 193). Khi đọc code `src/post_training/` của FareedKhan, hãy tìm đúng ba thứ: chỗ tính log π_θ(a_t|s_t), chỗ tính advantage, và chỗ giữ KL với model tham chiếu.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- **Alignment đứng trên khung RL.** SLP3 mục 8.4 (trang 219): "Current approaches to aligning LLMs using preference data are based on a Reinforcement Learning (RL) framework (Sutton and Barto, 1998)." Mục 8.3 (trang 215) là reward model học từ cặp ưu tiên, đúng loss ở mục 4 của tuần.
- **Khung RL gốc.** Sutton và Barto mục 3.1 (trang 47): "The learner and decision maker is called the agent. The thing it interacts with, comprising everything outside the agent, is called the environment." Với LLM, policy là model, action là token, reward đến từ reward model. Mục 13.1 (trang 322) đưa softmax policy π(a|s, θ) = e^{h(s,a,θ)} / Σ_b e^{h(s,b,θ)} (eq. 13.2), chính là softmax trên logits của LLM; mục 13.3 REINFORCE (trang 326) là tổ tiên của PPO và GRPO.
- **RLHF và DPO.** Xiao và Zhu, *Foundations of LLMs* mục 4.3 (trang 172) giải thích vì sao cần RLHF: sở thích con người khó viết thành dataset fine-tune, và "often, humans themselves cannot precisely express their own preferences". Mục 4.4.2 (trang 193) giới thiệu DPO là phương pháp "simplifies the training framework by eliminating the need to explicitly model rewards [Rafailov et al., 2024]", cùng kết luận với paper DPO trong kệ paper.
