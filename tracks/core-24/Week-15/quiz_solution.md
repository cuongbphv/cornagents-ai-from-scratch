# Tuần 15, Đáp án & Giải thích: Hybrid retrieval và reranking

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Candidate retrieval tốt hơn nhưng corpus cũng lớn hơn: đã xác nhận lợi ích riêng của fusion chưa?

**Trả lời mẫu:** Chưa. Cần giữ corpus cố định hoặc thêm ablation để tách ảnh hưởng của corpus và fusion.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 6, 8. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Hybrid retrieval và reranking”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Chọn corpus công khai được phép dùng hoặc giả lập; so retrieval baseline với fusion dưới budget rõ. Kiểm recall và lỗi nguồn ở từng query. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
