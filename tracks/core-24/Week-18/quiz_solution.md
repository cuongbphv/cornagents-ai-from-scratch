# Tuần 18, Đáp án & Giải thích: Serving, phiên bản và chi phí thực

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Fake model replay pass có thể ghi là benchmark LLM thật không?

**Trả lời mẫu:** Không. Ghi rõ replay/fixture; live-model cần runtime/model revision, dữ liệu, budget và kết quả thực riêng.

**Giải thích:** Nguồn: tài liệu chương trình CornAgents.AI, mục 8, 10. Đáp án là diễn giải bài học, không phải kết quả đo.

## Câu 2 (Tự luận)

Trong bài “Serving, phiên bản và chi phí thực”, hãy nêu một phép kiểm có thể bác bỏ kết luận của bạn và phần phép kiểm đó chưa xác nhận.

**Trả lời mẫu:** Xây adapter interface cho fake/local model, đo latency của đúng workload, ghi toàn bộ retry. Không cần API trả phí để hoàn thành bài offline. Phải ghi phạm vi fixture/dataset, giữ output thực và không mở rộng claim quá dữ liệu đã thử.

**Giải thích:** Câu hỏi kiểm phương pháp; không có một điểm benchmark mặc định.

## Câu 3 (Tự luận)

Sản phẩm chạy được của tuần này chứng minh điều gì về người học, hệ thống và bản cải tiến?

**Trả lời mẫu:** G1 cần người học tự giải thích/sửa bài biến thể; G2 cần outcome và evidence của hệ thống; G3 cần kiểm đúng candidate và quyết định riêng. Không lấy một demo để thay cả ba cửa.

**Giải thích:** Nguồn: mục 3.4, 8.4 và 18.1 của tài liệu chương trình.
