# Nguồn dữ liệu cho CornAgents.AI — Finance Banking, song ngữ VI/EN

> **Tuyên bố:** đây là tài liệu của một **dự án học thuật, nghiên cứu, không thương mại hóa**. Danh sách dưới đây **chỉ gồm dataset/model có license mở đã xác minh** (CC BY / CC0 / MIT / Apache 2.0 / BSD) hoặc nguồn chính phủ. Mọi nguồn thương mại, sau paywall, license non-commercial / research-only / cấm train / cấm distill / cấm redistribute / không xác minh được **đã bị loại khỏi tài liệu này** theo chính sách trong [CLAUDE.md](../CLAUDE.md).
>
> **Tài liệu này neo vào:** Tuần 8 (QLoRA — dataset fine-tune), Tuần 10–11 (RAG — corpus quy định), Tuần 14 (Knowledge Graph — nguồn tài liệu để extract). Xem [`advanced_topics_vi.md`](advanced_topics_vi.md) mục 🧭 để biết cơ chế neo.
>
> **Ngày tra cứu: 2026-08-11.** Mọi dòng có URL đã được fetch và xác nhận truy cập được tại thời điểm đó. Dataset card trên HuggingFace thay đổi liên tục: **kiểm tra lại license trước khi đưa vào pipeline.**

---

## 0. Đọc phần này trước: fine-tune KHÔNG phải cách để model "hiểu quy định"

Đây là quyết định kiến trúc quan trọng nhất của cả dự án, và nó đi ngược trực giác thông thường.

Nếu mục tiêu là "model hiểu Thông tư của NHNN", **fine-tuning là công cụ sai**:

| Vấn đề | Fine-tuning | RAG + Knowledge Graph |
|---|---|---|
| Thông tư mới ban hành / sửa đổi | Kiến thức đóng băng trong weights → phải train lại | Index lại tài liệu, xong trong vài phút |
| Trả lời phải **dẫn nguồn** ("theo Điều 5 Thông tư XX") | Không thể trích dẫn — weights không giữ provenance | Mỗi câu trả lời truy được về đúng điều khoản, đúng tài liệu |
| Rủi ro bịa (hallucination) trong ngành có quy định | Cao, và **không phát hiện được** | Kiểm chứng được: claim nào không có edge/đoạn chống lưng thì bị flag |
| Kiểm toán / giải trình | Gần như không làm được | Đây chính là thiết kế của Tuần 14 (provenance trên mọi edge) |
| Chi phí cập nhật | Một lần train lại mỗi khi luật đổi | Gần như bằng 0 |

**Vậy fine-tune để làm gì?** Những thứ RAG *không* làm được — vì chúng là **hành vi**, không phải **kiến thức**:

- **Định dạng & văn phong đầu ra**: sinh user story + acceptance criteria đúng template của bạn, mỗi lần đều giống nhau.
- **Nhất quán thuật ngữ song ngữ**: cùng một khái niệm nghiệp vụ luôn dịch nhất quán VI↔EN (đây là chỗ fine-tune thắng rõ nhất).
- **Phân loại nghiệp vụ hẹp**: gán nhãn cố định cho một loại văn bản — task lặp lại nhiều, model 7B local rẻ hơn và nhanh hơn gọi API.
- **Giảm "giọng trợ lý AI"**: bớt rào trước rào sau, trả lời trực tiếp theo phong cách tài liệu nội bộ.

> **Kết luận thực dụng:** kiến thức quy định → **RAG (Tuần 10–11) + KG (Tuần 14)**. Hành vi/định dạng/thuật ngữ → **QLoRA (Tuần 8–9)**. Hai nhánh này dùng **hai loại dataset khác nhau**, nên phần dưới chia theo *mục đích*, không chia theo ngôn ngữ.

---

## 1. Tiếng Việt — nguồn quy định & pháp lý (dùng cho RAG + KG, không phải để fine-tune)

| Dataset | URL (đã fetch) | Quy mô | License | Ghi chú |
|---|---|---|---|---|
| **vietnamese-legal-documents** (th1nhng0) | https://huggingface.co/datasets/th1nhng0/vietnamese-legal-documents | 171.556 văn bản + 1,03M dòng quan hệ, 4,37 GB; nguồn = **vbpl.vn** (cổng Bộ Tư pháp); cập nhật 2026-07-23 | **CC BY 4.0** | ⭐ Nguồn tốt nhất cho luật/nghị định/thông tư. vbpl.vn **có mục riêng cho NHNN** (đã xác minh: https://vbpl.vn/nganhangnhanuoc/Pages/vanban.aspx?cqbh=55&dvid=326) nên thông tư NHNN nằm trong bản scrape này — nhưng `[CHƯA XÁC MINH]` ở mức từng dòng dữ liệu, phải tự filter và kiểm tra. |
| **Vietnamese-Legal-Documents** (YuITC) | https://huggingface.co/datasets/YuITC/Vietnamese-Legal-Documents | 119.007 dòng (89,3k train / 29,7k test), 214 MB | **MIT** | Benchmark retrieval (query → văn bản liên quan). Dùng để **đo** retriever của bạn ở Tuần 10–11, không phải làm corpus chính. |

**Nguồn gốc chính thức:** **vbpl.vn** — Cơ sở dữ liệu quốc gia về văn bản pháp luật, do **Bộ Tư pháp** vận hành. Ưu tiên nguồn chính thức này; giữ lại metadata nguồn + ngày hiệu lực của từng văn bản (cần cho provenance ở Tuần 14).

---

## 2. Tiếng Việt — dữ liệu để fine-tune (instruction)

| Dataset | URL | Quy mô | License | Dùng làm gì |
|---|---|---|---|---|
| **vietnamese-legal-instruct** (duyet) | https://huggingface.co/datasets/duyet/vietnamese-legal-instruct | 233.866 dòng / **467.732 cặp instruction**, 14 loại task | **CC BY 4.0** | ⭐ Món quý nhất cho nhánh fine-tune tiếng Việt. Sinh từ chính bản scrape vbpl.vn ở trên: tóm tắt văn bản, phân loại, QA theo chuỗi căn cứ pháp lý, diễn giải sang ngôn ngữ thường. **Dùng làm khuôn mẫu** để tự sinh bộ instruction cho thông tư NHNN. |
| **UTS2017_Bank** | https://huggingface.co/datasets/undertheseanlp/UTS2017_Bank | 2.471 mẫu | **Apache 2.0** | ⭐ Dataset hiếm hoi vừa thực sự về ngân hàng VN vừa có license mở đã xác minh. Phản hồi khách hàng thật, 14 khía cạnh nghiệp vụ + sentiment 3 lớp. Nhỏ nhưng dùng ngay được cho task phân loại. |
| vnpdf-financial-reports-dataset | https://huggingface.co/datasets/kiethuynhanh/vnpdf-financial-reports-dataset | 401 dòng (text + ảnh trang) | **MIT** | Báo cáo tài chính VN dạng PDF — nhỏ, dùng để test pipeline trích xuất tài liệu. |

> ⚠️ **Lưu ý về data sinh từ model đóng:** dataset instruction sinh bằng GPT-4/3.5 (hoặc model đóng khác) thường vướng ToS của nhà cung cấp về việc dùng output để train model khác, độc lập với license dataset. Chính sách repo này: **không dùng**. Tự sinh instruction từ corpus license mở ở mục 1 (dùng `vietnamese-legal-instruct` làm khuôn mẫu).

---

## 3. Tiếng Anh — fine-tune hành vi (license mở đã xác minh)

| Dataset | URL | Quy mô | License | Dùng làm gì |
|---|---|---|---|---|
| **Sujet-Finance-Instruct-177k** | https://huggingface.co/datasets/Sujet-AI/Sujet-Finance-Instruct-177k | 177.597 dòng, 337 MB | **Apache 2.0** | ⭐ Gộp 18 nguồn thành 7 loại task, đã dedup — tương đối sạch và có nhãn task. Lựa chọn mặc định. |
| **finance-alpaca** | https://huggingface.co/datasets/gbharti/finance-alpaca | 68.912 dòng | **MIT** | Định dạng Alpaca, gọn, tốt để khởi động hành vi chat tài chính. |
| **FinGPT** task sets | https://github.com/AI4Finance-Foundation/FinGPT · vd. https://huggingface.co/datasets/flwrlabs/fingpt-sentiment-train | sentiment 76,8k · headline 82,2k · finred 27,6k · fiqa_qa 17,1k | **MIT** | Từng task riêng, định dạng instruction/input/output — dễ trộn chọn lọc. |
| **PIXIU / FIT** | https://github.com/The-FinAI/PIXIU | ~136k mẫu `[suy ra từ repo]` | **MIT** | Bộ instruction đa task đứng sau model FinMA. |
| **BANKING77** | https://huggingface.co/datasets/PolyAI/banking77 | 13.083 câu, **77 nhãn intent** | **CC BY 4.0** | ⭐ Chuẩn mực cho phân loại intent khách hàng ngân hàng. Dùng để train **routing** — đúng một trong 5 workflow patterns ở Tuần 13. |
| Finance-Instruct-500k | https://huggingface.co/datasets/Josephgflowers/Finance-Instruct-500k | 518.185 dòng | **Apache 2.0** | ⚠️ Chính card tự nhận có nhiễu ("malformed portions", PII tổng hợp) → **phải filter**, đừng train thô. |

**Reasoning có dẫn giải** (dùng được cho SFT nhưng **phải tự chuyển** annotation dạng program sang định dạng instruction):

- ConvFinQA — https://github.com/czyssrs/ConvFinQA — 3.037/421/434 hội thoại — **MIT**
- TAT-QA — https://github.com/NExTplusplus/TAT-QA — 16.552 câu hỏi trên bảng+text — **CC BY 4.0**

---

## 4. Đánh giá (held-out)

Nguyên tắc: giữ một phần dữ liệu license mở làm **held-out eval**, không bao giờ đưa vào tập train.

| Dataset | URL | License | Lý do |
|---|---|---|---|
| BizBench (Kensho) | https://huggingface.co/datasets/kensho/bizbench | **Apache 2.0** | Do chuyên gia tài chính curate làm **test set** → giữ làm eval mới có giá trị. |
| Held-out split của các bộ ở mục 2–3 | — | (theo từng bộ) | Tự cắt trước khi train; cố định seed và ghi lại cách cắt. |

> Đây chính là chỗ mục **H** trong appendix (Tuần 8, 11, 15) có ích: đừng tin một chỉ số duy nhất, và cẩn thận cạm bẫy LLM-as-judge.

---

## 5. Corpus lớn cho RAG / continued pretraining

| Nguồn | URL | Quy mô | License | Ghi chú |
|---|---|---|---|---|
| SEC-EDGAR (TeraflopAI) | https://huggingface.co/datasets/TeraflopAI/SEC-EDGAR | 590 GB, ~8,05M filing, 43,7B token | **Apache 2.0** | Corpus tài chính mở lớn nhất đã xác minh. Là **nguồn RAG / pretrain**, không phải instruction data. |
| edgar-corpus (eloukas) | https://huggingface.co/datasets/eloukas/edgar-corpus | 40,7 GB, 1993–2020, chỉ 10-K, đã tách mục | **Apache 2.0** | Sạch hơn, có cấu trúc mục — dễ chunk cho RAG. |

**Khoảng trống thật:** không tìm thấy corpus quy định ngân hàng quốc tế đóng gói sẵn kiểu EDGAR-CORPUS với license mở. Với dự án học thuật này, corpus quy định lấy từ **vbpl.vn / bản scrape CC BY 4.0 ở mục 1** là đủ.

---

## 6. ⚠️ Nguyên tắc pháp lý & license của dự án

### 6.1 Văn bản pháp luật VN

`[Chưa xác minh trên Công báo gốc]` Điều 15 Luật Sở hữu trí tuệ (bản hợp nhất 2025) liệt kê các đối tượng **không được bảo hộ quyền tác giả**, trong đó có văn bản quy phạm pháp luật, văn bản hành chính và bản dịch chính thức của chúng. Trước khi dựa vào điều này cho bất kỳ quyết định nào, **tự đối chiếu văn bản trên nguồn chính thức vbpl.vn** (CSDL quốc gia về văn bản pháp luật, Bộ Tư pháp).

Lưu ý phân biệt: **text gốc của văn bản pháp luật** (thuộc diện Điều 15) khác với **bản biên tập/tổng hợp/dịch của bên thứ ba** — bản sau có thể được bảo hộ riêng và kèm điều khoản dịch vụ. Chính sách repo: **chỉ lấy văn bản pháp luật từ nguồn chính thức (vbpl.vn) hoặc dataset license mở đã xác minh** (mục 1); không thu thập từ aggregator thương mại hay nội dung sau paywall.

### 6.2 Dữ liệu nội bộ / dữ liệu cá nhân

`[Cảnh báo chung, KHÔNG phải tư vấn pháp lý]`

- Dự án này **chỉ dùng dữ liệu công khai license mở**. Không đưa dữ liệu khách hàng, giao dịch, tài liệu nội bộ vào repo, dataset, hay prompt — kể cả khi train local.
- Model đã fine-tune trên dữ liệu thật **có thể nhả lại dữ liệu đó** trong output — đây là lý do nữa để **kiến thức đi qua RAG (đọc lúc chạy, phân quyền được) chứ không nướng vào weights**.

### 6.3 Bảng license các nguồn được dùng trong repo

| Nguồn | License (đã xác minh 2026-08-11) |
|---|---|
| th1nhng0/vietnamese-legal-documents | CC BY 4.0 |
| duyet/vietnamese-legal-instruct | CC BY 4.0 |
| YuITC/Vietnamese-Legal-Documents | MIT |
| UTS2017_Bank | Apache 2.0 |
| Sujet-Finance-Instruct-177k, Finance-Instruct-500k | Apache 2.0 |
| finance-alpaca, FinGPT, PIXIU, ConvFinQA | MIT |
| BANKING77, TAT-QA, MTet | CC BY 4.0 |
| SEC-EDGAR, edgar-corpus, BizBench | Apache 2.0 |

---

## 7. Base model — đừng train from scratch, hãy chọn nền tốt (chỉ license mở)

| Model | License (đã xác minh) | Bằng chứng tiếng Việt | Ghi chú |
|---|---|---|---|
| **Qwen2.5-7B-Instruct** | **Apache 2.0** | Card nêu "29+ ngôn ngữ" gồm tiếng Việt nhưng **không có benchmark riêng cho tiếng Việt** | ⭐ Lựa chọn an toàn nhất về pháp lý. Cũng là base của Fin-R1. |
| **PhoGPT-4B-Chat** (VinAI) | **BSD-3-Clause** | Pretrain from scratch trên 41GB corpus VN | Nhỏ (4B) → chạy thoải mái trên 8GB. VinAI khuyến nghị bản 4B thay cho 7B5. |
| Fin-R1 | **Apache 2.0** | Base Qwen2.5-7B-Instruct, SFT+RL cho reasoning tài chính, song ngữ EN/中文 | Đã tài chính hoá sẵn, nhưng **không có tiếng Việt** — cân nhắc như nguồn tham khảo cách làm. |

**Về VRAM trên 3070 Ti 8GB:** `[CHƯA XÁC MINH bằng nguồn kỹ thuật chính thức]` — thực tế: 7B là **ngưỡng trên** cho card 8GB, batch = 1, seq ngắn, bắt buộc gradient checkpointing. Với Mac 24GB: `[CHƯA XÁC MINH]` số cụ thể — phải tự benchmark. Đây đúng là việc của Tuần 8–9.

---

## 8. Song ngữ VI/EN — nên trộn hay tách?

**Đã có bằng chứng công bố (không phải folklore):**

- Fine-tune model multilingual **chỉ bằng data tiếng Anh** gây **catastrophic forgetting khả năng sinh văn bản ngôn ngữ khác** — hiện tượng có tên, đã công bố (ACL/EMNLP 2022, "Overcoming Catastrophic Forgetting in Zero-Shot Cross-Lingual Generation").
- *"Multilingual Instruction Tuning With Just a Pinch of Multilinguality"*: chỉ **~40 mẫu multilingual** trộn vào tập tiếng Anh đã cải thiện rõ khả năng làm theo instruction đa ngôn ngữ; model train trên hỗn hợp bằng hoặc hơn model train đơn ngữ dù ít data đích hơn nhiều.
- *"Monolingual or Multilingual Instruction Tuning"* (Findings EACL 2024): **dưới LoRA thì trộn multilingual tốt hơn**; dưới full fine-tuning thì kết quả lẫn lộn.

`[Suy luận từ các nghiên cứu liền kề, không phải kết luận đã kiểm chứng cho đúng ca của bạn]` Vì bạn dùng **QLoRA** (adapter-based, giống điều kiện LoRA ở trên), nên **trộn VI + EN trong cùng tập SFT** khả năng cao tốt hơn train riêng từng thứ tiếng, và giảm rủi ro làm hỏng tiếng Anh vốn có. Không tìm thấy nghiên cứu nào cho đúng tổ hợp (VI+EN, QLoRA, domain tài chính) → hãy tự đo.

**Nguồn song ngữ license mở / nguồn công quyền:**

| Nguồn | URL | License | Ghi chú |
|---|---|---|---|
| **MTet** | https://arxiv.org/abs/2210.05610 | **CC BY 4.0** | 4,2M cặp VI-EN đa domain. Nguồn parallel sạch license tốt nhất tìm được. |
| **CFPB Vietnamese-English Glossary of Financial Terms** | https://files.consumerfinance.gov/f/documents/cfpb_adult-fin-ed_vietnamese-style-guide-glossary.pdf | Tác phẩm của cơ quan liên bang Mỹ, công bố 3/2024 — `[CHƯA XÁC MINH]` tuyên bố quyền chính xác | ⭐ **Thuật ngữ tài chính VI-EN chuẩn hoá** — đúng thứ cần cho nhất quán thuật ngữ song ngữ. Là glossary, không phải câu song song. |

**Khoảng trống:** không có corpus song song **tài chính/ngân hàng** VI-EN nào license mở. Thực tế bạn sẽ tự xây từ dữ liệu công khai license mở + CFPB glossary làm xương sống thuật ngữ.

---

## 9. Đánh giá — làm sao biết nó thực sự chạy được tiếng Việt

| Benchmark | URL | Đo gì |
|---|---|---|
| **ViLLM-Eval** | https://arxiv.org/abs/2404.11086 · HF `vlsp-2023-vllm/ViLLM-Eval` | Bộ eval từ shared task VLSP 2023 (paper truy cập mở). |
| **VN-MTEB** | https://arxiv.org/abs/2507.21500 | 41 dataset, 6 loại task **embedding** (retrieval/rerank/clustering/STS) → dùng để chọn embedding model cho RAG ở **Tuần 10–11**, không phải để đo chat model. |

Ngoài ra **tự làm eval set riêng** là bắt buộc: ~50–100 câu hỏi nghiệp vụ, có đáp án đúng kèm điều khoản dẫn nguồn. Không benchmark công khai nào đo được "model trả lời đúng quy định cụ thể hay không". Đây là `02_eval_rubric.md` ở Tuần 15.

---

## 10. Lộ trình thực thi, bám theo tuần

| Tuần | Việc với dữ liệu |
|---|---|
| **8** | Chọn base (Qwen2.5-7B Apache-2.0 nếu ưu tiên pháp lý sạch). Fine-tune thử **hành vi/định dạng**, không nhồi kiến thức: trộn `Sujet-Finance-Instruct-177k` (EN) + `duyet/vietnamese-legal-instruct` (VI) theo tỉ lệ, thêm `UTS2017_Bank` cho task phân loại. Eval bằng held-out riêng + tham chiếu BizBench. |
| **9** | Chạy trên Mac/MLX, so tốc độ; test model đã fine-tune có giữ được tiếng Anh không (kiểm tra catastrophic forgetting). |
| **10** | Corpus RAG từ `th1nhng0/vietnamese-legal-documents`, **filter riêng phần NHNN**. Chọn embedding model theo VN-MTEB. |
| **11** | Đo retrieval bằng `YuITC/Vietnamese-Legal-Documents` + RAGAS; đọc appendix mục **H** về cạm bẫy LLM-as-judge trước khi tin số. |
| **14** | Dùng chính corpus thông tư NHNN làm input cho KG pipeline: extract entity (VĂN BẢN, ĐIỀU KHOẢN, TỔ CHỨC, NGHĨA VỤ...), quan hệ (sửa đổi, thay thế, căn cứ, áp dụng cho). **Chuỗi "văn bản A sửa đổi B, B căn cứ C"** chính là loại câu hỏi multi-hop mà RAG thuần không trả lời được — đây là lý do KG đáng công. |
| **15** | Eval capstone: success rate, human-override rate, **groundedness** (mọi câu trả lời có dẫn được về điều khoản nguồn không). |

---

## 11. Ba việc nên làm trước khi tải bất cứ thứ gì

1. **Kiểm tra lại license tại thời điểm dùng** — dataset card đổi thường xuyên; bảng trên là ảnh chụp ngày 2026-08-11.
2. **Ưu tiên vbpl.vn (nguồn Bộ Tư pháp)** cho text pháp luật, và giữ lại metadata nguồn + ngày hiệu lực của từng văn bản (bạn sẽ cần nó cho provenance ở Tuần 14).
3. **Chỉ dùng dữ liệu công khai license mở** — đây là dự án học thuật; dữ liệu nội bộ hay dữ liệu cá nhân không bao giờ được đưa vào.
