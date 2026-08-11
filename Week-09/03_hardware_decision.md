# Quyết định phần cứng: Mac vs 3070 Ti vs Cloud (deliverable Tuần 9)

> Bảng tham chiếu nhanh để chọn máy cho từng tác vụ. Điền số đo thật khi có.

## Bảng quyết định

| Tác vụ | Máy nên dùng | Lý do |
|--------|--------------|-------|
| Code from-scratch, train loop nhỏ | 3070 Ti / Mac | workload nhẹ, cần lặp nhanh |
| QLoRA 7B–8B | **3070 Ti** | fit 5–6GB, nhanh hơn Mac |
| Fine-tune 13B–14B | **Mac 24GB** | unified memory chứa được |
| Inference 7B–14B im lặng, lâu dài | **Mac** (Ollama) | tiết kiệm điện, yên tĩnh |
| Pretrain GPT-2 thật | **Cloud** | token budget lớn, local quá chậm |
| Full fine-tune / PPO-GRPO lớn | **Cloud** (A100/H100) | cần nhiều VRAM |

## Số đo thật (điền khi chạy)

| | 3070 Ti (8GB) | Mac (24GB) | Cloud 4090/A100 |
|---|---|---|---|
| Max model QLoRA | ~8B | ~14B | 70B+ |
| Tok/s inference 8B | ______ | ______ | ______ |
| Chi phí | điện | điện | $/giờ |

## Nguyên tắc

1. Mặc định **Unsloth QLoRA trên 3070 Ti** cho 7B–8B.
2. Dùng **Mac/MLX** khi cần 13B–14B hoặc chạy im lặng/lâu.
3. Thuê **A100** chỉ khi cần full fine-tune hoặc lặp nhanh.
4. *Threshold:* fine-tune > 24h local hoặc OOM ở batch 1 → lên cloud.
