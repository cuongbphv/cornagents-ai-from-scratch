# Kiến thức nền tảng (Prerequisites): chuẩn bị trước khi vào Tuần 1

> Tuyên bố: dự án học thuật, nghiên cứu cá nhân, không thương mại hóa. File này chỉ liệt kê nguồn học **mở, license đã xác minh tại ngày tra cứu** (ghi trong bảng §5). Nguồn license non-commercial (CC BY-NC-SA) chỉ dùng **để học qua link**, không sao chép nội dung vào repo. Xem [CLAUDE.md](../CLAUDE.md).

## 1. Cách dùng file này

- **Không học hết file này trước rồi mới bắt đầu.** Roadmap 18 tuần tự dạy lại phần lớn: toán và lý thuyết học máy ở Tuần 1-3 (Phase 0, trích dẫn sách theo trang trong [`../docs/books/README.md`](../docs/books/README.md)), PyTorch ở Tuần 4, autograd ở Tuần 5. File này để: (a) tự đánh giá lỗ hổng, (b) biết mở nguồn nào khi hổng đúng chỗ đó, (c) gom các mảng nền (DSA, OCR, big data, design pattern...) không nằm gọn trong tuần nào.
- Bảng dùng ba mức. Mức "Bắt buộc" nghĩa là thiếu thì Tuần 1-6 sẽ tắc, nên kiểm tra bằng checklist §4 trước khi bắt đầu. Mức "Cần trước Tuần X" có thể học bù ngay trước tuần đó, không cần trước Tuần 1. Mức "Awareness" chỉ cần hiểu khái niệm và biết công cụ tồn tại; roadmap không yêu cầu thực hành sâu.
- Việc xếp mức "Bắt buộc / Cần / Awareness" là đánh giá của người viết dựa trên nội dung các tuần trong repo này, không phải chuẩn khách quan.

## 2. Bản đồ: mảng nền, tuần nào cần, mức

| Mảng nền | Cần cho | Mức |
|---|---|---|
| Python (hàm, class, list/dict comprehension, virtualenv/pip) | Mọi tuần | **Bắt buộc** |
| Đại số tuyến tính + đạo hàm cơ bản (ma trận, dot product, chain rule) | Tuần 1-2 dạy có hệ thống; dùng từ Tuần 4 | Cần ở mức toán phổ thông; Tuần 1-2 dạy lại đầy đủ; nếu chỉ quên ký hiệu thì bài ôn nhanh [`Week-04/00_math_bridge.md`](../Week-04/00_math_bridge.md) là đủ |
| Cấu trúc dữ liệu & giải thuật (big-O, hash map, heap, graph traversal, DP) | Xuyên suốt (attention O(n²), BPE merge, beam search, KV cache) | **Bắt buộc** ở mức big-O + hash map; phần còn lại Cần trước Tuần 6 |
| Machine learning cơ bản (train/val/test, overfitting, loss, metrics) | Tuần 3 dạy có hệ thống; dùng ở Tuần 8-11 (pretrain, fine-tune, eval) | Tuần 3 dạy lại đầy đủ |
| Data science (NumPy, pandas: load/clean/transform dữ liệu) | Tuần 9, 11, 13 (chuẩn bị dataset, corpus RAG) | Cần trước Tuần 9 |
| DAG, directed acyclic graph | Tuần 5 (autograd = DAG), Tuần 15-16 (LangGraph), Tuần 17 (KG) | Cần trước Tuần 5 (khái niệm) |
| OCR & computer vision cơ bản | Tuần 13 (ingest PDF scan tiếng Việt vào RAG) | Cần trước Tuần 13, mức dùng-công-cụ |
| Big data & data pipeline (Spark, Airflow) | Tuần 8 (hiểu corpus pretrain cỡ FineWeb được xử lý thế nào) | Awareness |
| Design patterns | Tuần 15-16 (thiết kế agent: strategy, observer, pipeline...) | Awareness |
| System design | Tuần 15-18 (kiến trúc CornAgents.AI, tool boundaries, HITL) | Cần trước Tuần 15 |
| Công cụ lập trình (git, shell, debugger) | Mọi tuần | **Bắt buộc** ở mức git + shell cơ bản |

## 3. Chi tiết từng mảng + nguồn mở

### 3.1 Nền CS tổng quát & công cụ

- **OSSU, Open Source Society University** ([github.com/ossu/computer-science](https://github.com/ossu/computer-science), MIT): curriculum CS đầy đủ ghép từ các khóa miễn phí. Dùng làm **bản đồ tra cứu** khi phát hiện hổng mảng nào, không học tuần tự.
- **The Missing Semester of Your CS Education** ([missing.csail.mit.edu](https://missing.csail.mit.edu/), CC BY-NC-SA 4.0, chỉ học qua link): shell, git, debugging, profiling, đúng các kỹ năng "không ai dạy" mà roadmap này dùng hàng ngày.

Mức đủ dùng: clone/branch/commit/push với git; chạy script, đọc lỗi, kích hoạt virtualenv trong shell.

### 3.2 Cấu trúc dữ liệu, giải thuật & lý thuyết thuật toán

- **_Algorithms_, Jeff Erickson** ([jeffe.cs.illinois.edu/teaching/algorithms/](https://jeffe.cs.illinois.edu/teaching/algorithms/), CC BY 4.0, PDF miễn phí toàn văn): giáo trình lý thuyết thuật toán mở tốt nhất tôi xác minh được, recursion, DP, graph algorithms, NP-hardness.
- **cp-algorithms** ([cp-algorithms.com](https://cp-algorithms.com/), CC BY-SA 4.0): tra cứu nhanh từng thuật toán kèm code.
- **MIT OCW 6.006 Introduction to Algorithms** ([ocw.mit.edu](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/), CC BY-NC-SA 4.0, chỉ học qua link): bài giảng video + problem set nếu thích học theo khóa.

Vì sao roadmap cần: độ phức tạp attention là **O(n²·d)** theo sequence length (lý do mọi kỹ thuật KV cache/FlashAttention tồn tại, gặp ở Tuần 6 và appendix nâng cao); **BPE** là thuật toán greedy merge trên bảng tần suất (Tuần 6); **beam search / sampling** là duyệt cây (Tuần 7); hash map là nền của tokenizer vocab và vector store. Mức đủ dùng: ước lượng được big-O của một vòng lặp lồng nhau, dùng thành thạo dict/set/heap trong Python, biết BFS/DFS.

### 3.3 Data science (NumPy, pandas)

- **NumPy user guide** ([numpy.org/doc/stable/](https://numpy.org/doc/stable/)): đặc biệt phần *broadcasting*: Tuần 4-6 thao tác tensor PyTorch dùng đúng quy tắc này.
- **pandas user guide** ([pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)): load/filter/groupby/merge để chuẩn bị dataset fine-tune (Tuần 9, 11) và làm sạch corpus RAG (Tuần 13).

Mức đủ dùng: đọc CSV/JSON, lọc và biến đổi cột, xuất JSONL (định dạng dataset fine-tune).

### 3.4 Machine learning cơ bản

- **Dive into Deep Learning (d2l)** ([d2l.ai](https://d2l.ai/), CC BY-SA 4.0): sách mở code-first; các chương đầu (linear regression, rồi MLP, rồi optimization) trùng và bổ trợ trực tiếp cho Tuần 3-5.
- **scikit-learn MOOC (Inria)** ([inria.github.io/scikit-learn-mooc/](https://inria.github.io/scikit-learn-mooc/), CC BY 4.0): train/validation/test, overfitting/underfitting, cross-validation, metrics, nền để đọc hiểu loss curve (Tuần 8) và thiết kế eval (Tuần 11, 14, 18).
- **scikit-learn user guide** ([scikit-learn.org/stable/user_guide.html](https://scikit-learn.org/stable/user_guide.html)): tra cứu metric (precision/recall/F1, dùng lại nguyên xi khi đo KG ở Tuần 17).

Mức đủ dùng: giải thích được vì sao phải tách held-out set, đọc được một loss curve và chỉ ra overfitting, tính precision/recall bằng tay từ confusion matrix.

### 3.5 OCR & computer vision (phục vụ RAG tiếng Việt: Tuần 13)

Tài liệu nghiệp vụ thực tế thường là **PDF scan**, phải OCR trước khi chunk/embed. Đây là mảng có yếu tố tiếng Việt rõ nhất trong phần nền:

- **Tesseract** ([github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract), Apache-2.0): OCR truyền thống, có traineddata tiếng Việt (`vie`).
- **PaddleOCR** ([github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), Apache-2.0): OCR deep-learning đa ngôn ngữ, có hỗ trợ tiếng Việt.
- **VietOCR** ([github.com/pbcquoc/vietocr](https://github.com/pbcquoc/vietocr), Apache-2.0): model OCR chuyên tiếng Việt (TransformerOCR): đúng bài toán dấu thanh/mũ mà OCR đa ngôn ngữ hay sai.
- **OpenCV** ([docs.opencv.org](https://docs.opencv.org/), Apache-2.0): tiền xử lý ảnh trước OCR (deskew, threshold, denoise).

Với văn bản tiếng Việt, sai sót OCR ở dấu thanh ("lãi suất" thành "lai suat" hoặc "lãi suắt") làm hỏng cả BM25 lẫn embedding ở Tuần 13-14: BM25 chỉ khớp khi từ trùng đúng chính tả ("they work only if there is exact overlap of words between the query and document", SLP3 mục 11.3, trang 264), còn tokenizer của model embedding cắt từ sai dấu thành những mảnh khác hẳn; nên bước kiểm tra chất lượng OCR + chuẩn hóa Unicode NFC (xem `Week-13/01_theory_notes.md`) cần đặt trước bước chunk. Mức đủ dùng: chạy được một trong các công cụ trên cho 1 file PDF scan và đánh giá output bằng mắt.

### 3.6 Big data & data pipeline (awareness)

- **Apache Spark docs** ([spark.apache.org/docs/latest/](https://spark.apache.org/docs/latest/), Apache-2.0): hiểu mô hình xử lý phân tán, corpus pretrain cỡ FineWeb (Tuần 8) được lọc/dedup bằng pipeline kiểu này. Roadmap **không** yêu cầu tự chạy Spark.
- **Apache Airflow docs** ([airflow.apache.org/docs/](https://airflow.apache.org/docs/), Apache-2.0): orchestration theo DAG, đọc phần concept về DAG/task/operator là đủ.

Mức đủ dùng: giải thích được vì sao dataset pretrain không xử lý nổi trên 1 máy, và pipeline dữ liệu được mô hình hóa thành DAG như thế nào.

### 3.7 DAG: khái niệm xuyên suốt cả roadmap

Một khái niệm, xuất hiện ít nhất 4 lần với 4 bộ mặt:

| Tuần | DAG xuất hiện dưới dạng |
|---|---|
| 2 | **Computation graph của autograd**: backward = duyệt ngược topological order |
| 5 | Data pipeline lọc corpus (kiểu Airflow/Spark) |
| 12-13 | **Agent graph** (LangGraph): node = agent/tool, edge = luồng điều khiển |
| 14 | Knowledge graph trên **NetworkX** (BSD-3): lưu ý KG là MultiDiGraph *có thể có chu trình*, không còn là DAG; phần acyclic áp dụng cho pipeline xây nó |

Mức đủ dùng: định nghĩa được DAG, làm topological sort bằng tay trên 5-6 node. Nguồn: **NetworkX docs** ([networkx.org/documentation/stable/](https://networkx.org/documentation/stable/), BSD-3) + phần graph trong sách Erickson (§3.2).

### 3.8 Design patterns & system design (phục vụ Phase 3: Tuần 15-18)

- **The System Design Primer** ([github.com/donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer), CC BY 4.0): caching, queue, load balancing, trade-off consistency/availability, nền để thiết kế CornAgents.AI có tracing + HITL gate (Tuần 15-18).
- **The Architecture of Open Source Applications** ([aosabook.org](https://aosabook.org/), CC BY 3.0): đọc kiến trúc thật của các hệ mã nguồn mở, cách học system design qua case study.
- Tổng quan từng design pattern (GoF) xem Wikipedia ([Software design pattern](https://en.wikipedia.org/wiki/Software_design_pattern), CC BY-SA 4.0, dùng ở mức tổng quan). Các pattern gặp lại trong Phase 3: *Strategy* (chọn model/prompt theo route), *Observer* (tracing callback của Langfuse), *Chain of Responsibility* (prompt chaining), *Facade* (tool interface bọc API).
- Lưu ý minh bạch: repo `faif/python-patterns` phổ biến nhưng **không có file LICENSE** (kiểm tra 2026-08-12), nên bị loại theo chính sách nguồn của repo này. Tôi không kiểm chứng được tài liệu design-pattern chuyên sâu nào khác có license mở rõ ràng trong lần tra này.

Mức đủ dùng: nhận ra và gọi tên pattern khi gặp trong code agent framework; system design ở mức vẽ được sơ đồ 1 trang có data flow + failure point (đúng deliverable `03_cornagents_architecture.md` Tuần 15).

## 4. Checklist tự đánh giá trước Tuần 1 (mức Bắt buộc)

- [ ] Viết một class Python có `__init__`/method, dùng list/dict comprehension không cần tra cứu
- [ ] Nhân 2 ma trận bằng tay (2×3 · 3×2) và nói được shape kết quả
- [ ] Phát biểu chain rule và tính đạo hàm f(x) = (2x+1)² bằng nó
- [ ] Ước lượng big-O của một đoạn code 2 vòng lặp lồng nhau
- [ ] Dùng dict/set Python đúng chỗ (tra cứu O(1) thay vì quét list)
- [ ] git: clone, tạo branch, commit, push; shell: chạy script, kích hoạt virtualenv

Hụt ô nào thì mở đúng nguồn của mảng đó ở §3, học bù phần đó thôi rồi bắt đầu Tuần 1. Các mảng "Cần trước Tuần X" học bù sát tuần đó; các mảng "Awareness" đọc lướt khi tới tuần liên quan.

Nếu hụt ở ô toán mà đã học xong Tuần 1-3, mở [`../Week-04/00_math_bridge.md`](../Week-04/00_math_bridge.md) để ôn lại ký hiệu, log, exp và nhân ma trận tay trước khi vào `02_theory_notes.md` của Tuần 4.

## 5. Bảng nguồn tổng hợp (license xác minh ngày 2026-08-12)

| Nguồn | Mảng | License | Cách xác minh |
|---|---|---|---|
| OSSU computer-science | CS tổng quát | MIT | GitHub API |
| Missing Semester (MIT) | Công cụ | CC BY-NC-SA 4.0 *(chỉ học qua link)* | README repo |
| _Algorithms_, Jeff Erickson | Thuật toán | CC BY 4.0, PDF miễn phí | Trang sách (jeffe.cs.illinois.edu) |
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
| underthesea | NLP tiếng Việt (bổ trợ Tuần 13) | Apache-2.0 | GitHub API |

> Nhắc lại quy tắc repo: license là **ảnh chụp tại ngày tra cứu**: trước khi tái sử dụng code/nội dung từ bất kỳ nguồn nào ở trên, kiểm tra lại license tại thời điểm dùng.
