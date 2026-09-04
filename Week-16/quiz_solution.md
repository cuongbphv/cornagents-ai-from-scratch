# Tuần 16, Đáp án & Giải thích: Map LLM vào SDLC; build agent graph CornAgents.AI

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Cho ví dụ map agent ↔ stage SDLC (ít nhất 3 agent).

**Trả lời mẫu:** Requirements Analyst agent: biến feature request Finance Banking thành user story + acceptance criteria, grounded bởi RAG (Tuần 13-14) trên tài liệu nghiệp vụ nội bộ. Code Review agent: đọc diff/PR, flag bug/security/style. Test-Generation agent: từ story/code sinh test case. Có thể thêm Design và Docs agent. Mỗi agent có I/O contract rõ ràng và nối thành graph.

**Giải thích:** Requirements Analyst tận dụng đúng thế mạnh BA của bạn.

## Câu 2 (Trắc nghiệm)

Nguyên tắc 'least-privilege' cho agent nghĩa là gì?

- **A.** Không agent nào dùng tool
- **B.** Mỗi agent được mọi quyền để linh hoạt
- **C.** Mỗi agent chỉ được cấp quyền/tool tối thiểu cần cho nhiệm vụ của nó (đáp án đúng)
- **D.** Chỉ một agent có quyền

**Đáp án: C**

**Giải thích:** Giới hạn quyền giảm rủi ro khi agent lỗi/bị lạm dụng, đặc biệt quan trọng với hệ thống tài chính.

## Câu 3 (Tự luận)

Requirements Analyst agent dùng RAG để làm gì?

**Trả lời mẫu:** Dùng RAG để 'grounding' việc sinh user story/acceptance criteria vào tài liệu nguồn thật, ví dụ quy định nghiệp vụ và spec nội bộ, thay vì bịa. Khi nhận một feature request, agent retrieve các quy định/định nghĩa liên quan, đưa vào context, rồi sinh story bám đúng ràng buộc nghiệp vụ và có thể trích dẫn nguồn.

**Giải thích:** Đây là điểm nối Phase 2 (RAG) vào Phase 3 (agents).

## Câu 4 (Trắc nghiệm)

Trong workflow multi-agent có quy định, human approval gate nên đặt ở đâu?

- **A.** Chỉ ở đầu
- **B.** Không cần
- **C.** Giữa các stage quan trọng (vd. trước khi chốt requirement, trước khi merge) để người duyệt (đáp án đúng)
- **D.** Chỉ ở cuối cùng

**Đáp án: C**

**Giải thích:** Đặt gate giữa các stage cho phép bắt lỗi sớm và giữ con người kiểm soát các quyết định rủi ro.

## Câu 5 (Trắc nghiệm)

Vì sao cần 'I/O contract' rõ ràng giữa các agent?

- **A.** Để giảm token
- **B.** Để mã hoá dữ liệu
- **C.** Để output của agent này là input có cấu trúc, dự đoán được cho agent kế, dễ ghép graph, test và audit (đáp án đúng)
- **D.** Để agent chạy nhanh hơn

**Đáp án: C**

**Giải thích:** Contract (schema state trong LangGraph) làm hệ thống mô-đun và kiểm thử được từng mắt xích.

## Câu 6 (Trắc nghiệm)

Ghép đúng 5 workflow patterns của Anthropic với mô tả?

- **A.** Orchestrator-Workers = không có model trung tâm; Evaluator-Optimizer = chỉ chạy 1 lần
- **B.** Prompt Chaining = nhiều model bỏ phiếu; Routing = chạy tuần tự
- **C.** Prompt Chaining = các bước cố định nối tiếp; Routing = phân loại input rồi gửi tới prompt/model chuyên biệt; Parallelization = các call độc lập chạy song song; Orchestrator-Workers = model trung tâm phân rã & giao việc; Evaluator-Optimizer = một bên sinh, một bên chấm theo tiêu chí, lặp (đáp án đúng)
- **D.** Cả 5 pattern đều cần knowledge graph

**Đáp án: C**

**Giải thích:** Lời khuyên gốc của Anthropic: 'simple, composable patterns rather than complex frameworks', chọn pattern theo bài toán, đừng bê nguyên framework nặng.

## Câu 7 (Tự luận)

'Artifact contract' giữa các agent là gì và vì sao reviewer nên trả 'criterion-level defects' thay vì 'looks good'?

**Trả lời mẫu:** Artifact contract = mỗi handoff giữa hai agent là một artifact có schema rõ (user story JSON, defect list, test file) thay vì đoạn văn tự do, giúp validate tự động, test từng mắt xích, và audit. Reviewer trả defect theo từng tiêu chí (đúng/sai ở tiêu chí nào, bằng chứng gì) vì 'looks good' không cho downstream agent hay con người thông tin hành động được; defect có cấu trúc thì gate được (đếm, chặn, escalate) và đo được chất lượng review theo thời gian.

**Giải thích:** Từ mục VI.D của Karpathy-Loop PDF: 'Every handoff should be an artifact contract. A reviewer returns criterion-level defects, not looks-good.'

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Anthropic báo hệ đa agent thắng single agent 90,2% trên eval nội bộ nhưng tốn khoảng 15 lần token so với chat. Con số này dẫn tới nguyên tắc thiết kế nào?

- **A.** Chỉ dùng đa agent cho code
- **B.** Luôn dùng đa agent vì thắng lớn
- **C.** Không bao giờ dùng đa agent vì quá đắt
- **D.** Chỉ tách vai khi bài toán có nhiều hướng độc lập và chuyên môn hóa thêm tín hiệu; định nghĩa reducer trước khi fan-out; đặt budget token trước vì token usage giải thích phần lớn phương sai hiệu năng (đáp án đúng)

**Đáp án: D**

**Giải thích:** Nguồn: 'How we built our multi-agent research system' (anthropic.com/engineering, đọc 2026-09-04): 'outperformed single-agent Claude Opus 4 by 90.2%', 'about 15× more tokens than chats', 'token usage by itself explains 80% of the variance'.

## Nâng cao 2 (Tự luận)

Xiao và Zhu đặt chain of thought và decomposition vào khung problem decomposition và nhắc System 1, System 2 của Kahneman. Hãy nối khung này với pattern orchestrator-workers và evaluator-optimizer.

**Trả lời mẫu:** Decomposition chia bài lớn thành bài con đơn giản hơn (FoLLM mục 3.2.2, trang 117); orchestrator-workers là decomposition được thể chế hóa ở mức hệ thống: một model chia việc, worker giải, kết quả gộp lại. Self-refinement (FoLLM mục 3.2.3, trang 124) để model tự sửa output; evaluator-optimizer tách vai chấm ra một agent riêng có tiêu chí viết sẵn. System 2 của Kahneman là cách nói cho chế độ suy luận chậm mà cả hai kỹ thuật đều kéo LLM vào.

**Giải thích:** Khi điền 03_agent_design.md, ghi cho mỗi agent nó là hiện thân của ý tưởng nào; không ghi được thì có thể không cần agent đó.
