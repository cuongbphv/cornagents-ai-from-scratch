# Kiến thức nền tảng (Prerequisites) — chuẩn bị trước khi vào Tuần 1

> **Tuyên bố:** dự án học thuật, nghiên cứu cá nhân, không thương mại hóa. File này chỉ liệt kê nguồn học **mở, license đã xác minh tại ngày tra cứu** (ghi trong bảng §5). Nguồn license non-commercial (CC BY-NC-SA) chỉ dùng **để học qua link**, không sao chép nội dung vào repo. Xem [CLAUDE.md](../CLAUDE.md).

## 1. Cách dùng file này

- **Không học hết file này trước rồi mới bắt đầu.** Roadmap 15 tuần tự dạy lại phần lớn (toán ở Tuần 1, autograd ở Tuần 2...). File này để: (a) tự đánh giá lỗ hổng, (b) biết mở nguồn nào khi hổng đúng chỗ đó, (c) gom các mảng nền (DSA, OCR, big data, design pattern...) không nằm gọn trong tuần nào.
- Ba mức dùng trong bảng:
  - **Bắt buộc** — thiếu là Tuần 1–3 sẽ tắc; kiểm tra bằng checklist §4 trước khi bắt đầu.
  - **Cần trước Tuần X** — có thể học bù ngay trước tuần đó, không cần trước Tuần 1.
  - **Awareness** — chỉ cần hiểu khái niệm và biết công cụ tồn tại; roadmap không yêu cầu thực hành sâu.
- `[Suy luận]` Việc xếp mức "Bắt buộc / Cần / Awareness" là đánh giá của tôi dựa trên nội dung các tuần trong repo này, không phải chuẩn khách quan.

## 2. Bản đồ: mảng nền → tuần nào cần → mức

| Mảng nền | Cần cho | Mức |
|---|---|---|
| Python (hàm, class, list/dict comprehension, virtualenv/pip) | Mọi tuần | **Bắt buộc** |
| Đại số tuyến tính + đạo hàm cơ bản (ma trận, dot product, chain rule) | Tuần 1–3 | **Bắt buộc** (Tuần 1 có ôn lại) |
| Cấu trúc dữ liệu & giải thuật (big-O, hash map, heap, graph traversal, DP) | Xuyên suốt (attention O(n²), BPE merge, beam search, KV cache) | **Bắt buộc** ở mức big-O + hash map; phần còn lại Cần trước Tuần 3 |
| Machine learning cơ bản (train/val/test, overfitting, loss, metrics) | Tuần 5–8 (pretrain, fine-tune, eval) | Cần trước Tuần 5 |
| Data science (NumPy, pandas: load/clean/transform dữ liệu) | Tuần 6, 8, 10 (chuẩn bị dataset, corpus RAG) | Cần trước Tuần 6 |
| DAG — directed acyclic graph | Tuần 2 (autograd = DAG), Tuần 12–13 (LangGraph), Tuần 14 (KG) | Cần trước Tuần 2 (khái niệm) |
| OCR & computer vision cơ bản | Tuần 10 (ingest PDF scan tiếng Việt vào RAG) | Cần trước Tuần 10, mức dùng-công-cụ |
| Big data & data pipeline (Spark, Airflow) | Tuần 5 (hiểu corpus pretrain cỡ FineWeb được xử lý thế nào) | Awareness |
| Design patterns | Tuần 12–13 (thiết kế agent: strategy, observer, pipeline...) | Awareness |
| System design | Tuần 12–15 (kiến trúc CornAgents.AI, tool boundaries, HITL) | Cần trước Tuần 12 |
| Công cụ lập trình (git, shell, debugger) | Mọi tuần | **Bắt buộc** ở mức git + shell cơ bản |

## 3. Chi tiết từng mảng + nguồn mở

### 3.1 Nền CS tổng quát & công cụ

- **OSSU — Open Source Society University** ([github.com/ossu/computer-science](https://github.com/ossu/computer-science), MIT): curriculum CS đầy đủ ghép từ các khóa miễn phí. Dùng làm **bản đồ tra cứu** khi phát hiện hổng mảng nào, không học tuần tự.
- **The Missing Semester of Your CS Education** ([missing.csail.mit.edu](https://missing.csail.mit.edu/), CC BY-NC-SA 4.0 — chỉ học qua link): shell, git, debugging, profiling — đúng các kỹ năng "không ai dạy" mà roadmap này dùng hàng ngày.

Mức đủ dùng: clone/branch/commit/push với git; chạy script, đọc lỗi, kích hoạt virtualenv trong shell.

### 3.2 Cấu trúc dữ liệu, giải thuật & lý thuyết thuật toán

- **_Algorithms_ — Jeff Erickson** ([jeffe.cs.illinois.edu/teaching/algorithms/](https://jeffe.cs.illinois.edu/teaching/algorithms/), CC BY 4.0, PDF miễn phí toàn văn): giáo trình lý thuyết thuật toán mở tốt nhất tôi xác minh được — recursion, DP, graph algorithms, NP-hardness.
- **cp-algorithms** ([cp-algorithms.com](https://cp-algorithms.com/), CC BY-SA 4.0): tra cứu nhanh từng thuật toán kèm code.
- **MIT OCW 6.006 Introduction to Algorithms** ([ocw.mit.edu](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/), CC BY-NC-SA 4.0 — chỉ học qua link): bài giảng video + problem set nếu thích học theo khóa.

Vì sao roadmap cần: độ phức tạp attention là **O(n²·d)** theo sequence length (lý do mọi kỹ thuật KV cache/FlashAttention tồn tại — gặp ở Tuần 3 và appendix nâng cao); **BPE** là thuật toán greedy merge trên bảng tần suất (Tuần 3); **beam search / sampling** là duyệt cây (Tuần 4); hash map là nền của tokenizer vocab và vector store. Mức đủ dùng: ước lượng được big-O của một vòng lặp lồng nhau, dùng thành thạo dict/set/heap trong Python, biết BFS/DFS.

### 3.3 Data science (NumPy, pandas)

- **NumPy user guide** ([numpy.org/doc/stable/](https://numpy.org/doc/stable/)) — đặc biệt phần *broadcasting*: Tuần 1–3 thao tác tensor PyTorch dùng đúng quy tắc này.
- **pandas user guide** ([pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)) — load/filter/groupby/merge để chuẩn bị dataset fine-tune (Tuần 6, 8) và làm sạch corpus RAG (Tuần 10).

Mức đủ dùng: đọc CSV/JSON, lọc và biến đổi cột, xuất JSONL (định dạng dataset fine-tune).

### 3.4 Machine learning cơ bản

- **Dive into Deep Learning (d2l)** ([d2l.ai](https://d2l.ai/), CC BY-SA 4.0): sách mở code-first; các chương đầu (linear regression → MLP → optimization) trùng và bổ trợ trực tiếp cho Tuần 1–2.
- **scikit-learn MOOC (Inria)** ([inria.github.io/scikit-learn-mooc/](https://inria.github.io/scikit-learn-mooc/), CC BY 4.0): train/validation/test, overfitting/underfitting, cross-validation, metrics — nền để đọc hiểu loss curve (Tuần 5) và thiết kế eval (Tuần 8, 11, 15).
- **scikit-learn user guide** ([scikit-learn.org/stable/user_guide.html](https://scikit-learn.org/stable/user_guide.html)): tra cứu metric (precision/recall/F1 — dùng lại nguyên xi khi đo KG ở Tuần 14).

Mức đủ dùng: giải thích được vì sao phải tách held-out set, đọc được một loss curve và chỉ ra overfitting, tính precision/recall bằng tay từ confusion matrix.

### 3.5 OCR & computer vision (phục vụ RAG tiếng Việt — Tuần 10)

Tài liệu nghiệp vụ thực tế thường là **PDF scan**, phải OCR trước khi chunk/embed. Đây là mảng có yếu tố tiếng Việt rõ nhất trong phần nền:

- **Tesseract** ([github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract), Apache-2.0): OCR truyền thống, có traineddata tiếng Việt (`vie`).
- **PaddleOCR** ([github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), Apache-2.0): OCR deep-learning đa ngôn ngữ, có hỗ trợ tiếng Việt.
- **VietOCR** ([github.com/pbcquoc/vietocr](https://github.com/pbcquoc/vietocr), Apache-2.0): model OCR chuyên tiếng Việt (TransformerOCR) — đúng bài toán dấu thanh/mũ mà OCR đa ngôn ngữ hay sai.
- **OpenCV** ([docs.opencv.org](https://docs.opencv.org/), Apache-2.0): tiền xử lý ảnh trước OCR (deskew, threshold, denoise).

`[Suy luận]` Với văn bản tiếng Việt, sai sót OCR ở dấu thanh ("lãi suất" → "lai suat"/"lãi suắt") phá hoại cả BM25 lẫn embedding ở Tuần 10–11, nên bước kiểm tra chất lượng OCR + chuẩn hóa Unicode NFC (xem `Week-10/01_theory_notes.md`) cần đặt trước bước chunk. Mức đủ dùng: chạy được một trong các công cụ trên cho 1 file PDF scan và đánh giá output bằng mắt.

### 3.6 Big data & data pipeline (awareness)

- **Apache Spark docs** ([spark.apache.org/docs/latest/](https://spark.apache.org/docs/latest/), Apache-2.0): hiểu mô hình xử lý phân tán — corpus pretrain cỡ FineWeb (Tuần 5) được lọc/dedup bằng pipeline kiểu này. Roadmap **không** yêu cầu tự chạy Spark.
- **Apache Airflow docs** ([airflow.apache.org/docs/](https://airflow.apache.org/docs/), Apache-2.0): orchestration theo DAG — đọc phần concept về DAG/task/operator là đủ.

Mức đủ dùng: giải thích được vì sao dataset pretrain không xử lý nổi trên 1 máy, và pipeline dữ liệu được mô hình hóa thành DAG như thế nào.

### 3.7 DAG — khái niệm xuyên suốt cả roadmap

Một khái niệm, xuất hiện ít nhất 4 lần với 4 bộ mặt:

| Tuần | DAG xuất hiện dưới dạng |
|---|---|
| 2 | **Computation graph của autograd**: backward = duyệt ngược topological order |
| 5 | Data pipeline lọc corpus (kiểu Airflow/Spark) |
| 12–13 | **Agent graph** (LangGraph): node = agent/tool, edge = luồng điều khiển |
| 14 | Knowledge graph trên **NetworkX** (BSD-3) — lưu ý KG là MultiDiGraph *có thể có chu trình*, không còn là DAG; phần acyclic áp dụng cho pipeline xây nó |

Mức đủ dùng: định nghĩa được DAG, làm topological sort bằng tay trên 5–6 node. Nguồn: **NetworkX docs** ([networkx.org/documentation/stable/](https://networkx.org/documentation/stable/), BSD-3) + phần graph trong sách Erickson (§3.2).

### 3.8 Design patterns & system design (phục vụ Phase 3 — Tuần 12–15)

- **The System Design Primer** ([github.com/donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer), CC BY 4.0): caching, queue, load balancing, trade-off consistency/availability — nền để thiết kế CornAgents.AI có tracing + HITL gate (Tuần 12–15).
- **The Architecture of Open Source Applications** ([aosabook.org](https://aosabook.org/), CC BY 3.0): đọc kiến trúc thật của các hệ mã nguồn mở — cách học system design qua case study.
- **Design patterns (GoF)**: tổng quan từng pattern xem Wikipedia ([Software design pattern](https://en.wikipedia.org/wiki/Software_design_pattern), CC BY-SA 4.0 — dùng ở mức tổng quan). Các pattern gặp lại trong Phase 3: *Strategy* (chọn model/prompt theo route), *Observer* (tracing callback của Langfuse), *Chain of Responsibility* (prompt chaining), *Facade* (tool interface bọc API).
- Lưu ý minh bạch: repo `faif/python-patterns` phổ biến nhưng **không có file LICENSE** (kiểm tra 2026-08-12) → loại theo chính sách nguồn của repo này. Tôi không kiểm chứng được tài liệu design-pattern chuyên sâu nào khác có license mở rõ ràng trong lần tra này.

Mức đủ dùng: nhận ra và gọi tên pattern khi gặp trong code agent framework; system design ở mức vẽ được sơ đồ 1 trang có data flow + failure point (đúng deliverable `03_cornagents_architecture.md` Tuần 12).

## 4. Checklist tự đánh giá trước Tuần 1 (mức Bắt buộc)

- [ ] Viết một class Python có `__init__`/method, dùng list/dict comprehension không cần tra cứu
- [ ] Nhân 2 ma trận bằng tay (2×3 · 3×2) và nói được shape kết quả
- [ ] Phát biểu chain rule và tính đạo hàm f(x) = (2x+1)² bằng nó
- [ ] Ước lượng big-O của một đoạn code 2 vòng lặp lồng nhau
- [ ] Dùng dict/set Python đúng chỗ (tra cứu O(1) thay vì quét list)
- [ ] git: clone, tạo branch, commit, push; shell: chạy script, kích hoạt virtualenv

Hụt ô nào → mở đúng nguồn của mảng đó ở §3, học bù phần đó thôi rồi bắt đầu Tuần 1. Các mảng "Cần trước Tuần X" học bù sát tuần đó; các mảng "Awareness" đọc lướt khi tới tuần liên quan.

## 5. Bảng nguồn tổng hợp (license xác minh ngày 2026-08-12)

| Nguồn | Mảng | License | Cách xác minh |
|---|---|---|---|
| OSSU computer-science | CS tổng quát | MIT | GitHub API |
| Missing Semester (MIT) | Công cụ | CC BY-NC-SA 4.0 *(chỉ học qua link)* | README repo |
| _Algorithms_ — Jeff Erickson | Thuật toán | CC BY 4.0, PDF miễn phí | Trang sách (jeffe.cs.illinois.edu) |
| cp-algorithms | Thuật toán | CC BY-SA 4.0 | GitHub API |
| MIT OCW 6.006 | Thuật toán | CC BY-NC-SA 4.0 *(chỉ học qua link)* | Trang Terms of Use OCW |
| Dive into Deep Learning (d2l-en) | ML | CC BY-SA 4.0 | File LICENSE repo |
| scikit-learn MOOC (Inria) | ML | CC BY 4.0 | GitHub API |
| NumPy / pandas / scikit-learn docs | Data science | Docs chính thức, dự án BSD | Trang docs |
| Tesseract | OCR | Apache-2.0 | GitHub API |
| PaddleOCR | OCR | Apache-2.0 | GitHub API |
| VietOCR (pbcquoc) | OCR tiếng Việt | Apache-2.0 | GitHub API |
| OpenCV | Vision | Apache-2.0 | GitHub API |
| Apache Spark docs | Big data | Apache-2.0 | GitHub API |
| Apache Airflow docs | DAG/pipeline | Apache-2.0 | GitHub API |
| NetworkX docs | Graph | BSD-3 | File LICENSE repo |
| System Design Primer | System design | CC BY 4.0 | File LICENSE repo |
| AOSA (aosabook.org) | System design | CC BY 3.0 | Trang chủ sách |
| Wikipedia (Software design pattern) | Design patterns | CC BY-SA 4.0 | Chân trang Wikipedia |
| underthesea | NLP tiếng Việt (bổ trợ Tuần 10) | Apache-2.0 | GitHub API |

> Nhắc lại quy tắc repo: license là **ảnh chụp tại ngày tra cứu** — trước khi tái sử dụng code/nội dung từ bất kỳ nguồn nào ở trên, kiểm tra lại license tại thời điểm dùng.
