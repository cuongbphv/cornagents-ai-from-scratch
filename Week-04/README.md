# Tuần 4: PyTorch core: từ NumPy sang tensor, autograd, training loop

> Phase 1: Deep Internals, tuần mở đầu. Ba tuần Phase 0 bạn làm mọi thứ bằng NumPy và tính gradient bằng tay. Tuần này đổi công cụ, không đổi toán: cùng phép nhân ma trận, cùng chain rule, cùng negative log-likelihood, nhưng PyTorch giữ đồ thị tính toán và tính gradient thay bạn. Mục tiêu là thành thạo tensor, autograd, `nn.Module`, optimizer, đủ để Tuần 6 (attention) và Tuần 8 (pretraining) "click" thay vì gây nản.

## Bạn đến đây với gì, và tuần này đổi thành gì

| Bạn đã làm ở Phase 0 | Tuần này thay bằng | Đọc ở |
|---|---|---|
| `np.array`, `@`, quy tắc chiều (Tuần 1 mục 2) | `torch.tensor`, `@`, thêm `device` và `dtype` | `02_theory_notes.md` mục 1, 4.1 |
| Ma trận là ánh xạ tuyến tính (Tuần 1 mục 1) | `nn.Linear(in, out)` lưu W chiều (out, in), tính `x @ Wᵀ + b` | mục 1.3 |
| Gradient tính tay, kiểm bằng sai phân (Tuần 2 mục A1, A2) | `loss.backward()` điền `.grad`; sai phân vẫn là cách kiểm | mục 2.3 |
| Chain rule (Tuần 2 mục A3) | Autograd áp chain rule trên đồ thị, bạn chỉ viết forward | mục 2.2 |
| MLE, NLL là cross-entropy (Tuần 2 mục B6) | `nn.CrossEntropyLoss` gộp softmax, log, NLL; đưa thẳng logits | mục 3.2 |
| `gradient_descent_1d` tự viết (Tuần 2) | `optimizer.step()` và `zero_grad()` | mục 4.3 |
| Logistic regression NumPy, gradient viết tay (Tuần 3) | Viết lại bằng `nn.Linear` + autograd, rồi chồng thêm lớp thành MLP | `05_train_mlp.py` phần 2 và 3 |
| Train, validation, test (Tuần 3 mục 5) | Giữ nguyên: tách held-out trước khi train | `05_train_mlp.py` phần 1 |

Nếu bạn vừa học xong Tuần 1 đến 3, mục toán trong `02_theory_notes.md` (mục 1 đến 3) chỉ là ôn có gắn API; đọc nhanh, dành thời gian cho mục 4 và cho code.

## Mục tiêu

- Chuyển mọi phép toán NumPy của Phase 0 sang tensor PyTorch, thêm hai khái niệm mới: `device` và `dtype`.
- Hiểu autograd làm gì thay cho gradient viết tay ở Tuần 2 và 3, và vì sao gradient bị cộng dồn.
- Nhận ra softmax là pmf (Tuần 2 mục B2) và cross-entropy là NLL (Tuần 2 mục B6), rồi dùng đúng `nn.CrossEntropyLoss` với logits.
- Thành thạo `nn.Module`, optimizer, và khung training loop năm bước.
- Viết lại logistic regression của Tuần 3 bằng PyTorch, rồi chồng thêm một lớp ẩn thành MLP và thấy accuracy tăng trên dữ liệu không tách tuyến tính được.
- Xác nhận GPU chạy được trên RTX 3070 Ti (`torch.cuda.is_available()`) hoặc Mac MPS.

## Nguồn học

- Lý thuyết tự chứa của tuần: [`02_theory_notes.md`](02_theory_notes.md) (kèm link nguồn đã xác minh 2026-08-11). Mục 1 đến 3 dẫn ngược về đúng mục của Tuần 1 và 2.
- Ghi chú lý thuyết Tuần 1 đến 3 ([`../Week-01/01_theory_notes.md`](../Week-01/01_theory_notes.md), [`../Week-02/01_theory_notes.md`](../Week-02/01_theory_notes.md), [`../Week-03/01_theory_notes.md`](../Week-03/01_theory_notes.md)) để mở lại khi một công thức chưa rõ; MML mục 5.6 (trang 159) nếu muốn đọc backpropagation và autodiff theo sách.
- PyTorch official tutorials, **"Learn the Basics"** và **"Deep Learning with PyTorch: A 60 Minute Blitz"** (docs.pytorch.org/tutorials, địa chỉ pytorch.org/tutorials redirect về đây, kiểm tra 2026-08-11).
- PyTorch docs, `torch.Tensor`, autograd (`torch.autograd`), `nn.Module`, optimizer.

## Thứ tự học trong tuần (mở file theo số)

0. [`00_math_bridge.md`](00_math_bridge.md) + [`00_math_bridge_practice.py`](00_math_bridge_practice.py): bài ôn nhanh ký hiệu, log, exp và nhân ma trận tay (3-6 giờ). Bỏ qua nếu bạn vừa làm xong lab Tuần 1-2; chỉ dành cho người quay lại sau thời gian nghỉ dài.
1. [`01_check_gpu.py`](01_check_gpu.py): xác nhận môi trường trước tiên (5 phút).
2. [`02_theory_notes.md`](02_theory_notes.md): đọc lý thuyết, chạy lại từng snippet, song song với PyTorch tutorial.
3. [`03_math_cheat_sheet.md`](03_math_cheat_sheet.md): TỰ viết cheat sheet nối công thức Phase 0 với API PyTorch tương ứng (deliverable).
4. [`04_math_practice.py`](04_math_practice.py): luyện tương tác: đoán trước, chạy sau.
5. [`05_train_mlp.py`](05_train_mlp.py): TỰ code theo ba phần: tách held-out, logistic regression bằng PyTorch (viết lại Tuần 3), rồi MLP (deliverable chính).
6. [`06_solution_train_mlp.py`](06_solution_train_mlp.py): CHỈ mở sau khi tự code xong, để đối chiếu.
7. [`quiz.md`](quiz.md): làm quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Hai file này do `scripts/generate_quiz.py` sinh ra nên giữ nguyên tên, không đánh số.)*

## Nhiệm vụ (Task)

1. Viết lại logistic regression của Tuần 3 bằng `nn.Linear` và autograd; so gradient autograd với hàm `grad` viết tay của bạn ở Tuần 3 trên cùng một batch (phải khớp).
2. Chồng thêm một lớp ẩn thành **MLP nhỏ**, train bằng cùng training loop, so accuracy trên held-out với logistic regression.
3. Xác nhận GPU hoạt động.

## Deliverables

1. `05_train_mlp.py` chạy được: logistic regression rồi MLP, in accuracy held-out của cả hai và một câu giải thích vì sao khác nhau.
2. Một **cheat sheet 1 trang** tự viết → `03_math_cheat_sheet.md`: mỗi công thức ghi rõ học ở tuần nào và API PyTorch tương ứng.

## Thời lượng

~10-12 giờ. Thêm 3-6 giờ nếu làm bài ôn `00_math_bridge.md`.

## Phần cứng

RTX 3070 Ti (hoặc Mac MPS): khối lượng tính toán rất nhẹ.

---

## Checklist tiến độ

- [ ] (Tùy chọn) Làm `00_math_bridge.md` + `00_math_bridge_practice.py` nếu ký hiệu toán còn lạ
- [ ] Đọc bảng "Bạn đến đây với gì" ở trên; mở lại mục Tuần 1-3 nào còn mơ hồ trước khi đi tiếp
- [ ] Làm PyTorch tutorial "Learn the Basics" (tensor → autograd → training loop)
- [ ] Đọc docs autograd + `nn.Module` của PyTorch
- [x] Chạy `01_check_gpu.py` → xác nhận CUDA/MPS hoạt động
  - ✅ 2026-08-11, CUDA khả dụng: RTX 3070 Ti, VRAM 8.0 GB, torch 2.5.1+cu121, Windows. Log: [`../journal/evidence/W04/check_gpu_2026-08-11.log`](../journal/evidence/W04/check_gpu_2026-08-11.log)
  - Ghi chú cũ trong file này: "MPS khả dụng, macOS arm64, torch 2.12.1". `[Chưa xác minh]`: không có log kèm theo trong repo.
- [ ] Đọc `02_theory_notes.md`: chạy lại được mọi snippet trong đó
- [ ] `05_train_mlp.py` phần 2: logistic regression bằng PyTorch; gradient autograd khớp gradient tay của Tuần 3
- [ ] `05_train_mlp.py` phần 3: MLP train được, loss giảm, accuracy held-out cao hơn logistic regression
- [ ] Viết một câu giải thích vì sao MLP thắng logistic regression trên two moons (gợi ý: lớp giả thuyết, Tuần 3 mục 2)
- [ ] Hoàn thành `03_math_cheat_sheet.md` bằng lời của mình
- [ ] Tự kiểm tra: giải thích cho Claude bằng lời mình `loss.backward()` làm gì thay cho hàm `grad` bạn viết ở Tuần 3, và vì sao phải `zero_grad()`

## Cách dùng Claude làm bạn học (Tuần 4)

- **Giải thích toán:** dán một công thức (vd. cross-entropy) và nhờ Claude dẫn dắt từng bước, rồi nhờ Claude ra 3 câu hỏi kiểm tra.
- **Review code:** sau khi TỰ code MLP, dán code nhờ Claude so sánh với cách chuẩn, bắt bug. Đừng để Claude viết bản nháp đầu tiên, tự code trước, review sau.
- **Tạo flashcard/bài tập** tự kiểm tra theo từng chủ đề của tuần.

> Tiêu chí tự đánh giá: **nếu chưa giải thích được một thành phần cho Claude bằng lời của mình, nghĩa là chưa học xong**: đó là tín hiệu để đi chậm lại.

## 🚀 Bổ sung nâng cao

**Tuần này cố ý KHÔNG có mục nâng cao nào.** Bảng neo trong [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) để trống cho Tuần 4-5: mọi chủ đề nâng cao (RoPE, GQA, KV cache…) đều cần bạn nắm attention trước, nên đọc sớm chỉ gây tải vô ích.

Việc của tuần này là đổi công cụ từ NumPy sang PyTorch trên nền toán đã có. Phần nâng cao **bắt đầu từ Tuần 6**.

## File trong folder này

Số ở đầu tên file = thứ tự học (xem mục "Thứ tự học trong tuần" ở trên).

| # | File | Mô tả |
|---|------|-------|
| · | `README.md` | File này, mục tiêu, nguồn, checklist |
| 0 | `00_math_bridge.md` | Ôn nhanh ký hiệu, log, exp, tính tay (tùy chọn, không thêm chủ đề mới) |
| 0 | `00_math_bridge_practice.py` | Luyện 11 câu bằng thư viện chuẩn, không cần PyTorch |
| 1 | `01_check_gpu.py` | Kiểm tra CUDA/MPS, in thông tin device + VRAM |
| 2 | `02_theory_notes.md` | Lý thuyết tự chứa: mục 0 map NumPy sang PyTorch; mục 1-3 ôn toán có dẫn về Tuần 1-2; mục 4 PyTorch core |
| 3 | `03_math_cheat_sheet.md` | Cheat sheet nối công thức Phase 0 với API PyTorch (tự viết bằng lời mình) |
| 4 | `04_math_practice.py` | Luyện tập tương tác theo cheat sheet (đoán trước → chạy → so đáp án) |
| 5 | `05_train_mlp.py` | Skeleton ba phần: held-out split, logistic regression PyTorch (viết lại Tuần 3), MLP |
| 6 | `06_solution_train_mlp.py` | Lời giải tham khảo, CHỈ mở sau khi tự code xong |
| 7 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
