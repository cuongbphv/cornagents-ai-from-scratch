# Tuần 17, Đáp án & Giải thích: Document AI và số/đơn vị tiếng Việt

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Bảng chỉ ghi 12, không còn header đơn vị: có được đoán là triệu đồng không?

**Trả lời mẫu:** Không. Giữ raw span, báo thiếu đơn vị/AMBIGUOUS và chuyển người hoặc xin nguồn bổ sung.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 8, 12, 13. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Document AI và số/đơn vị tiếng Việt”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Tự viết parser số nguyên có đơn vị tường minh, thử thiếu đơn vị và dấu OCR. Xuất raw span, normalized value và lý do từ chối; so với fixture. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
