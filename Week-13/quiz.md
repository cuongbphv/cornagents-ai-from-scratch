# Tuần 13 — Quiz: Map LLM vào SDLC; build agent graph CornAgents.AI

> Tự kiểm tra **trước** khi xem solution. Tổng **7** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Cho ví dụ map agent ↔ stage SDLC (ít nhất 3 agent).

## Câu 2 (Trắc nghiệm)

Nguyên tắc 'least-privilege' cho agent nghĩa là gì?

- **A.** Mỗi agent được mọi quyền để linh hoạt
- **B.** Mỗi agent chỉ được cấp quyền/tool tối thiểu cần cho nhiệm vụ của nó
- **C.** Chỉ một agent có quyền
- **D.** Không agent nào dùng tool

## Câu 3 (Tự luận)

Requirements Analyst agent dùng RAG để làm gì?

## Câu 4 (Trắc nghiệm)

Trong workflow multi-agent có quy định, human approval gate nên đặt ở đâu?

- **A.** Không cần
- **B.** Giữa các stage quan trọng (vd. trước khi chốt requirement, trước khi merge) để người duyệt
- **C.** Chỉ ở cuối cùng
- **D.** Chỉ ở đầu

## Câu 5 (Trắc nghiệm)

Vì sao cần 'I/O contract' rõ ràng giữa các agent?

- **A.** Để agent chạy nhanh hơn
- **B.** Để output của agent này là input có cấu trúc, dự đoán được cho agent kế — dễ ghép graph, test và audit
- **C.** Để giảm token
- **D.** Để mã hoá dữ liệu

## Câu 6 (Trắc nghiệm)

Ghép đúng 5 workflow patterns của Anthropic với mô tả?

- **A.** Prompt Chaining = nhiều model bỏ phiếu; Routing = chạy tuần tự
- **B.** Prompt Chaining = các bước cố định nối tiếp; Routing = phân loại input rồi gửi tới prompt/model chuyên biệt; Parallelization = các call độc lập chạy song song; Orchestrator–Workers = model trung tâm phân rã & giao việc; Evaluator–Optimizer = một bên sinh, một bên chấm theo tiêu chí, lặp
- **C.** Orchestrator–Workers = không có model trung tâm; Evaluator–Optimizer = chỉ chạy 1 lần
- **D.** Cả 5 pattern đều cần knowledge graph

## Câu 7 (Tự luận)

'Artifact contract' giữa các agent là gì và vì sao reviewer nên trả 'criterion-level defects' thay vì 'looks good'?

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
