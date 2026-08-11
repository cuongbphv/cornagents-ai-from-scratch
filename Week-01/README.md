# Tuần 1 — Toán nền tảng + PyTorch (chỉ học những gì cần)

> Phase 1 — Deep Internals. Mục tiêu của tuần là ôn lại toán cốt lõi và thành thạo PyTorch tensor/autograd, đủ để Tuần 3 (attention) và Tuần 5 (pretraining) "click" thay vì gây nản.

## Mục tiêu

- Ôn **linear algebra**: phép nhân ma trận, dot product, shape/broadcasting.
- Ôn **calculus**: gradient, chain rule (nền tảng của backprop).
- Ôn **probability**: softmax, cross-entropy.
- Thành thạo **PyTorch**: tensor, autograd, `nn.Module`, optimizer, training loop.
- Xác nhận GPU chạy được trên RTX 3070 Ti (`torch.cuda.is_available()`) hoặc Mac MPS.

## Nguồn học

- Lý thuyết tự chứa của tuần: [`02_theory_notes.md`](02_theory_notes.md) (kèm link nguồn đã xác minh 2026-08-11).
- PyTorch official tutorials — **"Learn the Basics"** và **"Deep Learning with PyTorch: A 60 Minute Blitz"** (docs.pytorch.org/tutorials — địa chỉ pytorch.org/tutorials redirect về đây, kiểm tra 2026-08-11).
- PyTorch docs — `torch.Tensor`, autograd (`torch.autograd`), `nn.Module`, optimizer.

## Thứ tự học trong tuần (mở file theo số)

1. [`01_check_gpu.py`](01_check_gpu.py) — xác nhận môi trường trước tiên (5 phút).
2. [`02_theory_notes.md`](02_theory_notes.md) — đọc lý thuyết, chạy lại từng snippet, song song với PyTorch tutorial.
3. [`03_math_cheat_sheet.md`](03_math_cheat_sheet.md) — TỰ viết lại cheat sheet bằng lời mình (deliverable).
4. [`04_math_practice.py`](04_math_practice.py) — luyện tương tác: đoán trước, chạy sau.
5. [`05_train_mlp.py`](05_train_mlp.py) — TỰ code MLP + training loop (deliverable chính).
6. [`06_solution_train_mlp.py`](06_solution_train_mlp.py) — CHỈ mở sau khi tự code xong, để đối chiếu.
7. [`quiz.md`](quiz.md) — làm quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Hai file này do `scripts/generate_quiz.py` sinh ra nên giữ nguyên tên, không đánh số.)*

## Nhiệm vụ (Task)

Tự tay code lại một **MLP nhỏ** + training loop trong PyTorch từ đầu, và xác nhận GPU hoạt động.

## Deliverables

1. Một notebook/script train được MLP trên toy dataset → `05_train_mlp.py` (hoặc `.ipynb`).
2. Một **math cheat sheet 1 trang** tự viết (có thể nhờ Claude hỗ trợ) → `03_math_cheat_sheet.md`.

## Thời lượng

~10–12 giờ.

## Phần cứng

RTX 3070 Ti (hoặc Mac MPS) — khối lượng tính toán rất nhẹ.

---

## Checklist tiến độ

- [ ] Ôn linear algebra (matrix multiply, dot product) + calculus (chain rule) — tự viết lại bằng ví dụ nhỏ
- [ ] Làm PyTorch tutorial "Learn the Basics" (tensor → autograd → training loop)
- [ ] Đọc docs autograd + `nn.Module` của PyTorch
- [x] Chạy `01_check_gpu.py` → xác nhận CUDA/MPS hoạt động
  - ✅ 2026-08-11 — CUDA khả dụng: RTX 3070 Ti, VRAM 8.0 GB, torch 2.5.1+cu121, Windows. Log: [`../journal/evidence/W01/check_gpu_2026-08-11.log`](../journal/evidence/W01/check_gpu_2026-08-11.log)
  - Ghi chú cũ trong file này: "MPS khả dụng — macOS arm64, torch 2.12.1". `[Chưa xác minh]` — không có log kèm theo trong repo.
- [ ] Đọc `02_theory_notes.md` — chạy lại được mọi snippet trong đó
- [ ] Tự code lại `05_train_mlp.py` (KHÔNG copy — tự viết để hiểu)
- [ ] MLP train được, loss giảm, accuracy hợp lý trên toy dataset
- [ ] Hoàn thành `03_math_cheat_sheet.md` bằng lời của mình
- [ ] Tự kiểm tra: giải thích được cho Claude (bằng lời mình) softmax + cross-entropy + chain rule

## Cách dùng Claude làm bạn học (Tuần 1)

- **Giải thích toán:** dán một công thức (vd. cross-entropy) và nhờ Claude dẫn dắt từng bước, rồi nhờ Claude ra 3 câu hỏi kiểm tra.
- **Review code:** sau khi TỰ code MLP, dán code nhờ Claude so sánh với cách chuẩn, bắt bug. Đừng để Claude viết bản nháp đầu tiên — tự code trước, review sau.
- **Tạo flashcard/bài tập** tự kiểm tra theo từng chủ đề của tuần.

> Tiêu chí tự đánh giá: **nếu chưa giải thích được một thành phần cho Claude bằng lời của mình, nghĩa là chưa học xong** — đó là tín hiệu để đi chậm lại.

## 🚀 Bổ sung nâng cao

**Tuần này cố ý KHÔNG có mục nâng cao nào.** Bảng neo trong [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) để trống cho Tuần 1–2: mọi chủ đề nâng cao (RoPE, GQA, KV cache…) đều cần bạn nắm attention trước, nên đọc sớm chỉ gây tải vô ích.

Việc của tuần này là nền: tensor, autograd, softmax/cross-entropy, chain rule. Phần nâng cao **bắt đầu từ Tuần 3**.

## File trong folder này

Số ở đầu tên file = thứ tự học (xem mục "Thứ tự học trong tuần" ở trên).

| # | File | Mô tả |
|---|------|-------|
| — | `README.md` | File này — mục tiêu, nguồn, checklist |
| 1 | `01_check_gpu.py` | Kiểm tra CUDA/MPS, in thông tin device + VRAM |
| 2 | `02_theory_notes.md` | Lý thuyết tự chứa của tuần: linear algebra, calculus, softmax/CE, PyTorch core |
| 3 | `03_math_cheat_sheet.md` | Cheat sheet toán cho LLM (tự bổ sung bằng lời mình) |
| 4 | `04_math_practice.py` | Luyện tập tương tác theo cheat sheet (đoán trước → chạy → so đáp án) |
| 5 | `05_train_mlp.py` | Skeleton để TỰ code MLP + training loop trên toy dataset |
| 6 | `06_solution_train_mlp.py` | Lời giải tham khảo — CHỈ mở sau khi tự code xong |
| 7 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
