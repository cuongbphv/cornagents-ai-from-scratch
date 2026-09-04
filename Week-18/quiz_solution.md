# Tuần 18, Đáp án & Giải thích: Capstone + evaluation/observability

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Use case capstone khuyến nghị và 3 thành phần kỹ thuật của nó?

**Trả lời mẫu:** Use case: spec-to-stories + automated review cho một feature Finance Banking (nghiệp vụ Finance Banking tổng quát). Ba thành phần: (1) RAG, grounding vào tài liệu domain; (2) Agents, workflow multi-agent (requirements → review → test) với HITL gate; (3) tùy chọn model fine-tuned local (Tuần 11/12) cho một sub-task phân loại nghiệp vụ hẹp. Gắn tracing và viết eval rubric.

**Giải thích:** Đây là nơi hội tụ cả 3 phase của roadmap.

## Câu 2 (Trắc nghiệm)

Bộ ba metric đánh giá capstone agentic gồm?

- **A.** Loss, perplexity, BLEU
- **B.** Success rate, human-override rate, groundedness (đáp án đúng)
- **C.** FPS, latency, throughput
- **D.** Precision, recall, F1 (chỉ vậy)

**Đáp án: B**

**Giải thích:** Success rate (hoàn thành đúng), human-override rate (tần suất người phải sửa, đo độ tin), groundedness (bám tài liệu nguồn, chống bịa).

## Câu 3 (Tự luận)

Vì sao chiến lược 'Claude làm brain + model 7B fine-tuned cho sub-task' lại hợp lý?

**Trả lời mẫu:** Claude (model mạnh) làm bộ điều phối/suy luận chính cho các bước mở, cần năng lực rộng. Nhưng một sub-task hẹp, lặp lại nhiều (vd. phân loại văn bản nghiệp vụ thành các nhãn cố định) thì một model 7B fine-tuned local làm tốt với chi phí và độ trễ thấp hơn nhiều, lại chạy offline. Phối hợp tối ưu chi phí/độ trễ mà vẫn giữ chất lượng ở khâu khó.

**Giải thích:** Hiểu internals Phase 1 giúp lập luận lựa chọn model này có cơ sở.

## Câu 4 (Trắc nghiệm)

'Groundedness' đo điều gì?

- **A.** Tốc độ agent
- **B.** Mức độ output bám vào/được hỗ trợ bởi tài liệu nguồn (chống bịa) (đáp án đúng)
- **C.** Số agent dùng
- **D.** Chi phí token

**Đáp án: B**

**Giải thích:** Tương tự faithfulness trong RAGAS, áp cho output cuối của workflow, quan trọng trong domain tài chính.

## Câu 5 (Tự luận)

Viết retrospective 'nối về Phase 1' nghĩa là gì?

**Trả lời mẫu:** Sau khi ship capstone, nhìn lại và giải thích VÌ SAO các lựa chọn kỹ thuật hoạt động, dựa trên hiểu biết internals từ Phase 1: vì sao một model nhỏ fine-tuned đủ cho sub-task, vì sao context dài tốn KV cache, vì sao quantization 4-bit chấp nhận được, vì sao RAG cần grounding... Mục tiêu là khép vòng học: từ 'biết dùng' sang 'hiểu tại sao', biến cả roadmap thành kiến thức nền vững chứ không chỉ là làm theo công thức.

**Giải thích:** Đây là deliverable 03_retrospective.md, mục tiêu thật sự của toàn lộ trình.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

PDF Karpathy-Loop yêu cầu khai báo complexity budget trước mỗi run và làm gì khi hết budget?

- **A.** Chạy tiếp đến khi xong
- **B.** Trả artifact tốt nhất hiện có kèm danh sách việc chưa xử lý và lý do dừng; không che partial failure sau một câu trả lời trôi chảy (đáp án đúng)
- **C.** Tự động tăng budget
- **D.** Xóa artifact và báo lỗi

**Đáp án: B**

**Giải thích:** Budget gồm số lần gọi model, sub-agent, worker song song, thời gian, token, chi phí, retry, và bằng chứng tối thiểu để kết thúc (PDF mục VII). Metric bị game là rủi ro đi kèm: loop chỉ cải thiện thứ nó thấy.

## Nâng cao 2 (Tự luận)

Hãy nối ba metric capstone (success rate, human-override rate, groundedness) với các số đo trong giáo trình: accuracy trên test set chưa thấy, exact match, token F1, precision.

**Trả lời mẫu:** Success rate là accuracy trên một benchmark tự dựng với đáp án có dẫn điều khoản, đòi test set chưa thấy như SLP3 mục 1.9 (trang 25); các tiêu chí đúng sai là exact match, tiêu chí nội dung gần token F1 (SLP3 mục 11.6, trang 271). Groundedness là precision ở mức claim: trong các claim đưa ra, bao nhiêu claim dẫn được về một điều khoản hay một cạnh có provenance (IR-book mục 8.3). Human-override rate là số đo vận hành không có tương ứng trực tiếp trong các sách đã đọc, nhưng rẻ và trung thực nhất với người dùng nghiệp vụ.

**Giải thích:** Rubric nên có ít nhất một tiêu chí thuộc nhóm độ bền: đưa feature request mơ hồ và kiểm xem workflow dừng hỏi lại hay bịa (FoLLM mục 5.1.4, trang 221).
