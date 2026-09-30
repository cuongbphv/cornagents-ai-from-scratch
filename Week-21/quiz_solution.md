# Tuần 21, Đáp án & Giải thích: Checkpoint, idempotency và recovery

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Checkpoint mới nhất không có ack: có chắc thao tác chưa xảy ra không?

**Trả lời mẫu:** Không. Tool có thể đã ghi thành công trước crash; tra operation ID/trạng thái thật hoặc chuyển người khi không xác định được.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 4, 8, 10. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Checkpoint, idempotency và recovery”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Chạy DurableToy với ack bị mất, event trùng, payload đổi cùng key và quyền bị revoke. Viết event timeline và cách reconcile; không dùng service thật. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
