# Nguồn dữ liệu cho CornAgents.AI — Finance Banking, song ngữ VI/EN

> **Tài liệu này neo vào:** Tuần 8 (QLoRA — dataset fine-tune), Tuần 10–11 (RAG — corpus quy định), Tuần 14 (Knowledge Graph — nguồn tài liệu để extract). Xem [`advanced_topics_vi.md`](advanced_topics_vi.md) mục 🧭 để biết cơ chế neo.
>
> **Ngày tra cứu: 2026-08-11.** Mọi dòng có URL đã được fetch và xác nhận truy cập được tại thời điểm đó. Các mục ghi `[CHƯA XÁC MINH]` là thứ **không** kiểm chứng được — đừng dựa vào chúng khi ra quyết định. Dataset card trên HuggingFace thay đổi liên tục: **kiểm tra lại license trước khi đưa vào pipeline.**

---

## 0. Đọc phần này trước: fine-tune KHÔNG phải cách để model "hiểu quy định"

Đây là quyết định kiến trúc quan trọng nhất của cả dự án, và nó đi ngược trực giác thông thường.

Nếu mục tiêu là "model hiểu Thông tư của NHNN", **fine-tuning là công cụ sai**:

| Vấn đề | Fine-tuning | RAG + Knowledge Graph |
|---|---|---|
| Thông tư mới ban hành / sửa đổi | Kiến thức đóng băng trong weights → phải train lại | Index lại tài liệu, xong trong vài phút |
| Trả lời phải **dẫn nguồn** ("theo Điều 5 Thông tư XX") | Không thể trích dẫn — weights không giữ provenance | Mỗi câu trả lời truy được về đúng điều khoản, đúng tài liệu |
| Rủi ro bịa (hallucination) trong ngành có quy định | Cao, và **không phát hiện được** | Kiểm chứng được: claim nào không có edge/đoạn chống lưng thì bị flag |
| Kiểm toán / giải trình với compliance | Gần như không làm được | Đây chính là thiết kế của Tuần 14 (provenance trên mọi edge) |
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
| **zalo-ai-legal-text-retrieval-vn** | https://huggingface.co/datasets/GreenNode/zalo-ai-legal-text-retrieval-vn | 788 query, 60.701 văn bản | MIT (trên bản mirror) | ⚠️ License MIT là của bản mirror; **điều khoản gốc của Zalo AI Challenge 2021 `[CHƯA XÁC MINH]`** — repo gốc không có file license. Cẩn thận nếu dùng thương mại. |
| VLQA (arXiv 2507.19995) | https://arxiv.org/html/2507.19995v1 | 3.129 câu hỏi chuyên gia, 59.636 điều khoản, 27 lĩnh vực — **trong đó "Tiền tệ và Ngân hàng" 2.475 điều, "Tài chính công" 1.966 điều** | Chưa nêu | ⚠️ **Chưa tồn tại để tải.** Paper nói "will publicly release" nhưng không tìm được link. Đúng scope banking nhất trong tất cả — theo dõi, đừng lên kế hoạch dựa vào nó. |
| vietnamese-legal-documents (pdt590) | https://huggingface.co/datasets/pdt590/vietnamese-legal-documents | 518.255 văn bản, ~3,6 GB; nguồn = thuvienphapluat.vn | Card ghi CC BY 4.0 **nhưng đồng thời ghi "research purposes only"** | ⚠️ **Card tự mâu thuẫn** → coi như hạn chế. Ngoài ra nguồn là site có paywall (xem mục 6). |
| VLSP2025-LegalSML/legal-pretrain | https://huggingface.co/datasets/VLSP2025-LegalSML/legal-pretrain | 96.770 dòng, 1,8 GB | **Research/education only** | ❌ Không dùng cho mục đích nội bộ doanh nghiệp. Nhưng bộ `Public-Test` (440 dòng, 3 loại task) hữu ích để tham khảo cách thiết kế eval. |

**Không truy cập được** (HTTP 401, gated): `ntphuc149/ExtractiveQA_ALQAC`, `ntphuc149/ViBidLQA_v1`, `nqdhocai/vietnamese-legal-qa`. Bộ ALQAC không công bố license trên site chính thức → `[CHƯA XÁC MINH]`.

---

## 2. Tiếng Việt — dữ liệu để fine-tune (instruction)

| Dataset | URL | Quy mô | License | Dùng làm gì |
|---|---|---|---|---|
| **vietnamese-legal-instruct** (duyet) | https://huggingface.co/datasets/duyet/vietnamese-legal-instruct | 233.866 dòng / **467.732 cặp instruction**, 14 loại task | **CC BY 4.0** | ⭐ Món quý nhất cho nhánh fine-tune tiếng Việt. Sinh từ chính bản scrape vbpl.vn ở trên: tóm tắt văn bản, phân loại, QA theo chuỗi căn cứ pháp lý, diễn giải sang ngôn ngữ thường. **Dùng làm khuôn mẫu** để tự sinh bộ instruction cho thông tư NHNN. |
| **UTS2017_Bank** | https://huggingface.co/datasets/undertheseanlp/UTS2017_Bank | 2.471 mẫu | **Apache 2.0** | ⭐ **Dataset duy nhất vừa thực sự về ngân hàng VN vừa có license sạch cho thương mại.** Phản hồi khách hàng thật, 14 khía cạnh nghiệp vụ + sentiment 3 lớp. Nhỏ nhưng dùng ngay được cho task phân loại. |
| vnpdf-financial-reports-dataset | https://huggingface.co/datasets/kiethuynhanh/vnpdf-financial-reports-dataset | 401 dòng (text + ảnh trang) | **MIT** | Báo cáo tài chính VN dạng PDF — nhỏ, dùng để test pipeline trích xuất tài liệu. |
| vi-alpaca (bkai) / Vietnamese-alpaca-gpt4 (5CD-AI) | https://huggingface.co/datasets/bkai-foundation-models/vi-alpaca · https://huggingface.co/datasets/5CD-AI/Vietnamese-alpaca-gpt4-gg-translated | 50k / 52k dòng | **Không ghi license** `[CHƯA XÁC MINH]` | ⚠️ Sinh bằng GPT-4/3.5 → **điều khoản của OpenAI có thể cấm dùng để train model cạnh tranh**, độc lập với license dataset. Nếu cần instruction tiếng Việt tổng quát, tự kiểm tra ToS trước. |

**Về ViNumQA** (VLSP 2025, numerical reasoning trên báo cáo tài chính VN thật của MBS/SSI/MASVN, 4.074 triple): paper https://aclanthology.org/2025.vlsp-1.25.pdf xác nhận tồn tại, nhưng **không tìm được link tải** → `[CHƯA XÁC MINH khả dụng]`. Đây là dạng dữ liệu rất sát nếu sau này bạn làm feature phân tích số liệu.

---

## 3. Tiếng Anh — fine-tune hành vi (license sạch)

| Dataset | URL | Quy mô | License | Dùng làm gì |
|---|---|---|---|---|
| **Sujet-Finance-Instruct-177k** | https://huggingface.co/datasets/Sujet-AI/Sujet-Finance-Instruct-177k | 177.597 dòng, 337 MB | **Apache 2.0** | ⭐ Gộp 18 nguồn thành 7 loại task, đã dedup — tương đối sạch và có nhãn task. Lựa chọn mặc định. |
| **finance-alpaca** | https://huggingface.co/datasets/gbharti/finance-alpaca | 68.912 dòng | **MIT** | Định dạng Alpaca, gọn, tốt để khởi động hành vi chat tài chính. |
| **FinGPT** task sets | https://github.com/AI4Finance-Foundation/FinGPT · vd. https://huggingface.co/datasets/flwrlabs/fingpt-sentiment-train | sentiment 76,8k · headline 82,2k · finred 27,6k · fiqa_qa 17,1k | **MIT** | Từng task riêng, định dạng instruction/input/output — dễ trộn chọn lọc. |
| **PIXIU / FIT** | https://github.com/The-FinAI/PIXIU | ~136k mẫu `[suy ra từ repo]` | **MIT** | Bộ instruction đa task đứng sau model FinMA. |
| **BANKING77** | https://huggingface.co/datasets/PolyAI/banking77 | 13.083 câu, **77 nhãn intent** | **CC BY 4.0** | ⭐ Chuẩn mực cho phân loại intent khách hàng ngân hàng. Dùng để train **routing** — đúng một trong 5 workflow patterns ở Tuần 13. |
| Finance-Instruct-500k | https://huggingface.co/datasets/Josephgflowers/Finance-Instruct-500k | 518.185 dòng | **Apache 2.0** | ⚠️ Chính card tự nhận có nhiễu ("malformed portions", PII tổng hợp) → **phải filter**, đừng train thô. |

**Reasoning có dẫn giải** (FinQA, ConvFinQA, TAT-QA) — dùng được cho SFT nhưng **phải tự chuyển** annotation dạng program sang định dạng instruction:

- ConvFinQA — https://github.com/czyssrs/ConvFinQA — 3.037/421/434 hội thoại — **MIT**
- TAT-QA — https://github.com/NExTplusplus/TAT-QA — 16.552 câu hỏi trên bảng+text — **CC BY 4.0**
- FinQA — https://github.com/czyssrs/FinQA — ⚠️ **license xung đột**: repo GitHub ghi MIT, mirror HF `ibm-research/finqa` ghi CC-BY-4.0 → chưa giải quyết được, kiểm tra lại nếu dùng thương mại.

---

## 4. ⛔ Chỉ dùng để ĐÁNH GIÁ, không được đưa vào tập train

Các bộ này license **non-commercial** hoặc quá nhỏ/quá "vàng" để train — dùng làm held-out eval:

| Dataset | URL | License | Lý do |
|---|---|---|---|
| FinanceBench | https://huggingface.co/datasets/PatronusAI/financebench | **CC BY-NC 4.0** | Non-commercial; hơn nữa **chỉ công bố 150 mẫu**, bộ đầy đủ 10.231 câu phải liên hệ Patronus AI. |
| FiQA | https://huggingface.co/datasets/LLukas22/fiqa | **CC BY-NC 3.0** | Non-commercial. |
| Financial PhraseBank | https://huggingface.co/datasets/takala/financial_phrasebank | **CC BY-NC-SA 3.0** | Non-commercial; dùng thương mại phải xin phép tác giả. |
| BizBench (Kensho) | https://huggingface.co/datasets/kensho/bizbench | Apache 2.0 | License cho phép, nhưng do chuyên gia tài chính curate làm **test set** → giữ làm eval mới có giá trị. |

> Đây chính là chỗ mục **H** trong appendix (Tuần 8, 11, 15) có ích: đừng tin một chỉ số duy nhất, và cẩn thận cạm bẫy LLM-as-judge.

---

## 5. Corpus lớn cho RAG / continued pretraining

| Nguồn | URL | Quy mô | License | Ghi chú |
|---|---|---|---|---|
| SEC-EDGAR (TeraflopAI) | https://huggingface.co/datasets/TeraflopAI/SEC-EDGAR | 590 GB, ~8,05M filing, 43,7B token | **Apache 2.0** | Corpus tài chính mở lớn nhất đã xác minh. Là **nguồn RAG / pretrain**, không phải instruction data. |
| edgar-corpus (eloukas) | https://huggingface.co/datasets/eloukas/edgar-corpus | 40,7 GB, 1993–2020, chỉ 10-K, đã tách mục | **Apache 2.0** | Sạch hơn, có cấu trúc mục — dễ chunk cho RAG. |
| Basel / BCBS (BIS) | https://www.bis.org/bcbs/publications.htm | — | ⚠️ **KHÔNG public domain** | BIS chỉ cho phép "brief excerpts... provided the source is stated". Đọc tham khảo + RAG có dẫn nguồn thì được; **bulk scrape làm training corpus thì không**, chưa có cơ sở. |
| EBA | https://www.eba.europa.eu/publications-and-media/publications | — | `[CHƯA XÁC MINH]` | Không fetch được trang điều khoản bản quyền. |

**Khoảng trống thật:** không tìm thấy corpus quy định ngân hàng (Basel/EBA/central bank) đóng gói sẵn kiểu EDGAR-CORPUS. Muốn có thì phải tự thu thập — và phải kiểm tra điều khoản từng site trước.

---

## 6. ⚠️ PHÁP LÝ & LICENSE — phần quan trọng nhất vì bạn làm ngân hàng

### 6.1 Văn bản pháp luật VN có bản quyền không?

**Đã xác minh (nguồn thứ cấp):** Luật Sở hữu trí tuệ hợp nhất 2025, **Điều 15** liệt kê các đối tượng **không được bảo hộ quyền tác giả**, trong đó có:

> *"Văn bản quy phạm pháp luật, văn bản hành chính, văn bản khác thuộc lĩnh vực tư pháp và **bản dịch chính thức** của văn bản đó"*

Nguồn fetch: https://luatvietnam.vn/so-huu-tri-tue/van-ban-hop-nhat-155-vbhn-vpqh-nam-2025-...-411282-d5.html

⚠️ **Cảnh báo về chính câu trên:** đây là văn bản lấy từ **luatvietnam.vn — một aggregator thương mại, không phải Công báo chính thức**. Nội dung khớp với hiểu biết phổ biến về Điều 15, nhưng **tôi chưa đối chiếu với bản Công báo gốc**. Nếu dùng làm căn cứ pháp lý cho quyết định của bank, hãy tự đối chiếu nguồn chính thức.

### 6.2 Khác biệt sống còn: bản thân văn bản luật ≠ bản biên tập của aggregator

`[Suy luận, không phải kết luận pháp lý đã kiểm chứng]` Có hai thứ rất khác nhau:

1. **Text gốc của thông tư/nghị định** — theo Điều 15 thì không có bản quyền.
2. **Bản compile/format/cross-reference/tóm tắt/dịch không chính thức của một site thương mại** — rất có thể là tác phẩm phái sinh được bảo hộ riêng, **và ràng buộc hợp đồng qua ToS còn tồn tại độc lập với vấn đề bản quyền**.

**thuvienphapluat.vn** (đã thử fetch, trả về **HTTP 403** — site chủ động chặn bot): footer ghi **"© 2026 THƯ VIỆN PHÁP LUẬT"**, nội dung gated sau gói trả phí (Basic / **TVPL Pro**), bản dịch tiếng Anh nằm sau gói Pro. Không đọc được text "Thỏa ước dịch vụ" → `[CHƯA XÁC MINH]` điều khoản scraping cụ thể. **Đừng cho rằng nó cho phép.**

**vbpl.vn** — Cơ sở dữ liệu quốc gia về văn bản pháp luật, do **Bộ Tư pháp** vận hành, tức nguồn chính thức. Không đọc được trang điều khoản → `[CHƯA XÁC MINH]`, nhưng vì là nguồn chính thức và nội dung đã thuộc diện Điều 15, đây là **nguồn nên ưu tiên** thay vì aggregator thương mại.

> **Khuyến nghị cho bối cảnh bank:** trước khi scrape/bulk-download từ bất kỳ aggregator có paywall, cần **legal/compliance sign-off thật**, không chỉ dựa vào lập luận "luật thì public domain". Ba lý do: (a) chưa xác minh được ToS cho phép hay cấm; (b) nội dung sau paywall thường kèm ràng buộc hợp đồng riêng; (c) là ngân hàng, bạn có thêm rủi ro tuân thủ ngoài rủi ro bản quyền thường.

### 6.3 Dữ liệu nội bộ ngân hàng

`[Cảnh báo chung, KHÔNG phải tư vấn pháp lý — chưa nghiên cứu luật chuyên ngành VN trong lần tra này]`

- Dữ liệu khách hàng, giao dịch, tài liệu risk/compliance nội bộ đưa vào fine-tune — **kể cả QLoRA chạy local** — vẫn có thể cấu thành hành vi xử lý/lưu trữ dữ liệu, liên quan **Nghị định 13/2023/NĐ-CP** về bảo vệ dữ liệu cá nhân. **Chưa đối chiếu text nghị định** → phải để compliance review.
- Train local/air-gapped **giảm** rủi ro lộ ra bên thứ ba so với gọi API ngoài, nhưng **không loại bỏ** rủi ro.
- Model đã fine-tune trên dữ liệu thật **có thể nhả lại dữ liệu đó** trong output — đây là lý do nữa để **kiến thức đi qua RAG (đọc lúc chạy, phân quyền được) chứ không nướng vào weights**.

### 6.4 Bảng phân loại nhanh

| Dùng được cho nội bộ/thương mại (license đã xác minh) | Chỉ research / không rõ → tránh |
|---|---|
| th1nhng0/vietnamese-legal-documents (CC BY 4.0) | pdt590/vietnamese-legal-documents (card mâu thuẫn) |
| duyet/vietnamese-legal-instruct (CC BY 4.0) | VLSP2025-LegalSML/legal-pretrain (research only) |
| YuITC/Vietnamese-Legal-Documents (MIT) | PhoMT (research/education only, **cấm redistribute**) |
| UTS2017_Bank (Apache 2.0) | FiQA, Financial PhraseBank, FinanceBench (**NC** → chỉ eval) |
| Sujet-Finance-Instruct-177k, finance-alpaca, FinGPT, PIXIU | vi-alpaca & bản dịch GPT-4 (ToS OpenAI) |
| BANKING77 (CC BY 4.0), TAT-QA (CC BY 4.0), ConvFinQA (MIT) | FinQA (license xung đột MIT vs CC-BY) |
| SEC-EDGAR, edgar-corpus (Apache 2.0) | Basel/BIS, EBA (chưa có quyền reuse) |

---

## 7. Base model — đừng train from scratch, hãy chọn nền tốt

| Model | License (đã xác minh) | Bằng chứng tiếng Việt | Ghi chú |
|---|---|---|---|
| **Qwen2.5-7B-Instruct** | **Apache 2.0** — sạch nhất, không giới hạn thương mại | Card nêu "29+ ngôn ngữ" gồm tiếng Việt nhưng **không có benchmark riêng cho tiếng Việt** | ⭐ Lựa chọn an toàn nhất về pháp lý. Cũng là base của Fin-R1. |
| **Vistral-7B-Chat** | **AFL-3.0** (Academic Free License) | Continual-pretrain từ Mistral-7B trên text VN; card tự báo **VMLU 50,07%** (số tự công bố, chưa kiểm chứng độc lập) | Bằng chứng tiếng Việt mạnh nhất, nhưng license + điều khoản sử dụng **cần legal review trước khi dùng trong bank**. |
| **PhoGPT-4B-Chat** (VinAI) | **BSD-3-Clause** | Pretrain from scratch trên 41GB corpus VN | Nhỏ (4B) → chạy thoải mái trên 8GB. VinAI khuyến nghị bản 4B thay cho 7B5. |
| SeaLLMs-v3-7B-Chat | **License riêng "SeaLLMs"** | Số VN tự công bố khá tốt | ⚠️ **`[CHƯA XÁC MINH]` điều khoản thương mại** — chưa đọc được file Terms of Use. Đừng giả định là an toàn. |
| Fin-R1 | **Apache 2.0** | Base Qwen2.5-7B-Instruct, SFT+RL cho reasoning tài chính, song ngữ EN/中文 | Đã tài chính hoá sẵn, nhưng **không có tiếng Việt** — cân nhắc như nguồn tham khảo cách làm. |

**Về VRAM trên 3070 Ti 8GB:** `[CHƯA XÁC MINH bằng nguồn kỹ thuật chính thức]` — con số "7B 4-bit ≈ 5–6GB nhưng peak có thể vọt lên 14–15GB với sequence dài" chỉ đến từ blog tổng hợp. Thực tế: 7B là **ngưỡng trên** cho card 8GB, batch = 1, seq ngắn, bắt buộc gradient checkpointing. Với Mac 24GB: `[CHƯA XÁC MINH]` số cụ thể — phải tự benchmark. Đây đúng là việc của Tuần 8–9.

---

## 8. Song ngữ VI/EN — nên trộn hay tách?

**Đã có bằng chứng công bố (không phải folklore):**

- Fine-tune model multilingual **chỉ bằng data tiếng Anh** gây **catastrophic forgetting khả năng sinh văn bản ngôn ngữ khác** — hiện tượng có tên, đã công bố (ACL/EMNLP 2022, "Overcoming Catastrophic Forgetting in Zero-Shot Cross-Lingual Generation").
- *"Multilingual Instruction Tuning With Just a Pinch of Multilinguality"*: chỉ **~40 mẫu multilingual** trộn vào tập tiếng Anh đã cải thiện rõ khả năng làm theo instruction đa ngôn ngữ; model train trên hỗn hợp bằng hoặc hơn model train đơn ngữ dù ít data đích hơn nhiều.
- *"Monolingual or Multilingual Instruction Tuning"* (Findings EACL 2024): **dưới LoRA thì trộn multilingual tốt hơn**; dưới full fine-tuning thì kết quả lẫn lộn.

`[Suy luận từ các nghiên cứu liền kề, không phải kết luận đã kiểm chứng cho đúng ca của bạn]` Vì bạn dùng **QLoRA** (adapter-based, giống điều kiện LoRA ở trên), nên **trộn VI + EN trong cùng tập SFT** khả năng cao tốt hơn train riêng từng thứ tiếng, và giảm rủi ro làm hỏng tiếng Anh vốn có. Không tìm thấy nghiên cứu nào cho đúng tổ hợp (VI+EN, QLoRA, domain tài chính) → hãy tự đo.

**Nguồn song ngữ đã xác minh:**

| Nguồn | URL | License | Ghi chú |
|---|---|---|---|
| **MTet** | https://arxiv.org/abs/2210.05610 | **CC BY 4.0** | 4,2M cặp VI-EN đa domain. Nguồn parallel sạch license tốt nhất tìm được. |
| **CFPB Vietnamese-English Glossary of Financial Terms** | https://files.consumerfinance.gov/f/documents/cfpb_adult-fin-ed_vietnamese-style-guide-glossary.pdf | Tác phẩm của cơ quan liên bang Mỹ, công bố 3/2024 để "further the accessibility of financial information" — `[CHƯA XÁC MINH]` tuyên bố quyền chính xác | ⭐ **Thuật ngữ tài chính VI-EN chuẩn hoá** — đúng thứ cần cho nhất quán thuật ngữ song ngữ. Là glossary, không phải câu song song. |
| EVBCorpus | https://github.com/qhungngo/EVBCorpus | **Không có license** — phải email tác giả | Có **250 văn bản luật/pháp lệnh song song** — gần nhất với domain pháp lý, nhưng quyền dùng không rõ. |
| ❌ **PhoMT** | https://github.com/VinAIResearch/PhoMT | **research/education only, CẤM redistribute** | 3,02M cặp — chất lượng cao nhưng **không dùng được cho bank**. Ghi ở đây để bạn biết mà tránh. |

**Khoảng trống:** không có corpus song song **tài chính/ngân hàng** VI-EN nào license mở. Thực tế bạn sẽ phải tự xây từ tài liệu song ngữ nội bộ (sau khi qua compliance) + CFPB glossary làm xương sống thuật ngữ.

---

## 9. Đánh giá — làm sao biết nó thực sự chạy được tiếng Việt

| Benchmark | URL | Đo gì |
|---|---|---|
| **VMLU** | https://vmlu.ai/ | Trắc nghiệm tiếng Việt: Vi-MQA 10.880 câu / 58 môn, + Vi-SQuAD, Vi-DROP, Vi-Dialog. `[CHƯA XÁC MINH]` bảng xếp hạng hiện tại (không load được). |
| **ViLLM-Eval** | https://arxiv.org/abs/2404.11086 · HF `vlsp-2023-vllm/ViLLM-Eval` | Bộ eval từ shared task VLSP 2023. |
| **VN-MTEB** | https://arxiv.org/abs/2507.21500 | 41 dataset, 6 loại task **embedding** (retrieval/rerank/clustering/STS) → dùng để chọn embedding model cho RAG ở **Tuần 10–11**, không phải để đo chat model. |

Ngoài ra **tự làm eval set riêng** là bắt buộc: ~50–100 câu hỏi nghiệp vụ thật, có đáp án đúng kèm điều khoản dẫn nguồn. Không benchmark công khai nào đo được "model trả lời đúng quy định nội bộ của bạn hay không". Đây là `eval_rubric.md` ở Tuần 15.

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
2. **Ưu tiên vbpl.vn (nguồn Bộ Tư pháp) hơn aggregator thương mại** cho text pháp luật, và giữ lại metadata nguồn + ngày hiệu lực của từng văn bản (bạn sẽ cần nó cho provenance ở Tuần 14).
3. **Đưa câu hỏi "dùng dữ liệu nội bộ" cho compliance trước khi bắt đầu**, không phải sau khi đã train. Nếu chỉ để học, dùng hoàn toàn dữ liệu công khai là đủ — và an toàn hơn nhiều.
