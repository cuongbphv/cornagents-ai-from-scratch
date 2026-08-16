# Tuần 9 — Đáp án & Giải thích: Fine-tuning Mac/MLX + local inference stack

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Vì sao MacBook 24GB có thể fine-tune model lớn hơn RTX 3070 Ti 8GB?

- **A.** CPU Mac nhanh hơn GPU
- **B.** Unified memory 24GB dùng chung cho cả 'GPU', cho phép chứa model 13-14B (đổi lại chậm hơn ~2-4×) ✅
- **C.** MLX nén model xuống 1-bit
- **D.** Mac có nhiều GPU hơn

**Đáp án: B**

**Giải thích:** Unified memory là lợi thế của Apple Silicon: dung lượng lớn hơn VRAM rời 8GB, dù thông lượng thấp hơn NVIDIA.

## Câu 2 (Tự luận)

Mô tả luồng fine-tune → phục vụ bằng MLX trên Mac.

**Trả lời mẫu:** 1) mlx_lm.lora --model ... --train --data ... --iters 500 để train adapter LoRA. 2) mlx_lm.fuse --model ... --adapter-path ... để gộp adapter vào base. 3) Phục vụ qua Ollama (tạo Modelfile) hoặc LM Studio (load GGUF/MLX) để chat. Với 24GB có thể LoRA/QLoRA tới ~13-14B.

**Giải thích:** Mac dùng định dạng MLX (mlx-community/...); Ollama/LM Studio là lớp serving.

## Câu 3 (Trắc nghiệm)

Ollama và LM Studio đóng vai trò gì?

- **A.** Train model from scratch
- **B.** Lớp inference/serving local — tải, quản lý và chat với model (GGUF/MLX) qua API/GUI ✅
- **C.** Vector database cho RAG
- **D.** Tokenizer

**Đáp án: B**

**Giải thích:** Chúng giúp chạy model local dễ dàng; Ollama có API kiểu OpenAI tiện cắm vào RAG/agents.

## Câu 4 (Tự luận)

Tóm tắt phân vai 3070 Ti vs Mac 24GB vs Cloud.

**Trả lời mẫu:** 3070 Ti (8GB): code from-scratch, train nhỏ/validate loop, QLoRA 7B-8B nhanh. Mac 24GB: chứa & fine-tune model 13-14B, chạy yên tĩnh local, inference quantized. Cloud (RunPod/Lambda): lần pretrain GPT-2 một lần (~$15-35), full fine-tune, iterate nhanh khi local quá chậm/OOM.

**Giải thích:** Đây là nội dung deliverable 03_hardware_decision.md.

## Câu 5 (Trắc nghiệm)

Theo Ilharco et al. 2022 (task arithmetic, mục 7 theory notes), 'task vector' là gì và cộng/trừ nó dùng để làm gì?

- **A.** Vector embedding của mô tả task, dùng để retrieve adapter phù hợp
- **B.** τ = W_finetuned − W_base — 'hướng' fine-tune đã đẩy model tới trong không gian trọng số; CỘNG nhiều τ để ghép nhiều kỹ năng vào một model, PHỦ ĐỊNH (−τ) để giảm một hành vi mà ít ảnh hưởng task khác ✅
- **C.** Gradient trung bình của batch cuối cùng khi train
- **D.** Một hàng của ma trận LoRA A

**Đáp án: B**

**Giải thích:** Mục 7 của 01_theory_notes.md (arXiv 2212.04089): LoRA adapter merge về được dạng ΔW nên cũng quy về khung task vector. Caveat của repo: merging là kỹ thuật THỰC NGHIỆM — merge xong bắt buộc chạy lại bộ 10 prompt song ngữ + eval nghiệp vụ, chỉ giữ bản merge khi số đo không tụt.

## Câu 6 (Tự luận)

Mô tả quy trình kiểm tra catastrophic forgetting song ngữ bắt buộc của repo (mục 5 theory notes) và làm gì khi phát hiện suy giảm.

**Trả lời mẫu:** 1) TRƯỚC khi fine-tune: chốt bộ 10 prompt cố định (5 tiếng Việt + 5 tiếng Anh, có cả nghiệp vụ lẫn thường thức), sinh và lưu output của base. 2) SAU fine-tune: chạy đúng 10 prompt đó ở temperature 0, so từng cặp output. 3) Nếu suy giảm rõ ở tiếng Anh: giảm tỷ lệ data một chiều, trộn thêm data tiếng Anh rồi train lại. Bộ 10 prompt giữ cố định vĩnh viễn — là 'bài kiểm tra sức khỏe song ngữ' cho mọi model sau này của dự án (kể cả mọi bản merge ở mục 7).

**Giải thích:** Mục 5 của 01_theory_notes.md. Chỗ dựa từ paper: Biderman et al. 2024 (arXiv 2405.09673) đo được full fine-tuning quên kiến thức ngoài domain đích nhiều hơn hẳn LoRA — mức quên PHỤ THUỘC cách fine-tune, nên chỉ có đo mới biết mình ở đâu trên trade-off.
