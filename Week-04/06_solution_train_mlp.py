"""
06_solution_train_mlp.py: LỜI GIẢI THAM KHẢO cho ba phần của 05_train_mlp.py.

CHỈ mở file này SAU KHI bạn đã tự code xong 05_train_mlp.py.
Dùng để đối chiếu, không phải để copy.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


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
    n_val = int(len(X) * frac)
    return (X[:-n_val], y[:-n_val]), (X[-n_val:], y[-n_val:])


def get_device():
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


class LogisticRegression(nn.Module):
    """Một ánh xạ tuyến tính (Tuần 1) + softmax/CE (Tuần 2 mục B6). Không có lớp ẩn."""

    def __init__(self, in_dim=2, out_dim=2):
        super().__init__()
        self.linear = nn.Linear(in_dim, out_dim)

    def forward(self, x):
        return self.linear(x)


def compare_with_hand_gradient(model, X, y):
    """Gradient autograd của W phải bằng công thức tay Tuần 3 viết cho hai lớp: (p - onehot)^T X / n."""
    model.zero_grad()
    logits = model(X)
    loss = nn.CrossEntropyLoss()(logits, y)
    loss.backward()
    with torch.no_grad():
        p = F.softmax(logits, dim=1)
        dlogits = (p - F.one_hot(y, num_classes=p.shape[1]).float()) / len(y)
        dW_hand = dlogits.T @ X                      # shape (out, in), khớp layout của nn.Linear
        db_hand = dlogits.sum(0)
    ok_w = torch.allclose(model.linear.weight.grad, dW_hand, atol=1e-6)
    ok_b = torch.allclose(model.linear.bias.grad, db_hand, atol=1e-6)
    print(f"Gradient autograd khớp gradient tay Tuần 3? W: {ok_w}, b: {ok_b}")


class MLP(nn.Module):
    def __init__(self, in_dim=2, hidden=32, out_dim=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x):
        return self.net(x)


def train(model, X, y, epochs=200, lr=0.1, device="cpu"):
    model.to(device)
    X = torch.from_numpy(X).to(device)
    y = torch.from_numpy(y).to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    for epoch in range(epochs):
        optimizer.zero_grad()          # thứ mới so với vòng lặp NumPy Tuần 3
        logits = model(X)
        loss = loss_fn(logits, y)
        loss.backward()                # thay cho hàm grad viết tay
        optimizer.step()               # thay cho w -= lr * grad
        if (epoch + 1) % 50 == 0:
            print(f"  epoch {epoch + 1:3d} | loss {loss.item():.4f}")
    return model


@torch.no_grad()
def accuracy(model, X, y, device="cpu"):
    X = torch.from_numpy(X).to(device)
    y = torch.from_numpy(y).to(device)
    return (model(X).argmax(1) == y).float().mean().item()


def main():
    torch.manual_seed(0)
    device = get_device()
    print(f"Device: {device}")
    X, y = make_moons(n=1000, noise=0.15)
    (X_tr, y_tr), (X_val, y_val) = split_holdout(X, y)
    print(f"Train: {X_tr.shape}, held-out: {X_val.shape}")

    logreg = LogisticRegression()
    compare_with_hand_gradient(logreg, torch.from_numpy(X_tr[:64]), torch.from_numpy(y_tr[:64]))
    print("Logistic regression:")
    train(logreg, X_tr, y_tr, epochs=200, lr=0.05, device=device)
    print(f"Logistic regression | accuracy held-out = {accuracy(logreg, X_val, y_val, device):.3f}")

    mlp = MLP()
    print("MLP:")
    train(mlp, X_tr, y_tr, epochs=200, lr=0.05, device=device)
    print(f"MLP                 | accuracy held-out = {accuracy(mlp, X_val, y_val, device):.3f}")
    print("\nVì sao MLP cao hơn: two moons không tách được bằng một đường thẳng, nên lớp giả thuyết")
    print("của logistic regression có approximation error lớn (Tuần 3 mục 3). Thêm lớp ẩn + ReLU mở")
    print("rộng lớp giả thuyết, approximation error giảm; với 800 điểm train, estimation error chưa đáng kể.")


if __name__ == "__main__":
    main()
