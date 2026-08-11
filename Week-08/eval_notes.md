# Eval: Base vs Fine-tuned — Ghi chú (deliverable Tuần 8)

> Điền sau khi fine-tune. Mục tiêu: chứng minh fine-tune có cải thiện trên held-out.

## Setup

- Base model: ______ | adapter: r=16, α=16
- Dataset train: ______ (số mẫu: ______) | held-out: ______ mẫu
- Hardware: ______ | thời gian train: ______

## Phương pháp đánh giá

- [ ] Chọn 10–20 prompt held-out (không có trong train)
- [ ] Sinh phản hồi từ **base** và **fine-tuned** (cùng setting decode)
- [ ] Chấm: đúng/sai, độ liên quan domain, format. Có thể dùng LLM-as-judge (Claude)

## Kết quả

| Tiêu chí | Base | Fine-tuned |
|----------|------|-----------|
| Đúng (accuracy) | ______ | ______ |
| Bám domain | ______ | ______ |
| Format đúng | ______ | ______ |

## Ví dụ minh họa (1–2 cặp)

**Prompt:** ______
- Base: ______
- Fine-tuned: ______

## Nhận xét

- Cải thiện rõ ở đâu? ______
- Có dấu hiệu overfit / quên kiến thức (catastrophic forgetting)? ______
- Lần sau đổi gì (r, lr, số mẫu)? ______
