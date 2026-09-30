# Tuần 35, Đáp án & Giải thích: Duyệt đúng bản cải tiến, shadow và rollback

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Tại sao rollback và revoke cần hai quyết định riêng?

**Trả lời mẫu:** Bản cũ cũng có thể dùng nguồn đã bị thu hồi. Đổi pointer không sửa quyền hay hoàn tác hành động bên ngoài; phải xử lý từng phạm vi.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 4, 9, 14. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Duyệt đúng bản cải tiến, shadow và rollback”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Làm R11: promote đúng digest, sửa artifact sau eval, scope thiếu, violation và rollback. Viết release package; thử trong mô phỏng, không deploy production. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
