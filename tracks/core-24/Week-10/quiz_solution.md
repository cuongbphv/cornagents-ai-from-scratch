# Tuần 10, Đáp án & Giải thích: KV cache và báo cáo tài nguyên

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Khi cached logits khác reference, có nên tăng tolerance đến khi pass?

**Trả lời mẫu:** Không. Điều tra position, mask, cache update và số học; tolerance phải có lý do và không chọn hậu nghiệm để che lỗi.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 6, 8. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “KV cache và báo cáo tài nguyên”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Kiểm cached/uncached logits trong tolerance định trước; đo peak memory, context, dtype và throughput. Không chép benchmark máy khác vào báo cáo của mình. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
