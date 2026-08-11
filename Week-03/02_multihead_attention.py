"""
02_multihead_attention.py — SKELETON Tuần 3 (attention from scratch).

TỰ code attention stack: self-attention -> causal -> multi-head.
Chỗ TODO là phần bạn điền. Tự làm trước, đối chiếu nanoGPT/model.py + chạy 03_test_attention.py sau.
"""

import torch
import torch.nn as nn


class CausalSelfAttention(nn.Module):
    """Single-head scaled dot-product attention CÓ causal mask + dropout."""

    def __init__(self, d_in, d_out, context_length, dropout=0.0, qkv_bias=False):
        super().__init__()
        self.d_out = d_out
        # TODO: 3 lớp Linear không bias (trừ khi qkv_bias) cho Q, K, V: d_in -> d_out
        #   self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        #   self.W_key   = ...
        #   self.W_value = ...
        self.dropout = nn.Dropout(dropout)
        # mask tam giác trên (gồm đường chéo +1) = vị trí tương lai cần che
        self.register_buffer(
            "mask",
            torch.triu(torch.ones(context_length, context_length), diagonal=1),
        )
        raise NotImplementedError("TODO: khởi tạo W_query/W_key/W_value")

    def forward(self, x):
        # x: (batch, num_tokens, d_in)
        b, num_tokens, d_in = x.shape
        # TODO:
        #   queries = self.W_query(x)   # (b, num_tokens, d_out)
        #   keys    = self.W_key(x)
        #   values  = self.W_value(x)
        #   attn_scores = queries @ keys.transpose(1, 2)        # (b, T, T)
        #   attn_scores = attn_scores.masked_fill(
        #       self.mask.bool()[:num_tokens, :num_tokens], -torch.inf)
        #   attn_weights = torch.softmax(attn_scores / keys.shape[-1]**0.5, dim=-1)
        #   attn_weights = self.dropout(attn_weights)
        #   context = attn_weights @ values                     # (b, T, d_out)
        #   return context
        raise NotImplementedError("TODO: forward causal self-attention")


class MultiHeadAttention(nn.Module):
    """Multi-head: chia d_out thành num_heads head song song."""

    def __init__(self, d_in, d_out, context_length, dropout=0.0, num_heads=2, qkv_bias=False):
        super().__init__()
        assert d_out % num_heads == 0, "d_out phải chia hết cho num_heads"
        self.d_out = d_out
        self.num_heads = num_heads
        self.head_dim = d_out // num_heads
        # TODO: W_query/W_key/W_value (d_in -> d_out) + out_proj (d_out -> d_out)
        self.dropout = nn.Dropout(dropout)
        self.register_buffer(
            "mask",
            torch.triu(torch.ones(context_length, context_length), diagonal=1),
        )
        raise NotImplementedError("TODO: khởi tạo các lớp multi-head")

    def forward(self, x):
        b, num_tokens, d_in = x.shape
        # TODO các bước:
        #   1) tính Q,K,V -> (b, T, d_out)
        #   2) reshape -> (b, T, num_heads, head_dim) rồi transpose -> (b, num_heads, T, head_dim)
        #   3) attn_scores = Q @ K.transpose(2,3)  -> (b, num_heads, T, T)
        #   4) áp mask + softmax(.../ head_dim**0.5) + dropout
        #   5) context = attn @ V -> (b, num_heads, T, head_dim)
        #   6) transpose lại + reshape -> (b, T, d_out), qua out_proj
        raise NotImplementedError("TODO: forward multi-head attention")
