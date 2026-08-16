# Alignment: SFT vs DPO vs GRPO — Ghi chú (deliverable Tuần 7)

> Viết bằng lời mình sau khi đọc FareedKhan `src/post_training/` + chạy một stage. Điền các chỗ ______.

## Bức tranh tổng: pipeline alignment

```
Base model (pretrained)
   │  (1) SFT — học bắt chước phản hồi tốt
   ▼
SFT model
   │  (2) Reward Model — học chấm điểm phản hồi
   ▼
   │  (3) RLHF: PPO / DPO / GRPO — tối ưu theo sở thích người dùng
   ▼
Aligned model
```

## 1. SFT (Supervised Fine-Tuning)

- **Dữ liệu**: cặp (prompt → phản hồi tốt). Vd: Alpaca, Dolly.
- **Mục tiêu học**: ______ (gợi ý: cross-entropy next-token trên phần response).
- **Ưu/nhược**: ______
- TODO: SFT khác instruction fine-tuning ở Tuần 6 thế nào? ______

## 2. Reward Model (RM)

- **Dữ liệu**: cặp so sánh (chosen, rejected). Vd: Anthropic HH-RLHF, UltraFeedback.
- **Mục tiêu**: học hàm cho điểm sao cho score(chosen) > score(rejected).
- TODO: loss của RM có dạng gì? (gợi ý: log-sigmoid của hiệu score) ______

## 3. PPO vs DPO vs GRPO

| | Cần Reward Model riêng? | Ý tưởng cốt lõi | Độ phức tạp |
|---|---|---|---|
| **PPO** | Có | RL on-policy, tối ưu reward + KL với SFT | Cao |
| **DPO** | **Không** | Tối ưu trực tiếp trên cặp (chosen, rejected), bỏ qua RM | Thấp hơn |
| **GRPO** | Không (reward có thể là verifiable) | So sánh nhóm sample, chuẩn hóa advantage trong nhóm | Trung bình; mạnh cho reasoning/RLVR |

- TODO DPO: vì sao DPO bỏ được bước train RM riêng? Loss DPO trông thế nào? ______
- TODO GRPO: "group-relative" nghĩa là gì? Vì sao hợp cho bài toán có đáp án kiểm chứng được (toán/code)? ______
- TODO: KL divergence với policy gốc đóng vai trò gì? ______

## 4. Stage mình đã chạy

- Stage: ______ | dataset: ______ | hardware: ______
- Quan sát: ______
- So với base/SFT, phản hồi thay đổi ra sao? (ví dụ cụ thể) ______

## 5. Tóm tắt 3 câu

1. ______
2. ______
3. ______

---
*Lưu ý:* cho GRPO/RLVR, dùng paper DeepSeekMath (arXiv 2402.03300) + nanochat `chat_rl.py` làm nguồn tham chiếu.
