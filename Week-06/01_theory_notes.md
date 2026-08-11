# Lý thuyết Tuần 6 — Fine-tuning: classification, instruction, LoRA

> Đọc trước khi điền TODO trong [`02_instruction_finetune.py`](02_instruction_finetune.py). Số liệu kiểm chứng ngày 2026-08-11; nguồn cuối file. Cần nắm GPT model (Tuần 4) + training loop (Tuần 5).

---

## 1. Fine-tuning khác pretraining ở đâu

Cùng một loop 5 bước, khác 3 thứ: **khởi điểm** (trọng số pretrained, không phải random), **dữ liệu** (nhỏ, có chủ đích), **mục tiêu** (dạy hành vi/miền cụ thể thay vì đoán token trên mọi thứ). LR nhỏ hơn pretrain nhiều (thường 1e-5–1e-4) — đi bước to là phá kiến thức nền.

📄 **Fine-tune dạy hành vi, không phải chỗ nhồi kiến thức mới** — nay có đối chứng thực nghiệm: Gekhman et al. 2024 (PDF trong repo: [`../docs/papers/2405.05904_finetuning-new-knowledge-hallucinations.pdf`](../docs/papers/2405.05904_finetuning-new-knowledge-hallucinations.pdf)) báo cáo mẫu chứa kiến thức mới được "learned significantly slower than those consistent with the model's knowledge", và khi cuối cùng cũng học được thì "linearly increase the model's tendency to hallucinate". Đây là bằng chứng trực tiếp cho nguyên tắc xương sống của repo: kiến thức quy định để ở RAG/KG (Tuần 10–14), fine-tune để dạy hành vi/định dạng.

## 2. Classification fine-tuning — thay đầu, giữ thân

- Thay head `(d → vocab)` bằng head `(d → n_classes)` — với spam: `nn.Linear(768, 2)`.
- Model đọc cả chuỗi, lấy biểu diễn ở **token cuối** (causal attention nên token cuối là chỗ duy nhất "đã nhìn" toàn chuỗi) → head → cross-entropy trên nhãn lớp.
- Có thể freeze phần lớn thân, chỉ train head + vài block cuối — nhanh và ít quên; trade-off tự đo bằng accuracy val.
- Đo **accuracy trên train/val/test riêng biệt** — quen kỷ luật này trước khi sang Tuần 8.

## 3. Instruction fine-tuning — dạy model "nghe lời"

Format mỗi mẫu theo template cố định (Alpaca-style):

```
Below is an instruction that describes a task...

### Instruction:
{instruction}

### Input:
{input}          ← có thể trống

### Response:
{output}
```

Hai điểm bản chất:
1. **Template phải nhất quán tuyệt đối** giữa train và inference — model học phân phối văn bản, lệch một dấu xuống dòng cũng là phân phối khác.
2. **Masking phần prompt**: chỉ tính loss trên token phần Response (gán nhãn `-100` cho phần trước — `F.cross_entropy` có `ignore_index=-100` mặc định). Không mask thì model tốn dung lượng học "viết lại đề bài".
   - 📄 Nuance từ paper *Instruction Modelling* (arXiv [2405.14394](https://arxiv.org/abs/2405.14394), abstract tra 2026-08-12): mask response-only là mặc định tốt, nhưng nhóm tác giả báo cáo tính loss **cả trên phần instruction** lại có lợi ở hai điều kiện — "datasets with lengthy instructions paired with brief outputs" và khi có ít mẫu train; họ quy lợi ích cho "reduced overfitting". Bài tuần này cứ mask chuẩn; nhớ ngoại lệ này khi dataset của bạn rơi đúng hai điều kiện đó.

Đây chính là bước **SFT** trong pipeline alignment mà Tuần 7 mở rộng: `Pretrain → SFT → RM → PPO/DPO`.

## 4. LoRA — fine-tune bằng 2% tham số

Ý tưởng (Hu et al., arXiv 2106.09685): thay vì cập nhật cả ma trận `W (d×d)`, học phần **delta hạng thấp**:

```
h = W·x + (α/r) · B·A·x        A: (r×d), B: (d×r), r ≪ d
```

- `B` khởi tạo **0** → lúc bắt đầu `BA = 0`, model y hệt base — train từ điểm an toàn.
- `W` đóng băng; chỉ `A, B` nhận gradient.
- Inference có thể **merge**: `W' = W + (α/r)BA` → không thêm latency.

Đếm tham số (kiểm chứng số học 2026-08-11):

| Ma trận gốc | Full FT | LoRA r=8 | LoRA r=16 |
|-------------|---------|----------|-----------|
| 768×768 (GPT-2) | 589,824 | 12,288 (**2.08%**) | 24,576 (4.17%) |
| 4096×4096 (cỡ 7B) | 16,777,216 | — | 131,072 (**0.78%**) |

**Vì sao VRAM giảm mạnh hơn cả tỷ lệ trên:** AdamW giữ 2 giá trị moment cho **mỗi tham số được train** (Tuần 5 mục 7). LoRA cắt số tham số train được ~50–100× → cắt luôn optimizer state tương ứng — thường là phần ăn VRAM lớn nhất khi full FT.

So sánh full FT vs LoRA cho deliverable: cùng dataset + cùng số step, ghi 3 cột — tham số train được, VRAM đỉnh (`torch.cuda.max_memory_allocated()`), chất lượng trên vài prompt cố định.

## 5. Tiếng Việt trong tuần này

- **Model học phân phối nó nhìn thấy:** instruction data toàn tiếng Anh thì đừng kỳ vọng model trả lời tiếng Việt tử tế. Muốn hành vi song ngữ → trộn data hai thứ tiếng (chiến lược trộn: mục 8 của [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md)).
- **Template và ngôn ngữ instruction phải nhất quán cả lúc eval:** nếu train template tiếng Anh + output tiếng Việt, thì lúc test cũng đúng cấu trúc đó; đổi kiểu giữa chừng là tự làm hỏng phép so sánh của mình.
- GPT-2 124M của bạn pretrain trên tiếng Anh — bài instruction-FT tuần này nên làm bằng tiếng Anh cho khớp base; fine-tune tiếng Việt thật để dành cho Tuần 8 với base đa ngôn ngữ.

## 6. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| Hu et al. 2021 — LoRA | https://arxiv.org/abs/2106.09685 | 4 |
| Ouyang et al. 2022 — InstructGPT | https://arxiv.org/abs/2203.02155 | 3 |
| HF PEFT docs | https://huggingface.co/docs/peft | 4 |
| Gekhman et al. 2024 — FT trên kiến thức mới & hallucination (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2405.05904 — PDF local: [`../docs/papers/`](../docs/papers/README.md) | 1 |
| Shi et al. 2024 — Instruction Modelling (chỉ link, arXiv non-exclusive, kiểm 2026-08-12) | https://arxiv.org/abs/2405.14394 | 3 |

## Sau khi đọc xong

1. Làm classification FT trước (đơn giản hơn, quen tay), rồi instruction FT trong [`02_instruction_finetune.py`](02_instruction_finetune.py).
2. Áp LoRA, điền bảng so sánh full FT vs LoRA (3 cột ở mục 4) — số tự đo, kèm ngày.
3. Chat thử với mini-model, lưu vài ví dụ vào nhật ký.
4. Làm [`quiz.md`](quiz.md); phần sơ đồ pipeline ở mục nâng cao đọc lướt — Tuần 7 học kỹ.
