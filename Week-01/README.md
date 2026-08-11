# Tuần 1 — Toán nền tảng + PyTorch (chỉ học những gì cần)

> Phase 1 — Deep Internals. Mục tiêu của tuần là ôn lại toán cốt lõi và thành thạo PyTorch tensor/autograd, đủ để Tuần 3 (attention) và Tuần 5 (pretraining) "click" thay vì gây nản.

## Mục tiêu

- Ôn **linear algebra**: phép nhân ma trận, dot product, shape/broadcasting.
- Ôn **calculus**: gradient, chain rule (nền tảng của backprop).
- Ôn **probability**: softmax, cross-entropy.
- Thành thạo **PyTorch**: tensor, autograd, `nn.Module`, optimizer, training loop.
- Xác nhận GPU chạy được trên RTX 3070 Ti (`torch.cuda.is_available()`) hoặc Mac MPS.

## Nguồn học

- 3Blue1Brown — series **"Neural Networks"** và **"Linear Algebra"** (3blue1brown.com) — trực quan hóa.
- Sebastian Raschka — **"PyTorch in One Hour: From Tensors to Training Neural Networks on Multiple GPUs"** (sebastianraschka.com/teaching/pytorch-1h/).
- Raschka — sách *Build a LLM (From Scratch)*, **Appendix A** (PyTorch).

## Nhiệm vụ (Task)

Tự tay code lại một **MLP nhỏ** + training loop trong PyTorch từ đầu, và xác nhận GPU hoạt động.

## Deliverables

1. Một notebook/script train được MLP trên toy dataset → `train_mlp.py` (hoặc `.ipynb`).
2. Một **math cheat sheet 1 trang** tự viết (có thể nhờ Claude hỗ trợ) → `math_cheat_sheet.md`.

## Thời lượng

~10–12 giờ.

## Phần cứng

RTX 3070 Ti (hoặc Mac MPS) — khối lượng tính toán rất nhẹ.

---

## Checklist tiến độ

- [ ] Xem 3B1B: Neural Networks (ch.1–4) + Linear Algebra (matrix, dot product)
- [ ] Đọc/làm theo Raschka "PyTorch in One Hour"
- [ ] Đọc Appendix A sách Raschka
- [x] Chạy `check_gpu.py` → xác nhận CUDA/MPS hoạt động (✅ MPS khả dụng — macOS arm64, torch 2.12.1)
- [ ] Tự code lại `train_mlp.py` (KHÔNG copy — tự viết để hiểu)
- [ ] MLP train được, loss giảm, accuracy hợp lý trên toy dataset
- [ ] Hoàn thành `math_cheat_sheet.md` bằng lời của mình
- [ ] Tự kiểm tra: giải thích được cho Claude (bằng lời mình) softmax + cross-entropy + chain rule

## Cách dùng Claude làm bạn học (Tuần 1)

- **Giải thích toán:** dán một công thức (vd. cross-entropy) và nhờ Claude dẫn dắt từng bước, rồi nhờ Claude ra 3 câu hỏi kiểm tra.
- **Review code:** sau khi TỰ code MLP, dán code nhờ Claude so sánh với cách chuẩn, bắt bug. Đừng để Claude viết bản nháp đầu tiên — tự code trước, review sau.
- **Tạo flashcard/bài tập** ôn tập theo phong cách "Test Yourself" của Raschka.

> Tiêu chí tự đánh giá: **nếu chưa giải thích được một thành phần cho Claude bằng lời của mình, nghĩa là chưa học xong** — đó là tín hiệu để đi chậm lại.

## File trong folder này

| File | Mô tả |
|------|-------|
| `README.md` | File này — mục tiêu, nguồn, checklist |
| `check_gpu.py` | Kiểm tra CUDA/MPS, in thông tin device + VRAM |
| `train_mlp.py` | Skeleton để TỰ code MLP + training loop trên toy dataset |
| `math_cheat_sheet.md` | Cheat sheet toán cho LLM (tự bổ sung bằng lời mình) |
