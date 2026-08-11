# Tuần 14 — Đáp án & Giải thích: Graph Engineering: Knowledge Graph làm shared memory cho multi-agent

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Bốn stage của knowledge graph pipeline (Anthropic Playbook) theo đúng thứ tự?

- **A.** Querying → Assembly → Resolution → Extraction
- **B.** Extraction (Haiku, structured outputs) → Resolution (Sonnet, cluster) → Assembly (NetworkX graph) → Querying (subgraph + grounded answer) ✅
- **C.** Embedding → Chunking → Retrieval → Generation
- **D.** Extraction → Querying → Resolution → Assembly

**Đáp án: B**

**Giải thích:** Mỗi stage là một prompt/model call: Haiku extract entities+relations theo Pydantic schema; Sonnet resolve surface forms; NetworkX MultiDiGraph lắp graph với provenance; Sonnet trả lời trên subgraph đã serialize.

## Câu 2 (Tự luận)

RAG và Knowledge Graph khác nhau thế nào, khi nào cần cái nào?

**Trả lời mẫu:** RAG retrieve chunk theo tương đồng ngữ nghĩa với câu hỏi — tốt cho câu hỏi single-hop (đáp án nằm trong một đoạn). Nó thất bại với multi-hop: khi đáp án phải NỐI facts từ nhiều tài liệu không giống nhau về mặt lexical/semantic. Knowledge graph biến entity chung thành node tường minh có edge sang cả hai tài liệu — graph traversal tìm ra kết nối bất kể surface form. Hai cách bổ trợ: RAG rẻ cho direct retrieval, KG cho structural reasoning; thực tế dùng cùng nhau.

**Giải thích:** Quy tắc: cần CHAIN facts xuyên nguồn / SHARE structured state / GROUND phán xét → graph. Chỉ cần retrieve/classify → RAG hoặc đơn giản hơn là đủ.

## Câu 3 (Trắc nghiệm)

Vì sao extraction prompt yêu cầu viết 'one-sentence description grounded in this document' cho mỗi entity?

- **A.** Để hiển thị đẹp trong UI
- **B.** Description là tín hiệu ngữ nghĩa cho stage RESOLUTION — thiếu nó resolver chỉ thấy tên và phải đoán; 'Armstrong — phi hành gia' và 'Armstrong — nghệ sĩ jazz' trùng tên nhưng không được merge ✅
- **C.** Để giảm token
- **D.** Để thay thế cho embeddings

**Đáp án: B**

**Giải thích:** Description không phải metadata mà là input hạng nhất cho resolution — nó thay thứ mà trained classifier phải học từ labeled data theo domain.

## Câu 4 (Trắc nghiệm)

Vì sao với knowledge graph, PRECISION của extraction thường quan trọng hơn RECALL?

- **A.** Vì recall không đo được
- **B.** Vì một entity SAI sinh ra các quan hệ sai và lan truyền qua multi-hop reasoning (graph chủ động gây nhiễu), còn entity THIẾU chỉ làm graph không đầy đủ nhưng vẫn đúng ✅
- **C.** Vì precision rẻ hơn để tính
- **D.** Vì Haiku không thể đạt recall cao

**Đáp án: B**

**Giải thích:** Kết quả trên Apollo corpus: precision 1.00, recall 0.38–0.55 — extractor bảo thủ là trade-off ĐÚNG cho production; evaluation harness giúp bạn chỉnh trade-off này có chủ đích.

## Câu 5 (Tự luận)

Nêu 3 vai trò của knowledge graph trong kiến trúc multi-agent (theo Playbook).

**Trả lời mẫu:** (1) Shared memory cho orchestrator–workers: worker đọc/ghi graph trực tiếp thay vì đẩy summary qua context window của orchestrator — window của orchestrator không phình theo số worker. (2) Grounding layer cho evaluator–optimizer: evaluator kiểm tra từng claim theo edge có provenance ('triple X không tồn tại; graph chứa Y từ document Z') — fact-check thay vì cảm giác. (3) Persistent world model cho loop chạy dài: context window bị flush thì graph vẫn còn — 'the agent forgets, the graph does not'.

**Giải thích:** Đây là 3 chỗ cắm graph vào CornAgents.AI: workers ghi, evaluator check, loop qua đêm không mất trí nhớ.

## Câu 6 (Trắc nghiệm)

'Grounded answer' khác 'ungrounded answer' thế nào khi query graph?

- **A.** Grounded chạy nhanh hơn
- **B.** Grounded bị ràng buộc 'answer using ONLY the graph, cite edges' — trả lời truy vết được về triples có provenance và nói rõ graph KHÔNG chứa gì; ungrounded dựa vào pretraining nên nghe hợp lý nhưng trên private corpus thì không kiểm chứng được ✅
- **C.** Ungrounded luôn sai
- **D.** Grounded không cần model

**Đáp án: B**

**Giải thích:** Trên corpus riêng (tài liệu Finance Banking nội bộ) model không có kiến thức pretraining — chỉ grounded answer là dùng được, và citation kiểm tra được bằng string matching.

## Câu 7 (Tự luận)

Evaluation feedback loop của KG pipeline hoạt động thế nào và vì sao nó 'cùng hình dạng' với ratchet loop của Karpathy autoresearch?

**Trả lời mẫu:** Lập gold set (entities/relations tự label từ 2+ tài liệu đại diện) → chạy extraction → scorer đo precision/recall/F1 → đổi extraction prompt/schema → chạy lại → giữ thay đổi nếu F1 tăng, revert nếu giảm. Cùng hình dạng với autoresearch: act (extract) → observe (score) → learn (tune prompt) → repeat; chỉ khác artifact được tối ưu không phải train.py mà là prompt/ontology/resolution policy — 'graph autoresearch'. Không có harness này, không biết thay đổi prompt làm chất lượng tốt lên hay tệ đi, và drift theo corpus không ai bắt được.

**Giải thích:** Trí tuệ của loop nằm ở chất lượng environmental feedback, không nằm trong model.
