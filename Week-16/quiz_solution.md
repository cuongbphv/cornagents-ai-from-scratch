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

## Câu 8 (Trắc nghiệm)

FoLLM nêu khung tổng quát của problem decomposition gồm hai thành phần. Khi map sang orchestrator-workers trong CornAgents.AI, hai thành phần đó là gì?

- **A.** Prompt ensembling và output ensembling: chạy nhiều prompt hoặc lấy nhiều mẫu đầu ra rồi kết hợp chúng thành dự đoán cuối cùng
- **B.** Prediction và refinement: sinh câu trả lời ban đầu rồi thu phản hồi và dùng phản hồi đó để sửa dần cho tới khi đầu ra đạt yêu cầu
- **C.** Reasoning path search và verifier: tìm nhiều đường suy luận rồi chấm điểm từng bước để chọn đường tốt nhất trong không gian tìm kiếm
- **D.** Sub-problem generation và sub-problem solving: tách bài toán thành các bài con, rồi giải từng bài con để rút ra kết luận trung gian và cuối (đáp án đúng)

**Đáp án: D**

**Giải thích:** FoLLM: "A general framework for problem decomposition involves two elements. Sub-problem Generation. This involves decomposing the input problem into a number of sub-problems. Sub-problem Solving. This involves solving each sub-problem and deriving intermediate and final conclusions through reasoning." Các phương án khác là self-refinement (3.2.3) và ensembling (3.2.4). (FoLLM mục 3.2.2, tr. 120)

## Câu 9 (Trắc nghiệm)

FoLLM phân biệt sinh toàn bộ bài con một lần ({p1,...,pn} = G(p0), phương trình 3.2) với sinh từng bài con theo bước (pi = Gi(p0, {p<i, a<i}), phương trình 3.5). Orchestrator của bạn nên sinh sub-task theo cách thứ hai trong trường hợp nào?

- **A.** Khi các bước suy luận không cố định và mỗi bước phụ thuộc kết quả bước trước, nên đường giải phải được điều chỉnh trong lúc giải (đáp án đúng)
- **B.** Khi muốn chạy các bài con song song để giảm chi phí tính toán, vì sinh theo bước cho phép phân phối đều tải giữa các worker
- **C.** Khi bài toán có tính hợp thành rõ như viết tài liệu theo dàn ý, vì mỗi phần có thể được viết độc lập với các phần trước nó
- **D.** Khi cần giảm số lần gọi LLM, vì sinh theo bước gộp việc sinh bài con và việc giải bài con vào cùng một lượt dự đoán duy nhất

**Đáp án: A**

**Giải thích:** FoLLM: cách hai bước (sinh hết rồi giải) "assumes that the problem is compositional, making it more suitable for tasks like writing and code generation"; ngược lại với bài toán suy luận phức tạp "the reasoning steps may not be fixed ... each step of reasoning may depend on the outcomes of prior steps. In such cases, it is undesirable to use fixed sub-problem generation in advance" (tr. 120 đến 121). Phương trình 3.5 cho phép "the reasoning paths are not fixed in advance, and the models can choose and adapt their reasoning strategies during problem-solving." (FoLLM mục 3.2.2, tr. 120-123)

## Câu 10 (Tự luận)

Reviewer agent trong CornAgents.AI chạy vòng lặp sửa dần. FoLLM mô tả khung self-refinement ba bước của Madaan et al. như thế nào, và sách cảnh báo hai vấn đề gì riêng của phương pháp lặp mà bạn phải xử lý khi thiết kế vòng lặp này?

**Trả lời mẫu:** Ba bước: Prediction (LLM sinh đầu ra ban đầu), Feedback Collection (thu phản hồi về đầu ra, có thể do người, reward model hay chính LLM tạo), Refinement (LLM sửa đầu ra dựa trên phản hồi); hai bước sau có thể lặp nhiều lần và chất lượng phản hồi cụ thể, chi tiết là yếu tố quyết định. FoLLM cảnh báo phương pháp lặp có hai vấn đề không có ở phương pháp một lượt: lỗi ở bước sớm có thể ảnh hưởng xấu tới các bước sau, và việc quyết định khi nào dừng lặp thường cần thêm công sức kỹ thuật. Với reviewer agent, điều này nghĩa là phản hồi phải chỉ ra lỗi cụ thể theo tiêu chí và phải có điều kiện dừng rõ (số vòng tối đa hoặc ngưỡng chất lượng).

**Giải thích:** FoLLM: "A general framework of self-refinement with LLMs involves three steps [Madaan et al., 2024]. Prediction ... Feedback Collection ... Refinement" và "receiving accurate and detailed feedback is critical". Về phương pháp lặp (tr. 129 đến 130): "errors in earlier steps may negatively impact subsequent problem-solving, and determining when to stop iterating often requires additional engineering effort." (FoLLM mục 3.2.3, tr. 126-130)

## Câu 11 (Trắc nghiệm)

Theo FoLLM, khác biệt then chốt giữa tool use và RAG là gì, và điểm chung nào khiến sách gọi cả hai là cùng một việc dưới góc nhìn language modeling?

- **A.** Trong tool use, model tự quyết định có gọi hay không; trong RAG, hệ IR luôn được gọi cho mọi câu hỏi; cả hai đều được FoLLM xếp vào nhóm self-refinement vì đều sửa câu trả lời ban đầu bằng thông tin lấy từ bên ngoài
- **B.** Trong tool use, hàm ngoài được gọi ngay trong lúc suy luận; trong RAG, văn bản truy hồi được cung cấp trước khi dự đoán bắt đầu; cả hai đều dùng hệ ngoài để tạo ngữ cảnh đủ và liên quan trước khi sinh kết quả cuối (đáp án đúng)
- **C.** Tool use trả kết quả có cấu trúc còn RAG trả văn bản tự do; cả hai đều được đánh giá bằng exact match trên câu trả lời cuối, và FoLLM xếp cả hai vào nhóm phương pháp chain of thought nhiều vòng
- **D.** Tool use chỉ dùng cho tính toán số còn RAG chỉ dùng cho văn bản; cả hai đều cần fine-tune model để sinh marker gọi hệ ngoài trước khi trả lời, và FoLLM xếp cả hai vào nhóm phương pháp ensembling

**Đáp án: B**

**Giải thích:** FoLLM: "A key difference between the tool use examples here and the previously discussed RAG examples is that in tool use, external functions can be called during inference. In contrast, in RAG, the retrieved texts are provided before the prediction process begins. However, from the language modeling perspective, they are actually doing the same thing: before generating the final result, we use external tools ... to obtain sufficient and relevant context." Sách xếp RAG vào khung problem decomposition (tr. 137), không phải self-refinement. (FoLLM mục 3.2.5, tr. 138)

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
