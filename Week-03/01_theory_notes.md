# Lý thuyết Tuần 3 — Tokenization, embeddings, attention từ đầu

> Đây là tuần crux khái niệm — đọc chậm, chạy lại từng snippet rồi mới code [`02_multihead_attention.py`](02_multihead_attention.py). Mọi ví dụ số đã chạy kiểm chứng bằng PyTorch 2.5.1 + tiktoken ngày 2026-08-11. Nguồn dẫn cuối file, xác minh cùng ngày. Cần nắm chắc Tuần 1 (dot product, softmax, matmul) và Tuần 2 (permutation-equivariance).

---

## 1. Tokenization — BPE (Byte Pair Encoding)

### 1.1 Vấn đề

Model chỉ ăn số. Tách theo từ → vocab khổng lồ + từ lạ (OOV); tách theo ký tự → chuỗi quá dài. **BPE là điểm giữa**: đơn vị là "mảnh từ" (subword), đề xuất cho NMT bởi Sennrich et al. 2015 (arXiv 1508.07909).

### 1.2 Thuật toán train BPE — ngắn gọn đến bất ngờ

1. Khởi đầu: vocab = từng byte/ký tự riêng lẻ.
2. Đếm **cặp token liền kề** xuất hiện nhiều nhất trong corpus.
3. **Gộp (merge)** cặp đó thành token mới, thêm vào vocab.
4. Lặp bước 2–3 đến khi đủ vocab size mong muốn.

Encode văn bản mới = áp lại các merge theo đúng thứ tự đã học. Từ hay gặp thành 1 token, từ hiếm bị tách thành nhiều mảnh:

```python
import tiktoken
enc = tiktoken.get_encoding("gpt2")
enc.encode("unbelievable")          # [403, 6667, 11203, 540]
# → ['un', 'bel', 'iev', 'able']   — 4 mảnh subword
enc.n_vocab                          # 50257 (vocab GPT-2)
```

(Đã chạy kiểm chứng 2026-08-11.) Tuần này dùng `tiktoken` cho nhanh; mục nâng cao E là tự train BPE bằng cách đọc `karpathy/minbpe` — bản cài đặt tối giản của đúng thuật toán 4 bước trên.

### 1.3 Nâng cao: BPE với tiếng Việt — quan trọng vì domain của dự án là VN banking

BPE chỉ "tốt" với ngôn ngữ có nhiều trong corpus train tokenizer. Đo thực nghiệm trên máy này (tiktoken, 2026-08-11) với cùng một câu nghiệp vụ ngân hàng, bản Việt (16 từ) và bản Anh (11 từ):

| Encoding | Câu tiếng Việt | Câu tiếng Anh | VI "đắt" gấp |
|----------|---------------|---------------|--------------|
| `gpt2` (50k vocab) | **73 token** | 13 token | ~5.6× |
| `cl100k_base` | 37 token | 13 token | ~2.8× |
| `o200k_base` | 22 token | 12 token | ~1.8× |

Vì sao `gpt2` tệ với tiếng Việt — thấy ngay trong output encode:

```python
enc = tiktoken.get_encoding("gpt2")
[enc.decode([i]) for i in enc.encode("lãi suất")]
# ['l', 'ã', 'i', ' su', '�', '�', '�', 't']  — 8 token cho 2 từ!
```

- Ký tự có dấu là **2–3 byte UTF-8** (`ã` = 2 byte, `ấ` = 3 byte — đã kiểm chứng); vocab `gpt2` không có merge nào cho các cụm tiếng Việt nên rơi về **từng byte thô** (các ô `�` ở trên chính là 3 byte lẻ của `ấ`).
- Encoding đời mới hơn của tiktoken (`cl100k_base`, `o200k_base` — theo docs repo tiktoken) đỡ hơn hẳn vì vocab lớn hơn và corpus train đa ngôn ngữ hơn, nhưng vẫn đắt hơn tiếng Anh.

**Hệ quả thực tế cho dự án này:**
1. Cùng context length, văn bản tiếng Việt "ăn" gấp nhiều lần token → chứa được ít nội dung hơn, chi phí inference/train cao hơn.
2. Khi tự train tokenizer (mục nâng cao E): muốn dùng cho dữ liệu VN banking thì **corpus train BPE phải có tiếng Việt** — đây là lý do trực tiếp để làm mục E chứ không chỉ dùng tiktoken.
3. Khi chọn base model để fine-tune (Tuần 9+): đo fertility (token/từ) của tokenizer model đó trên chính văn bản tiếng Việt của bạn bằng đúng phương pháp ở bảng trên trước khi chọn — vài dòng code, tránh được quyết định đắt.

📄 **Đọc thêm (paper):** BPE gốc là Sennrich et al. 2015 (PDF trong repo: [`../docs/papers/1508.07909_bpe-neural-mt-rare-words.pdf`](../docs/papers/1508.07909_bpe-neural-mt-rare-words.pdf)) — ý tưởng nguyên bản: "encoding rare and unknown words as sequences of subword units" cho bài toán open-vocabulary. Về mặt trái của tokenization, *Tokenization Falling Short* (arXiv [2406.11687](https://arxiv.org/abs/2406.11687), EMNLP 2024 Findings — abstract tra 2026-08-12) chỉ ra tokenizer "inherently sensitive to typographical errors, length variations, and largely oblivious to the internal structure of tokens" — đúng lớp vấn đề mà văn bản tiếng Việt nhiều dấu gặp đậm hơn, và scale model chỉ giảm được một phần.

### 1.4 Data loading — sliding window

LM học bài toán "đoán token kế": input là cửa sổ `T` token, target là **cùng cửa sổ dịch phải 1**:

```
tokens:  [t0, t1, t2, t3, t4, ...]
input :  [t0, t1, t2, t3]
target:  [t1, t2, t3, t4]     ← mỗi vị trí i học đoán token i+1
```

Một batch có shape `(batch, T)`. Đây là toàn bộ "nhãn" của pretraining — không cần gán nhãn tay (Tuần 5).

---

## 2. Embeddings — token + position

Hai bảng tra, **cộng vào nhau**:

```python
tok_emb = nn.Embedding(vocab_size, d_model)     # (50257, d)  — nghĩa của token
pos_emb = nn.Embedding(context_length, d_model) # (T_max, d)  — vị trí trong chuỗi
x = tok_emb(idx) + pos_emb(torch.arange(T))     # (batch, T, d)
```

- `nn.Embedding` = bảng tra hàng — chính là `one_hot @ W` của makemore Tuần 2 (mục 2.2), viết gọn.
- Phải cộng positional embedding vì attention permutation-equivariant (Tuần 2, mục 3.2) — không có nó model mù thứ tự.
- GPT-2 dùng positional embedding **học được, tuyệt đối** như trên; Llama 3/Qwen3 thay bằng RoPE (mục nâng cao A1 — đọc sau khi xong tuần).

---

## 3. Attention — leo 4 bậc thang

Quy ước shape (thuộc lòng — trùng "Mốc shape cần nhớ" trong [README.md](README.md)):
input `x: (batch, T, d_in)` → Q/K/V: `(batch, T, d_out)` → scores/weights: `(batch, T, T)` → context: `(batch, T, d_out)`.

### Bậc 1 — simplified self-attention (chưa có gì học được)

```python
scores  = x @ x.transpose(1, 2)          # (b, T, T): dot product mọi cặp token
weights = torch.softmax(scores, dim=-1)  # mỗi hàng = phân phối "chú ý" của 1 token
context = weights @ x                    # (b, T, d): trung bình có trọng số
```

Đọc cho được câu này: **hàng i của `weights` nói token i trộn thông tin các token khác theo tỉ lệ nào; `context[i]` là kết quả trộn.** Toàn bộ attention chỉ là thế, các bậc sau thêm dần chi tiết.

### Bậc 2 — scaled dot-product với W_Q, W_K, W_V trainable

Cho token **đóng ba vai khác nhau** thay vì tự so với chính mình:

```python
Q = self.W_query(x)   # tôi đang tìm gì?
K = self.W_key(x)     # tôi chứa gì để người khác tìm?
V = self.W_value(x)   # nếu được chọn, tôi đưa ra thông tin gì?
scores  = Q @ K.transpose(1, 2) / math.sqrt(d_k)
weights = torch.softmax(scores, dim=-1)
context = weights @ V
```

**Vì sao chia √d_k:** dot product của hai vector ngẫu nhiên d_k chiều có variance ≈ d_k — đo thực nghiệm 2026-08-11 với d_k=64, 100k cặp: `var(q·k) ≈ 63.9`; sau khi chia √d_k: `≈ 0.998`. Không chia thì score phình theo d_k, softmax bão hòa về one-hot → gradient gần 0, khó train. (Lập luận variance nêu trong chính paper Vaswani et al. 2017, mục 3.2.1.)

### Bậc 3 — causal mask + dropout

GPT sinh trái→phải: token i **không được nhìn tương lai** (j > i). Che bằng `-inf` **trước** softmax:

```python
mask = torch.triu(torch.ones(T, T), diagonal=1).bool()   # tam giác trên
scores = scores.masked_fill(mask, float("-inf"))
weights = torch.softmax(scores, dim=-1)                   # e^{-inf}=0, hàng vẫn tổng=1
weights = self.dropout(weights)
```

Đã kiểm chứng 2026-08-11: sau mask, hàng 0 dồn 100% trọng số vào vị trí 0, mọi hàng vẫn tổng 1. Phải là `-inf` trước softmax chứ không phải gán 0 sau softmax — gán 0 sau làm hàng không còn là phân phối. Test thứ ba trong [`03_test_attention.py`](03_test_attention.py) kiểm đúng tính chất này: đổi token tương lai không được làm đổi output vị trí 0.

### Bậc 4 — multi-head: nhiều "góc nhìn" chạy song song

Chia `d_out` thành `num_heads × head_dim`, mỗi head làm attention độc lập trên lát mỏng của nó, rồi ghép lại:

```python
# (b, T, d_out) -view-> (b, T, H, hd) -transpose(1,2)-> (b, H, T, hd)
Q = Q.view(b, T, num_heads, head_dim).transpose(1, 2)
# ... attention y bậc 3, thao tác trên 2 chiều cuối (T, hd), H head song song ...
# ngược lại: (b, H, T, hd) -> (b, T, H, hd) -> contiguous().view(b, T, d_out)
context = context.transpose(1, 2).contiguous().view(b, T, d_out)
out = self.out_proj(context)             # trộn thông tin giữa các head
```

Shape đã kiểm chứng 2026-08-11 với `(b=2, T=6, d_out=16, H=4)`: sau view+transpose là `(2, 4, 6, 4)`. Lưu ý `d_out % num_heads == 0`, và cần `.contiguous()` trước `.view()` sau transpose. Đối chiếu cách viết gộp QKV trong `nanoGPT/model.py` (class `CausalSelfAttention`) sau khi tự code xong.

### Vì sao attention là O(n²) — biết trước để Tuần 5+ đỡ ngạc nhiên

Ma trận scores là `(T, T)`: gấp đôi độ dài chuỗi thì compute và bộ nhớ attention tăng 4 lần. Đây là lý do tồn tại FlashAttention, sliding window, KV cache... (mục nâng cao C1–C2, B1 — đọc sau khi pass test).

---

## 4. Nguồn chính thức (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | License / loại | Dùng cho mục |
|-------|-----|----------------|--------------|
| Sennrich et al. 2015 — BPE cho NMT | https://arxiv.org/abs/1508.07909 — PDF local: [`../docs/papers/`](../docs/papers/README.md) | CC BY 4.0 (kiểm 2026-08-12) | 1 |
| Tokenization Falling Short (2024) | https://arxiv.org/abs/2406.11687 — chỉ link (arXiv non-exclusive) | arXiv mở (kiểm 2026-08-12) | 1.3 |
| openai/tiktoken | https://github.com/openai/tiktoken | MIT | 1.2 |
| karpathy/minbpe | https://github.com/karpathy/minbpe | MIT | 1.2, nâng cao E |
| karpathy/nanoGPT (`model.py`) | https://github.com/karpathy/nanoGPT | MIT | 3 |
| Vaswani et al. 2017 — Attention Is All You Need | https://arxiv.org/abs/1706.03762 | arXiv mở | 3 |
| The Annotated Transformer (Harvard NLP) | https://nlp.seas.harvard.edu/annotated-transformer/ | web mở | 2, 3 |

## Sau khi đọc xong

1. Chạy lại từng snippet ở mục 1–3 (gõ tay).
2. Tự code [`02_multihead_attention.py`](02_multihead_attention.py) theo đúng 4 bậc — không nhìn nanoGPT khi code lần đầu.
3. Chạy [`03_test_attention.py`](03_test_attention.py) → pass cả 3 test (2 shape + 1 causal).
4. Dán code nhờ Claude review, đối chiếu `nanoGPT/model.py`.
5. Làm [`quiz.md`](quiz.md), đối chiếu [`quiz_solution.md`](quiz_solution.md); rồi mới mở mục nâng cao (A1, A4–A5, B1, C1–C2, E).
