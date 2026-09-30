# Tuần 19, Đáp án & Giải thích: Hợp đồng công cụ và agent có giới hạn

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

JSON đúng schema nhưng action ngoài scope có được chạy không?

**Trả lời mẫu:** Không. Schema là một kiểm tra; quyền, semantics và trạng thái phải được executor kiểm riêng.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 3, 4, 8, 10. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Hợp đồng công cụ và agent có giới hạn”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Dùng R01/R10 reference offline; tạo schema cho read_fixture, từ chối tool không có trong contract. Viết starter executor chỉ hỗ trợ công cụ giả lập. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
