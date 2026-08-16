"""
02_gpt_model.py — SKELETON Tuần 4 (lắp ráp GPT-2 from scratch).

Lắp ráp kiến trúc GPT-2. Tái sử dụng MultiHeadAttention bạn viết ở Tuần 3.
Chỗ TODO là phần bạn điền. Tự code trước, đối chiếu nanoGPT sau.

Gợi ý import attention từ Tuần 3 (tên module bắt đầu bằng số → dùng importlib):
    import sys, importlib; sys.path.append("../Week-03")
    MultiHeadAttention = importlib.import_module("02_multihead_attention").MultiHeadAttention
"""

import torch
import torch.nn as nn

GPT_CONFIG_124M = {
    "vocab_size": 50257,
    "context_length": 1024,
    "emb_dim": 768,
    "n_heads": 12,
    "n_layers": 12,
    "drop_rate": 0.1,
    "qkv_bias": True,
}


class LayerNorm(nn.Module):
    def __init__(self, emb_dim, eps=1e-5):
        super().__init__()
        self.eps = eps
        self.scale = nn.Parameter(torch.ones(emb_dim))
        self.shift = nn.Parameter(torch.zeros(emb_dim))

    def forward(self, x):
        # TODO: chuẩn hóa theo chiều cuối:
        #   mean = x.mean(-1, keepdim=True)
        #   var  = x.var(-1, keepdim=True, unbiased=False)
        #   return self.scale * (x - mean) / sqrt(var + eps) + self.shift
        raise NotImplementedError("TODO: LayerNorm.forward")


class GELU(nn.Module):
    def forward(self, x):
        # TODO: GELU xấp xỉ (công thức tanh của GPT-2)
        #   0.5*x*(1+tanh( sqrt(2/pi)*(x+0.044715*x**3) ))
        raise NotImplementedError("TODO: GELU.forward")


class FeedForward(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        # TODO: Linear(emb_dim -> 4*emb_dim) -> GELU -> Linear(4*emb_dim -> emb_dim)
        raise NotImplementedError("TODO: FeedForward.__init__")

    def forward(self, x):
        raise NotImplementedError("TODO: FeedForward.forward")


class TransformerBlock(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        # TODO:
        #   self.att = MultiHeadAttention(cfg["emb_dim"], cfg["emb_dim"],
        #                cfg["context_length"], cfg["drop_rate"],
        #                cfg["n_heads"], cfg["qkv_bias"])
        #   self.ff = FeedForward(cfg)
        #   self.norm1 = LayerNorm(cfg["emb_dim"]); self.norm2 = LayerNorm(...)
        #   self.drop = nn.Dropout(cfg["drop_rate"])
        raise NotImplementedError("TODO: TransformerBlock.__init__")

    def forward(self, x):
        # TODO: pre-LN + residual:
        #   x = x + drop(att(norm1(x)))
        #   x = x + drop(ff(norm2(x)))
        raise NotImplementedError("TODO: TransformerBlock.forward")


class GPTModel(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.tok_emb = nn.Embedding(cfg["vocab_size"], cfg["emb_dim"])
        self.pos_emb = nn.Embedding(cfg["context_length"], cfg["emb_dim"])
        self.drop = nn.Dropout(cfg["drop_rate"])
        # TODO:
        #   self.trf_blocks = nn.Sequential(*[TransformerBlock(cfg) for _ in range(cfg["n_layers"])])
        #   self.final_norm = LayerNorm(cfg["emb_dim"])
        #   self.out_head = nn.Linear(cfg["emb_dim"], cfg["vocab_size"], bias=False)
        raise NotImplementedError("TODO: GPTModel.__init__")

    def forward(self, in_idx):
        # in_idx: (batch, seq_len)
        # TODO:
        #   b, t = in_idx.shape
        #   tok = self.tok_emb(in_idx)
        #   pos = self.pos_emb(torch.arange(t, device=in_idx.device))
        #   x = self.drop(tok + pos)
        #   x = self.trf_blocks(x); x = self.final_norm(x)
        #   logits = self.out_head(x)   # (b, t, vocab_size)
        raise NotImplementedError("TODO: GPTModel.forward")


def generate_text_simple(model, idx, max_new_tokens, context_size):
    """Greedy generation đơn giản (xem 01_theory_notes.md)."""
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -context_size:]
        with torch.no_grad():
            logits = model(idx_cond)
        logits = logits[:, -1, :]                  # token cuối
        next_id = torch.argmax(logits, dim=-1, keepdim=True)
        idx = torch.cat([idx, next_id], dim=1)
    return idx


# ----------------------------------------------------------------------
# 🚀 EXTENSION (tùy chọn): KV cache cho generation
# Lý thuyết: ../Week-00/advanced_topics_vi.md §B1.
# Làm SAU khi xong toàn bộ skeleton phía trên. Không bắt buộc cho deliverable.
# Ý tưởng: generate_text_simple chạy lại FULL forward trên cả chuỗi mỗi bước.
# Với KV cache, mỗi bước chỉ feed TOKEN MỚI; K,V của các token cũ được lưu
# lại per-layer và append thêm — attention vẫn nhìn đủ quá khứ.
# ----------------------------------------------------------------------
def generate_with_kv_cache(model, idx, max_new_tokens, context_size):
    """Greedy generation dùng KV cache (kết quả phải TRÙNG generate_text_simple)."""
    # EXT-TODO 1: thêm tham số `use_cache`/`kv_cache` xuyên suốt forward:
    #   - MultiHeadAttention.forward nhận cache (K_cũ, V_cũ) per-layer,
    #     tính K,V của token mới rồi torch.cat vào cache theo chiều thời gian;
    #   - GPTModel.forward trả thêm cache mới để bước sau dùng lại.
    #   Lưu ý pos_emb: token mới ở vị trí t = số token đã cache (không phải 0).
    # EXT-TODO 2: viết vòng generate: bước đầu feed cả prompt (prefill),
    #   các bước sau CHỈ feed next_id (shape (b, 1)) + cache;
    #   greedy argmax như generate_text_simple; dừng khi đủ max_new_tokens
    #   hoặc chạm context_size.
    raise NotImplementedError("EXT-TODO: generation với KV cache")


def check_kv_cache_matches(model, idx, max_new_tokens=8, context_size=64):
    """Sanity check: cached vs uncached phải cho CÙNG dãy token id (greedy)."""
    # EXT-TODO 3: chạy cả hai đường rồi assert khớp từng token:
    #   model.eval()
    #   with torch.no_grad():
    #       out_plain  = generate_text_simple(model, idx, max_new_tokens, context_size)
    #       out_cached = generate_with_kv_cache(model, idx, max_new_tokens, context_size)
    #   assert torch.equal(out_plain, out_cached), "KV cache làm lệch output!"
    #   (Greedy + eval() nên hai đường phải ra đúng một dãy id.)
    raise NotImplementedError("EXT-TODO: assert cached == uncached")


# ----------------------------------------------------------------------
# 🚀 EXTENSION (tùy chọn): RoPE — Rotary Position Embedding
# Lý thuyết: ../Week-00/advanced_topics_vi.md §A1.
# Làm SAU khi xong toàn bộ skeleton phía trên. Không bắt buộc cho deliverable.
# Ý tưởng: thay pos_emb học được bằng phép XOAY từng cặp chiều của q, k
# theo góc tỉ lệ với vị trí token. Attention score q·k khi đó chỉ phụ thuộc
# khoảng cách tương đối (m - n) — không phụ thuộc vị trí tuyệt đối.
# ----------------------------------------------------------------------
def precompute_rope_freqs(head_dim, max_len, base=10000):
    """Tính trước (cos, sin) cho mọi vị trí 0..max_len-1.

    Trả về tensor (hoặc tuple cos/sin) shape (max_len, head_dim // 2).
    """
    # EXT-TODO 4a: tính tần số cho từng CẶP chiều (head_dim phải chẵn):
    #   inv_freq = 1.0 / (base ** (torch.arange(0, head_dim, 2).float() / head_dim))
    #   pos = torch.arange(max_len).float()
    #   angles = torch.outer(pos, inv_freq)        # (max_len, head_dim//2)
    #   return torch.cos(angles), torch.sin(angles)
    raise NotImplementedError("EXT-TODO: precompute cos/sin cho RoPE")


def apply_rope(q, k, freqs):
    """Xoay q, k theo cặp chiều xen kẽ (interleaved pairs).

    q, k: (batch, n_heads, seq_len, head_dim); freqs = (cos, sin) đã cắt theo seq_len.
    """
    # EXT-TODO 4b: với mỗi cặp (x1, x2) = (x[..., 0::2], x[..., 1::2]):
    #   x1' = x1 * cos - x2 * sin
    #   x2' = x1 * sin + x2 * cos
    #   rồi ghép xen kẽ lại về shape ban đầu (stack theo chiều mới + flatten,
    #   hoặc dùng torch.stack([x1', x2'], dim=-1).flatten(-2)).
    #   Áp CÙNG phép xoay cho cả q và k; trả về (q_rot, k_rot).
    raise NotImplementedError("EXT-TODO: apply rotation cho q, k")


def check_rope_properties(head_dim=64, max_len=128):
    """Sanity check 2 tính chất của RoPE trên tensor ngẫu nhiên."""
    # EXT-TODO 5: kiểm tra bằng số (torch.allclose):
    #   (1) Vị trí 0 là identity: xoay q, k tại pos=0 (cos=1, sin=0)
    #       phải cho lại đúng q, k ban đầu.
    #   (2) Tính tương đối (shift-invariance): với q cố định ở pos m, k ở pos n,
    #       dot product (q_rot_m · k_rot_n) chỉ phụ thuộc (m - n).
    #       Cách check: chọn (m, n) và (m + s, n + s) với shift s bất kỳ,
    #       assert torch.allclose(dot(m, n), dot(m + s, n + s), atol=1e-5).
    #   Gợi ý: sinh q, k ngẫu nhiên shape (1, 1, max_len, head_dim),
    #   dùng precompute_rope_freqs + apply_rope ở trên.
    raise NotImplementedError("EXT-TODO: check identity tại pos 0 + shift-invariance")


# ----------------------------------------------------------------------
# 🚀 EXTENSION (tùy chọn): MoE FFN toy — Mixture of Experts
# Lý thuyết: ../Week-00/advanced_topics_vi.md §A7.
# Làm SAU khi xong toàn bộ skeleton phía trên. Không bắt buộc cho deliverable.
# LƯU Ý: đây là bài tập TOY ĐỘC LẬP để hiểu router + expert + aux loss,
# KHÔNG thay FFN trong GPT skeleton chính ở trên.
# Ý tưởng: thay 1 FFN dày bằng n_experts FFN nhỏ; router chọn top-k expert
# cho từng token; aux loss ép tải phân bổ đều giữa các expert (Switch
# Transformer, arXiv 2101.03961).
# ----------------------------------------------------------------------
class MoEFeedForward(nn.Module):
    """FFN kiểu MoE: router top-k trên n_experts expert nhỏ."""

    def __init__(self, emb_dim, n_experts=4, top_k=2):
        super().__init__()
        self.n_experts = n_experts
        self.top_k = top_k
        # EXT-TODO 6a: khởi tạo
        #   self.router = nn.Linear(emb_dim, n_experts, bias=False)
        #   self.experts = nn.ModuleList([
        #       nn.Sequential(nn.Linear(emb_dim, 4 * emb_dim), GELU(),
        #                     nn.Linear(4 * emb_dim, emb_dim))
        #       for _ in range(n_experts)])
        raise NotImplementedError("EXT-TODO: MoEFeedForward.__init__")

    def forward(self, x):
        """x: (batch, seq_len, emb_dim) → (output cùng shape, aux_loss scalar)."""
        # EXT-TODO 6b: router — chọn top-k expert cho từng token:
        #   logits = self.router(x)                        # (b, t, n_experts)
        #   probs = torch.softmax(logits, dim=-1)
        #   topk_probs, topk_idx = probs.topk(self.top_k, dim=-1)
        # EXT-TODO 6c: dispatch — tổng có trọng số output của các expert được chọn:
        #   out = torch.zeros_like(x)
        #   với mỗi expert e: mask = (topk_idx == e) → lấy token thuộc e,
        #   out[token] += trọng_số_router * self.experts[e](x[token])
        #   (cách chậm-nhưng-rõ: loop qua n_experts; đủ cho toy này.)
        # EXT-TODO 7a: aux load-balancing loss theo Switch Transformer:
        #   f_e = tỉ lệ token được GÁN cho expert e (trong top-k, tính từ topk_idx)
        #   p_e = trung bình xác suất router cho expert e (từ probs, trên mọi token)
        #   aux_loss = n_experts * sum(f_e * p_e)
        #   return out, aux_loss
        raise NotImplementedError("EXT-TODO: router + dispatch + aux loss")


def check_moe_shapes(emb_dim=32, batch=2, seq_len=8):
    """Sanity check: output shape khớp input, aux_loss là scalar > 0."""
    # EXT-TODO 7b: chạy trên input ngẫu nhiên và assert:
    #   moe = MoEFeedForward(emb_dim)
    #   x = torch.randn(batch, seq_len, emb_dim)
    #   out, aux_loss = moe(x)
    #   assert out.shape == x.shape, "MoE làm đổi shape!"
    #   assert aux_loss.dim() == 0 and aux_loss.item() > 0, "aux_loss phải là scalar > 0"
    raise NotImplementedError("EXT-TODO: assert shape + aux_loss scalar")


if __name__ == "__main__":
    torch.manual_seed(123)
    model = GPTModel(GPT_CONFIG_124M)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Tổng tham số: {n_params:,}  (~124M nếu đúng)")
