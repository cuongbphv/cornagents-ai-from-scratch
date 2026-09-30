# Tuần 32, Đáp án & Giải thích: Bảo vệ evaluator và dữ liệu xác nhận

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Sửa candidate sau khi có report tốt rồi giữ report cũ có hợp lệ không?

**Trả lời mẫu:** Không. Nội dung ảnh hưởng kết quả đã đổi; phải đóng băng và đánh giá đúng bản mới trước khi xét sử dụng.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 4, 7, 9. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Bảo vệ evaluator và dữ liệu xác nhận”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Làm R08: tính digest, sửa một tham số và kiểm từ chối. Thiết kế process/credential tách biệt và sổ query budget; diễn tập contamination bằng trace chứa nhãn. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
