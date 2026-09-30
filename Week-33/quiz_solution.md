# Tuần 33, Đáp án & Giải thích: Học tham số offline và giữ năng lực cũ

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

DPO preference chọn văn phong tự tin có đảm bảo factuality không?

**Trả lời mẫu:** Không. Phải định nghĩa chosen tốt hơn theo tiêu chí nào; preference văn phong khác nhãn sự thật và outcome.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 2, 9, 11. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Học tham số offline và giữ năng lực cũ”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Làm R09: kiểm low-rank update nhỏ và rollback weights; lập data card/preference rubric. Nhánh live-model chỉ chạy khi có runtime, license, dataset và budget rõ. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
