# Tuần 11, Đáp án & Giải thích: Nguồn dữ liệu, dedup và chia tập

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Chia hai chunk từ cùng tài liệu sang train và test có làm chúng độc lập không?

**Trả lời mẫu:** Không mặc định. Nội dung, template và đáp án có thể trùng; cần chia theo đơn vị nguồn/task family phù hợp và kiểm gần trùng.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 5, 7, 8. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Nguồn dữ liệu, dedup và chia tập”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Tạo manifest của corpus giả lập có hai bản gần trùng, nhóm theo nguồn trước khi chia tập. Ghi quyền đọc và quyền train riêng; không dùng dữ liệu chưa xác minh license. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
