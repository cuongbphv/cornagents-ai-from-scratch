# Load trọng số GPT-2 OpenAI — Ghi chú & checklist

> Mục tiêu: nạp weights GPT-2 pretrained vào kiến trúc bạn tự build, để **xác nhận kiến trúc đúng** (nếu sinh text mạch lạc nghĩa là mapping đúng).

## 2 cách lấy weights

1. **Qua Hugging Face** (dễ nhất):
   ```python
   from transformers import GPT2Model
   gpt2_hf = GPT2Model.from_pretrained("gpt2")  # 124M
   ```
2. **Script `gpt_download.py` của Raschka** (tải checkpoint TF gốc của OpenAI) — có sẵn trong repo `rasbt/LLMs-from-scratch` ch.5.

## Điểm DỄ SAI khi map (kiểm tra kỹ)

- [ ] **QKV gộp**: GPT-2 lưu Q,K,V trong **một** ma trận `c_attn` → phải **tách 3 phần** trước khi gán vào `W_query/W_key/W_value` của bạn.
- [ ] **Transpose**: weight của `Conv1D` (GPT-2 HF) cần `.T` để khớp `nn.Linear`.
- [ ] **Bias QKV**: GPT-2 CÓ bias ở QKV (`qkv_bias=True`).
- [ ] **Weight tying**: `out_head.weight` dùng chung với `tok_emb.weight`.
- [ ] **Tên LN**: `ln_1/ln_2/ln_f` ↔ `norm1/norm2/final_norm` của bạn.
- [ ] **Pos/token emb**: `wte` → `tok_emb`, `wpe` → `pos_emb`.

## Quy trình kiểm chứng

1. Load weights → gán vào model bạn.
2. Dùng `tiktoken` (encoding `gpt2`) encode 1 prompt, vd. "Every effort moves you".
3. Chạy `generate_text_simple`, decode kết quả.
4. **Tiêu chí đậu**: output là tiếng Anh mạch lạc, không phải ký tự ngẫu nhiên.

## Tự kiểm tra (nhờ Claude)

- [ ] Vì sao phải tách `c_attn` thành 3? Shape trước/sau là gì?
- [ ] Weight tying tiết kiệm bao nhiêu tham số? Vì sao hợp lý?
- [ ] Nếu quên `.T`, triệu chứng sẽ là gì?
