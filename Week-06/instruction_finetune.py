"""
instruction_finetune.py — SKELETON Tuần 6 (instruction fine-tuning).

Instruction fine-tuning cho GPT bạn build (Tuần 4) hoặc một pretrained nhỏ.
Chỗ TODO là phần bạn điền. Tự code trước, đối chiếu ch.7 sau.

Import model + loss từ các tuần trước:
    import sys; sys.path.append("../Week-04"); sys.path.append("../Week-05")
    from gpt_model import GPTModel, GPT_CONFIG_124M
    from train_loop import calc_loss_batch
"""

import torch
from torch.utils.data import Dataset


# ---------------------------------------------------------------
# 1) Prompt template kiểu Alpaca
# ---------------------------------------------------------------
def format_input(entry):
    """entry = {"instruction":..., "input":..., "output":...}"""
    text = (
        "Below is an instruction that describes a task. "
        "Write a response that appropriately completes the request.\n\n"
        f"### Instruction:\n{entry['instruction']}"
    )
    if entry.get("input"):
        text += f"\n\n### Input:\n{entry['input']}"
    return text


# ---------------------------------------------------------------
# 2) Dataset: tokenize prompt + response
# ---------------------------------------------------------------
class InstructionDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.encoded = []
        for entry in data:
            # TODO:
            #   prompt = format_input(entry)
            #   full = prompt + "\n\n### Response:\n" + entry["output"]
            #   self.encoded.append(tokenizer.encode(full))
            raise NotImplementedError("TODO: tokenize từng mẫu")

    def __getitem__(self, i):
        return self.encoded[i]

    def __len__(self):
        return len(self.data)


# ---------------------------------------------------------------
# 3) Collate: pad batch + tạo target (shift 1) + mask padding
# ---------------------------------------------------------------
def custom_collate(batch, pad_id=50256, ignore_index=-100, device="cpu"):
    max_len = max(len(x) + 1 for x in batch)
    inputs, targets = [], []
    for item in batch:
        # TODO:
        #   new = item + [pad_id]
        #   padded = new + [pad_id] * (max_len - len(new))
        #   inp = torch.tensor(padded[:-1])
        #   tgt = torch.tensor(padded[1:])
        #   - thay token pad trong tgt (trừ pad đầu tiên) bằng ignore_index
        #     để loss bỏ qua phần padding
        #   inputs.append(inp); targets.append(tgt)
        raise NotImplementedError("TODO: pad + tạo target + mask")
    return torch.stack(inputs).to(device), torch.stack(targets).to(device)


# ---------------------------------------------------------------
# 4) Fine-tune loop (tái dùng calc_loss_batch của Tuần 5, dùng ignore_index)
# ---------------------------------------------------------------
def finetune(model, train_loader, val_loader, optimizer, device, num_epochs=2):
    model.to(device)
    for epoch in range(num_epochs):
        model.train()
        for xb, yb in train_loader:
            # TODO: dùng F.cross_entropy(..., ignore_index=-100)
            #   optimizer.zero_grad(); loss.backward(); optimizer.step()
            raise NotImplementedError("TODO: bước fine-tune")
        print(f"epoch {epoch+1} xong")


if __name__ == "__main__":
    print("Skeleton Tuần 6. Tải Alpaca/Dolly, điền TODO, rồi chat thử với model.")
