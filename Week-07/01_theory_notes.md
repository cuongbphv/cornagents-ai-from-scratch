# Lý thuyết Tuần 7 — Alignment: SFT → Reward Model → PPO/DPO → GRPO

> Đọc trước khi chạy stage alignment và viết [`02_alignment_notes.md`](02_alignment_notes.md). Ví dụ số kiểm chứng bằng PyTorch 2.5.1 ngày 2026-08-11; nguồn cuối file.

---

## 1. Bản đồ pipeline — thuộc lòng trước, chi tiết sau

```
Pretrain → (Midtrain) → SFT → Reward Model → PPO / DPO → GRPO/RLVR
```

- **Pretrain**: đoán token kế (Tuần 5) — biết *ngôn ngữ*, chưa biết *nghe lời*.
- **SFT**: instruction FT (Tuần 6) — bắt chước demonstration.
- **RM → PPO** hoặc **DPO**: học từ *so sánh cặp* thay vì demonstration — vì "câu nào hay hơn" dễ gán nhãn hơn "viết câu hay".
- **GRPO/RLVR**: RL với reward kiểm chứng được (toán đúng/sai, test pass) — nền của reasoning model.
- **Midtrain** (khái niệm nanochat, không có trong pipeline kinh điển): dạy format hội thoại/special token trước SFT.

## 2. Reward Model — chấm điểm bằng so sánh cặp

Data: `(prompt, chosen, rejected)`. RM là model + head scalar; loss Bradley–Terry:

```
L_RM = −log σ(r(x, y_chosen) − r(x, y_rejected))
```

Kiểm chứng: `r_chosen=2.0, r_rejected=1.0` → `−logsigmoid(1.0) = 0.3133`. Chênh lệch càng đúng chiều và càng lớn, loss càng nhỏ. RM chỉ học **thứ tự tương đối** — điểm tuyệt đối không có ý nghĩa.

## 3. PPO — RL trên reward đã học (mức khái niệm là đủ)

Policy (model đang train) sinh câu trả lời → RM chấm → cập nhật policy tăng reward, **kèm phanh KL** giữ policy không trôi xa model tham chiếu (xa quá = reward hacking: câu được RM khen nhưng thực chất tệ). Cồng kềnh: cần 4 model trong bộ nhớ (policy, reference, RM, critic) — lý do DPO ra đời.

## 4. DPO — bỏ hẳn RM và RL loop

Insight của Rafailov et al. (arXiv 2305.18290, đúng như tựa đề *"Your Language Model is Secretly a Reward Model"*): bài toán RLHF-với-phanh-KL có nghiệm dạng đóng, cho phép viết reward **ẩn trong chính policy**, đưa về một loss supervised trên cặp preference:

```
L_DPO = −log σ( β·[ log πθ(y_w|x)/πref(y_w|x) − log πθ(y_l|x)/πref(y_l|x) ] )
```

Kiểm chứng toy: log-ratio chosen 0.5, rejected −0.3, β=0.1 → loss 0.6539. Đọc loss này bằng lời: **tăng xác suất câu được chọn, giảm câu bị loại, so tương đối với reference model, β điều phanh**. Chỉ cần 2 model (policy + reference đóng băng), train như supervised — vì thế DPO là stage được khuyến nghị chạy thử tuần này.

## 5. GRPO — advantage tính theo nhóm, khỏi cần critic

DeepSeekMath (arXiv 2402.03300): với mỗi prompt, sample **một nhóm** G câu trả lời, advantage của từng câu = chuẩn hóa reward **trong nhóm đó**:

```
A_i = (r_i − mean(r_nhóm)) / std(r_nhóm)
```

Không cần critic model như PPO. Hợp **RLVR** — reward kiểm chứng được bằng máy (đáp số đúng/sai, test pass/fail): reward sạch, không sợ RM bị hack. Đổi lại, chỉ áp được cho task có verifier.

## 6. Chọn stage nào khi nào — khung cho `02_alignment_notes.md`

| | SFT | DPO | GRPO |
|---|-----|-----|------|
| Data cần | demonstration | cặp chosen/rejected | prompt + verifier |
| Số model lúc train | 1 | 2 (policy + ref) | 2 + verifier (không critic) |
| Dạy được gì | format, hành vi, miền | "gu" — chọn giữa các câu khả dĩ | năng lực có thể chấm đúng/sai |
| Khi nào dùng | luôn là bước đầu | có preference data, muốn rẻ | toán/code/task verify được |

Viết lại bảng này **bằng lời mình** + trải nghiệm sau khi chạy một stage — đó là deliverable.

## 7. Tiếng Việt trong tuần này

- Các dataset trong nguồn học tuần này (Alpaca, Dolly, HH-RLHF, UltraFeedback) — **kiểm tra ngôn ngữ từng bộ trước khi dùng**; phần lớn thiên tiếng Anh. Stage bạn chạy tuần này nên làm tiếng Anh cho khớp base model nhỏ.
- Preference data tiếng Việt chất lượng cao hiếm và đắt (cần người gán "câu nào hơn" — với văn bản nghiệp vụ là chuyên gia). [Suy luận] Với domain VN banking của dự án, thứ tự đầu tư hợp lý là SFT tiếng Việt + RAG trước, DPO tiếng Việt chỉ khi đã có nguồn preference thật — vì SFT/RAG giải quyết phần format + kiến thức, còn DPO cần data đắt nhất.
- RLVR là ngoại lệ thú vị: reward do máy chấm nên **không phụ thuộc ngôn ngữ** — bài toán tính toán nghiệp vụ (đối chiếu số liệu, tính lãi) về lý thuyết làm RLVR tiếng Việt được mà không cần người gán nhãn preference.

## 8. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| Ouyang et al. 2022 — InstructGPT (RLHF/PPO) | https://arxiv.org/abs/2203.02155 | 2, 3 |
| Rafailov et al. 2023 — DPO | https://arxiv.org/abs/2305.18290 | 4 |
| Shao et al. 2024 — DeepSeekMath (GRPO) | https://arxiv.org/abs/2402.03300 | 5 |

(FareedKhan-dev/train-llm-from-scratch: link trong README — đọc `src/post_training/` để thấy cả 5 stage bằng PyTorch thuần.)

## Sau khi đọc xong

1. Vẽ lại pipeline mục 1 bằng tay, không nhìn tài liệu.
2. Đọc code FareedKhan `src/post_training/` — đối chiếu công thức mục 2/4/5 với code thật.
3. Chạy MỘT stage scaled-down (khuyến nghị DPO), lưu log/checkpoint làm bằng chứng.
4. Viết [`02_alignment_notes.md`](02_alignment_notes.md) từ bảng mục 6; làm [`quiz.md`](quiz.md).
