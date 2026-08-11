# Phân tích Loss Curve — Write-up (deliverable Tuần 5)

> Viết SAU KHI chạy xong. Mục tiêu: so sánh loss curve của bạn với GPT-2 gốc. Điền vào các chỗ ______.

## 1. Setup

- Model: GPT-2 ______ (số layer/emb_dim/heads): ______
- Dataset: ______ (số token train: ______)
- Hardware: ______ | thời gian chạy: ______ | chi phí: ______
- Hyperparams: lr=______, warmup=______, batch hiệu dụng=______ token/update, seq_len=______

## 2. Kết quả

| Mốc | Train loss | Val loss |
|-----|-----------|----------|
| Đầu | ______ | ______ |
| Giữa | ______ | ______ |
| Cuối | ______ | ______ |

- (Chèn ảnh loss curve: `loss_curve.png`)

## 3. So sánh tham chiếu

| Nguồn | Loss | Ghi chú |
|-------|------|---------|
| GPT-2 gốc | ~3.5 | mục tiêu |
| llm.c reproduce 124M | (xem Discussion #481) | 8×A100, ~90 phút |
| **Của bạn** | ______ | ______ |

## 4. Quan sát & câu hỏi (trả lời bằng lời mình)

- Loss của bạn cách GPT-2 gốc bao nhiêu? Vì sao? (token budget? model size? data?) ______
- Train vs val loss có dấu hiệu overfit không? ______
- Warmup + cosine ảnh hưởng đường cong thế nào? ______
- Nếu chạy lại, bạn đổi gì? ______

## 5. Bài học rút ra

1. ______
2. ______
3. ______
