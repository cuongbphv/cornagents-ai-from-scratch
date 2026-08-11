"""
train_mlp.py — SKELETON Tuần 1.

Mục tiêu: TỰ TAY code một MLP nhỏ + training loop trên toy dataset.
Triết lý của roadmap: TỰ code trước, nhờ Claude review sau. Đừng copy lời giải.

Toy task: phân loại 2D "two moons" (2 lớp). Dữ liệu sinh bằng numpy thuần
nên KHÔNG cần scikit-learn.

Phần khung (data, device, vòng lặp ngoài) đã có sẵn.
Chỗ có TODO là phần BẠN tự điền để thực sự hiểu.

Chạy:  python train_mlp.py
"""

import numpy as np
import torch
import torch.nn as nn


# ----------------------------------------------------------------------
# 1) Toy dataset: "two moons" (tự sinh, không cần thư viện ngoài)
# ----------------------------------------------------------------------
def make_moons(n=1000, noise=0.15, seed=0):
    rng = np.random.default_rng(seed)
    n_a = n // 2
    n_b = n - n_a
    t_a = np.pi * rng.random(n_a)
    t_b = np.pi * rng.random(n_b)
    xa = np.stack([np.cos(t_a), np.sin(t_a)], axis=1)
    xb = np.stack([1 - np.cos(t_b), 0.5 - np.sin(t_b)], axis=1)
    X = np.concatenate([xa, xb], axis=0)
    y = np.concatenate([np.zeros(n_a), np.ones(n_b)], axis=0)
    X += noise * rng.standard_normal(X.shape)
    perm = rng.permutation(n)
    return X[perm].astype(np.float32), y[perm].astype(np.int64)


def get_device():
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


# ----------------------------------------------------------------------
# 2) Mô hình MLP  —— TODO: BẠN tự định nghĩa
# ----------------------------------------------------------------------
class MLP(nn.Module):
    def __init__(self, in_dim=2, hidden=32, out_dim=2):
        super().__init__()
        # TODO: định nghĩa các layer.
        #   Gợi ý: nn.Linear(in_dim, hidden) -> nn.ReLU() -> nn.Linear(hidden, out_dim)
        #   Có thể dùng nn.Sequential hoặc khai báo từng layer rồi viết forward.
        raise NotImplementedError("TODO: định nghĩa các layer của MLP")

    def forward(self, x):
        # TODO: trả về logits shape (batch, out_dim)
        raise NotImplementedError("TODO: viết forward pass")


# ----------------------------------------------------------------------
# 3) Training loop  —— TODO: BẠN tự viết
# ----------------------------------------------------------------------
def train(model, X, y, epochs=200, lr=0.1, device="cpu"):
    model.to(device)
    X = torch.from_numpy(X).to(device)
    y = torch.from_numpy(y).to(device)

    # TODO: chọn loss function. Phân loại nhiều lớp -> dùng cái nào?
    #   Gợi ý: nn.CrossEntropyLoss() (nhận logits + nhãn dạng index)
    loss_fn = None  # TODO

    # TODO: chọn optimizer (vd. torch.optim.SGD hoặc Adam) với model.parameters()
    optimizer = None  # TODO

    for epoch in range(epochs):
        # TODO: 5 bước kinh điển của 1 training step:
        #   (a) optimizer.zero_grad()
        #   (b) logits = model(X)
        #   (c) loss = loss_fn(logits, y)
        #   (d) loss.backward()
        #   (e) optimizer.step()
        raise NotImplementedError("TODO: viết 1 bước training")

        # (sau khi xong, bỏ raise ở trên và bật phần log dưới đây)
        # if (epoch + 1) % 20 == 0:
        #     acc = (logits.argmax(1) == y).float().mean().item()
        #     print(f"epoch {epoch+1:3d} | loss {loss.item():.4f} | acc {acc:.3f}")


def main():
    device = get_device()
    print(f"Device: {device}")
    X, y = make_moons(n=1000, noise=0.15)
    print(f"Dataset: X={X.shape}, y={y.shape}, số lớp={len(set(y.tolist()))}")

    model = MLP(in_dim=2, hidden=32, out_dim=2)
    train(model, X, y, epochs=200, lr=0.1, device=device)

    print("\nXong! Khi loss giảm và acc > ~0.95 là bạn đã làm đúng.")
    print("Bước tiếp: dán code này cho Claude để review so với cách chuẩn.")


if __name__ == "__main__":
    main()
