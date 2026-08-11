# Báo cáo RAGAS: Before/After Reranking (deliverable Tuần 11)

> Điền sau khi đo. Mục tiêu: cho thấy cải thiện relevancy đo được.

## Setup

- Corpus: ______ | eval set: ______ câu hỏi
- Embedding: ______ | reranker: ______ | LLM generate: ______

## Kết quả

| Metric | Baseline (Tuần 10) | + Hybrid | + Hybrid & Rerank |
|--------|-------------------|----------|-------------------|
| context_precision | ______ | ______ | ______ |
| context_recall | ______ | ______ | ______ |
| faithfulness | ______ | ______ | ______ |
| answer_relevancy | ______ | ______ | ______ |

## Phân tích

- Reranking cải thiện rõ nhất ở metric nào? Vì sao? ______
- Có trade-off latency không? (đo tok/s hoặc giây/truy vấn) ______
- Trường hợp nào hybrid thắng vector-only? (ví dụ keyword/mã UCP) ______

## Trace mẫu (Langfuse/LangSmith)

- Link/ảnh 1 trace tiêu biểu: ______
- Quan sát bottleneck: ______

## Kết luận

1. ______
2. ______
