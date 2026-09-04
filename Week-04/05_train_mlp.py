"""
05_train_mlp.py: SKELETON Tuần 4, ba phần.

Phần 1: sinh dữ liệu two moons và tách held-out (Tuần 3 mục 5: không chọn model bằng dữ liệu
        dùng để train).
Phần 2: viết lại logistic regression của Tuần 3 (04_logistic_regression_numpy.py) bằng
        nn.Linear và autograd. Gradient tay của bạn ở Tuần 3 là X^T (p - y) / n; ở đây
        loss.backward() phải cho ra cùng con số trên cùng một batch.
Phần 3: chồng thêm một lớp ẩn thành MLP, train bằng CÙNG training loop, so accuracy held-out.

Triết lý của roadmap: TỰ code trước, nhờ Claude review sau. Đừng copy lời giải.
Dữ liệu sinh bằng numpy thuần nên KHÔNG cần scikit-learn.

Chạy:  python 05_train_mlp.py
"""

import numpy as np
import torch
import torch.nn as nn


# ----------------------------------------------------------------------
# 1) Dữ liệu two moons + tách held-out
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


def split_holdout(X, y, frac=0.2):
    """Tách phần cuối làm held-out. Dữ liệu đã được trộn ngẫu nhiên trong make_moons."""
    n_val = int(len(X) * frac)
    return (X[:-n_val], y[:-n_val]), (X[-n_val:], y[-n_val:])


def get_device():
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


# ----------------------------------------------------------------------
# 2) Logistic regression bằng PyTorch  : :  TODO: BẠN tự viết lại bài Tuần 3
# ----------------------------------------------------------------------
class LogisticRegression(nn.Module):
    def __init__(self, in_dim=2, out_dim=2):
        super().__init__()
        # TODO: một nn.Linear(in_dim, out_dim). Không có lớp ẩn, không có activation.
        #   Với out_dim=2 và CrossEntropyLoss, đây là bản 2 lớp của sigmoid + BCE ở Tuần 3
        #   (softmax hai lớp rút gọn về sigmoid). Thử tự chứng minh điều đó trên giấy.
        raise NotImplementedError("TODO: định nghĩa nn.Linear")

    def forward(self, x):
        # TODO: trả về logits shape (batch, out_dim)
        raise NotImplementedError("TODO: viết forward pass")


def compare_with_hand_gradient(model, X, y):
    """Đối chiếu gradient autograd với công thức tay của Tuần 3 trên một batch.

    TODO: với model là LogisticRegression, lấy W = model.linear.weight (shape (2, 2)).
      1. logits = model(X); loss = CrossEntropyLoss()(logits, y); loss.backward().
      2. Tính tay: p = softmax(logits); dL/dlogits = (p - onehot(y)) / n; dL/dW = dL/dlogits^T @ X.
      3. In torch.allclose(W.grad, dL/dW, atol=1e-6). Phải là True.
    Đây là hàm grad của Tuần 3 (X^T (p - y) / n) viết cho hai lớp.
    """
    raise NotImplementedError("TODO: đối chiếu gradient autograd với gradient tay")


# ----------------------------------------------------------------------
# 3) MLP  : :  TODO: thêm một lớp ẩn vào giữa
# ----------------------------------------------------------------------
class MLP(nn.Module):
    def __init__(self, in_dim=2, hidden=32, out_dim=2):
        super().__init__()
        # TODO: nn.Linear(in_dim, hidden) -> nn.ReLU() -> nn.Linear(hidden, out_dim)
        #   Có thể dùng nn.Sequential hoặc khai báo từng layer rồi viết forward.
        raise NotImplementedError("TODO: định nghĩa các layer của MLP")

    def forward(self, x):
        # TODO: trả về logits shape (batch, out_dim)
        raise NotImplementedError("TODO: viết forward pass")


# ----------------------------------------------------------------------
# 4) Một training loop dùng chung cho cả hai model  : :  TODO: BẠN tự viết
# ----------------------------------------------------------------------
def train(model, X, y, epochs=200, lr=0.1, device="cpu"):
    model.to(device)
    X = torch.from_numpy(X).to(device)
    y = torch.from_numpy(y).to(device)

    # TODO: chọn loss function. Phân loại nhiều lớp -> dùng cái nào? (nhận logits + nhãn index)
    loss_fn = None  # TODO

    # TODO: chọn optimizer (vd. torch.optim.SGD hoặc Adam) với model.parameters()
    optimizer = None  # TODO

    for epoch in range(epochs):
        # TODO: 5 bước kinh điển của 1 training step (02_theory_notes.md mục 4.3):
        #   (a) optimizer.zero_grad()      <- thứ mới so với vòng lặp NumPy Tuần 3
        #   (b) logits = model(X)
        #   (c) loss = loss_fn(logits, y)
        #   (d) loss.backward()            <- thay cho hàm grad viết tay
        #   (e) optimizer.step()           <- thay cho w -= lr * grad
        raise NotImplementedError("TODO: viết 1 bước training")

        # (sau khi xong, bỏ raise ở trên và bật phần log dưới đây)
        # if (epoch + 1) % 50 == 0:
        #     print(f"epoch {epoch+1:3d} | loss {loss.item():.4f}")


@torch.no_grad()
def accuracy(model, X, y, device="cpu"):
    X = torch.from_numpy(X).to(device)
    y = torch.from_numpy(y).to(device)
    return (model(X).argmax(1) == y).float().mean().item()


def main():
    device = get_device()
    print(f"Device: {device}")
    X, y = make_moons(n=1000, noise=0.15)
    (X_tr, y_tr), (X_val, y_val) = split_holdout(X, y)
    print(f"Train: {X_tr.shape}, held-out: {X_val.shape}")

    logreg = LogisticRegression()
    compare_with_hand_gradient(logreg, torch.from_numpy(X_tr[:64]), torch.from_numpy(y_tr[:64]))
    train(logreg, X_tr, y_tr, epochs=200, lr=0.1, device=device)
    print(f"Logistic regression | accuracy held-out = {accuracy(logreg, X_val, y_val, device):.3f}")

    mlp = MLP(in_dim=2, hidden=32, out_dim=2)
    train(mlp, X_tr, y_tr, epochs=200, lr=0.1, device=device)
    print(f"MLP                 | accuracy held-out = {accuracy(mlp, X_val, y_val, device):.3f}")

    print("\nCâu hỏi: vì sao MLP cao hơn? Trả lời bằng khái niệm lớp giả thuyết của Tuần 3 mục 2 và 3.")
    print("Bước tiếp: dán code này cho Claude để review so với cách chuẩn.")


if __name__ == "__main__":
    main()
