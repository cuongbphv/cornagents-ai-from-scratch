# MLX / Ollama / LM Studio — Lệnh sẵn dùng (Tuần 9)

> Chạy trên MacBook Apple Silicon. Thay đường dẫn/model theo nhu cầu.

## 1. Cài đặt

```bash
pip install mlx-lm            # fine-tune + inference MLX
brew install ollama          # hoặc tải app từ ollama.com
# LM Studio: tải app từ lmstudio.ai
```

## 2. Inference nhanh với MLX

```bash
python -m mlx_lm.generate \
  --model mlx-community/Meta-Llama-3.1-8B-Instruct-4bit \
  --prompt "Giải thích một khái niệm Finance Banking trong 3 câu" \
  --max-tokens 256
```

## 3. LoRA fine-tune (MLX)

```bash
# data/ chứa train.jsonl + valid.jsonl, mỗi dòng: {"text": "..."}
python -m mlx_lm.lora \
  --model mlx-community/Meta-Llama-3.1-8B-Instruct-4bit \
  --train \
  --data ./data \
  --iters 500 \
  --batch-size 1 \
  --num-layers 16
```

Fuse adapter vào base:

```bash
python -m mlx_lm.fuse \
  --model mlx-community/Meta-Llama-3.1-8B-Instruct-4bit \
  --adapter-path ./adapters \
  --save-path ./fused_model
```

## 4. Chạy qua Ollama

```bash
# Tạo Modelfile cho GGUF (vd. xuất từ Tuần 8)
cat > Modelfile <<'EOF'
FROM ./gguf_model/model-q4_k_m.gguf
PARAMETER temperature 0.7
SYSTEM "Bạn là trợ lý Finance Banking."
EOF

ollama create my-tf-model -f Modelfile
ollama run my-tf-model "Tóm tắt một quy trình nghiệp vụ ngân hàng trong 3 câu"
```

## 5. Ghi chú so sánh (điền khi chạy thật)

- Tốc độ MLX 8B trên Mac: ______ tok/s
- Tốc độ 3070 Ti 8B: ______ tok/s
- Mac fit được tới: ______ B params
- Khi nào chọn cái nào → xem `hardware_decision.md`
