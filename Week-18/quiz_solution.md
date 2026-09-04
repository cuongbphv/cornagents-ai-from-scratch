# Tuần 18, Đáp án & Giải thích: Capstone + evaluation/observability

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Use case capstone khuyến nghị và 3 thành phần kỹ thuật của nó?

**Trả lời mẫu:** Use case: spec-to-stories + automated review cho một feature Finance Banking (nghiệp vụ Finance Banking tổng quát). Ba thành phần: (1) RAG, grounding vào tài liệu domain; (2) Agents, workflow multi-agent (requirements → review → test) với HITL gate; (3) tùy chọn model fine-tuned local (Tuần 11/12) cho một sub-task phân loại nghiệp vụ hẹp. Gắn tracing và viết eval rubric.

**Giải thích:** Đây là nơi hội tụ cả 3 phase của roadmap.

## Câu 2 (Trắc nghiệm)

Bộ ba metric đánh giá capstone agentic gồm?

- **A.** FPS, latency, throughput
- **B.** Loss, perplexity, BLEU
- **C.** Precision, recall, F1 (chỉ vậy)
- **D.** Success rate, human-override rate, groundedness (đáp án đúng)

**Đáp án: D**

**Giải thích:** Success rate (hoàn thành đúng), human-override rate (tần suất người phải sửa, đo độ tin), groundedness (bám tài liệu nguồn, chống bịa).

## Câu 3 (Tự luận)

Vì sao chiến lược 'Claude làm brain + model 7B fine-tuned cho sub-task' lại hợp lý?

**Trả lời mẫu:** Claude (model mạnh) làm bộ điều phối/suy luận chính cho các bước mở, cần năng lực rộng. Nhưng một sub-task hẹp, lặp lại nhiều (vd. phân loại văn bản nghiệp vụ thành các nhãn cố định) thì một model 7B fine-tuned local làm tốt với chi phí và độ trễ thấp hơn nhiều, lại chạy offline. Phối hợp tối ưu chi phí/độ trễ mà vẫn giữ chất lượng ở khâu khó.

**Giải thích:** Hiểu internals Phase 1 giúp lập luận lựa chọn model này có cơ sở.

## Câu 4 (Trắc nghiệm)

'Groundedness' đo điều gì?

- **A.** Chi phí token
- **B.** Tốc độ agent
- **C.** Số agent dùng
- **D.** Mức độ output bám vào/được hỗ trợ bởi tài liệu nguồn (chống bịa) (đáp án đúng)

**Đáp án: D**

**Giải thích:** Tương tự faithfulness trong RAGAS, áp cho output cuối của workflow, quan trọng trong domain tài chính.

## Câu 5 (Tự luận)

Viết retrospective 'nối về Phase 1' nghĩa là gì?

**Trả lời mẫu:** Sau khi ship capstone, nhìn lại và giải thích VÌ SAO các lựa chọn kỹ thuật hoạt động, dựa trên hiểu biết internals từ Phase 1: vì sao một model nhỏ fine-tuned đủ cho sub-task, vì sao context dài tốn KV cache, vì sao quantization 4-bit chấp nhận được, vì sao RAG cần grounding... Mục tiêu là khép vòng học: từ 'biết dùng' sang 'hiểu tại sao', biến cả roadmap thành kiến thức nền vững chứ không chỉ là làm theo công thức.

**Giải thích:** Đây là deliverable 03_retrospective.md, mục tiêu thật sự của toàn lộ trình.

## Câu 6 (Trắc nghiệm)

Eval set capstone của bạn được xây từ chính các văn bản đã dùng để fine-tune model 7B ở Tuần 11. SLP3 gọi hiện tượng này là gì, hệ quả lên metric là gì, và sách nêu cách giảm nhẹ nào?

- **A.** Overfitting; metric sẽ thấp hơn thực tế vì model học thuộc dữ liệu huấn luyện; giảm nhẹ bằng regularization và early stopping khi fine-tune
- **B.** Goodhart's Law; metric mất ý nghĩa khi bị tối ưu trực tiếp làm mục tiêu; giảm nhẹ bằng cách đổi metric định kỳ và giữ nhiều metric song song
- **C.** Data contamination; metric sẽ thổi phồng hiệu năng thật; giảm nhẹ bằng cách công khai dữ liệu huấn luyện hoặc báo cáo phần trùng với test set (đáp án đúng)
- **D.** Label leakage; metric sẽ dao động mạnh giữa các lần chạy vì nhãn lọt vào input; giảm nhẹ bằng cách tăng kích cỡ test set và chạy nhiều seed

**Đáp án: C**

**Giải thích:** SLP3: "data contamination, the name for the situation where a test dataset makes its way into our training set ... If those questions are used for evaluation, the metric will overstate the performance of the language model" (tr. 26). "One way to mitigate data contamination is to make available the exact training data used to train a model (or at least to report training overlap with specific test sets". Goodhart's Law là chuyện khác, ở mục 1.9.4. (SLP3 mục 1.9.1, tr. 27)

## Câu 7 (Tự luận)

Bạn dùng LLM-as-a-judge để chấm groundedness cho capstone. SLP3 khuyên phải làm gì để tin được phán xét của judge, phân biệt hai chế độ chấm nào, và Goodhart's Law cảnh báo gì khi bạn tối ưu agent theo điểm judge?

**Trả lời mẫu:** SLP3 nói prompt cho LLM judge phải được viết cẩn thận và thường phải so LLM với chuyên gia người trên một mẫu nhỏ để kiểm tra phán xét của LLM khớp với chuẩn của người. Có hai chế độ: chấm đơn (single, một đầu ra nhận một điểm) và chấm cặp (pairwise, hai đầu ra và quyết định cái nào tốt hơn). Goodhart's Law: khi một độ đo trở thành mục tiêu thì nó không còn là độ đo tốt; nếu bạn tinh chỉnh agent để tối đa điểm judge, agent có thể học các đặc điểm ngẫu nhiên mà judge thưởng thay vì mục tiêu thật, nên cần giữ một tập kiểm tra do người chấm để đối chiếu định kỳ.

**Giải thích:** SLP3: "The prompts for the LLM judge must be carefully written, and often we compare the LLM to expert humans on a small sample of data to ensure that the LLM judgments on the task match a human benchmark. For both humans and LLMs as judges, we can evaluate singly or pairwise." Goodhart's Law được trích: "When a measure becomes a target, it ceases to be a good measure." (SLP3 mục 1.9.3, tr. 28)

## Câu 8 (Trắc nghiệm)

Agent capstone trả lời "Lãi suất tối đa là 6,5% một năm" trong khi đáp án chuẩn là "6,5%/năm". Theo SLP3 mục 11.6, độ đo nào phù hợp cho câu trả lời dạng văn bản tự do như vậy và nó được tính thế nào?

- **A.** Mean average precision, xếp hạng các token dự đoán theo xác suất rồi tính precision tại mỗi token trùng với đáp án và lấy trung bình
- **B.** Perplexity, tính xác suất model gán cho đáp án chuẩn khi cho trước câu hỏi; câu trả lời dài hơn đáp án thì perplexity thấp hơn
- **C.** Exact match, vì mọi câu hỏi có đáp án chuẩn đều phải khớp từng ký tự với đáp án; câu trả lời này bị tính 0 điểm dù đúng về nội dung
- **D.** Token F1, coi câu dự đoán và đáp án chuẩn là hai túi token, tính F1 cho từng câu hỏi rồi lấy trung bình trên toàn bộ câu hỏi (đáp án đúng)

**Đáp án: D**

**Giải thích:** SLP3: exact match dùng cho câu hỏi trắc nghiệm như MMLU; với câu trả lời tự do như Natural Questions, "we commonly evaluated with token F1 score to roughly measure the partial string overlap between the answer and the reference answer: ... Treat the prediction and gold as a bag of tokens, and compute F1 for each question, then return the average F1 over all questions." (SLP3 mục 11.6, tr. 271)

## Câu 9 (Trắc nghiệm)

Người dùng thử capstone phàn nàn agent "đứng im khá lâu rồi mới bắt đầu trả lời", còn khi đã trả lời thì chữ hiện đều. Theo FoLLM mục 5.1.4, metric hiệu năng nào phản ánh đúng phàn nàn này và nó chủ yếu đo giai đoạn gì?

- **A.** Inter-token Latency (ITL), là thời gian sinh mỗi token sau token đầu tiên, phản ánh hiệu suất của giai đoạn decoding trên GPU
- **B.** Resource Utilization, là mức sử dụng CPU, GPU và bộ nhớ của model trong quá trình suy luận, đo trên toàn bộ vòng đời của request
- **C.** Time to First Token (TTFT), chủ yếu là thời gian prefilling và dự đoán token đầu tiên nếu truyền dữ liệu không tốn nhiều thời gian (đáp án đúng)
- **D.** Throughput, là số token hoặc số request mà model xử lý được mỗi giây trên toàn hệ thống phục vụ, gồm cả prefilling và decoding

**Đáp án: C**

**Giải thích:** FoLLM: "Time to First Token (TTFT). This metric measures the time it takes from the beginning of a request being sent to the generation of the first token of the response. If data transmission does not consume too much time, then TTFT is mainly the time for prefilling and predicting the first token." Chữ hiện đều sau đó nghĩa là ITL bình thường. Sách cũng nhắc khung đánh giá đầy đủ phải gồm cả metric chất lượng và metric hiệu năng. (FoLLM mục 5.1.4, tr. 222)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

PDF Karpathy-Loop yêu cầu khai báo complexity budget trước mỗi run và làm gì khi hết budget?

- **A.** Trả artifact tốt nhất hiện có kèm danh sách việc chưa xử lý và lý do dừng; không che partial failure sau một câu trả lời trôi chảy (đáp án đúng)
- **B.** Xóa artifact và báo lỗi
- **C.** Tự động tăng budget
- **D.** Chạy tiếp đến khi xong

**Đáp án: A**

**Giải thích:** Budget gồm số lần gọi model, sub-agent, worker song song, thời gian, token, chi phí, retry, và bằng chứng tối thiểu để kết thúc (PDF mục VII). Metric bị game là rủi ro đi kèm: loop chỉ cải thiện thứ nó thấy.

## Nâng cao 2 (Tự luận)

Hãy nối ba metric capstone (success rate, human-override rate, groundedness) với các số đo trong giáo trình: accuracy trên test set chưa thấy, exact match, token F1, precision.

**Trả lời mẫu:** Success rate là accuracy trên một benchmark tự dựng với đáp án có dẫn điều khoản, đòi test set chưa thấy như SLP3 mục 1.9 (trang 25); các tiêu chí đúng sai là exact match, tiêu chí nội dung gần token F1 (SLP3 mục 11.6, trang 271). Groundedness là precision ở mức claim: trong các claim đưa ra, bao nhiêu claim dẫn được về một điều khoản hay một cạnh có provenance (IR-book mục 8.3). Human-override rate là số đo vận hành không có tương ứng trực tiếp trong các sách đã đọc, nhưng rẻ và trung thực nhất với người dùng nghiệp vụ.

**Giải thích:** Rubric nên có ít nhất một tiêu chí thuộc nhóm độ bền: đưa feature request mơ hồ và kiểm xem workflow dừng hỏi lại hay bịa (FoLLM mục 5.1.4, trang 221).
