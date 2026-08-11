"""
06_solution_train_mlp.py — LỜI GIẢI THAM KHẢO.

CHỈ mở file này SAU KHI bạn đã tự code xong 05_train_mlp.py.
Dùng để đối chiếu, không phải để copy.
"""

import numpy as np
import torch
import torch.nn as nn


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


class MLP(nn.Module):
    def __init__(self, in_dim=2, hidden=32, out_dim=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
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
        optimizer.zero_grad()
        logits = model(X)
        loss = loss_fn(logits, y)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            acc = (logits.argmax(1) == y).float().mean().item()
            print(f"epoch {epoch + 1:3d} | loss {loss.item():.4f} | acc {acc:.3f}")
    return model


def main():
    device = get_device()
    print(f"Device: {device}")
    X, y = make_moons(n=1000, noise=0.15)
    print(f"Dataset: X={X.shape}, y={y.shape}")
    model = MLP()
    train(model, X, y, epochs=200, lr=0.01, device=device)


if __name__ == "__main__":
    main()
