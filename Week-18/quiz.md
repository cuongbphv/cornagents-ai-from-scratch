# Tuần 18, Quiz: Capstone + evaluation/observability

> Tự kiểm tra **trước** khi xem solution. Tổng **7** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Use case capstone khuyến nghị và 3 thành phần kỹ thuật của nó?

## Câu 2 (Trắc nghiệm)

Bộ ba metric đánh giá capstone agentic gồm?

- **A.** FPS, latency, throughput
- **B.** Loss, perplexity, BLEU
- **C.** Precision, recall, F1 (chỉ vậy)
- **D.** Success rate, human-override rate, groundedness

## Câu 3 (Tự luận)

Vì sao chiến lược 'Claude làm brain + model 7B fine-tuned cho sub-task' lại hợp lý?

## Câu 4 (Trắc nghiệm)

'Groundedness' đo điều gì?

- **A.** Chi phí token
- **B.** Tốc độ agent
- **C.** Số agent dùng
- **D.** Mức độ output bám vào/được hỗ trợ bởi tài liệu nguồn (chống bịa)

## Câu 5 (Tự luận)

Viết retrospective 'nối về Phase 1' nghĩa là gì?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

PDF Karpathy-Loop yêu cầu khai báo complexity budget trước mỗi run và làm gì khi hết budget?

- **A.** Trả artifact tốt nhất hiện có kèm danh sách việc chưa xử lý và lý do dừng; không che partial failure sau một câu trả lời trôi chảy
- **B.** Xóa artifact và báo lỗi
- **C.** Tự động tăng budget
- **D.** Chạy tiếp đến khi xong

## Nâng cao 2 (Tự luận)

Hãy nối ba metric capstone (success rate, human-override rate, groundedness) với các số đo trong giáo trình: accuracy trên test set chưa thấy, exact match, token F1, precision.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
