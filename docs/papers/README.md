# Paper shelf — paper mở xếp theo tuần học

> **Nguồn tuyển chọn:** lọc từ 2 repo aggregator license mở — [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) (CC0-1.0) và [itsual/Notable-LLM-Research-Papers](https://github.com/itsual/Notable-LLM-Research-Papers) (MIT) — đối chiếu với lộ trình 15 tuần. License repo và license từng paper kiểm tra ngày **2026-08-12**.
>
> **Quy tắc tải về:** chỉ paper có license **CC BY 4.0 / CC0** (cho phép redistribute) mới được lưu PDF trong thư mục này. Paper mang **arXiv.org perpetual non-exclusive license** không trao quyền redistribute rõ ràng cho bên thứ ba → **chỉ để link**, tự tải về máy khi đọc. Paper CC BY-**NC**-ND bị chính sách repo loại khỏi việc lưu trữ → chỉ link, có nhãn.

## Đã tải về đây (12 PDF, license CC BY 4.0 trừ khi ghi khác)

| File | Paper | Tuần | Vì sao đáng đọc |
|---|---|---|---|
| `1508.07909_*.pdf` | Neural MT of Rare Words with Subword Units (Sennrich 2015) | 3 | Bản gốc của thuật toán BPE mà Tuần 3 bạn tự cài lại. Đọc để thấy nó sinh ra cho bài toán dịch máy gặp từ hiếm — trước cả khi LLM tồn tại — và vì sao ý tưởng "ghép từ mảnh nhỏ" sống dai đến vậy. |
| `2201.11903_*.pdf` | Chain-of-Thought Prompting | 12 | Paper mở màn cho việc bắt model "nghĩ thành lời" trước khi trả lời. Mọi reasoning prompt bạn viết cho agent về sau đều đứng trên vai nó. |
| `2210.03629_*.pdf` | ReAct: Reasoning + Acting | 12 | Đan xen suy luận với hành động gọi tool — chính là agent loop của Tuần 12 ở dạng nguyên thủy. Đọc xong sẽ thấy các SDK agent hiện đại "đóng gói" lại ý tưởng này chứ không phát minh gì mới. |
| `2305.14314_*.pdf` | QLoRA | 8 | Paper gốc của đúng kỹ thuật bạn chạy ở Tuần 8. NF4, double quantization, paged optimizer — đọc trước khi train để log không còn là chữ lạ. |
| `2305.18290_*.pdf` | DPO | 7 | Loss DPO bạn tính tay trong theory notes Tuần 7 được derive từ đầu ở đây. Tựa phụ "Your Language Model is Secretly a Reward Model" tóm tắt cả paper trong một câu. |
| `2309.15217_*.pdf` | RAGAS | 11 | Định nghĩa gốc của 4 metric Tuần 11 dùng để chấm RAG. Chỉ 8 trang — một buổi tối là xong. |
| `2404.16130_*.pdf` | GraphRAG: Local to Global (Microsoft) | 14 | Mở rộng pipeline KG Tuần 14 sang loại câu hỏi mà subgraph k-hop chịu thua: hỏi tổng hợp trên toàn corpus, trả lời bằng tóm tắt theo community. |
| `2405.05904_*.pdf` | Does Fine-Tuning on New Knowledge Encourage Hallucinations? | 6, 10 | Bằng chứng thực nghiệm cho luận điểm xương sống của repo: nhét kiến thức mới qua fine-tune vừa chậm vừa làm model bịa nhiều hơn. Kiến thức quy định để ở RAG/KG. |
| `2405.09673_*.pdf` | LoRA Learns Less and Forgets Less | 8, 9 | Đo đạc cẩn thận trade-off "học ít hơn nhưng quên cũng ít hơn" của LoRA so với full fine-tuning — đúng câu hỏi mà bài kiểm tra song ngữ 10 prompt ở Tuần 9 đặt ra. |
| `2406.12624_*.pdf` (CC0) | Judging the Judges: Evaluating LLMs-as-Judges | 11, 15 | Cho 13 judge model chấm cùng bộ bài rồi so với người chấm: ngay cả judge tốt nhất vẫn lệch đáng kể. Đọc trước khi tin điểm judge trong eval rubric Tuần 15. |
| `2406.17557_*.pdf` | The FineWeb Datasets | 5 | Chính là dataset bạn pretrain ở Tuần 5. Paper kể lại từng quyết định lọc/dedup ở quy mô web — hiếm có chỗ nào tài liệu hóa việc này kỹ như vậy. |
| `2407.01219_*.pdf` | Searching for Best Practices in RAG | 11 | Người ta đã ablate hộ bạn các tổ hợp module RAG (chunking, rerank, hybrid...). Đọc trước khi tự thí nghiệm để đỡ đi lại đường người khác đã đi. |

## Chỉ link (arXiv non-exclusive license — tự tải khi đọc, không lưu vào repo)

| Paper | arXiv | Tuần | Vì sao đáng đọc |
|---|---|---|---|
| Attention Is All You Need | [1706.03762](https://arxiv.org/abs/1706.03762) | 3 | Paper Transformer gốc — Tuần 3 bạn cài lại đúng cơ chế attention mô tả ở đây. |
| Scaling Laws for Neural Language Models | [2001.08361](https://arxiv.org/abs/2001.08361) | 5 | Nơi quan hệ loss ~ compute/data/params được đo lần đầu một cách hệ thống. |
| Training Compute-Optimal LLMs (Chinchilla) | [2203.15556](https://arxiv.org/abs/2203.15556) | 5 | Sửa lại scaling law ở trên: model nhỏ hơn, data nhiều hơn (~20 token/param) — thay đổi cách cả ngành phân bổ compute. |
| InstructGPT | [2203.02155](https://arxiv.org/abs/2203.02155) | 6–7 | Pipeline SFT → RM → PPO nguyên bản mà Tuần 7 vẽ lại — đây là paper biến GPT-3 thành thứ chat được. |
| LoRA | [2106.09685](https://arxiv.org/abs/2106.09685) | 8 | ΔW = BA gốc, đã dẫn trong theory notes Tuần 6 và 8. |
| RAG (Lewis et al. 2020) | [2005.11401](https://arxiv.org/abs/2005.11401) | 10 | Paper đặt ra cái tên RAG và khung retrieve-rồi-generate mà Tuần 10 xây theo. |
| MT-Bench / LLM-as-a-judge | [2306.05685](https://arxiv.org/abs/2306.05685) | 11 | Nơi các thiên vị của LLM judge (độ dài, vị trí, tự khen) được gọi tên — đã dẫn ở Tuần 11. |
| DeepSeekMath (GRPO) | [2402.03300](https://arxiv.org/abs/2402.03300) | 7 | GRPO của Tuần 7 được định nghĩa ở đây, trong bối cảnh dạy model làm toán. |
| DeepSeek-R1 | [2501.12948](https://arxiv.org/abs/2501.12948) | 7 | RLVR chạy ở quy mô thật cho reasoning model. Đọc sau khi đã hiểu GRPO. |
| Instruction Tuning With Loss Over Instructions | [2405.14394](https://arxiv.org/abs/2405.14394) | 6 | Đối chứng thực nghiệm cho prompt masking (`ignore_index=-100`) của Tuần 6, kèm hai ngoại lệ đáng nhớ. |
| Is DPO Superior to PPO for LLM Alignment? | [2404.10719](https://arxiv.org/abs/2404.10719) | 7 | So sánh có kiểm soát, kết quả ngược với cảm nhận phổ biến — thuốc giải cho việc coi "DPO ăn đứt PPO" là chân lý. |
| Tokenization Falling Short | [2406.11687](https://arxiv.org/abs/2406.11687) | 3 | Hệ quả của tokenization kém (lỗi chính tả, cấu trúc trong token) — nối thẳng vào mục BPE tiếng Việt Tuần 3. |
| The Instruction Hierarchy | [2404.13208](https://arxiv.org/abs/2404.13208) | 12–13 | Vì sao tool output phải bị coi là input không đáng tin, và người ta định dạy model ưu tiên instruction theo cấp ra sao. |
| Multi-Agent Collaboration Mechanisms: A Survey | [2501.06322](https://arxiv.org/abs/2501.06322) | 13 | Khung 5 chiều để mô tả một hệ multi-agent — dùng làm checklist khi viết `03_agent_design.md`. |
| Is Cosine-Similarity of Embeddings Really About Similarity? | [2403.05440](https://arxiv.org/abs/2403.05440) | 10 | Phản biện ngắn gọn về metric mặc định của mọi vector store. Đọc để bớt tin công thức, tin eval set hơn. |
| RAG vs Fine-tuning (case study Agriculture) | [2401.08406](https://arxiv.org/abs/2401.08406) — **CC BY-NC-ND, chỉ link** | 6, 10 | So sánh trực diện hai con đường bơm kiến thức domain vào hệ thống — đúng câu hỏi repo này đã chọn phe. |

## Ghi chú

- Bảng **Milestone Papers** trong Awesome-LLM (CC0) là dòng thời gian tốt để đặt các paper trên vào bối cảnh: Transformer (2017) → GPT-2 (2019) → Scaling Laws (2020) → InstructGPT (2022) → LLaMA/DPO (2023) → GRPO/R1 (2024–25). Không cần đọc hết — lộ trình 15 tuần đã chọn sẵn điểm dừng.
- GPT-2 paper ("Language Models are Unsupervised Multitask Learners") không nằm trên arXiv — bản PDF chính thức của OpenAI: [link](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) (chỉ link, không rõ license redistribute).
- Số trong tên file = arXiv ID; version là bản mới nhất tại ngày tải 2026-08-12. Khi trích dẫn, kiểm tra lại version trên arXiv.
