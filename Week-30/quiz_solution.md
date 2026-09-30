# Tuần 30, Đáp án & Giải thích: Thiết kế và chọn thí nghiệm

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Có được dừng ngay khi thấy một kết quả đẹp rồi bỏ run thất bại không?

**Trả lời mẫu:** Không. Phải theo stopping rule và giữ history; chọn/dừng hậu nghiệm có thể làm claim thống kê không còn áp dụng.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 6, 9, 16. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Thiết kế và chọn thí nghiệm”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Làm R06: giữ model/corpus, thay một cấu hình; runner dừng trước khi vượt budget. Lưu run fail, tiêu chí chọn và tổng chi phí. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
