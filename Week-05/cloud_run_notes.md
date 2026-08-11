# Chạy pretraining trên Cloud — Ghi chú & checklist

> Lý do: 8GB 3070 Ti chạy được nhưng quá chậm cho token budget thật. Dùng local chỉ để **validate loop**; chạy thật trên cloud (one-time, ~$15–35).

## Lựa chọn provider (giá 2026 — kiểm tra lại lúc deploy)

| Provider | GPU | Giá tham khảo | Dùng khi |
|----------|-----|---------------|----------|
| RunPod Community | RTX 4090 | từ **$0.34/hr** | chạy vài giờ, rẻ nhất |
| RunPod Secure | RTX 4090 / A100 / H100 | ~$0.69 / ~$1.49 / ~$2.89 /hr | cần ổn định |
| Lambda | 8×A100 (node) | ~**$14/hr** | reproduce <4h (~$35) |
| Colab free | T4 (15GB) | miễn phí | thử nghiệm nhẹ |

> Giá marketplace biến động. Từ VN: chọn region Asia-Pacific nếu cần tương tác; thanh toán cần thẻ quốc tế.

## Quy trình (RunPod RTX 4090, ví dụ)

- [ ] Tạo pod, chọn template PyTorch CUDA
- [ ] `git clone` repo của bạn + push code Tuần 4–5 lên (hoặc scp)
- [ ] Tải dataset: FineWeb-Edu sample (HF `datasets`) hoặc shard nhỏ
- [ ] Cấu hình: seq 1024, micro-batch theo VRAM, grad accum để đạt ~524,288 token/update
- [ ] Chạy **smoke test 50–100 step** → xác nhận loss giảm + không OOM
- [ ] Bật checkpointing (lưu định kỳ phòng pod bị kill)
- [ ] Chạy full run; log loss train/val
- [ ] Tải checkpoint + log về máy → phân tích ở `loss_analysis.md`
- [ ] **Tắt pod** ngay khi xong (tránh tính tiền thừa)

## Mục tiêu so sánh

- GPT-2 gốc: val loss ~**3.5**.
- Giles Thomas (163M, 3090, ~48h local): loss **3.944**.
- Karpathy llm.c (124M, 10B token FineWeb): reproduce ~90 phút trên 8×A100.

## Checklist chi phí

- [ ] Ước tính giờ × giá trước khi chạy
- [ ] Spot/community instance nếu chấp nhận bị ngắt (rẻ hơn)
- [ ] Đặt budget alert nếu provider hỗ trợ
- [ ] Xác nhận pod đã TẮT sau khi tải kết quả
