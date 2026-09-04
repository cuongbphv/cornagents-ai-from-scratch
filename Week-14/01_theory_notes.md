# Lý thuyết Tuần 14: Hybrid search, reranking, RAGAS, tracing

> Đọc trước khi nâng cấp pipeline theo [`02_advanced_rag_notes.md`](02_advanced_rag_notes.md). Ví dụ số kiểm chứng 2026-08-11; nguồn cuối file. Cần baseline Tuần 13 đã chạy.

---

## 1. Vì sao vector search một mình không đủ

Hai chế độ thất bại **bù nhau**. Vector search (dense) trượt term chính xác: với câu hỏi chứa mã văn bản `"39/2016/TT-NHNN"`, không có gì bảo chứng rằng embedding đặt chuỗi ký hiệu này "gần" đúng chunk chứa nó về cosine. BM25 (sparse/lexical) thì trượt diễn đạt khác: hỏi "vay vốn mua nhà" không match chunk viết "cấp tín dụng phục vụ nhu cầu nhà ở", vì không trùng từ nên BM25 mù.

Hybrid nghĩa là chạy cả hai rồi trộn kết quả. BM25 là hàm chấm điểm họ TF-IDF: điểm cao khi term của query xuất hiện nhiều trong document, hiếm trong corpus, có điều chỉnh độ dài document.

## 2. Reciprocal Rank Fusion: trộn hai bảng xếp hạng không cần chỉnh trọng số

```
RRF(doc) = Σ_retriever 1 / (k + rank_doc)        k = 60 (mặc định phổ biến)
```

Chỉ dùng **thứ hạng**, không dùng điểm thô, nên trộn được hai hệ điểm khác thang (BM25 score vs cosine). Ví dụ kiểm chứng 2026-08-11, k=60:

| Doc | Hạng BM25 | Hạng vector | RRF |
|-----|-----------|-------------|-----|
| A | 1 | 8 | 0.031099 |
| B | 3 | 2 | **0.032002** ← thắng |

Bài học nằm trong ví dụ: doc B **không đứng đầu bảng nào** nhưng thắng vì tốt đều ở cả hai, RRF thưởng sự đồng thuận giữa hai retriever, đúng cái hybrid cần.

## 3. Cross-encoder reranking: chậm mà chuẩn, nên chỉ chấm chung kết

Bi-encoder dùng cho retrieval: embed query và document **riêng rẽ**, rồi so cosine. Nhanh (document embed trước từ lúc index), nhưng hai bên không "đọc" nhau. Cross-encoder dùng cho rerank: nhét `(query, document)` **vào cùng một lượt** qua model, cho ra điểm liên quan. Chuẩn hơn hẳn vì attention chạy chéo giữa query và document (bạn hiểu vì sao, Tuần 6), nhưng phải chạy model cho TỪNG cặp, nên không thể chấm cả corpus.

Kiến trúc chuẩn là retrieve rẻ lấy top-20..50, rồi cross-encoder chấm lại, rồi lấy top-3..5 đưa vào prompt. BGE reranker (mã mở) chạy ổn trên máy local.

## 4. RAGAS: tách "lỗi tìm" khỏi "lỗi trả lời"

Bốn metric, chia đúng hai nửa pipeline:

| Metric | Đo cái gì | Lỗi ở đâu khi thấp |
|--------|-----------|---------------------|
| Context precision | context lấy về có liên quan không | retrieval |
| Context recall | có lấy đủ thông tin cần không | retrieval |
| Faithfulness | câu trả lời có bám context không | generation (bịa) |
| Answer relevancy | có trả lời đúng câu hỏi không | generation |

Đọc kết quả theo cặp: faithfulness thấp trong khi context tốt nghĩa là model bịa, cần hạ temperature và siết prompt; context recall thấp là lỗi tìm, cần sửa retriever, đừng đổi model. Eval set tối thiểu 20-30 cặp (câu hỏi, ground truth) để bắt đầu, mục tiêu 50-100 khi có thời gian (như README): **so before/after cùng eval set** mới thành bảng số có nghĩa.

Định nghĩa gốc của 4 metric nằm trong paper RAGAS (PDF trong repo: [`../docs/papers/2309.15217_ragas-rag-evaluation.pdf`](../docs/papers/2309.15217_ragas-rag-evaluation.pdf)): 8 trang, đọc được trong một buổi. Còn nếu muốn xem người khác đã ablate các tổ hợp module (chunking, rerank, hybrid...) ra sao trước khi tự thí nghiệm: Wang et al. 2024, *Searching for Best Practices in RAG* ([`../docs/papers/2407.01219_rag-best-practices.pdf`](../docs/papers/2407.01219_rag-best-practices.pdf)): họ "investigate existing RAG approaches and their potential combinations" và đề xuất các chiến lược cân bằng chất lượng/chi phí.

## 5. Bẫy LLM-as-judge: RAGAS chấm bằng LLM nên dính đủ

Zheng et al. (arXiv 2306.05685) ghi nhận các thiên vị của LLM judge: **thiên vị độ dài** (chuộng câu trả lời dài), **thiên vị vị trí** (chuộng phương án đứng trước khi so cặp), **tự khen model cùng họ**. Áp vào tuần này:

- Điểm RAGAS tăng ≠ chắc chắn tốt hơn, kiểm tay 5-10 mẫu mỗi lần đo, nhất là các mẫu điểm cao bất thường.
- Giữ judge model **cố định** giữa before/after, đổi judge giữa chừng là vô hiệu phép so sánh.
- Đừng tin một chỉ số duy nhất (mục nâng cao H): bảng số + đọc tay đi cùng nhau.

Mức độ đáng ngại có số đo hẳn hoi: *Judging the Judges* (Bavaresco et al. 2024, PDF trong repo: [`../docs/papers/2406.12624_judging-the-judges.pdf`](../docs/papers/2406.12624_judging-the-judges.pdf)) cho 13 judge model chấm cùng bộ bài mà con người đồng thuận cao, và thấy ngay cả judge tốt nhất vẫn "quite far behind inter-human agreement", điểm số lệch tới 5 điểm so với người chấm, kèm "a tendency toward leniency". Điểm an ủi: model nhỏ (thậm chí metric lexical) vẫn **xếp hạng** tương đối ổn dù điểm tuyệt đối kém, nên dùng judge để so sánh A/B thì đáng tin hơn là đọc điểm tuyệt đối.

## 6. Tracing: nhìn thấy từng bước thay vì đoán

Langfuse/LangSmith ghi lại mỗi request theo chuỗi: query, rồi các chunk lấy về kèm điểm số, rồi prompt cuối, rồi câu trả lời, kèm latency và số token. Giá trị thật: khi một câu trả lời sai, mở trace ra **biết ngay lỗi ở khâu nào**: retrieval lấy sai chunk hay generation bịa trên chunk đúng. Không có trace, mọi debug RAG là đoán mò.

## 7. Tiếng Việt trong tuần này

- BM25 với tiếng Việt buộc phải nghĩ về tách từ. Tiếng Việt viết rời từng âm tiết, nên tokenize theo khoảng trắng biến "ngân hàng" thành 2 term `ngân` + `hàng`, match nhầm với "hàng hóa", "hàng không". Hai hướng xử lý: (a) word segmentation trước khi index BM25 (thư viện tách từ tiếng Việt, kiểm tra license trước khi thêm vào repo theo chính sách CLAUDE.md); (b) chấp nhận âm tiết + dựa vào **cụm từ trong query** và vế vector của hybrid bù lại. Với corpus văn bản pháp luật nhiều thuật ngữ cố định, giả thuyết để bạn kiểm bằng eval set là (a) cải thiện precision vì term khớp đúng cụm thay vì từng âm tiết; chưa đo thì chưa kết luận.
- Nhớ chuẩn hóa NFC trước khi index BM25 (Tuần 13 mục 6): `"tín"` NFC và NFD là hai term khác nhau, corpus trộn hai dạng làm BM25 "mất" document một cách âm thầm.
- Eval set phải là câu hỏi tiếng Việt nghiệp vụ thật (README: tối thiểu 20-30 câu để bắt đầu, mục tiêu 50-100 khi có thời gian, kèm điều khoản nguồn, không benchmark công khai nào thay được). Ground truth dẫn về số Điều/Khoản cụ thể.
- Với judge chấm văn bản tiếng Việt, chọn judge model đọc tiếng Việt tốt và giữ cố định. Các thiên vị ở mục 5 được Zheng et al. đo trên MT-Bench và Chatbot Arena, dữ liệu tiếng Anh, nên mức độ trên tiếng Việt chưa có số; càng thêm lý do kiểm tay một mẫu nhỏ.

## 8. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| Zheng et al. 2023, Judging LLM-as-a-Judge | https://arxiv.org/abs/2306.05685 | 5 |
| explodinggradients/ragas (Apache 2.0) | https://github.com/explodinggradients/ragas | 4 |
| Es et al. 2023, paper RAGAS (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2309.15217, PDF local: [`../docs/papers/`](../docs/papers/README.md) | 4 |
| Wang et al. 2024, Searching for Best Practices in RAG (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2407.01219, PDF local: [`../docs/papers/`](../docs/papers/README.md) | 4 |
| Bavaresco et al. 2024, Judging the Judges (CC0, kiểm 2026-08-12) | https://arxiv.org/abs/2406.12624, PDF local: [`../docs/papers/`](../docs/papers/README.md) | 5 |

(Trang docs.ragas.io trả HTTP 429 tại thời điểm kiểm tra 2026-08-11, dùng repo GitHub ở trên làm cửa vào. BGE reranker, Langfuse/LangSmith: link trong README nguồn học.)

## Sau khi đọc xong

1. Thêm BM25 (nhớ NFC), rồi trộn bằng RRF, rồi thêm BGE reranker, theo [`02_advanced_rag_notes.md`](02_advanced_rag_notes.md).
2. Xây eval set tiếng Việt kèm điều khoản nguồn, tối thiểu 20-30 câu để bắt đầu, mục tiêu 50-100 khi có thời gian.
3. Đo RAGAS before/after, kiểm tay 5-10 mẫu, wire tracing.
4. Viết [`03_ragas_report.md`](03_ragas_report.md): bảng số + nhận xét đọc tay; làm [`quiz.md`](quiz.md).

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- BM25 là gì thì đọc IR-book mục 11.4.3 Okapi BM25 (trang 232): mô hình nhị phân độc lập không để ý tần suất từ và độ dài tài liệu, nên BM25 "was developed as a way of building a probabilistic model sensitive to these quantities while not introducing too many additional parameters into the model (Spärck Jones et al. 2000)". Đọc trước khi bật `rank_bm25` để biết hai tham số k₁ và b điều khiển gì.
- Đánh giá retrieval có xếp hạng nằm ở IR-book mục 8.4 (trang 158): precision và recall là số đo trên tập không thứ tự; với kết quả xếp hạng ta tính chúng trên top-k và vẽ precision-recall curve có hình răng cưa. Mục 8.3 (trang 155) là các số đo không xếp hạng. Context precision và recall của RAGAS là phiên bản dùng LLM chấm của đúng các số đo này. SLP3 mục 11.2 (trang 261) nói cùng chuyện trong bối cảnh QA.
