# Tuần 15 — Đáp án & Giải thích: Capstone + evaluation/observability

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Use case capstone khuyến nghị và 3 thành phần kỹ thuật của nó?

**Trả lời mẫu:** Use case: spec-to-stories + automated review cho một feature Finance Banking (nghiệp vụ Finance Banking tổng quát). Ba thành phần: (1) RAG — grounding vào tài liệu domain; (2) Agents — workflow multi-agent (requirements → review → test) với HITL gate; (3) tùy chọn model fine-tuned local (Tuần 8/9) cho một sub-task phân loại nghiệp vụ hẹp. Gắn tracing và viết eval rubric.

**Giải thích:** Đây là nơi hội tụ cả 3 phase của roadmap.

## Câu 2 (Trắc nghiệm)

Bộ ba metric đánh giá capstone agentic gồm?

- **A.** Loss, perplexity, BLEU
- **B.** Success rate, human-override rate, groundedness ✅
- **C.** FPS, latency, throughput
- **D.** Precision, recall, F1 (chỉ vậy)

**Đáp án: B**

**Giải thích:** Success rate (hoàn thành đúng), human-override rate (tần suất người phải sửa — đo độ tin), groundedness (bám tài liệu nguồn — chống bịa).

## Câu 3 (Tự luận)

Vì sao chiến lược 'Claude làm brain + model 7B fine-tuned cho sub-task' lại hợp lý?

**Trả lời mẫu:** Claude (model mạnh) làm bộ điều phối/suy luận chính cho các bước mở, cần năng lực rộng. Nhưng một sub-task hẹp, lặp lại nhiều (vd. phân loại văn bản nghiệp vụ thành các nhãn cố định) thì một model 7B fine-tuned local làm tốt với chi phí và độ trễ thấp hơn nhiều, lại chạy offline. Phối hợp tối ưu chi phí/độ trễ mà vẫn giữ chất lượng ở khâu khó.

**Giải thích:** Hiểu internals Phase 1 giúp lập luận lựa chọn model này có cơ sở.

## Câu 4 (Trắc nghiệm)

'Groundedness' đo điều gì?

- **A.** Tốc độ agent
- **B.** Mức độ output bám vào/được hỗ trợ bởi tài liệu nguồn (chống bịa) ✅
- **C.** Số agent dùng
- **D.** Chi phí token

**Đáp án: B**

**Giải thích:** Tương tự faithfulness trong RAGAS, áp cho output cuối của workflow — quan trọng trong domain tài chính.

## Câu 5 (Tự luận)

Viết retrospective 'nối về Phase 1' nghĩa là gì?

**Trả lời mẫu:** Sau khi ship capstone, nhìn lại và giải thích VÌ SAO các lựa chọn kỹ thuật hoạt động, dựa trên hiểu biết internals từ Phase 1: vì sao một model nhỏ fine-tuned đủ cho sub-task, vì sao context dài tốn KV cache, vì sao quantization 4-bit chấp nhận được, vì sao RAG cần grounding... Mục tiêu là khép vòng học: từ 'biết dùng' sang 'hiểu tại sao', biến cả roadmap thành kiến thức nền vững chứ không chỉ là làm theo công thức.

**Giải thích:** Đây là deliverable 03_retrospective.md — mục tiêu thật sự của toàn lộ trình.
