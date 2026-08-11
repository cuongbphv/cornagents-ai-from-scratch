# Lý thuyết Tuần 4 — Lắp ráp kiến trúc GPT-2

> Đọc trước khi điền TODO trong [`02_gpt_model.py`](02_gpt_model.py). Mọi con số đã chạy kiểm chứng bằng PyTorch 2.5.1 ngày 2026-08-11. Nguồn ở cuối file, xác minh cùng ngày. Cần nắm attention Tuần 3.

---

## 1. LayerNorm — giữ activation "trong khuôn"

Chuẩn hóa **từng vector token** (theo chiều feature) về mean 0, variance 1, rồi cho model tự co giãn lại bằng hai tham số học được:

```
LN(x) = γ · (x − μ) / √(σ² + ε) + β        (μ, σ² tính trên chiều d_model của TỪNG token)
```

Kiểm chứng: `nn.LayerNorm(8)` trên input mean≈1, std≈3 → output mean ≈ 0.0, std ≈ 1.0 (đã chạy 2026-08-11). Không có LN, qua vài chục layer activation trôi dần → train không ổn định. GPT-2 đặt LN **trước** attention/FFN (**pre-LN**) — tự code đúng vị trí này, đặt sau (post-LN) train khó hơn hẳn ở model sâu.

## 2. GELU — ReLU "mượt"

`GELU(x) = x · Φ(x)` với Φ là CDF của phân phối chuẩn (Hendrycks & Gimpel, arXiv 1606.08415). Khác ReLU: âm nhẹ vẫn cho tín hiệu nhỏ đi qua, đạo hàm liên tục tại 0. Giá trị kiểm chứng bằng `F.gelu`:

| x | GELU(x) | ReLU(x) |
|---|---------|---------|
| −1 | −0.1587 | 0 |
| 0 | 0 | 0 |
| +1 | +0.8413 | 1 |

(Nhận ra 0.1587 và 0.8413? Chính là Φ(−1) và Φ(1) — đúng định nghĩa x·Φ(x).)

## 3. FeedForward — mở rộng 4× rồi nén lại

```python
nn.Sequential(
    nn.Linear(d, 4*d),   # 768 → 3072
    nn.GELU(),
    nn.Linear(4*d, d),   # 3072 → 768
)
```

Mỗi token đi qua FFN **độc lập** (không nhìn token khác — việc đó là của attention). FFN chiếm phần tham số lớn nhất trong block: `768·3072 + 3072 + 3072·768 + 768 = 4,722,432` trên tổng 7,087,872 của một block (≈ 67%, kiểm chứng bằng tính tay khớp script).

## 4. TransformerBlock — residual là mạch máu

```python
def forward(self, x):
    x = x + self.att(self.ln1(x))    # pre-LN + residual
    x = x + self.ffn(self.ln2(x))
    return x
```

Vì sao `x + ...`: chain rule (Tuần 2) **nhân dồn** đạo hàm qua từng layer — 12 block nhân liên tiếp dễ làm gradient tiêu biến. Residual mở một "đường cao tốc" cộng thẳng, gradient luôn có lối về layer đầu. Đây là lý do stack sâu train được.

## 5. GPTModel hoàn chỉnh + đếm tham số (kiểm chứng 124M)

```
idx → tok_emb + pos_emb → dropout → 12 × TransformerBlock → LayerNorm cuối → head (768 → 50257)
```

Đếm tham số với config chuẩn trong [README.md](README.md) (`V=50257, T=1024, d=768, L=12, qkv_bias=True`), **head chia sẻ trọng số với token embedding (weight tying)** — đã tính kiểm chứng 2026-08-11:

| Thành phần | Tham số | Ghi chú |
|------------|---------|---------|
| Token embedding | 38,597,376 | **31.0% toàn model** — chỉ là bảng tra V×d |
| Positional embedding | 786,432 | 1024×768 |
| 12 × block | 85,054,464 | mỗi block 7,087,872 (attn 2.36M + FFN 4.72M + 2 LN) |
| LN cuối | 1,536 | |
| Head | 0 | tied với token embedding |
| **Tổng** | **124,439,808** | ≈ "124M" |

Checklist "verify số tham số ≈ 124M" trong README: `sum(p.numel() for p in model.parameters())` phải ra **đúng 124,439,808** nếu bạn tie weight; ra ~163M nghĩa là head đứng riêng — không sai về chạy, nhưng khác GPT-2 chuẩn.

## 6. Load trọng số GPT-2 — chỗ dễ sai nhất tuần

- Từng tên tham số của bạn phải map sang tên trong checkpoint OpenAI; sai map thì model vẫn chạy nhưng sinh rác.
- Tham chiếu hàm `from_pretrained` trong `nanoGPT/model.py` — đọc kỹ phần nó xử lý **transpose** một số ma trận trước khi copy (nguyên nhân nằm ở cách checkpoint gốc lưu trọng số; tự đối chiếu code thay vì tin trí nhớ).
- Cách verify rẻ nhất: load xong, sinh text với prompt tiếng Anh đơn giản — **mạch lạc = mapping đúng**; rác = soi lại từng nhóm (emb → attn → ffn → head).
- Sampling khi sinh: greedy để debug (tái lập được), temperature/top-k để chơi (mục nâng cao B2).

## 7. Tiếng Việt trong tuần này

- **31% tham số của GPT-2 124M là bảng embedding** cho vocab BPE 50257 thiên tiếng Anh (Tuần 3 đã đo: câu tiếng Việt tốn ~5.6× token so với câu Anh tương đương). Nếu một ngày bạn build model tiếng Việt from scratch, quyết định vocab/tokenizer định đoạt gần **1/3 kích thước model** trước khi viết dòng code kiến trúc nào.
- `context_length = 1024` token: với fertility đo ở Tuần 3, cùng cửa sổ đó chứa được **ít văn bản tiếng Việt hơn hẳn** văn bản Anh — nhớ điều này khi thử nhét văn bản dài vào model tuần này.
- Model GPT-2 load về **train chủ yếu trên tiếng Anh** — sinh thử tiếng Việt sẽ kém; đó là hành vi kỳ vọng, không phải bug mapping của bạn. Verify mapping bằng prompt tiếng Anh.

## 8. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| karpathy/nanoGPT (`model.py`, MIT) | https://github.com/karpathy/nanoGPT | 4, 5, 6 |
| Ba et al. 2016 — Layer Normalization | https://arxiv.org/abs/1607.06450 | 1 |
| Hendrycks & Gimpel 2016 — GELU | https://arxiv.org/abs/1606.08415 | 2 |

(Paper GPT-2 "Language Models are Unsupervised Multitask Learners" phát hành dạng PDF trên trang OpenAI, không có trên arXiv — xem link trong README nguồn học.)

## Sau khi đọc xong

1. Điền TODO trong [`02_gpt_model.py`](02_gpt_model.py) theo thứ tự: LayerNorm → GELU → FFN → Block → GPTModel.
2. Đếm tham số, đối chiếu bảng mục 5 — khớp 124,439,808 mới đi tiếp.
3. Load trọng số GPT-2 theo [`03_load_weights_notes.md`](03_load_weights_notes.md), sinh text mạch lạc.
4. Làm [`quiz.md`](quiz.md); sau đó mới mở mục nâng cao (RMSNorm/SwiGLU/MoE).
