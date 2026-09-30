# Tuần 8, Đáp án & Giải thích: Causal attention và dịch nhãn

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Test nào mạnh hơn chỉ kiểm shape để phát hiện lỗi causal mask?

**Trả lời mẫu:** Giữ prefix cố định, đổi suffix tương lai và kiểm output tại prefix không đổi trong cấu hình deterministic đã khai báo.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 6, 8. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Causal attention và dịch nhãn”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Sửa attention skeleton, gây lỗi bằng cách bỏ mask; thay token tương lai và kiểm đầu ra ở vị trí trước đó. Viết một test dịch nhãn trên chuỗi ngắn. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
