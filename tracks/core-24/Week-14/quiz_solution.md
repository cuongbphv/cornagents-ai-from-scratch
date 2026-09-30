# Tuần 14, Đáp án & Giải thích: Preference learning và DPO

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

DPO, GRPO và RLVR có phải ba bước bắt buộc liên tiếp không?

**Trả lời mẫu:** Không. DPO là phương pháp preference optimization; GRPO là optimizer policy; RLVR nói về reward kiểm chứng được. Chọn theo bài toán và dữ liệu.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 6, 8, 11. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Preference learning và DPO”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Tự viết DPO loss toy, giải thích reference policy và tiêu chí chọn cặp. Dùng fixture để phân biệt câu trôi chảy với câu có outcome đúng. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
