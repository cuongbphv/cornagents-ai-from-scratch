"""
test_attention.py — Kiểm tra SHAPE cho attention bạn tự code.

Chạy SAU KHI điền xong TODO trong multihead_attention.py:
    python test_attention.py

Test không kiểm tra giá trị tuyệt đối, chỉ xác nhận luồng shape đúng —
đây là cách Raschka khuyến nghị để bắt bug attention.
"""

import torch
from multihead_attention import CausalSelfAttention, MultiHeadAttention


def test_single_head():
    b, T, d_in, d_out = 2, 6, 8, 16
    x = torch.randn(b, T, d_in)
    attn = CausalSelfAttention(d_in, d_out, context_length=T, dropout=0.0)
    out = attn(x)
    assert out.shape == (b, T, d_out), f"sai shape: {out.shape}"
    print(f"[OK] CausalSelfAttention -> {tuple(out.shape)}")


def test_multi_head():
    b, T, d_in, d_out, heads = 2, 6, 8, 16, 4
    x = torch.randn(b, T, d_in)
    attn = MultiHeadAttention(d_in, d_out, context_length=T, dropout=0.0, num_heads=heads)
    out = attn(x)
    assert out.shape == (b, T, d_out), f"sai shape: {out.shape}"
    print(f"[OK] MultiHeadAttention ({heads} heads) -> {tuple(out.shape)}")


def test_causal_property():
    """Token đầu tiên không được 'nhìn' token sau: đổi token tương lai
    không làm đổi output ở vị trí 0."""
    torch.manual_seed(0)
    b, T, d_in, d_out = 1, 5, 4, 4
    attn = CausalSelfAttention(d_in, d_out, context_length=T, dropout=0.0)
    attn.eval()
    x1 = torch.randn(b, T, d_in)
    x2 = x1.clone()
    x2[:, 1:, :] = torch.randn(b, T - 1, d_in)  # đổi mọi token sau vị trí 0
    with torch.no_grad():
        o1 = attn(x1)
        o2 = attn(x2)
    assert torch.allclose(o1[:, 0], o2[:, 0], atol=1e-5), "causal bị vi phạm!"
    print("[OK] Tính causal đúng: vị trí 0 độc lập với token tương lai")


if __name__ == "__main__":
    test_single_head()
    test_multi_head()
    test_causal_property()
    print("\n=> Tất cả test shape PASS.")
