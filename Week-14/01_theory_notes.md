# Lý thuyết Tuần 14 — Knowledge Graph pipeline làm shared memory

> Đọc trước khi điền [`02_kg_pipeline.py`](02_kg_pipeline.py). Ví dụ NetworkX kiểm chứng local 2026-08-11 (nx 3.6.1); nguồn chính là 2 PDF trong `docs/` của repo.

---

## 1. Vì sao graph — một câu đủ

*"The agent forgets, the graph does not."* Mỗi agent chết theo context window của nó; graph là nơi **facts sống xuyên session**. Ba vai trò trong multi-agent (từ Playbook, chi tiết trong [README.md](README.md)): shared memory (worker ghi findings vào graph thay vì dồn qua context orchestrator), grounding layer (evaluator fact-check claim theo edge), persistent world model (loop qua đêm không mất trí nhớ).

**RAG vs KG — không thay thế nhau:** RAG trả lời "đoạn văn nào giống câu hỏi nhất" (single-hop, ngữ nghĩa); KG trả lời "đi theo quan hệ từ A qua B tới C" (multi-hop, cấu trúc). Ví dụ quyết định trong README: *"văn bản A sửa đổi B, mà B căn cứ C"* — hai văn bản có thể không giống nhau ngữ nghĩa chút nào, RAG mù, KG đi 2 cạnh là tới.

## 2. Pipeline 4 bước — model cho phán xét, code cho phần còn lại

```
1. Extraction  (Haiku + structured outputs)  → Entity(name, type, description) + Relation(S–P–O)
2. Resolution  (Sonnet)                      → cluster surface forms về canonical entity
3. Assembly    (NetworkX MultiDiGraph)       → node có type/source/description; edge có predicate + provenance
4. Querying    (Sonnet)                      → serialize k-hop subgraph thành triples → trả lời + cite edges
```

Demo assembly kiểm chứng local 2026-08-11 — đúng dữ liệu domain của bạn:

```python
import networkx as nx
G = nx.MultiDiGraph()
G.add_edge("TT 39/2016/TT-NHNN", "Luật các TCTD 2010", predicate="căn_cứ",  source_doc="tt39.pdf")
G.add_edge("TT 06/2023/TT-NHNN", "TT 39/2016/TT-NHNN", predicate="sửa_đổi", source_doc="tt06.pdf")
# → 3 nodes, 2 edges; edge data giữ nguyên {'predicate': ..., 'source_doc': ...}
```

`MultiDiGraph` vì: có hướng (A sửa đổi B ≠ B sửa đổi A) và cho phép **nhiều cạnh giữa cùng cặp node** (A vừa `căn_cứ` vừa `dẫn_chiếu` B).

## 3. Bốn nguyên tắc chất lượng — lý do đằng sau (bảng gốc trong README)

1. **Description là chìa khóa resolution** — resolver nhìn tên trần "TT 06" thì chỉ đoán; kèm mô tả grounded ("Thông tư 06/2023 của NHNN sửa đổi quy định cho vay...") mới phân xử được.
2. **Precision > recall cho extraction** — một entity SAI sinh quan hệ sai **lan truyền qua multi-hop** (mọi câu trả lời đi qua node đó đều nhiễm); entity THIẾU chỉ làm graph chưa đầy đủ — sai bất đối xứng nên ưu tiên bất đối xứng. Prompt extraction vì thế viết "only entities central to the document".
3. **Provenance trên mọi edge** — thiếu `source_doc` thì bước Querying "cite edges" thành trích dẫn suông, evaluator hết đường fact-check.
4. **Evaluation feedback loop** — gold set + scorer + sửa prompt + xem F1: đúng hình dạng ratchet loop Tuần 12, áp cho pipeline dữ liệu.

## 4. Diagnostics — đọc sức khỏe graph bằng 3 con số

| Chỉ số | Khỏe | Bệnh gì khi lệch |
|--------|------|-------------------|
| Connected components | tiến về 1 | nhiều mảnh rời = resolution kém (cùng entity, nhiều tên chưa gộp) |
| Degree distribution | ít hub hợp lý | node degree khổng lồ bất thường = false merge (gộp nhầm nhiều entity làm một) |
| Edges/nodes ratio | ~1.0–2.0 (theo Playbook) | quá thấp = extraction bỏ sót quan hệ; quá cao bất thường = quan hệ rác |

Hai failure mode chết người (mục nâng cao I4): **silent entity loss** và **false merge** — cái thứ hai độc hơn vì nó *thêm* thông tin sai thay vì chỉ thiếu.

## 5. Eval extraction — precision/recall vs gold set

Gold set mini (~10 entities, ~10 relations từ 2 tài liệu, gán tay): `precision = đúng/trích_ra`, `recall = đúng/gold`, `F1 = 2PR/(P+R)`. Chạy vòng: đo → sửa prompt extraction → đo lại → chỉ giữ thay đổi làm F1 tăng ("graph autoresearch"). Không có vòng này, pipeline drift mà không ai biết.

## 6. Tiếng Việt trong tuần này — resolution là chỗ tiếng Việt thử thách nhất

- **NFC trước mọi so khớp** (kiểm chứng Tuần 10: `ế` NFC = 1 codepoint, NFD = 3, so sánh trực tiếp KHÔNG bằng nhau): hai node "Ngân hàng Nhà nước" ở hai dạng normalize là **hai node khác nhau** — một nguồn "nhiều mảnh rời" (mục 4) thuần kỹ thuật, sửa bằng 1 dòng `unicodedata.normalize("NFC", ...)` lúc ingest, rẻ hơn mọi prompt.
- **Alias tiếng Việt cho resolver**: cùng một tổ chức xuất hiện là "NHNN" / "Ngân hàng Nhà nước" / "Ngân hàng Nhà nước Việt Nam" / "State Bank of Vietnam" — đây chính là bài "Edwin Aldrin → Buzz Aldrin" của Playbook, phiên bản nghiệp vụ. Description grounded (nguyên tắc 1) là thứ cứu resolver ở đây.
- **Số hiệu văn bản là pattern tất định — đừng phí model**: `39/2016/TT-NHNN`, `06/2023/TT-NHNN` match được bằng regex; chuẩn hóa số hiệu bằng code, để model phân xử phần thật sự mơ hồ (đúng pattern "model cho phán xét, logic tất định cho phần còn lại" của mục nâng cao I4).
- Entity types + predicates tiếng Việt (`VAN_BAN`, `sửa_đổi`...) như README gợi ý là ổn — chỉ cần **nhất quán tuyệt đối** (một danh sách đóng trong prompt, không cho model tự chế predicate mới).

## 7. Nguồn

| Nguồn | Vị trí | Dùng cho mục |
|-------|--------|--------------|
| Graph Engineering Playbook | [`../docs/Graph-Engineering-Athropic-Playbook.pdf`](../docs/Graph-Engineering-Athropic-Playbook.pdf) | 2, 3, 4, 5 |
| Karpathy-Loop PDF | [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) | 1 |
| NetworkX (cài local, nx 3.6.1 — demo kiểm chứng 2026-08-11) | https://networkx.org/documentation/stable/ | 2, 4 |

(Anthropic Knowledge Graph Construction Cookbook: link trong README nguồn học.)

## Sau khi đọc xong

1. Định nghĩa Pydantic schema + danh sách đóng entity types/predicates (mục 6).
2. Điền [`02_kg_pipeline.py`](02_kg_pipeline.py) theo 4 bước — NFC ngay lúc ingest, regex cho số hiệu văn bản.
3. Chạy diagnostics 3 con số + so grounded vs ungrounded trên 3–5 câu multi-hop.
4. Gold set + đo F1 + tune prompt; cắm graph vào workflow Tuần 13; ghi [`03_graph_notes.md`](03_graph_notes.md); làm [`quiz.md`](quiz.md).
