"""
03_check_grad.py — Kiểm tra micrograd của bạn cho gradient ĐÚNG bằng cách
so với PyTorch autograd trên cùng một biểu thức.

Chạy SAU KHI điền xong các TODO trong 02_micrograd.py:
    python 03_check_grad.py

Cần PyTorch để đối chiếu (chạy được trên máy bạn).
"""

import importlib

# Tên module bắt đầu bằng chữ số không dùng được với "import ..." thường,
# phải nạp qua importlib.
Value = importlib.import_module("02_micrograd").Value


def micrograd_expr():
    # f = tanh( (a*b + c) ) * d   với d = relu(a + 2)
    a = Value(2.0)
    b = Value(-3.0)
    c = Value(10.0)
    d = (a + 2.0).relu()
    f = ((a * b + c).tanh()) * d
    f.backward()
    return {"a": a.grad, "b": b.grad, "c": c.grad}, f.data


def torch_expr():
    import torch

    a = torch.tensor(2.0, requires_grad=True)
    b = torch.tensor(-3.0, requires_grad=True)
    c = torch.tensor(10.0, requires_grad=True)
    d = torch.relu(a + 2.0)
    f = torch.tanh(a * b + c) * d
    f.backward()
    return {"a": a.grad.item(), "b": b.grad.item(), "c": c.grad.item()}, f.item()


def main():
    g_mine, f_mine = micrograd_expr()
    try:
        g_torch, f_torch = torch_expr()
    except ImportError:
        print("Chưa có PyTorch — chỉ in kết quả micrograd:")
        print("  f =", f_mine, "| grads =", g_mine)
        return

    print(f"forward:  micrograd={f_mine:.6f}  torch={f_torch:.6f}")
    ok = abs(f_mine - f_torch) < 1e-5
    for k in ["a", "b", "c"]:
        diff = abs(g_mine[k] - g_torch[k])
        ok = ok and diff < 1e-5
        print(f"  d/d{k}:  micrograd={g_mine[k]:+.6f}  torch={g_torch[k]:+.6f}  diff={diff:.2e}")
    print("\n=> KHỚP! Backprop của bạn đúng." if ok else "\n=> CHƯA khớp — kiểm tra lại các _backward.")


if __name__ == "__main__":
    main()
