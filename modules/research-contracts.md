# Nghiên cứu và CornLoop

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s1"></a>

## 1. Định hướng thiết kế CornAgents.AI

### 1.1. Giữ nền “from scratch”, mở rộng đích đến

lịch rút gọn đi từ kiến thức mô hình tới hệ thống có kiểm thử. chương trình bổ sung khả năng **cải tiến có kiểm soát qua nhiều phiên**. Không bỏ toán, Transformer, dữ liệu, retrieval và kỹ thuật hệ thống để thay bằng một danh sách framework tự động hóa.

| Khía cạnh | Giữ từ lịch rút gọn | Bổ sung trong chương trình |
|---|---|---|
| Nền tảng | Toán, tự triển khai phần lõi, tiny model, SFT/LoRA, RAG | Phân biệt học trong context, học bộ nhớ, học kỹ năng và học trọng số |
| Agent | Typed tools, policy gate, checkpoint | Research contract, experiment protocol, quyền tự chủ có thời hạn |
| Bộ nhớ | Nguồn, thời gian, quyền đọc | Quarantine, kiểm chứng bài học, phản ví dụ, thu hồi dữ liệu dẫn xuất |
| Evaluation | Outcome, citation, recovery, cost | Risk–coverage, cận thống kê, kiểm soát thử nhiều ứng viên, giữ kín test |
| Cải tiến | Đề xuất của người phát triển | Agent tạo candidate; evaluator độc lập; người có thẩm quyền quyết định phát hành |
| Học tập | AI-off và AI-on | Bảo vệ một cải tiến có thể bác bỏ và tái lập |
| Capstone | Workflow tiếng Việt có bằng chứng | Nhiều chu kỳ nghiên cứu–học, có đo chuyển giao và quên kiến thức cũ |
| Bản sắc | Hiểu thật và kiểm được | Học được điều mới mà không tự nới quyền hoặc tự hạ chuẩn |

Những lỗi học thuật lịch rút gọn đã chỉ ra vẫn phải sửa: validation khác test; DPO không bắt buộc có reward model riêng; RAG không mặc định chỉ single-hop; chỉ số cấu trúc graph không phải chuẩn chất lượng phổ quát; bộ nhớ GPU không chỉ là weights. chương trình không lặp lại toàn bộ audit đó và không coi các sửa đổi đã được commit. Repository công khai là đầu vào tham khảo, không phải snapshot đã pin SHA trong tài liệu này. [S28]

### 1.2. Điều làm CornAgents có bản sắc

Đề xuất xây một **AI research engineering apprentice**: trợ lý nghiên cứu kỹ thuật có khả năng cải tiến các tác vụ hẹp bằng thí nghiệm, phù hợp kinh nghiệm backend/DevOps và hệ thống doanh nghiệp của người xây chương trình.

Thành phẩm không chỉ là câu trả lời. Mỗi lần làm việc nên tạo được:

- **Báo cáo có bằng chứng:** điều đã biết, điều chưa biết, phản chứng và phạm vi kết luận.
- **Thí nghiệm có thể chạy lại:** cấu hình, dữ liệu, kết quả, lỗi và chi phí.
- **Đề xuất học có thể duyệt:** fact, lesson, skill, prompt, retrieval config hoặc adapter mới.

Tài sản riêng tích lũy qua thời gian là bộ dữ liệu tiếng Việt có quyền sử dụng, lỗi được gán nhãn, evaluator, biến thể kiểm tra chuyển giao và báo cáo nghiên cứu âm. Một tên mới hoặc nhiều agent không đủ tạo bản sắc.

### 1.3. Những mục tiêu không đặt ra

Không cam kết AGI, tự nghiên cứu mọi ngành, không bao giờ hallucinate hoặc tự cải tiến vô hạn. Không tự giao dịch tài chính thật, tự triển khai vào production ngân hàng, tự mua tài nguyên không hạn mức, hay tự thay đổi chính sách quyền.

Giới hạn này không cản trở nghiên cứu mới: agent vẫn được đề xuất thuật toán và thực hiện thí nghiệm trong phạm vi đã duyệt. **Kết quả âm hợp lệ là một đóng góp; không có áp lực phải báo “đã cải thiện” sau mọi vòng chạy.**

---

<a id="s2"></a>

## 2. Tự nghiên cứu và tự học nghĩa là gì?

### 2.1. Không đồng nhất model, harness và hệ thống

Một LLM tạo dự đoán từ input/context. Một agent harness quản lý trạng thái, gọi model, gọi tool và chuyển kết quả lại. Một hệ thống nghiên cứu đầy đủ còn cần nguồn dữ liệu, môi trường thực nghiệm, evaluator và cơ chế kiểm soát. Các công bố Deep Research và nghiên cứu multi-agent minh họa việc kết hợp nhiều bước với công cụ; chúng không công khai toàn bộ chi tiết nội bộ để người ngoài suy ra một bản triển khai chính xác. [S01] [S02] [S27]

Vì vậy, chương trình học **nguyên lý có thể tái lập**, không tự nhận sao chép nội bộ OpenAI hoặc Anthropic.

### 2.2. Năm mức “học” cần gọi đúng tên

| Mức | Đối tượng thực sự thay đổi | Ví dụ | Điều không được suy ra |
|---|---|---|---|
| L0 — thích nghi trong phiên | Context và trạng thái | Đọc lỗi compiler rồi sửa lời giải | Weights đã học một kiến thức mới |
| L1 — học bộ nhớ | Kho fact/episode/lesson có version | Lưu bài học có điều kiện và bằng chứng | Mọi điều model ghi lại đều đúng |
| L2 — học kỹ năng | Prompt, skill, parser, retrieval policy | Chọn prompt candidate qua eval | Điểm validation tăng thì chắc chắn generalize |
| L3 — học tham số | Adapter hoặc weights qua training offline | SFT/LoRA; DPO cho preference đúng mục tiêu | Có thể fine-tune ngay từ output tự sinh chưa kiểm |
| L4 — cải tiến harness trong phòng thí nghiệm | Code/cấu trúc điều phối cho phép sửa | Thử chiến lược search hoặc scheduler mới | Có quyền sửa policy, evaluator hay release service |

Reflexion là ví dụ rõ của phản hồi ngôn ngữ và episodic memory, không phải cập nhật weights. GEPA là ví dụ tối ưu prompt bằng phản hồi và tìm kiếm ứng viên. DPO thuộc nhóm tối ưu theo preference ở tầng model. Ba nhóm này có cơ chế và cách đánh giá khác nhau. [S04] [S07] [S16]

**Mặc định của core chương trình:** L0–L2. L3 là nhánh được duyệt riêng, có dữ liệu và tài nguyên; L4 chỉ trong sandbox với vùng sửa code giới hạn.

### 2.3. Bốn năng lực nghiên cứu phải tách

**Tổng hợp tri thức:** tìm và đối chiếu nguồn để trả lời điều đã có bằng chứng.

**Tái lập:** chạy lại một kết quả trong phạm vi nguồn lực và cấu hình được công bố.

**Nghiên cứu thực nghiệm:** tạo giả thuyết, baseline, thay đổi có kiểm soát và kiểm tra trên dữ liệu chưa dùng để tối ưu.

**Tự cải tiến:** biến một phát hiện đã kiểm tra thành candidate cho những tác vụ về sau.

Một báo cáo dài có citations có thể chỉ đạt năng lực thứ nhất. Một pipeline tự sinh paper không tự chứng minh đóng góp đúng hoặc mới. AI Scientist, AlphaEvolve và Darwin Gödel Machine cung cấp những hướng tham khảo khác nhau; kết quả trong miền có evaluator cụ thể không bảo đảm đúng trên mọi câu hỏi nghiên cứu mở. [S09] [S10] [S11]

### 2.4. Quyền tự chủ không phải điểm IQ của agent

| Chế độ vận hành đề xuất | Được làm | Điểm dừng bắt buộc |
|---|---|---|
| A0 — read-only | Đọc nguồn công khai/được cấp quyền, viết báo cáo | Không side effect nghiệp vụ |
| A1 — sandbox | Chạy code/thí nghiệm trong workspace cách ly | Không secret thật, không ghi ra hệ thống ngoài |
| A2 — propose | Tạo lesson/skill/patch candidate | Chưa vào memory/registry đang phục vụ |
| A3 — shadow | Chạy cạnh bản đang dùng với dữ liệu đã cho phép | Không tác động quyết định thực tế |
| A4 — bounded operation | Thực hiện thao tác đã duyệt, có thể kiểm soát và giới hạn | Quyền hết hạn, budget hết, drift hoặc cảnh báo → dừng |

Không mở A4 chỉ vì accuracy vượt một ngưỡng. Cần chủ thể cấp quyền, phạm vi, mức tác động, giới hạn tài nguyên và cơ chế thu hồi riêng. Trong lộ trình người mới, A0–A3 là đủ để tốt nghiệp.

---

<a id="s3"></a>

## 3. CornLoop: ba vòng lặp, ba cửa kiểm soát

### 3.1. Vòng nhanh — nghiên cứu một nhiệm vụ

```text
Research contract
  -> tách câu hỏi và điều chưa biết
  -> tìm nguồn / quan sát môi trường
  -> lập bảng claim–evidence–counterevidence
  -> đề xuất giả thuyết hoặc lời giải
  -> chạy phép kiểm / thí nghiệm được phép
  -> cập nhật kết luận theo kết quả
  -> báo cáo, hỏi người hoặc dừng theo budget
```

Contract phải xác định câu hỏi, miền, thời gian của dữ liệu, công cụ được phép, nguồn bị loại, ngân sách và tiêu chí hoàn thành. Không cho agent tự mở rộng thành một nhiệm vụ khác chỉ vì tìm được điều thú vị.

**Stop rule khởi đầu:** hết budget; không có quyền; không còn phép kiểm hợp lệ; đã có bằng chứng đủ theo contract; hoặc hai vòng phát triển liên tiếp không tạo thêm bằng chứng liên quan. “Hai vòng” là tham số thí nghiệm, không phải định luật tối ưu. Nếu dừng do thiếu bằng chứng, report phải ghi incomplete/uncertain chứ không chuyển thành successful.

### 3.2. Vòng chậm — học để tốt hơn ở nhiệm vụ sau

```text
Trace + kết quả thật + failure taxonomy
  -> đề xuất một bài học có điều kiện
  -> quarantine
  -> tạo candidate memory / skill / config / adapter
  -> development eval và phản ví dụ
  -> đóng băng candidate digest
  -> đánh giá độc lập trên tập chưa dùng để tối ưu
  -> quyết định promote / reject / cần thêm bằng chứng
  -> shadow, canary có giới hạn, theo dõi và rollback
```

Một failure không tự động sinh một “quy tắc đúng”. Ví dụ lỗi truy vấn do thiếu index không có nghĩa “luôn thêm index vào mọi cột”. Lesson phải ghi rõ điều kiện, chi phí và trường hợp không nên áp dụng.

### 3.3. Vòng kiểm soát — luôn ở ngoài hai vòng trên

Supervisor kiểm tra quyền, thời hạn, budget, trạng thái tiến trình, danh tính phiên bản, egress và release policy. Nó phải dừng được worker khi model im lặng, bị treo hoặc không tuân thủ hướng dẫn. Đây là thiết kế kiểm soát của chương trình, không phải chỉ thêm một “safety agent” cùng quyền với worker.

Dữ liệu ngoài và tool output được xem như input không đáng tin. Sandboxing, phạm vi truy cập và policy enforcement là biên bảo vệ; phản hồi của model hoặc một classifier không được là biên duy nhất. [S20] [S21]

### 3.4. Ba cửa khác nhau, không bù điểm cho nhau

| Cửa | Chủ thể được đánh giá | Câu hỏi |
|---|---|---|
| G1 — AI-off | Người học | Có tự giải thích, triển khai phần lõi và sửa lỗi mới không? |
| G2 — AI-on | Hệ thống | Có hoàn thành tác vụ đúng, có bằng chứng và đúng phạm vi không? |
| G3 — change gate | Bản cải tiến | Có đủ bằng chứng để thay bản đang dùng, không phá khả năng cũ và không nới quyền không? |

Ví dụ, model mới viết báo cáo hay hơn nhưng gọi thêm nguồn ngoài allowlist: G2/G3 không đạt. Sinh artifact tốt nhờ AI nhưng không giải thích được leakage: G1 không đạt. Candidate không thắng baseline nhưng thí nghiệm được thiết kế và báo cáo đúng vẫn có thể đạt môn nghiên cứu; nó chỉ không được promote.

### 3.5. Dạng tối ưu hóa có ràng buộc

Gọi `c` là một candidate. Đề xuất lựa chọn theo mục tiêu đo được:

\[
\max_c\;\text{VerifiedTaskUtility}(c)
\]

với các ràng buộc đã đặt trước về ngân sách, mức lỗi chấp nhận, khả năng cũ, nguồn dữ liệu và quyền thực thi. Các kiểm tra quyền/cách ly là **điều kiện loại**, không cộng chung thành một điểm để chất lượng cao bù cho vi phạm nghiêm trọng.

Hàm utility và trọng số cho chất lượng, độ trễ, người sửa phải công bố trước. Không gọi đây là một định lý bảo đảm an toàn; đây là khung ra quyết định để triển khai và kiểm chứng.

---

[S01]: https://openai.com/index/introducing-deep-research/
[S02]: https://www.anthropic.com/engineering/multi-agent-research-system
[S03]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
[S04]: https://arxiv.org/abs/2303.11366v4
[S05]: https://arxiv.org/abs/2210.03629
[S06]: https://arxiv.org/abs/2310.11511
[S07]: https://arxiv.org/abs/2507.19457
[S08]: https://github.com/stanfordnlp/dspy
[S09]: https://arxiv.org/abs/2408.06292
[S10]: https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
[S11]: https://arxiv.org/abs/2505.22954
[S12]: https://arxiv.org/abs/1706.04599
[S13]: https://arxiv.org/abs/2110.01052
[S14]: https://arxiv.org/abs/2208.02814
[S15]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html
[S16]: https://arxiv.org/abs/2305.18290
[S17]: https://arxiv.org/abs/2402.03300
[S18]: https://arxiv.org/abs/2305.17493
[S19]: https://arxiv.org/abs/1807.02811
[S20]: https://www.anthropic.com/engineering/how-we-contain-claude
[S21]: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
[S22]: https://docs.langchain.com/oss/python/langgraph/persistence
[S23]: https://www.anthropic.com/research/multiagent-systems
[S24]: https://arxiv.org/abs/2203.11171
[S25]: https://openai.com/index/devday-2026-recap/
[S26]: https://github.com/gepa-ai/gepa
[S27]: https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt
[S28]: https://github.com/cuongbphv/cornagents-ai-from-scratch
