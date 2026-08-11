# Tuần 8 — QLoRA fine-tuning thực tế trên 3070 Ti với Unsloth

> Phase 2 — Applied. Chuyển từ "from-scratch" sang tooling production: fine-tune một model 7B–8B thật bằng QLoRA 4-bit.

## Mục tiêu

- Fine-tune model 7B–8B thật với **4-bit QLoRA** trên 3070 Ti (8GB).
- Hiểu LoRA hyperparameters (r, α, target modules) trong thực tế.

## Nguồn học

- **Unsloth docs** (unsloth.ai/docs): Fine-tuning Guide, LoRA Hyperparameters Guide, Requirements table.
- HF **PEFT** + **TRL** (`SFTTrainer`).
- NVIDIA — "How to Fine-Tune LLMs on RTX GPUs With Unsloth."

## Nhiệm vụ (Task)

QLoRA fine-tune **Llama 3.1 8B** hoặc **Qwen** trên dataset instruction nhỏ (bắt đầu 500–1,000 mẫu). Export merged model + GGUF.

## Cấu hình cho 8GB

```
load_in_4bit = True
batch_size   = 1–2
seq_len      ≤ 1024
gradient_checkpointing = True
r = 16, lora_alpha = 16
target = tất cả attention + MLP projections
```

VRAM: 7B QLoRA ≈ 5GB, 8B ≈ 6GB (fits). 11B (~7.5GB) ở rìa; 14B (~8.5GB) vượt 8GB.

## Deliverable

Adapter 7B/8B đã fine-tune + **eval so base vs fine-tuned** trên held-out examples.

## Thời lượng

~10–12 giờ. Một run 1,000–5,000 mẫu: vài giờ → qua đêm trên 8GB.

## Phần cứng

- **3070 Ti** (chính). Hoặc **Colab free T4 (15GB)** làm phương án dễ hơn.
- *Threshold:* nếu fine-tune > 24h hoặc OOM ở batch 1 → chuyển 4090/A100 thuê.

---

## Checklist tiến độ

- [ ] Cài Unsloth + dependencies (kiểm tra CUDA khớp)
- [ ] Chọn base model (Llama 3.1 8B / Qwen2.5 7B) ở 4-bit
- [ ] Chuẩn bị dataset 500–1,000 mẫu (gợi ý: dùng domain Finance Banking của bạn)
- [ ] Cấu hình LoRA (r=16, α=16, target all proj) + SFTTrainer
- [ ] Smoke test vài step → xác nhận không OOM, loss giảm
- [ ] Chạy full run + lưu adapter
- [ ] Merge adapter + export GGUF (để chạy Ollama/LM Studio ở Tuần 9)
- [ ] Eval base vs fine-tuned trên held-out → ghi `eval_notes.md`

## 🚀 Bổ sung nâng cao (quantization internals)

Tuần này dùng QLoRA/NF4 ở mức "bật cờ". Hiểu sâu hơn trong [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **B4**:

- **NF4** (QLoRA): 4-bit "normal float", chỉ quantize base, train adapter LoRA ở bf16.
- **GPTQ** (per-layer, Hessian) vs **AWQ** (bảo vệ kênh salient theo activation).
- **GGUF** là *định dạng file* của llama.cpp (Q4_K_M, Q5_K_M, Q8_0…) — thứ Ollama/LM Studio load, không phải thuật toán.

> Quy tắc: 8-bit gần như không mất chất lượng; 4-bit là điểm ngọt local; perplexity tăng dần khi bit giảm.

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `qlora_finetune.py` | Starter script Unsloth QLoRA (điền dataset + tinh chỉnh) |
| `eval_notes.md` | Template eval base vs fine-tuned |
