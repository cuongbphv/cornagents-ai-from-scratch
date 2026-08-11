"""
gpt_model.py — SKELETON Tuần 4 (lắp ráp GPT-2 from scratch).

Lắp ráp kiến trúc GPT-2. Tái sử dụng MultiHeadAttention bạn viết ở Tuần 3.
Chỗ TODO là phần bạn điền. Tự code trước, đối chiếu nanoGPT sau.

Gợi ý import attention từ Tuần 3:
    import sys; sys.path.append("../Week-03")
    from multihead_attention import MultiHeadAttention
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
    """Greedy generation đơn giản (ch.4)."""
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -context_size:]
        with torch.no_grad():
            logits = model(idx_cond)
        logits = logits[:, -1, :]                  # token cuối
        next_id = torch.argmax(logits, dim=-1, keepdim=True)
        idx = torch.cat([idx, next_id], dim=1)
    return idx


if __name__ == "__main__":
    torch.manual_seed(123)
    model = GPTModel(GPT_CONFIG_124M)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Tổng tham số: {n_params:,}  (~124M nếu đúng)")
