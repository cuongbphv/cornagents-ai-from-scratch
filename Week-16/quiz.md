# Tuần 16, Quiz: Map LLM vào SDLC; build agent graph CornAgents.AI

> Tự kiểm tra **trước** khi xem solution. Tổng **9** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Cho ví dụ map agent ↔ stage SDLC (ít nhất 3 agent).

## Câu 2 (Trắc nghiệm)

Nguyên tắc 'least-privilege' cho agent nghĩa là gì?

- **A.** Không agent nào dùng tool
- **B.** Mỗi agent được mọi quyền để linh hoạt
- **C.** Mỗi agent chỉ được cấp quyền/tool tối thiểu cần cho nhiệm vụ của nó
- **D.** Chỉ một agent có quyền

## Câu 3 (Tự luận)

Requirements Analyst agent dùng RAG để làm gì?

## Câu 4 (Trắc nghiệm)

Trong workflow multi-agent có quy định, human approval gate nên đặt ở đâu?

- **A.** Chỉ ở đầu
- **B.** Không cần
- **C.** Giữa các stage quan trọng (vd. trước khi chốt requirement, trước khi merge) để người duyệt
- **D.** Chỉ ở cuối cùng

## Câu 5 (Trắc nghiệm)

Vì sao cần 'I/O contract' rõ ràng giữa các agent?

- **A.** Để giảm token
- **B.** Để mã hoá dữ liệu
- **C.** Để output của agent này là input có cấu trúc, dự đoán được cho agent kế, dễ ghép graph, test và audit
- **D.** Để agent chạy nhanh hơn

## Câu 6 (Trắc nghiệm)

Ghép đúng 5 workflow patterns của Anthropic với mô tả?

- **A.** Orchestrator-Workers = không có model trung tâm; Evaluator-Optimizer = chỉ chạy 1 lần
- **B.** Prompt Chaining = nhiều model bỏ phiếu; Routing = chạy tuần tự
- **C.** Prompt Chaining = các bước cố định nối tiếp; Routing = phân loại input rồi gửi tới prompt/model chuyên biệt; Parallelization = các call độc lập chạy song song; Orchestrator-Workers = model trung tâm phân rã & giao việc; Evaluator-Optimizer = một bên sinh, một bên chấm theo tiêu chí, lặp
- **D.** Cả 5 pattern đều cần knowledge graph

## Câu 7 (Tự luận)

'Artifact contract' giữa các agent là gì và vì sao reviewer nên trả 'criterion-level defects' thay vì 'looks good'?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Anthropic báo hệ đa agent thắng single agent 90,2% trên eval nội bộ nhưng tốn khoảng 15 lần token so với chat. Con số này dẫn tới nguyên tắc thiết kế nào?

- **A.** Chỉ dùng đa agent cho code
- **B.** Luôn dùng đa agent vì thắng lớn
- **C.** Không bao giờ dùng đa agent vì quá đắt
- **D.** Chỉ tách vai khi bài toán có nhiều hướng độc lập và chuyên môn hóa thêm tín hiệu; định nghĩa reducer trước khi fan-out; đặt budget token trước vì token usage giải thích phần lớn phương sai hiệu năng

## Nâng cao 2 (Tự luận)

Xiao và Zhu đặt chain of thought và decomposition vào khung problem decomposition và nhắc System 1, System 2 của Kahneman. Hãy nối khung này với pattern orchestrator-workers và evaluator-optimizer.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
