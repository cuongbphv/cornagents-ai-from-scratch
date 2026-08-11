# Eval Rubric — Capstone CornAgents.AI (deliverable Tuần 15)

> Điền các chỗ ______. Định nghĩa "tốt" trước khi đo.

## 1. Use case

- Workflow: ______ (vd. spec-to-stories + auto review cho feature LC)
- Input mẫu: ______ | output mong đợi: ______

## 2. Metrics

| Metric | Định nghĩa | Cách đo | Mục tiêu |
|--------|-----------|---------|----------|
| Success rate | % task hoàn thành đúng | LLM-as-judge / người chấm | ______ |
| Human-override rate | % lần người phải sửa output | đếm ở human gate | ______ (càng thấp càng tốt) |
| Groundedness | % câu trả lời bám nguồn (không bịa) | RAGAS faithfulness | ______ |
| Latency / cost | giây & token mỗi run | tracing | ______ |

## 3. Bộ test (eval set)

- Số case: ______ | nguồn: ______
- Phân bố: dễ/trung bình/khó = ______

## 4. Kết quả

| Metric | Giá trị đo | Đạt mục tiêu? |
|--------|-----------|----------------|
| Success rate | ______ | ______ |
| Human-override | ______ | ______ |
| Groundedness | ______ | ______ |

## 5. Phân tích lỗi

- Loại lỗi hay gặp nhất: ______
- Nguyên nhân (retrieval? prompt? model?): ______
- Hướng cải thiện: ______
