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
- Khi nào chọn cái nào → xem `03_hardware_decision.md`

## 6. Speculative decoding (mở rộng — xem `01_theory_notes.md` mục 8)

Đo cùng prompt, cùng `max_tokens`, ≥3 lần mỗi cấu hình (có draft vs không), bỏ lần đầu; ghi ngày + máy.

### MLX (`mlx_lm.generate`)

```bash
# Flag --draft-model / --num-draft-tokens verify từ
# https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/generate.py ngày 2026-08-16
python -m mlx_lm.generate \
  --model mlx-community/Meta-Llama-3.1-8B-Instruct-4bit \
  --draft-model mlx-community/Llama-3.2-1B-Instruct-4bit \
  --num-draft-tokens 3 \
  --prompt "Giải thích một khái niệm Finance Banking trong 3 câu" \
  --max-tokens 256
```

[Chưa xác minh] Tên repo draft model ở trên chỉ là ví dụ minh họa "model nhỏ cùng họ Llama" — kiểm tồn tại/license trên HF trước khi tải, và tôi không kiểm chứng được cặp này cho speedup trên máy bạn; đo rồi mới kết luận.

### llama.cpp (`llama-server`)

```bash
# Flag --model-draft (-md) và --spec-draft-n-max verify từ
# https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md ngày 2026-08-16
llama-server \
  -m ./gguf_model/model-q4_k_m.gguf \
  --model-draft ./gguf_model/draft-1b-q4_k_m.gguf \
  --spec-draft-n-max 8
```

So sánh: chạy lại `llama-server` **không có** hai flag draft, cùng prompt qua API, so tokens/giây.
