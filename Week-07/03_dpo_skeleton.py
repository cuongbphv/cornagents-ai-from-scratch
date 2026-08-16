"""
03_dpo_skeleton.py — SKELETON Tuần 7 (DPO loss from scratch).

TỰ TAY code loss DPO trên logprob cố định (toy), không cần model/data thật,
không cần mạng. Chỗ TODO là phần bạn điền. Đối chiếu paper DPO
(arXiv 2305.18290) + FareedKhan src/post_training/ sau khi tự làm.

Công thức (01_theory_notes.md mục 4):
    L_DPO = -log σ( β·[ log πθ(y_w|x)/πref(y_w|x) − log πθ(y_l|x)/πref(y_l|x) ] )

Check cuối file tái lập ĐÚNG ví dụ toy đã kiểm chứng trong
01_theory_notes.md mục 4: log-ratio chosen 0.5, rejected −0.3, β=0.1
→ loss 0.6539 (kiểm bằng PyTorch 2.5.1, 2026-08-11).

Chạy:  python 03_dpo_skeleton.py
"""

import torch
import torch.nn.functional as F


def dpo_log_ratios(policy_logps, ref_logps):
    """Log-ratio log πθ(y|x) − log πref(y|x) cho một batch câu trả lời.

    policy_logps, ref_logps: tensor (batch,) — tổng logprob của cả câu.
    """
    # TODO 1: trả về policy_logps - ref_logps (shape (batch,)).
    #   Lưu ý: log(a/b) = log a − log b — làm việc trên LOGprob, không prob.
    raise NotImplementedError("TODO: tính log-ratio")


def dpo_loss(chosen_ratio, rejected_ratio, beta=0.1):
    """Loss DPO cho từng cặp (chosen, rejected). Trả về (loss, margin).

    chosen_ratio / rejected_ratio: log-ratio từ dpo_log_ratios, shape (batch,).
    """
    # TODO 2: margin = beta * (chosen_ratio - rejected_ratio)
    #   Đây chính là hiệu "reward ẩn" — β·log-ratio là implicit reward của DPO.
    # TODO 3: loss = -F.logsigmoid(margin)   (shape (batch,))
    #   Vì sao -logsigmoid chứ không -log(sigmoid)? Ổn định số học (tránh
    #   sigmoid saturate về 0 rồi log(0)).
    # TODO 4: return loss.mean(), margin.mean()
    raise NotImplementedError("TODO: loss DPO + implicit reward margin")


def implicit_rewards(chosen_ratio, rejected_ratio, beta=0.1):
    """Reward ẩn r̂ = β·log-ratio cho chosen và rejected (để log khi train)."""
    # TODO 5: return beta * chosen_ratio, beta * rejected_ratio
    #   Khi train thật, theo dõi hiệu hai giá trị này tăng dần = policy đang
    #   tách chosen khỏi rejected so với reference.
    raise NotImplementedError("TODO: implicit reward")


if __name__ == "__main__":
    # Toy cố định — khớp ví dụ ĐÃ KIỂM CHỨNG ở 01_theory_notes.md mục 4:
    # log-ratio chosen 0.5, rejected −0.3, β=0.1 → loss 0.6539.
    # Dựng logprob sao cho hiệu ra đúng các log-ratio đó:
    policy_chosen = torch.tensor([-1.0])   # log πθ(y_w|x)
    ref_chosen = torch.tensor([-1.5])      # log πref(y_w|x)  → ratio +0.5
    policy_rejected = torch.tensor([-2.3])  # log πθ(y_l|x)
    ref_rejected = torch.tensor([-2.0])     # log πref(y_l|x) → ratio −0.3

    chosen_ratio = dpo_log_ratios(policy_chosen, ref_chosen)
    rejected_ratio = dpo_log_ratios(policy_rejected, ref_rejected)
    assert torch.allclose(chosen_ratio, torch.tensor([0.5]))
    assert torch.allclose(rejected_ratio, torch.tensor([-0.3]))

    loss, margin = dpo_loss(chosen_ratio, rejected_ratio, beta=0.1)
    r_chosen, r_rejected = implicit_rewards(chosen_ratio, rejected_ratio, beta=0.1)

    print(f"log-ratio chosen  = {chosen_ratio.item():+.4f}")
    print(f"log-ratio rejected= {rejected_ratio.item():+.4f}")
    print(f"implicit reward: chosen {r_chosen.item():+.4f} | rejected {r_rejected.item():+.4f}")
    print(f"margin = {margin.item():.4f} | loss = {loss.item():.4f}")

    # Assert khớp con số đã kiểm chứng trong 01_theory_notes.md mục 4.
    assert abs(loss.item() - 0.6539) < 1e-4, f"loss {loss.item():.4f} != 0.6539"
    print("\nOK — khớp ví dụ đã kiểm chứng (loss 0.6539). Bạn code DPO đúng.")
