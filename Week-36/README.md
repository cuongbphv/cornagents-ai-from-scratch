# Tuần 36: CornBench-VI: học qua nhiều vòng và báo cáo tái lập

> CornAgents.AI · Lịch học chính · Phase 4. Nguồn: [Đặc tả R01–R12](../labs/specifications.md) · [Thiết kế CornBench-VI Research & Learning](../benchmarks/cornbench_vi_rl/DESIGN.md) · [Giả thuyết và phương pháp nghiên cứu](../modules/research-methods.md) · [Tốt nghiệp và bảo trì chương trình](../modules/graduation-and-maintenance.md), mục 9, 12, 15, 18; đọc bản local ngày 30/09/2026.

**Trạng thái:** tài liệu, quiz và starter đã có; bài làm của người học và đánh giá live-model chưa được thực hiện ở đây. Starter có phần cần tự triển khai. Reference offline (nếu dùng) chỉ kiểm các fixture công khai, không phải chứng nhận runtime production.

## Mục tiêu

- Capstone gồm frozen baseline, một cơ chế học và nhiều cohort mới. Chấm G1/G2/G3 riêng; báo gain, retention, risk–coverage và tổng chi phí kể cả kết quả âm.
- Giải thích một phản ví dụ mới mà không nhờ AI làm hộ.
- Ghi rõ bằng chứng phép kiểm cung cấp và phần còn chưa biết.

## Nguồn học

- [Đặc tả R01–R12](../labs/specifications.md) · [Thiết kế CornBench-VI Research & Learning](../benchmarks/cornbench_vi_rl/DESIGN.md) · [Giả thuyết và phương pháp nghiên cứu](../modules/research-methods.md) · [Tốt nghiệp và bảo trì chương trình](../modules/graduation-and-maintenance.md), mục 9, 12, 15, 18. Nội dung bên dưới là biên tập từ tài liệu chương trình; bài tập được bổ sung cho repo, chưa phải kết quả nghiên cứu.
- Lab thực hành: [R12](../labs/r12-cornbench-learning/README.md).

## Thứ tự học trong tuần (mở file theo số)

1. [01_theory_notes.md](01_theory_notes.md): cơ chế, phản ví dụ và phần nguồn liên quan.
2. [02_exercise.py](02_exercise.py): starter; viết protocol trong [02_experiment_protocol.md](02_experiment_protocol.md) trước khi chạy.
3. [03_report.md](03_report.md): điền từ output thật; không điền số liệu mẫu như kết quả.
4. [quiz.md](quiz.md), rồi [quiz_solution.md](quiz_solution.md).

## Nhiệm vụ (Task)

Làm R12 và H1: đăng ký protocol, chia development/confirmation/retention theo family; chạy baseline/lesson ablation. Reference parser replay chỉ kiểm fixture; nộp report giới hạn và lệnh tái lập.

**Gây lỗi:** Fixture vài task dùng tìm lỗi kỹ thuật, không phải benchmark đã xuất bản hay bằng chứng accuracy của agent. H1 chưa được xác nhận tốt hơn.

## Deliverable

Code hoặc artifact thực hành; protocol trước thí nghiệm; output và báo cáo có nguồn/cấu hình. Bài kiểm mới cần mô tả expected outcome và lý do. Chưa chạy thì giữ ô kết quả trống, không ghi pass.

## Tiêu chí qua môn

- **G1 — AI-off:** trả lời và bảo vệ: Candidate không cải thiện nhưng thí nghiệm đúng có được hạ ngưỡng để tốt nghiệp không?
- **G2 — AI-on:** outcome được xác minh bằng fixture/nguồn/reviewer theo protocol, có cả lỗi và giới hạn.
- **G3 — thay đổi:** nếu đề nghị dùng candidate, phải có snapshot và đánh giá đúng phạm vi; chưa đủ bằng chứng thì chưa promote. Với tuần nền không tạo candidate, ghi “không áp dụng” cho cửa này.

## Thời lượng

10–12 giờ/tuần, giả định phân bổ của kế hoạch; chưa đo. Đây là giả định thiết kế ở mục 8.1 của nguồn, không cam kết mỗi bài hoàn thành trong thời lượng đó.

## Phần cứng

Bài offline dùng CPU và dữ liệu giả lập. Bài model tái sử dụng có thể cần NumPy/PyTorch hoặc runtime riêng; kiểm môi trường trước khi chạy. Không bắt mua API/GPU lớn; đo tài nguyên khi chọn workload.

## Checklist tiến độ

- [ ] Đọc ghi chú và phân biệt claim từ nguồn với đề xuất bài tập.
- [ ] Tự viết phần lõi hoặc hoàn thành starter trước khi mở bản tham chiếu.
- [ ] Chạy phép kiểm với cả trường hợp đúng, sai và thiếu bằng chứng.
- [ ] Lưu cấu hình, output thực và mọi lần thử thất bại.
- [ ] Nộp báo cáo, nêu giới hạn và trả lời bài AI-off bằng lời mình.

## Đi tiếp

[Toàn bộ đường học](../ENTRYPOINTS.md) · [Tri thức tích hợp](../modules/README.md)


## File trong folder

| File | Vai trò |
|---|---|
| README.md | Mục tiêu, nguồn, trình tự học và tiêu chí |
| 01_theory_notes.md | Ghi chú và nội dung nguồn được chọn |
| 02_exercise.py | Starter của người học, chưa có lời giải |
| 02_experiment_protocol.md | Mẫu đăng ký phép kiểm trước khi chạy |
| 03_report.md | Mẫu báo cáo, giữ kết quả chưa chạy trống |
| quiz.md / quiz_solution.md | Sinh từ scripts/quiz_bank.json |
