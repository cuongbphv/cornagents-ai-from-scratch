# Tuần 9 — Fine-tuning trên Mac/MLX + local inference stack

> Phase 2 — Applied. Dùng MacBook 24GB cho thế mạnh của nó (unified memory) và dựng bộ công cụ inference local.

## Mục tiêu

- Fine-tune model 7B–8B với LoRA/QLoRA bằng **MLX** trên Mac.
- Dựng **local inference stack** (Ollama + LM Studio).

## Nguồn học

- **`mlx-lm`** docs + `mlx_lm.lora`.
- Tùy chọn: **MLX LoRA Studio** (GUI), **mlx-tune** (SFT/DPO/GRPO trên MLX).
- **Ollama**, **LM Studio** (chạy cả GGUF & MLX), **llama.cpp**.

## Nhiệm vụ (Task)

Fine-tune 7B–8B bằng LoRA/QLoRA trong MLX trên Mac, fuse adapter, chạy qua Ollama/LM Studio. Với 24GB unified memory có thể fine-tune tới ~13–14B (QLoRA ~14–18GB working memory).

## Deliverable

- Local inference stack hoạt động (Ollama + LM Studio).
- Một model MLX đã fine-tune.
- Ghi chú ngắn: khi nào dùng **Mac vs 3070 Ti vs cloud** → `hardware_decision.md`.

## Thời lượng

~8–10 giờ.

## Phần cứng

**MacBook Pro 24GB** (unified memory tỏa sáng; ~2–4× chậm hơn NVIDIA nhưng chứa model lớn hơn). Dựng **Ollama** trên cả hai máy để serve.

---

## Checklist tiến độ

- [ ] Cài `mlx-lm` (`pip install mlx-lm`) trên Mac
- [ ] Tải model MLX-format (HF `mlx-community/...`)
- [ ] LoRA fine-tune: `mlx_lm.lora --model ... --train --data ... --iters 500`
- [ ] Fuse adapter: `mlx_lm.fuse --model ... --adapter-path ...`
- [ ] Cài Ollama + tạo Modelfile cho model GGUF (từ Tuần 8) / MLX
- [ ] Cài LM Studio, load model, test chat
- [ ] So tốc độ Mac vs 3070 Ti trên cùng prompt
- [ ] Viết `hardware_decision.md`

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `mlx_commands.md` | Các lệnh MLX/Ollama/LM Studio sẵn dùng |
| `hardware_decision.md` | Bảng quyết định Mac vs 3070 Ti vs cloud (deliverable) |
