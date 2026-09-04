# Tuần 17, Quiz: Graph Engineering: Knowledge Graph làm shared memory cho multi-agent

> Tự kiểm tra **trước** khi xem solution. Tổng **9** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Bốn stage của knowledge graph pipeline (Anthropic Playbook) theo đúng thứ tự?

- **A.** Querying → Assembly → Resolution → Extraction
- **B.** Embedding → Chunking → Retrieval → Generation
- **C.** Extraction (Haiku, structured outputs) → Resolution (Sonnet, cluster) → Assembly (NetworkX graph) → Querying (subgraph + grounded answer)
- **D.** Extraction → Querying → Resolution → Assembly

## Câu 2 (Tự luận)

RAG và Knowledge Graph khác nhau thế nào, khi nào cần cái nào?

## Câu 3 (Trắc nghiệm)

Vì sao extraction prompt yêu cầu viết 'one-sentence description grounded in this document' cho mỗi entity?

- **A.** Để hiển thị đẹp trong UI
- **B.** Description là tín hiệu ngữ nghĩa cho stage RESOLUTION, thiếu nó resolver chỉ thấy tên và phải đoán; 'Armstrong, phi hành gia' và 'Armstrong, nghệ sĩ jazz' trùng tên nhưng không được merge
- **C.** Để giảm token
- **D.** Để thay thế cho embeddings

## Câu 4 (Trắc nghiệm)

Vì sao với knowledge graph, PRECISION của extraction thường quan trọng hơn RECALL?

- **A.** Vì Haiku không thể đạt recall cao
- **B.** Vì precision rẻ hơn để tính
- **C.** Vì một entity SAI sinh ra các quan hệ sai và lan truyền qua multi-hop reasoning (graph chủ động gây nhiễu), còn entity THIẾU chỉ làm graph không đầy đủ nhưng vẫn đúng
- **D.** Vì recall không đo được

## Câu 5 (Tự luận)

Nêu 3 vai trò của knowledge graph trong kiến trúc multi-agent (theo Playbook).

## Câu 6 (Trắc nghiệm)

'Grounded answer' khác 'ungrounded answer' thế nào khi query graph?

- **A.** Grounded bị ràng buộc 'answer using ONLY the graph, cite edges', trả lời truy vết được về triples có provenance và nói rõ graph KHÔNG chứa gì; ungrounded dựa vào pretraining nên nghe hợp lý nhưng trên private corpus thì không kiểm chứng được
- **B.** Grounded chạy nhanh hơn
- **C.** Ungrounded luôn sai
- **D.** Grounded không cần model

## Câu 7 (Tự luận)

Evaluation feedback loop của KG pipeline hoạt động thế nào và vì sao nó 'cùng hình dạng' với ratchet loop của Karpathy autoresearch?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Playbook Graph Engineering dùng blocking trước resolution. Blocking là gì và nguyên tắc chung nào nó minh họa?

- **A.** Gom ứng viên bằng tín hiệu rẻ (trùng token tên, Jaccard, quy tắc) thành block 50-100 rồi chỉ để model phân xử trong block; nguyên tắc: model cho phần cần phán xét, logic tất định cho phần còn lại
- **B.** Chia tài liệu thành chunk cố định 512 token
- **C.** Chặn model không được đọc tài liệu dài
- **D.** Xóa mọi thực thể xuất hiện một lần

## Nâng cao 2 (Tự luận)

Ma và Tang định nghĩa ma trận kề A ∈ {0,1}^{N×N}. Vì sao knowledge graph của bạn không biểu diễn được bằng một ma trận như vậy, và hệ quả lên precision ở bước extraction là gì?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
