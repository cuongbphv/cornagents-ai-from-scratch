# Tuần 11: QLoRA fine-tuning thực tế trên 3070 Ti với Unsloth

> Phase 2: Applied. Chuyển từ "from-scratch" sang tooling production: fine-tune một model 7B-8B thật bằng QLoRA 4-bit.

## Mục tiêu

- Fine-tune model 7B-8B thật với **4-bit QLoRA** trên 3070 Ti (8GB).
- Hiểu LoRA hyperparameters (r, α, target modules) trong thực tế.

## Nguồn học

- **Unsloth docs** (unsloth.ai/docs): Fine-tuning Guide, LoRA Hyperparameters Guide, Requirements table.
- HF **PEFT** + **TRL** (`SFTTrainer`).
- NVIDIA, "How to Fine-Tune LLMs on RTX GPUs With Unsloth."
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md) (kèm nguồn đã xác minh 2026-08-11).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md): QLoRA/NF4, hyperparameters, quy trình 8GB, kỷ luật eval.
2. [`02_qlora_finetune.py`](02_qlora_finetune.py): smoke test rồi full run (deliverable).
3. [`03_eval_notes.md`](03_eval_notes.md): eval base vs fine-tuned trên held-out (deliverable).
4. [`quiz.md`](quiz.md): quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Giữ nguyên tên vì do `scripts/generate_quiz.py` sinh ra.)*

## Nhiệm vụ (Task)

QLoRA fine-tune **Llama 3.1 8B** hoặc **Qwen** trên dataset instruction nhỏ (bắt đầu 500-1,000 mẫu). Export merged model + GGUF.

## Cấu hình cho 8GB

```
load_in_4bit = True
batch_size   = 1-2
seq_len      ≤ 1024
gradient_checkpointing = True
r = 16, lora_alpha = 16
target = tất cả attention + MLP projections
```

VRAM phải đo với model, batch, sequence length, dtype, optimizer và runtime thực tế. Không dùng bảng weights để cam kết toàn workload vừa máy.

## Deliverable

Adapter 7B/8B đã fine-tune + **eval so base vs fine-tuned** trên held-out examples.

## Thời lượng

~10-12 giờ. Một run 1,000-5,000 mẫu mất từ vài giờ đến qua đêm trên 8GB.

## Phần cứng

- **3070 Ti** là máy chính; **Colab free T4 (15GB)** là phương án dễ hơn.
- Ngưỡng chuyển máy: nếu fine-tune > 24h hoặc OOM ở batch 1 thì chuyển sang thuê 4090/A100.

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` và giải thích được vì sao 8GB fine-tune được 8B
- [ ] Cài Unsloth và dependencies (kiểm tra CUDA khớp)
- [ ] Chọn base model (Llama 3.1 8B / Qwen2.5 7B) ở 4-bit
- [ ] Chuẩn bị dataset 500-1,000 mẫu (gợi ý: dùng domain Finance Banking của bạn)
- [ ] Cấu hình LoRA (r=16, α=16, target all proj) và SFTTrainer
- [ ] Smoke test vài step để xác nhận không OOM và loss giảm
- [ ] Chạy full run và lưu adapter
- [ ] Merge adapter và export GGUF (để chạy Ollama/LM Studio ở Tuần 12)
- [ ] Eval base vs fine-tuned trên held-out rồi ghi `03_eval_notes.md`

## Bổ sung nâng cao (quantization internals + cách eval)

Tuần này dùng QLoRA/NF4 ở mức "bật cờ". Hiểu sâu hơn trong [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **B4**:

NF4 của QLoRA là 4-bit "normal float"; nó chỉ quantize base và train adapter LoRA ở bf16. Mục này cũng so GPTQ (per-layer, Hessian) với AWQ (bảo vệ kênh salient theo activation). GGUF là *định dạng file* của llama.cpp (Q4_K_M, Q5_K_M, Q8_0…), thứ Ollama/LM Studio load, không phải thuật toán.

> Quy tắc: 8-bit gần như không mất chất lượng; 4-bit là điểm ngọt local; perplexity tăng dần khi bit giảm.

Deliverable tuần này là "eval base vs fine-tuned", nên đọc thêm mục **H**:

- Đừng tin một chỉ số duy nhất: loss/perplexity giảm không tự động nghĩa là model hữu ích hơn trên việc bạn cần.
- Nếu so hai model **khác tokenizer/backend**, dùng **bits-per-byte** thay perplexity thô.
- Giữ một held-out set cố định để mọi lần fine-tune sau đều so được với lần này.

## Dữ liệu cho tuần này

Xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md): mục **3** (dataset tiếng Anh license sạch), mục **2** (tiếng Việt), mục **7** (chọn base model), mục **8** (chiến lược song ngữ).

Gợi ý cho lần fine-tune đầu: trộn `Sujet-Finance-Instruct-177k` (Apache 2.0) + `duyet/vietnamese-legal-instruct` (CC BY 4.0), thêm `UTS2017_Bank` (Apache 2.0) nếu làm task phân loại. Base an toàn về pháp lý: **Qwen2.5-7B-Instruct** (Apache 2.0).

> **Fine-tune ở tuần này là để dạy HÀNH VI/ĐỊNH DẠNG, không phải nhồi kiến thức quy định.** Kiến thức quy định đi qua RAG (Tuần 13-14) + KG (Tuần 17): đọc mục **0** của tài liệu dataset để hiểu vì sao. Và chỉ dùng dataset license mở đã xác minh trong tài liệu dataset; tự cắt held-out split để eval trước khi train.

## File trong folder

Số ở đầu tên file = thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| · | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: QLoRA/NF4, hyperparameters, kỷ luật eval |
| 2 | `02_qlora_finetune.py` | Starter script Unsloth QLoRA (điền dataset + tinh chỉnh) |
| 3 | `03_eval_notes.md` | Template eval base vs fine-tuned |
| 4 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
