# Advanced RAG: Hybrid + Rerank + Tracing — Ghi chú (Tuần 11)

> Code mẫu để nâng cấp pipeline Tuần 10. Cài thêm:
> `pip install rank_bm25 langchain-community ragas langfuse FlagEmbedding`

## 1. Hybrid retrieval (BM25 + vector)

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

bm25 = BM25Retriever.from_documents(chunks); bm25.k = 10
vector = vectorstore.as_retriever(search_kwargs={"k": 10})

hybrid = EnsembleRetriever(
    retrievers=[bm25, vector],
    weights=[0.4, 0.6],          # tinh chỉnh theo eval
)
```

- **BM25** mạnh ở keyword/khớp chính xác (mã số, thuật ngữ UCP).
- **Vector** mạnh ở ngữ nghĩa/diễn giải.
- Kết hợp thường tốt hơn từng cái riêng.

## 2. Reranking (cross-encoder)

```python
from FlagEmbedding import FlagReranker
reranker = FlagReranker("BAAI/bge-reranker-base")

def rerank(query, docs, top_k=4):
    pairs = [[query, d.page_content] for d in docs]
    scores = reranker.compute_score(pairs)
    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    return [d for _, d in ranked[:top_k]]
```

- Quy trình: retrieve top-N (vd. 20) → rerank → giữ top-k (vd. 4) đưa vào prompt.
- Cross-encoder chính xác hơn bi-encoder nhưng chậm hơn → chỉ chạy trên N nhỏ.

## 3. Đánh giá RAGAS

```python
from ragas import evaluate
from ragas.metrics import (context_precision, context_recall,
                           faithfulness, answer_relevancy)

# dataset: cột question, answer, contexts, ground_truth
result = evaluate(dataset, metrics=[context_precision, context_recall,
                                    faithfulness, answer_relevancy])
print(result)
```

- **context precision/recall**: retrieval lấy đúng đoạn không?
- **faithfulness**: câu trả lời có bịa ngoài context không?
- **answer relevancy**: trả lời có đúng trọng tâm câu hỏi không?

## 4. Tracing (Langfuse)

```python
from langfuse.callback import CallbackHandler
handler = CallbackHandler()   # cần LANGFUSE_PUBLIC_KEY / SECRET_KEY
chain.invoke(query, config={"callbacks": [handler]})
```

→ Xem từng bước retrieval/rerank/generate, latency, token, để debug.

## 5. So sánh cần ghi lại

- Baseline (Tuần 10) vs Hybrid vs Hybrid+Rerank trên cùng eval set.
- Ghi delta từng metric RAGAS vào `ragas_report.md`.
