# Tuần 16, Quiz: Map LLM vào SDLC; build agent graph CornAgents.AI

> Tự kiểm tra **trước** khi xem solution. Tổng **13** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
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

## Câu 8 (Trắc nghiệm)

FoLLM nêu khung tổng quát của problem decomposition gồm hai thành phần. Khi map sang orchestrator-workers trong CornAgents.AI, hai thành phần đó là gì?

- **A.** Prompt ensembling và output ensembling: chạy nhiều prompt hoặc lấy nhiều mẫu đầu ra rồi kết hợp chúng thành dự đoán cuối cùng
- **B.** Prediction và refinement: sinh câu trả lời ban đầu rồi thu phản hồi và dùng phản hồi đó để sửa dần cho tới khi đầu ra đạt yêu cầu
- **C.** Reasoning path search và verifier: tìm nhiều đường suy luận rồi chấm điểm từng bước để chọn đường tốt nhất trong không gian tìm kiếm
- **D.** Sub-problem generation và sub-problem solving: tách bài toán thành các bài con, rồi giải từng bài con để rút ra kết luận trung gian và cuối

## Câu 9 (Trắc nghiệm)

FoLLM phân biệt sinh toàn bộ bài con một lần ({p1,...,pn} = G(p0), phương trình 3.2) với sinh từng bài con theo bước (pi = Gi(p0, {p<i, a<i}), phương trình 3.5). Orchestrator của bạn nên sinh sub-task theo cách thứ hai trong trường hợp nào?

- **A.** Khi các bước suy luận không cố định và mỗi bước phụ thuộc kết quả bước trước, nên đường giải phải được điều chỉnh trong lúc giải
- **B.** Khi muốn chạy các bài con song song để giảm chi phí tính toán, vì sinh theo bước cho phép phân phối đều tải giữa các worker
- **C.** Khi bài toán có tính hợp thành rõ như viết tài liệu theo dàn ý, vì mỗi phần có thể được viết độc lập với các phần trước nó
- **D.** Khi cần giảm số lần gọi LLM, vì sinh theo bước gộp việc sinh bài con và việc giải bài con vào cùng một lượt dự đoán duy nhất

## Câu 10 (Tự luận)

Reviewer agent trong CornAgents.AI chạy vòng lặp sửa dần. FoLLM mô tả khung self-refinement ba bước của Madaan et al. như thế nào, và sách cảnh báo hai vấn đề gì riêng của phương pháp lặp mà bạn phải xử lý khi thiết kế vòng lặp này?

## Câu 11 (Trắc nghiệm)

Theo FoLLM, khác biệt then chốt giữa tool use và RAG là gì, và điểm chung nào khiến sách gọi cả hai là cùng một việc dưới góc nhìn language modeling?

- **A.** Trong tool use, model tự quyết định có gọi hay không; trong RAG, hệ IR luôn được gọi cho mọi câu hỏi; cả hai đều được FoLLM xếp vào nhóm self-refinement vì đều sửa câu trả lời ban đầu bằng thông tin lấy từ bên ngoài
- **B.** Trong tool use, hàm ngoài được gọi ngay trong lúc suy luận; trong RAG, văn bản truy hồi được cung cấp trước khi dự đoán bắt đầu; cả hai đều dùng hệ ngoài để tạo ngữ cảnh đủ và liên quan trước khi sinh kết quả cuối
- **C.** Tool use trả kết quả có cấu trúc còn RAG trả văn bản tự do; cả hai đều được đánh giá bằng exact match trên câu trả lời cuối, và FoLLM xếp cả hai vào nhóm phương pháp chain of thought nhiều vòng
- **D.** Tool use chỉ dùng cho tính toán số còn RAG chỉ dùng cho văn bản; cả hai đều cần fine-tune model để sinh marker gọi hệ ngoài trước khi trả lời, và FoLLM xếp cả hai vào nhóm phương pháp ensembling

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
