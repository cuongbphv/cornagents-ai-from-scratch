# Lý thuyết Tuần 13: RAG pipeline end-to-end

> Đọc trước khi điền [`02_rag_pipeline.py`](02_rag_pipeline.py). Ví dụ số kiểm chứng bằng PyTorch 2.5.1 + tiktoken ngày 2026-08-11; nguồn cuối file.

---

## 1. Vì sao RAG: và vì sao không phải fine-tune

Nguyên tắc đã chốt từ Tuần 11: **fine-tune dạy hành vi, RAG cung cấp kiến thức.** Kiến thức quy định (thông tư, điều khoản) thay đổi liên tục và cần dẫn nguồn, nhét vào trọng số thì không cập nhật được, không trích dẫn được, và không kiểm chứng được. RAG (Lewis et al., arXiv 2005.11401) tách đôi: kiến thức nằm trong **kho tài liệu truy xuất được**, model chỉ làm việc đọc-hiểu-trả-lời trên context được đưa vào.

Pipeline baseline 6 khâu, hỏng khâu nào hỏng cả chuỗi:

```
Load PDF → Chunk → Embed → Vector store → Retrieve top-k → Generate (kèm context)
```

## 2. Embeddings + cosine similarity: thước đo "gần nghĩa"

Embedding model biến đoạn văn thành vector; hai đoạn gần nghĩa cho ra hai vector gần nhau theo **cosine similarity**:

```
cos(a, b) = (a·b) / (|a||b|)     ∈ [−1, 1]
```

Kiểm chứng 2026-08-11: `cos(a, 2a) = 1.0` (cùng hướng tuyệt đối, cosine bỏ qua độ dài, chỉ đo hướng); hai vector lệch hướng cho 0.378. Retrieval là embed câu hỏi rồi tìm k chunk có cosine cao nhất trong store. Lưu ý nền từ Tuần 4: đây vẫn chỉ là dot product sau khi chuẩn hóa.

Embedding model là quyết định chất lượng số 1 của RAG, vì nó quyết định "gần nghĩa" nghĩa là gì. Chọn theo benchmark phù hợp ngôn ngữ của corpus (mục 6).

Đừng coi cosine là chân lý mặc định. Steck et al. 2024 (arXiv [2403.05440](https://arxiv.org/abs/2403.05440), abstract tra 2026-08-12) chỉ ra với embedding học từ model có regularization, "cosine-similarity can yield arbitrary and therefore meaningless 'similarities'", có trường hợp thua cả dot product không chuẩn hóa. Chất lượng retrieval đo bằng eval set của bạn (Tuần 14), không suy ra từ việc "đã dùng đúng công thức".

## 3. Chunking: cắt tài liệu không làm đứt nghĩa

- Baseline trong README là `RecursiveCharacterTextSplitter`, size ~800, overlap ~100. Splitter này đếm theo **ký tự** và ưu tiên cắt tại ranh giới tự nhiên theo thứ tự separator: đoạn trước, rồi câu, rồi từ.
- Ký tự không phải token. Đo thật trên một câu thông tư tiếng Việt (cl100k, 2026-08-11): 115 ký tự cho ra 52 token, tức ~**2.2 ký tự/token**, nên chunk 800 ký tự tiếng Việt ≈ 360 token. Muốn kiểm soát ngân sách context chính xác thì đếm bằng token của đúng model bạn dùng, đừng áng chừng theo ký tự.
- Overlap tồn tại để câu nằm vắt qua ranh giới chunk không bị mất ngữ cảnh ở cả hai phía.
- Với văn bản pháp luật, ranh giới tự nhiên tốt nhất là **Điều/Khoản/Điểm**: cắt theo cấu trúc văn bản (semantic) luôn thắng cắt theo đếm ký tự mù; giữ số hiệu Điều trong metadata của chunk.

## 4. Vector store + metadata: chỗ provenance bắt đầu

- Dùng **Chroma** cho dev (persist xuống đĩa, không cần server); chuyển sang pgvector/Qdrant khi cần production.
- Mỗi chunk lưu kèm **metadata: tên văn bản, số hiệu, điều khoản, ngày hiệu lực**: Tuần 17 cần chúng làm provenance, và câu trả lời có dẫn nguồn cần chúng ngay tuần này. Mất metadata lúc ingest là mất vĩnh viễn.

## 5. Generate: grounding là mục tiêu, không phải văn hay

- Prompt template tối thiểu: *"Chỉ trả lời dựa trên context dưới đây. Không tìm thấy thông tin thì nói không tìm thấy."* + context top-k + câu hỏi.
- Giữ temperature ≤ 0.3 cho RAG nghiệp vụ (khuyến nghị trong README, mục nâng cao B2): cùng context đó, temperature cao làm model "suy diễn vượt nguồn" nhiều hơn.
- Test 10 câu hỏi domain: với mỗi câu trả lời, tự hỏi **"câu này dẫn về được chunk nào?"**: không dẫn được = chưa grounded, đánh dấu lại làm baseline cho Tuần 14 đo.

## 6. Tiếng Việt trong tuần này: 3 bẫy có bằng chứng

1. Unicode NFC và NFD là bẫy âm thầm nhất. Kiểm chứng 2026-08-11: ký tự `ế` dạng NFC là **1 codepoint**, dạng NFD là **3 codepoint** (e + dấu mũ + dấu sắc), và hai chuỗi **không bằng nhau** khi so sánh trực tiếp. Corpus scrape từ nhiều nguồn có thể trộn cả hai dạng, dẫn tới cùng một từ thành hai chuỗi khác nhau khi match, đếm ký tự lệch, highlight sai. **Chuẩn hóa `unicodedata.normalize("NFC", text)` ngay tại bước load, trước mọi xử lý khác.**
2. Embedding model phải hỗ trợ tiếng Việt thật, vì model embedding train chủ yếu tiếng Anh cho cosine similarity kém nghĩa trên tiếng Việt. Chọn theo **VN-MTEB** (benchmark embedding tiếng Việt, mục 9 của [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md)); nghi ngờ thì tự test: 5 cặp câu nghiệp vụ đồng nghĩa + 5 cặp không liên quan, xem cosine có tách hai nhóm không.
3. Ngân sách token tiếng Việt tính theo 2.2 ký tự/token (đo ở mục 3): khi ước lượng "top-k chunk có vừa context window không", tính bằng token thật, nhất là khi generate bằng model local context ngắn.

Corpus khuyến nghị + lưu ý pháp lý: xem mục Dữ liệu cho tuần này trong [README.md](README.md) (nguồn vbpl.vn, giữ metadata ngày hiệu lực).

## 7. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| Lewis et al. 2020, RAG | https://arxiv.org/abs/2005.11401 | 1 |
| Steck et al. 2024, Is Cosine-Similarity Really About Similarity? (chỉ link, arXiv non-exclusive, kiểm 2026-08-12) | https://arxiv.org/abs/2403.05440 | 2 |
| Gekhman et al. 2024, FT trên kiến thức mới & hallucination (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2405.05904, PDF local: [`../docs/papers/`](../docs/papers/README.md) | 1 |

(LlamaIndex/LangChain docs, NirDiamant/RAG_Techniques: link trong README nguồn học, API đổi theo version, đọc docs đúng version bạn cài.)

## Sau khi đọc xong

1. Thu thập corpus vào `data/`, **normalize NFC ngay khi load**.
2. Điền [`02_rag_pipeline.py`](02_rag_pipeline.py) theo 6 khâu; chunk giữ metadata điều khoản.
3. Test 10 câu hỏi domain, ghi lại câu nào grounded/câu nào không, đây là baseline Tuần 14.
4. Làm [`quiz.md`](quiz.md).

## 8. RAG trong dòng lịch sử information retrieval

Pipeline sáu khâu ở mục 1 là cách một kỹ sư dựng RAG. Mục này kể lại cùng hệ thống bằng ngôn ngữ của ngành information retrieval, để bạn dùng đúng thuật ngữ khi đọc paper và khi thiết kế eval ở Tuần 14.

**Từ vựng chuẩn.** Jurafsky và Martin (SLP3 mục 11.1, trang 254) gọi bài toán là **ad hoc retrieval**: người dùng đưa một query, hệ thống trả về một tập tài liệu có thứ tự từ một collection. **Document** là bất kỳ đơn vị text nào hệ thống index và trả về, có thể là trang web, bài báo, hay đoạn ngắn như một paragraph; với RAG, chunk của bạn chính là document. **Collection** là tập tài liệu phục vụ truy vấn; **term** là từ (hoặc cụm từ) trong collection; **query** biểu diễn nhu cầu thông tin dưới dạng tập term. Kiến trúc chung (Figure 11.1 của SLP3) có hai nhánh: xử lý và index tài liệu, và xử lý query thành vector; xếp hạng dựa trên điểm liên quan giữa hai vector. Hai lớp hệ thống IR khác nhau ở loại vector: **sparse**, tức vector đếm có trọng số tf-idf hoặc BM25, và **dense**, tức embedding từ encoder. Pipeline Tuần 13 của bạn là dense retrieval; Tuần 14 thêm nhánh sparse thành hybrid.

**Vì sao cần dense.** SLP3 mục 11.3 (trang 264) chỉ ra khiếm khuyết của tf-idf và BM25: "they work only if there is exact overlap of words between the query and document", nên người hỏi phải đoán đúng từ người viết đã dùng, vấn đề mang tên vocabulary mismatch (Furnas et al. 1987). Embedding dày giải quyết bằng cách so nghĩa; ý tưởng có từ Latent Semantic Indexing (Deerwester et al. 1990) và nay hiện thực bằng encoder như BERT. [Suy luận] Với tài liệu pháp lý tiếng Việt, mismatch dễ xảy ra: người hỏi nói "phí phạt trả nợ trước hạn", văn bản viết "phí trả nợ trước hạn" hoặc dẫn số điều khoản. Đây là lý do baseline dense của tuần này đáng có, và cũng là lý do Tuần 14 vẫn cần BM25 cho các trường hợp cần khớp chính xác số hiệu văn bản.

**RAG hai giai đoạn.** SLP3 mục 11.4 (trang 267) mô tả RAG cơ bản: giai đoạn retrieve lấy các passage liên quan từ một collection định trước, ví dụ bằng dense retriever; giai đoạn generate ghép các passage đó với prompt của người dùng và đưa cho LLM sinh câu trả lời điều kiện trên cả hai. Hệ thống có hai thành phần chính, retriever và generator, thành phần sau đôi khi gọi là reader vì lý do lịch sử. Ba mục tiêu của RAG theo SLP3: giảm hallucination bằng cách cho model một tập tài liệu đáng tin, sinh text đúng về dữ liệu riêng (email, hồ sơ, tài liệu nội bộ, văn bản pháp lý), và xử lý kiến thức thay đổi theo thời gian, khi nhu cầu thông tin nói về dữ liệu sau thời điểm model được train. Ba mục tiêu này trùng khít với lý do repo chọn RAG cho kiến thức quy định thay vì fine-tune: văn bản pháp luật thay đổi, cần dẫn nguồn, và không được bịa.

**Ghi gì cho baseline.** Với mỗi câu hỏi trong bộ 10 câu, lưu id chunk được retrieve, điểm cosine, và câu trả lời. Tuần 14 bạn sẽ cần đúng ba cột này để tính context precision và recall theo định nghĩa IR-book mục 8, và để so trước và sau khi thêm BM25 và reranker.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- SLP3 chương 11 đặt RAG trong dòng lịch sử IR: mục 11.1 (trang 254) là IR cổ điển, mục 11.3 (trang 264) chỉ ra khiếm khuyết của tf-idf và BM25: "they work only if there is exact overlap of words between the query and document", gọi là vocabulary mismatch problem, và dense embedding là cách giải. Mục 11.4 (trang 267) định nghĩa RAG gồm hai thành phần retriever và generator, và nêu các mục tiêu: "RAG can help mitigate hallucination, by giving the model a set of trusted documents", dữ liệu riêng, và kiến thức thay đổi theo thời gian. Ba mục tiêu này trùng với lý do repo chọn RAG cho kiến thức quy định.
- IR-book mục 6.2.2 Tf-idf weighting (trang 118) và 6.3 (trang 120) trình bày tf-idf và vector space model: điểm giống nhau giữa cosine similarity của embedding và cosine trên vector tf-idf là cùng công thức góc của Tuần 1; khác ở cách dựng vector.
- Code tham chiếu mở là hai notebook `chapter08/Chapter 8 - Semantic Search.ipynb` và `chapter10/Chapter 10 - Creating Text Embedding Models.ipynb` trong repo Hands-On LLM (Apache-2.0).
