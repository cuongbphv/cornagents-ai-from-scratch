# Tuần 12: Training dynamics và thí nghiệm tách ảnh hưởng

> CornAgents.AI · Lịch học chính · Phase 1. Nguồn: [Thuật toán và học có kiểm chứng](../../../modules/controlled-learning.md) · [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md) · [Giả thuyết và phương pháp nghiên cứu](../../../modules/research-methods.md), mục 6, 8, 16; đọc bản local ngày 30/09/2026.

**Trạng thái:** tài liệu, quiz và starter đã có; bài làm của người học và đánh giá live-model chưa được thực hiện ở đây. Starter có phần cần tự triển khai. Reference offline (nếu dùng) chỉ kiểm các fixture công khai, không phải chứng nhận runtime production.

## Mục tiêu

- Giữ baseline và các biến không nghiên cứu cố định; ablation bỏ hoặc đổi một thành phần để kiểm vai trò của nó. Lưu cả run lỗi và run không cải thiện.
- Giải thích một phản ví dụ mới mà không nhờ AI làm hộ.
- Ghi rõ bằng chứng phép kiểm cung cấp và phần còn chưa biết.

## Nguồn học

- [Thuật toán và học có kiểm chứng](../../../modules/controlled-learning.md) · [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md) · [Giả thuyết và phương pháp nghiên cứu](../../../modules/research-methods.md), mục 6, 8, 16. Nội dung bên dưới là biên tập từ tài liệu chương trình; bài tập được bổ sung cho repo, chưa phải kết quả nghiên cứu.
- [Week-08/04_loss_analysis.md](../../../Week-08/04_loss_analysis.md)
- [Week-08/README.md](../../../Week-08/README.md)

## Thứ tự học trong tuần (mở file theo số)

1. [01_theory_notes.md](01_theory_notes.md): cơ chế, phản ví dụ và phần nguồn liên quan.
2. [02_exercise.py](02_exercise.py): starter; viết protocol trong [02_experiment_protocol.md](02_experiment_protocol.md) trước khi chạy.
3. [03_report.md](03_report.md): điền từ output thật; không điền số liệu mẫu như kết quả.
4. [quiz.md](quiz.md), rồi [quiz_solution.md](quiz_solution.md).

## Nhiệm vụ (Task)

Train tiny model theo budget tự đặt trước, so một thay đổi như lịch LR. Lưu code/data/config/seed, loss, thời gian và lỗi của toàn bộ lượt chạy.

**Gây lỗi:** Đổi model, corpus và token budget cùng lúc rồi gán gain cho optimizer là kết luận không được thiết kế thí nghiệm hỗ trợ.

## Deliverable

Code hoặc artifact thực hành; protocol trước thí nghiệm; output và báo cáo có nguồn/cấu hình. Bài kiểm mới cần mô tả expected outcome và lý do. Chưa chạy thì giữ ô kết quả trống, không ghi pass.

## Tiêu chí qua môn

- **G1 — AI-off:** trả lời và bảo vệ: Kết quả âm có phải lý do xóa run khỏi báo cáo không?
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

[Toàn bộ đường học](../../../ENTRYPOINTS.md) · [Tri thức tích hợp](../../../modules/README.md)


## File trong folder

| File | Vai trò |
|---|---|
| README.md | Mục tiêu, nguồn, trình tự học và tiêu chí |
| 01_theory_notes.md | Ghi chú và nội dung nguồn được chọn |
| 02_exercise.py | Starter của người học, chưa có lời giải |
| 02_experiment_protocol.md | Mẫu đăng ký phép kiểm trước khi chạy |
| 03_report.md | Mẫu báo cáo, giữ kết quả chưa chạy trống |
| quiz.md / quiz_solution.md | Sinh từ scripts/quiz_bank.json |
