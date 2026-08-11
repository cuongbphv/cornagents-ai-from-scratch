# Tuần 14 — Graph Engineering: Knowledge Graph làm shared memory cho multi-agent

> Phase 3 — SDLC / CornAgents.AI. Xây knowledge graph pipeline bằng Claude API (thay pipeline NLP cổ điển) và cắm vào CornAgents.AI làm shared memory / grounding layer / persistent world model.
> Nguồn gốc tuần này: `docs/Graph-Engineering-Athropic-Playbook.pdf`, `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`, `docs/5-layers-multi-agent.jpg`.

## Mục tiêu

- Hiểu vì sao multi-agent cần **lớp hạ tầng graph**: mỗi agent chết theo context window của nó; graph là nơi facts sống xuyên session ("the agent forgets, the graph does not").
- Tự xây **knowledge graph pipeline 4 bước** hoàn toàn bằng Claude API:
  1. **Extraction** (Haiku + structured outputs) — entities + quan hệ S–P–O theo Pydantic schema.
  2. **Resolution** (Sonnet) — cluster các surface form về canonical entity ("Edwin Aldrin" → "Buzz Aldrin").
  3. **Assembly** (NetworkX MultiDiGraph) — node mang type/source/description, edge mang predicate + provenance.
  4. **Querying** (Sonnet) — serialize k-hop subgraph thành triples, trả lời multi-hop **có trích dẫn edge**.
- Hiểu 3 vai trò của graph trong multi-agent: **shared memory** (orchestrator–workers), **grounding layer** (evaluator–optimizer fact-check claim theo edge), **persistent world model** (loop qua đêm không mất trí nhớ).
- Phân biệt **RAG vs Knowledge Graph**: RAG cho single-hop retrieval; KG cho multi-hop reasoning nối facts xuyên tài liệu — hai thứ bổ trợ, không thay thế nhau.

## Nguồn học

- `docs/Graph-Engineering-Athropic-Playbook.pdf` — pipeline 4 stage, prompt extraction/resolution/summarization đầy đủ, evaluation vs gold set, scaling guidance.
- `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` — tiến trình Loop → Chain → Swarm → DAG → Knowledge Graph; commit DAG (work lineage) vs knowledge graph (domain knowledge); build path Day 1 → Month 2.
- Anthropic **Knowledge Graph Construction Cookbook** (claude-cookbooks repo).
- NetworkX docs (MultiDiGraph).

## Nhiệm vụ (Task)

1. Build KG pipeline trên **5–10 tài liệu Finance Banking** của bạn (tài liệu nghiệp vụ nội bộ): extract → resolve → assemble → query.
2. Chạy **graph diagnostics**: connected components (1 component = resolution tốt), degree distribution (hub nodes), edge/node ratio (~1.0–2.0 là khỏe).
3. So sánh **grounded vs ungrounded answer**: cùng một câu hỏi multi-hop, một lần trả lời tự do, một lần bắt buộc "answer using ONLY the graph, cite edges".
4. Cắm graph vào workflow Tuần 13 làm **shared memory**: Requirements Analyst agent ghi entities/relations vào graph; Review agent fact-check claim theo edge.
5. Lập **mini gold set** (~10 entities, ~10 relations từ 2 tài liệu) và đo precision/recall của extraction — chạy evaluation feedback loop: sửa prompt → chạy lại scorer → xem F1 di chuyển ("graph autoresearch").

## Deliverable

- `kg_pipeline.py` chạy được trên corpus của bạn (extract → resolve → assemble → query có trích dẫn).
- Bản so sánh grounded vs ungrounded + số liệu precision/recall vs gold set → `graph_notes.md`.

## Thời lượng

~10–12 giờ.

## Phần cứng

Bất kỳ — đây là việc API (Haiku cho extraction volume lớn, Sonnet cho resolution/query). Chi phí thấp: extraction bằng Haiku + prompt caching.

## Kiến thức lõi

### 5 tầng engineering (ảnh `5-layers-multi-agent.jpg`)

```
1. Prompt engineering    — the message      (một input)
2. Context engineering   — the memory       (cái gì ở trong window)
3. Harness engineering   — the machine      (gather → act → verify)
4. Loop engineering      — the system       (run → check → decide, có budget + stop rule)
5. Graph engineering     — the organization (nhiều agent chia sẻ state & knowledge)
```

Mỗi tầng bọc tầng trước. **Model là commodity — hệ thống quanh nó mới là chỗ engineering thật.**

### Mỗi kiến trúc externalize một bottleneck khác nhau (Karpathy Loop paper)

| Kiến trúc | Externalize cái gì |
|---|---|
| **Loop** | iteration + evaluation |
| **Chain** | thứ tự task |
| **Swarm** | parallel search + chuyên môn hoá vai |
| **DAG** | lineage thí nghiệm (cái gì thử rồi, từ đâu) |
| **Knowledge graph** | shared facts, provenance, cross-session memory |

### Khi nào dùng Knowledge Graph (decision framework)

- Multi-doc **multi-hop** → KG. Single-doc QA / multi-doc single-hop → RAG (+ rerank) là đủ.
- Agents cần **chain** facts xuyên nguồn, **share** structured state, hoặc **ground** phán xét vào bằng chứng truy vết được → KG.
- Task độc lập, không cần state xuyên session, quan hệ đơn giản → **đừng** thêm graph (chi phí extraction > giá trị traversal).

### Bốn nguyên tắc chất lượng

1. **Descriptions là chìa khoá resolution** — mỗi entity kèm 1 câu mô tả grounded trong tài liệu; thiếu nó resolver chỉ đoán theo tên.
2. **Precision > recall cho extraction** — một entity sai sinh ra các quan hệ sai lan truyền qua multi-hop; entity thiếu chỉ làm graph không đầy đủ.
3. **Provenance trên mọi edge** — mỗi quan hệ truy được về tài liệu nguồn → evaluator fact-check được, không "ước lượng".
4. **Evaluation feedback loop** — gold set + scorer + đổi prompt + xem F1: cùng hình dạng với ratchet loop của autoresearch; không có nó, pipeline drift mà không ai biết.

---

## Checklist tiến độ

- [ ] Đọc 2 PDF trong `docs/` + ảnh 5 layers
- [ ] Định nghĩa Pydantic schema: `Entity(name, type, description)`, `Relation(source, predicate, target)`
- [ ] Viết extraction prompt ("only entities central to the document" — precision-first)
- [ ] Extraction bằng Haiku + structured outputs trên 5–10 tài liệu domain
- [ ] Resolution bằng Sonnet: cluster theo type, dùng descriptions làm ngữ cảnh
- [ ] Assembly: NetworkX MultiDiGraph, edge mang predicate + source_doc
- [ ] Diagnostics: connected components, degree distribution, edges/nodes ratio
- [ ] Query: serialize k-hop subgraph (k=2) → grounded answer có cite edges
- [ ] So sánh grounded vs ungrounded trên 3–5 câu hỏi multi-hop
- [ ] Lập mini gold set + đo precision/recall → tune prompt → đo lại
- [ ] Cắm graph vào workflow Tuần 13 (agent ghi/đọc graph thay vì dồn context)
- [ ] Viết `graph_notes.md`

## 🚀 Bổ sung nâng cao (đưa KG lên quy mô production)

Pipeline bạn build tuần này là notebook-scale (5–10 tài liệu, in-memory). Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **I4** để biết cần gì khi lên hàng nghìn tài liệu:

- **Blocking trước khi resolve** — nhét 10.000 entity vào một prompt là thất bại; gom candidate bằng tín hiệu rẻ (trùng token, embedding) thành block 50–100 rồi mới để model phân xử *trong* block. Pattern chung: **model cho phần cần phán xét, logic tất định cho mọi thứ còn lại.**
- **Incremental update** — resolve tài liệu mới *với canonical set đã có*; re-summarize một entity chỉ khi tập nguồn của nó đổi thật. Graph **tích luỹ**, không rebuild.
- **Storage** — NetworkX ổn tới vài trăm nghìn edge; quá đó dùng Neo4j hoặc 3 bảng Postgres (`entities`/`relations`/`aliases`) + recursive CTE. Code extraction/resolution **không đổi**, chỉ đổi lớp persistence.
- **Chunking tài liệu dài** — cắt theo ranh giới mục/đoạn (semantic), không theo số token, để entity và quan hệ của nó nằm cùng chunk.
- **4 tín hiệu monitoring** + **3 kỷ luật vận hành** (đáng chú ý: *đọc tay 1 node mỗi ngày* — khi bạn không giải thích được vì sao một edge tồn tại, hiểu biết của bạn đã tụt sau graph).
- **Hai failure mode chết người**: *silent entity loss* và *false merge*.

> Nguồn gốc: [`../docs/Graph-Engineering-Athropic-Playbook.pdf`](../docs/Graph-Engineering-Athropic-Playbook.pdf) mục IX & XI + Appendix D.

## 📦 Dữ liệu cho tuần này

Xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md) — mục **1** (nguồn văn bản) và mục **10** (lộ trình theo tuần).

Dùng chính corpus thông tư NHNN đã chuẩn bị ở Tuần 10 làm input cho KG pipeline. Entity types gợi ý cho domain này: `VAN_BAN`, `DIEU_KHOAN`, `TO_CHUC`, `NGHIA_VU`, `KHAI_NIEM`. Predicate: `sửa đổi`, `thay thế`, `căn cứ`, `áp dụng cho`, `bãi bỏ`.

> 💡 Vì sao KG đáng công ở đúng domain này: chuỗi **"văn bản A sửa đổi B, mà B căn cứ C"** là câu hỏi multi-hop mà RAG thuần *không* trả lời được — hai văn bản có thể không hề giống nhau về mặt ngữ nghĩa. Đây là ví dụ sạch nhất của "KG bridges the gap" trong Playbook.

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `kg_pipeline.py` | Skeleton pipeline 4 bước: extract → resolve → assemble → query (TODO) |
| `graph_notes.md` | Template ghi chú diagnostics + eval + grounded-vs-ungrounded (deliverable) |
