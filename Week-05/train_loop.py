"""
train_loop.py — SKELETON Tuần 5 (pretraining loop).

Pretraining loop cho GPT bạn build ở Tuần 4. Bắt đầu local với một text nhỏ
thuộc public domain (vd. truyện ngắn từ Project Gutenberg), rồi mang lên cloud
cho dataset lớn.

Chỗ TODO là phần bạn điền. Tự code trước, đối chiếu nanoGPT/train.py sau.

Import model từ Tuần 4:
    import sys; sys.path.append("../Week-04")
    from gpt_model import GPTModel, GPT_CONFIG_124M
"""

import torch


# ---------------------------------------------------------------
# Loss
# ---------------------------------------------------------------
def calc_loss_batch(input_batch, target_batch, model, device):
    input_batch = input_batch.to(device)
    target_batch = target_batch.to(device)
    logits = model(input_batch)  # (b, T, vocab)
    # TODO: cross-entropy giữa logits.flatten(0,1) và target_batch.flatten()
    #   return torch.nn.functional.cross_entropy(
    #       logits.flatten(0, 1), target_batch.flatten())
    raise NotImplementedError("TODO: calc_loss_batch")


def calc_loss_loader(data_loader, model, device, num_batches=None):
    total, n = 0.0, 0
    for i, (xb, yb) in enumerate(data_loader):
        if num_batches is not None and i >= num_batches:
            break
        total += calc_loss_batch(xb, yb, model, device).item()
        n += 1
    return total / max(n, 1)


# ---------------------------------------------------------------
# LR schedule: warmup tuyến tính + cosine decay
# ---------------------------------------------------------------
def get_lr(step, max_lr, warmup_steps, max_steps, min_lr_ratio=0.1):
    import math
    min_lr = max_lr * min_lr_ratio
    # TODO:
    #   if step < warmup_steps: return max_lr * (step + 1) / warmup_steps
    #   if step > max_steps: return min_lr
    #   ratio = (step - warmup_steps) / (max_steps - warmup_steps)
    #   coeff = 0.5 * (1 + cos(pi * ratio))
    #   return min_lr + coeff * (max_lr - min_lr)
    raise NotImplementedError("TODO: get_lr (warmup + cosine)")


# ---------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------
def train_model(model, train_loader, val_loader, optimizer, device,
                num_epochs, max_lr, warmup_steps, max_steps,
                grad_accum_steps=1, clip=1.0, eval_every=100):
    model.to(device)
    step = 0
    use_amp = device == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    track = {"step": [], "train": [], "val": []}

    for epoch in range(num_epochs):
        for micro, (xb, yb) in enumerate(train_loader):
            # TODO các bước (chú ý grad accumulation):
            #   - tính lr = get_lr(step, ...) và set vào optimizer.param_groups
            #   - với autocast(enabled=use_amp): loss = calc_loss_batch(...) / grad_accum_steps
            #   - scaler.scale(loss).backward()
            #   - khi (micro+1) % grad_accum_steps == 0:
            #       scaler.unscale_(optimizer)
            #       clip_grad_norm_(model.parameters(), clip)
            #       scaler.step(optimizer); scaler.update(); optimizer.zero_grad()
            #       step += 1
            raise NotImplementedError("TODO: 1 bước training với grad accumulation")

            if step % eval_every == 0:
                model.eval()
                tl = calc_loss_loader(train_loader, model, device, num_batches=5)
                vl = calc_loss_loader(val_loader, model, device, num_batches=5)
                model.train()
                track["step"].append(step)
                track["train"].append(tl)
                track["val"].append(vl)
                print(f"step {step:5d} | train {tl:.3f} | val {vl:.3f} | lr {get_lr(step, max_lr, warmup_steps, max_steps):.2e}")
    return track


def save_checkpoint(path, model, optimizer, step):
    torch.save(
        {"model": model.state_dict(), "optimizer": optimizer.state_dict(), "step": step},
        path,
    )
    print(f"Đã lưu checkpoint: {path}")


if __name__ == "__main__":
    print("Skeleton Tuần 5. Điền TODO rồi nối với DataLoader trên một text public-domain nhỏ.")
