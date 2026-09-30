# Tuần 28, Đáp án & Giải thích: Học từ lỗi bằng bài học có điều kiện

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Lesson “luôn dùng parser” sai ở trường hợp nào trong lab?

**Trả lời mẫu:** Khi input ngoài grammar, OCR mơ hồ hoặc thiếu đơn vị/header. Parser phải báo ambiguous thay vì đoán; bài học cần nêu chống chỉ định.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 2, 5, 6, 9, 11. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Học từ lỗi bằng bài học có điều kiện”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Làm R04: so parser rule/bộ nhớ lesson trên trường có grammar; kiểm đổi đơn vị và thiếu header. Thiết kế nhánh Reflexion live riêng; reference offline không gọi LLM. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
