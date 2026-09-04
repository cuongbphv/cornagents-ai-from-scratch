# Lý thuyết Tuần 17: Knowledge Graph pipeline làm shared memory

> Đọc trước khi điền [`02_kg_pipeline.py`](02_kg_pipeline.py). Ví dụ NetworkX kiểm chứng local 2026-08-11 (nx 3.6.1); nguồn chính là 2 PDF trong `docs/` của repo.

---

## 1. Vì sao graph: một câu đủ

*"The agent forgets, the graph does not."* Mỗi agent chết theo context window của nó; graph là nơi **facts sống xuyên session**. Ba vai trò trong multi-agent (từ Playbook, chi tiết trong [README.md](README.md)): shared memory (worker ghi findings vào graph thay vì dồn qua context orchestrator), grounding layer (evaluator fact-check claim theo edge), persistent world model (loop qua đêm không mất trí nhớ).

RAG và KG không thay thế nhau. RAG trả lời "đoạn văn nào giống câu hỏi nhất" (single-hop, ngữ nghĩa); KG trả lời "đi theo quan hệ từ A qua B tới C" (multi-hop, cấu trúc). Ví dụ quyết định trong README: *"văn bản A sửa đổi B, mà B căn cứ C"*, hai văn bản có thể không giống nhau ngữ nghĩa chút nào, RAG mù, KG đi 2 cạnh là tới.

## 2. Pipeline 4 bước: model cho phán xét, code cho phần còn lại

```
1. Extraction  (Haiku + structured outputs)  → Entity(name, type, description) + Relation(S-P-O)
2. Resolution  (Sonnet)                      → cluster surface forms về canonical entity
3. Assembly    (NetworkX MultiDiGraph)       → node có type/source/description; edge có predicate + provenance
4. Querying    (Sonnet)                      → serialize k-hop subgraph thành triples → trả lời + cite edges
```

Demo assembly kiểm chứng local 2026-08-11, đúng dữ liệu domain của bạn:

```python
import networkx as nx
G = nx.MultiDiGraph()
G.add_edge("TT 39/2016/TT-NHNN", "Luật các TCTD 2010", predicate="căn_cứ",  source_doc="tt39.pdf")
G.add_edge("TT 06/2023/TT-NHNN", "TT 39/2016/TT-NHNN", predicate="sửa_đổi", source_doc="tt06.pdf")
# → 3 nodes, 2 edges; edge data giữ nguyên {'predicate': ..., 'source_doc': ...}
```

`MultiDiGraph` vì: có hướng (A sửa đổi B ≠ B sửa đổi A) và cho phép **nhiều cạnh giữa cùng cặp node** (A vừa `căn_cứ` vừa `dẫn_chiếu` B).

## 3. Bốn nguyên tắc chất lượng: lý do đằng sau (bảng gốc trong README)

1. Description là chìa khóa của resolution. Resolver nhìn tên trần "TT 06" thì chỉ đoán; kèm mô tả grounded ("Thông tư 06/2023 của NHNN sửa đổi quy định cho vay...") mới phân xử được.
2. Precision quan trọng hơn recall cho extraction. Một entity SAI sinh quan hệ sai **lan truyền qua multi-hop** (mọi câu trả lời đi qua node đó đều nhiễm); entity THIẾU chỉ làm graph chưa đầy đủ, sai bất đối xứng nên ưu tiên bất đối xứng. Prompt extraction vì thế viết "only entities central to the document".
3. Provenance phải có trên mọi edge. Thiếu `source_doc` thì bước Querying "cite edges" thành trích dẫn suông, evaluator hết đường fact-check.
4. Evaluation feedback loop gồm gold set, scorer, sửa prompt, xem F1; đúng hình dạng ratchet loop Tuần 15, áp cho pipeline dữ liệu.

## 4. Diagnostics: đọc sức khỏe graph bằng 3 con số

| Chỉ số | Khỏe | Bệnh gì khi lệch |
|--------|------|-------------------|
| Connected components | tiến về 1 | nhiều mảnh rời = resolution kém (cùng entity, nhiều tên chưa gộp) |
| Degree distribution | ít hub hợp lý | node degree khổng lồ bất thường = false merge (gộp nhầm nhiều entity làm một) |
| Edges/nodes ratio | ~1.0-2.0 (theo Playbook) | quá thấp = extraction bỏ sót quan hệ; quá cao bất thường = quan hệ rác |

Hai failure mode chết người (mục nâng cao I4): **silent entity loss** và **false merge**: cái thứ hai độc hơn vì nó *thêm* thông tin sai thay vì chỉ thiếu.

## 5. Eval extraction: precision/recall vs gold set

Gold set mini (~10 entities, ~10 relations từ 2 tài liệu, gán tay): `precision = đúng/trích_ra`, `recall = đúng/gold`, `F1 = 2PR/(P+R)`. Chạy vòng: đo, sửa prompt extraction, đo lại, rồi chỉ giữ thay đổi làm F1 tăng ("graph autoresearch"). Không có vòng này, pipeline drift mà không ai biết.

## 6. Tiếng Việt trong tuần này: resolution là chỗ tiếng Việt thử thách nhất

- Chuẩn hóa NFC trước mọi so khớp (kiểm chứng Tuần 13: `ế` NFC = 1 codepoint, NFD = 3, so sánh trực tiếp KHÔNG bằng nhau). Hai node "Ngân hàng Nhà nước" ở hai dạng normalize là **hai node khác nhau**, một nguồn "nhiều mảnh rời" (mục 4) thuần kỹ thuật, sửa bằng 1 dòng `unicodedata.normalize("NFC", ...)` lúc ingest, rẻ hơn mọi prompt.
- Alias tiếng Việt là bài khó của resolver: cùng một tổ chức xuất hiện là "NHNN" / "Ngân hàng Nhà nước" / "Ngân hàng Nhà nước Việt Nam" / "State Bank of Vietnam", đây chính là bài gom "Edwin Aldrin" về "Buzz Aldrin" của Playbook, phiên bản nghiệp vụ. Description grounded (nguyên tắc 1) là thứ cứu resolver ở đây.
- Số hiệu văn bản là pattern tất định, đừng phí model: `39/2016/TT-NHNN`, `06/2023/TT-NHNN` match được bằng regex; chuẩn hóa số hiệu bằng code, để model phân xử phần thật sự mơ hồ (đúng pattern "model cho phán xét, logic tất định cho phần còn lại" của mục nâng cao I4).
- Entity types + predicates tiếng Việt (`VAN_BAN`, `sửa_đổi`...) như README gợi ý là ổn, chỉ cần **nhất quán tuyệt đối** (một danh sách đóng trong prompt, không cho model tự chế predicate mới).

## 7. Prompt caching: cơ chế thật đằng sau claim chi phí

Tuần này (và plan) claim "extraction bằng Haiku chi phí thấp nhờ prompt caching", đây là cơ chế thật, theo docs Anthropic (tra 2026-08-16; URL cũ `docs.anthropic.com/.../prompt-caching` đã 301 về `platform.claude.com`):

- Cache hoạt động theo prefix. API băm phần đầu prompt tới điểm đánh dấu `cache_control` (tối đa **4 breakpoint**/request); request sau **trùng 100% prefix** tới breakpoint thì đọc từ cache thay vì xử lý lại. Thứ tự cache cố định là `tools`, rồi `system`, rồi `messages`; đổi bất kỳ tầng nào là vô hiệu tầng đó và mọi tầng sau.
- Về giá (theo docs, 2026-08-16), cache write 5 phút = **1.25×** giá input thường; cache read = **0.1×** (tức 10% giá input); TTL mặc định **5 phút**, tùy chọn **1 giờ** với giá write 2×. Prompt ngắn hơn ngưỡng tối thiểu của model (512-4,096 token tùy model, theo bảng trong docs) thì không cache được, không báo lỗi, chỉ thấy `cache_creation_input_tokens` và `cache_read_input_tokens` đều bằng 0 trong response.
- Điều kiện sống còn là "identical" theo nghĩa đen, thêm một dấu cách vào system prompt là mất cache. Docs cũng ghi rõ: đổi `output_config.format` (schema structured outputs của mục 8) cũng vô hiệu cache.

Áp vào pipeline KG tuần này, bước Extraction gọi Haiku hàng trăm lần, mỗi lần chỉ khác nhau **đúng phần chunk văn bản**. Vậy xếp prompt theo nguyên tắc "phần bất biến đứng trước": system prompt + Pydantic schema + danh sách đóng entity types/predicates (mục 6) đặt trước, gắn `cache_control` sau khối đó; nội dung chunk thay đổi đặt sau cùng. Với cách xếp này, từ call thứ hai trở đi phần prefix bất biến tính theo giá cache read, bằng 10% giá input thường theo bảng giá trong docs đã dẫn; prefix càng dài so với chunk thì tiết kiệm càng gần mốc đó; con số thật đọc từ hai field usage nói trên, đừng ước lượng chay. Chạy batch chunk liên tục trong 5 phút TTL là khớp tự nhiên với vòng lặp extraction; batch chạy rải rác thì cân nhắc TTL 1 giờ và tự làm phép tính write 2× có đáng không.

## 8. Structured outputs: cơ chế constrained decoding

Tuần này dùng Pydantic structured outputs như hộp đen; mở hộp:

- Cách thứ nhất là prompt-based JSON, tức "xin" model: viết "hãy trả về JSON đúng schema sau", model *thường* nghe, nhưng không có gì bảo chứng: sai dấu phẩy, thiếu field, sai type đều có thể xảy ra và bạn phải retry. Đây là cách của Tuần 15 khi chưa có gì tốt hơn.
- Cách thứ hai là constrained decoding, tức "cưỡng chế" ở decoder: JSON schema được biên dịch thành **grammar**; tại **mỗi bước sinh token**, engine chỉ cho phép các token giữ output còn hợp lệ theo grammar, token vi phạm bị loại khỏi phân phối trước khi sample (masking trên logits). Model *không thể* sinh JSON sai cú pháp/sai schema, vì lựa chọn đó không tồn tại. Docs Anthropic (tra 2026-08-16) mô tả đúng cơ chế này: "constrained sampling" với grammar biên dịch từ schema, compile lần đầu có độ trễ rồi cache 24 giờ; kèm giới hạn schema (không hỗ trợ recursive schema, `minimum`/`maximum` cho số, ràng buộc độ dài chuỗi...): Pydantic schema của mục 6 nên tránh các ràng buộc đó.
- Phía mã nguồn mở có XGrammar (Dong et al., arXiv 2411.15100, abstract kiểm 2026-08-16), một engine kiểu này: chia vocab thành token kiểm tra được **độc lập ngữ cảnh** (precompute mask sẵn) và token phải kiểm tra runtime bằng stack, claim "up to 100x speedup" so với các engine trước (nguyên văn abstract).
- Ranh giới cần nhớ là constrained decoding chỉ bảo chứng **hình thức** (JSON hợp lệ, đúng schema), không bảo chứng **nội dung** (entity có thật trong văn bản, predicate đúng nghĩa). Vì thế nguyên tắc precision > recall (mục 3) và vòng eval F1 (mục 5) vẫn đứng nguyên, không bị structured outputs thay thế.

## 9. Nguồn

| Nguồn | Vị trí | Dùng cho mục |
|-------|--------|--------------|
| Graph Engineering Playbook | [`../docs/Graph-Engineering-Athropic-Playbook.pdf`](../docs/Graph-Engineering-Athropic-Playbook.pdf) | 2, 3, 4, 5 |
| Karpathy-Loop PDF | [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) | 1 |
| NetworkX (cài local, nx 3.6.1, demo kiểm chứng 2026-08-11) | https://networkx.org/documentation/stable/ | 2, 4 |
| Edge et al. 2024, GraphRAG: Local to Global (Microsoft; CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2404.16130, PDF local: [`../docs/papers/2404.16130_graphrag-local-to-global.pdf`](../docs/papers/2404.16130_graphrag-local-to-global.pdf) | đọc thêm sau mục 2, mở rộng querying từ subgraph k-hop sang câu hỏi tổng hợp toàn corpus (community summarization) |
| Anthropic docs, Prompt caching (tra 2026-08-16; giá/TTL là ảnh chụp ngày tra, kiểm lại trước khi tính chi phí) | https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | 7 |
| Anthropic docs, Structured outputs (tra 2026-08-16) | https://platform.claude.com/docs/en/docs/build-with-claude/structured-outputs | 8 |
| Dong et al. 2024, XGrammar (abstract kiểm 2026-08-16) | https://arxiv.org/abs/2411.15100 | 8 |

(Anthropic Knowledge Graph Construction Cookbook: link trong README nguồn học.)

## Sau khi đọc xong

1. Định nghĩa Pydantic schema + danh sách đóng entity types/predicates (mục 6).
2. Điền [`02_kg_pipeline.py`](02_kg_pipeline.py) theo 4 bước, NFC ngay lúc ingest, regex cho số hiệu văn bản; xếp prompt extraction theo mục 7 (phần bất biến trước, chunk sau) và xác nhận cache hit bằng 2 field usage.
3. Chạy diagnostics 3 con số + so grounded vs ungrounded trên 3-5 câu multi-hop.
4. Gold set + đo F1 + tune prompt; cắm graph vào workflow Tuần 16; ghi [`03_graph_notes.md`](03_graph_notes.md); làm [`quiz.md`](quiz.md).

## 10. Nền đồ thị: định nghĩa, ma trận kề, degree, centrality và hai bài toán cơ bản

Pipeline KG bốn bước ở các mục trên dùng NetworkX như hộp đen. Mục này đưa vào đúng lượng lý thuyết đồ thị mà một knowledge graph cần, lấy từ Ma và Tang, *Deep Learning on Graphs*, chương 2 (catalog ở [`../docs/books/README.md`](../docs/books/README.md)).

**Đồ thị và ma trận kề.** Một đồ thị được viết G = {V, E}, với V = {v₁, ..., v_N} là tập N = |V| node và E = {e₁, ..., e_M} là tập M cạnh (Definition 2.1, trang 18). Mỗi cạnh nối hai node; trong đồ thị có hướng cạnh đi từ node đầu tới node cuối, trong đồ thị vô hướng thứ tự không quan trọng. Hai node gọi là kề (adjacent) khi có cạnh nối chúng. Cùng đồ thị đó biểu diễn tương đương bằng **ma trận kề** A ∈ {0, 1}^{N×N}, với A_{i,j} = 1 khi v_i kề v_j và 0 khi không (Definition 2.2, trang 18); đồ thị vô hướng cho ma trận đối xứng. Với knowledge graph của bạn, có hai khác biệt cần gọi tên: cạnh có hướng (chủ thể, vị ngữ, đối tượng) và có nhiều loại quan hệ, nên NetworkX dùng MultiDiGraph; khi viết ra ma trận, mỗi loại quan hệ cho một ma trận kề riêng, tức một tensor N × N × R; đây là mở rộng thẳng của Definition 2.2 cho R loại quan hệ, và chính là dạng đồ thị dị thể (heterogeneous graph) với nhiều loại node và cạnh mà Ma và Tang định nghĩa ở Definition 2.35 (mục 2.6.1, trang 33). Câu "precision hơn recall" ở mục nguyên tắc chất lượng dịch sang ngôn ngữ này: một entry sai trong A lan qua mọi phép nhân ma trận về sau, tức mọi truy vấn k-hop.

**Degree và centrality.** Degree của node v_i là số node kề với nó (Definition 2.4, trang 19); trong ma trận kề, đó là tổng hàng i. Centrality đo tầm quan trọng của một node, và có nhiều cách đo; cách đầu tiên sách giới thiệu là degree centrality: node quan trọng nếu có nhiều node khác nối tới nó (mục 2.3.3, trang 23). Với KG tài liệu pháp lý, hãy kỳ vọng node degree cao là các thực thể trung tâm như tên cơ quan ban hành hay loại sản phẩm; in top 10 node theo degree sau bước assembly là cách kiểm nhanh xem extraction có bắt đúng thực thể trung tâm hay đang bị nhiễu bởi các thực thể phụ như ngày tháng.

**Hai bài toán cơ bản trên node.** Sách chia tác vụ trên đồ thị thành node-focused (toàn bộ dữ liệu là một đồ thị, node là mẫu) và graph-focused (mỗi mẫu là một đồ thị) (mục 2.7, trang 39). Hai tác vụ node-focused điển hình: **node classification**, gán nhãn cho node dựa trên thông tin đi kèm và cấu trúc lân cận, và **link prediction**, dự đoán cạnh còn thiếu. Với KG của bạn, node classification là bước resolution gán type cho thực thể; link prediction là câu hỏi "hai thực thể này có quan hệ nhưng extraction chưa bắt được không", thứ mà truy vấn subgraph k = 2 ở bước querying trả lời gián tiếp. Chương 5 của sách (Graph Neural Networks) là bước tiếp theo nếu bạn muốn học các quan hệ đó thay vì extract bằng prompt; lộ trình này dừng ở extraction và truy vấn tường minh vì cần provenance trên mọi cạnh.

**Spectral graph theory, đọc thêm.** Mục 2.4 (trang 26) giới thiệu ma trận Laplacian và trị riêng của nó, nền của community detection và của GraphRAG (paper trong kệ paper) khi tóm tắt theo cộng đồng. Trị riêng ở đây là đúng khái niệm Tuần 1 mục 6, áp lên một ma trận dựng từ A và degree.
