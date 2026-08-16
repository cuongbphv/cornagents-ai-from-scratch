# Khóa học LinkedIn Learning bổ trợ lộ trình (recommendation cá nhân)

> **Tính chất file này:** danh sách **gợi ý tự học** trên LinkedIn Learning, map vào từng tuần của lộ trình. Đây KHÔNG phải nguồn trích dẫn (citation) — theo CLAUDE.md §3, chỉ liệt kê tên khóa/giảng viên/link/metadata công khai; **không** dẫn lại nội dung bài giảng, transcript, slide hay bài tập của khóa học vào repo.
>
> **Ngày tra cứu toàn bộ metadata: 2026-08-16.** "✅ Đã xác minh" = trang khóa học được fetch trực tiếp và đọc metadata từ trang, HOẶC chủ repo mở được khóa học từ tài khoản LinkedIn Learning của mình (ghi rõ cách xác minh trong cột trạng thái); `[Chưa xác minh]` = chỉ xuất hiện trong kết quả tìm kiếm, chưa fetch được trang. LinkedIn Learning có thể gỡ/đổi tên khóa (2 URL đã redirect ngay trong lúc tra cứu) — kiểm tra lại link trước khi học.

## Cách dùng

- Khóa học ở đây là **bổ trợ**, không thay thế deliverable from-scratch của tuần. Xem trước/sau khi làm skeleton để đối chiếu góc nhìn tooling-production với góc nhìn from-scratch.
- Ưu tiên khóa phát hành **2024 trở về sau**; khóa 2022 chỉ dùng phần khái niệm còn đúng (đánh dấu "cũ").
- Các mảng lộ trình đi sâu hơn LinkedIn Learning (GPT from scratch, RLHF/DPO, MLX/llama.cpp, RAGAS, NetworkX): **không tìm thấy khóa tương ứng** tại ngày tra cứu — phần này học bằng nguồn mở trong `docs/papers/` và skeleton của repo.

## Bảng map theo tuần

| Tuần | Khóa học | Giảng viên | Phát hành | Thời lượng | Trạng thái |
|---|---|---|---|---|---|
| 1 | [PyTorch Essential Training: Deep Learning](https://www.linkedin.com/learning/pytorch-essential-training-deep-learning) | Terezija Semenski | 2024-04-15 | 1h21 | ✅ Đã xác minh |
| 1 | [Machine Learning Foundations: Linear Algebra](https://www.linkedin.com/learning/machine-learning-foundations-linear-algebra) | Terezija Semenski | 2022-08-30 (cũ) | 1h21 | ✅ Đã xác minh |
| 1 | [Machine Learning Foundations: Calculus](https://www.linkedin.com/learning/machine-learning-foundations-calculus) | — | — | — | [Chưa xác minh] |
| 1 | [Hands-On PyTorch Machine Learning](https://www.linkedin.com/learning/hands-on-pytorch-machine-learning) | — | — | — | [Chưa xác minh] |
| 2–4 | [Generative AI: Working with Large Language Models](https://www.linkedin.com/learning/generative-ai-working-with-large-language-models) | Jonathan Fernandes | 2022-09-30 (cũ — chỉ dùng phần kiến trúc transformer/self-attention) | 1h22 | ✅ Đã xác minh |
| 2–4 | [Applied AI: Getting Started with Hugging Face Transformers](https://www.linkedin.com/learning/applied-ai-getting-started-with-hugging-face-transformers) | — | — | — | [Chưa xác minh] |
| 6 | [Fine-Tuning for LLMs: from Beginner to Advanced](https://www.linkedin.com/learning/fine-tuning-for-llms-from-beginner-to-advanced) | Axel Sirota | 2024-09-03 | 3h25 | ✅ Đã xác minh |
| 6, 8 | [Fine-Tune Your LLMs](https://www.linkedin.com/learning/fine-tune-your-llms) | Kesha Williams | 2024-04-18 | 1h14 | ✅ Đã xác minh |
| 8–9 | [Generative AI and LLMOps: Building Blocks and Applications](https://www.linkedin.com/learning/generative-ai-and-llmops-building-blocks-and-applications) (có bài quantize LLM) | Soham Chatterjee, Archana Vaidheeswaran | 2024-02-26 | 1h21 | ✅ Đã xác minh |
| 9 | [Introduction to AI Orchestration with LangChain and LlamaIndex](https://www.linkedin.com/learning/introduction-to-ai-orchestration-with-langchain-and-llamaindex) (chương "Running local LLMs") | M. Joel Dubinko | 2024-02-16 | 1h27 | ✅ Đã xác minh |
| 10 | [Hands-On AI: Introduction to Retrieval-Augmented Generation (RAG)](https://www.linkedin.com/learning/hands-on-ai-introduction-to-retrieval-augmented-generation-rag) | Yujian Tang | 2025-06-04 | 39m | ✅ Đã xác minh |
| 10–11 | [Advanced RAG Applications with Vector Databases](https://www.linkedin.com/learning/advanced-rag-applications-with-vector-databases) | Yujian Tang | 2024-10-17 | 1h18 | ✅ Đã xác minh |
| 10–11 | [LLM Foundations: Vector Databases for Caching and RAG](https://www.linkedin.com/learning/llm-foundations-vector-databases-for-caching-and-retrieval-augmented-generation-rag) | Kumaran Ponnambalam | 2024-02-23 | 1h33 | ✅ Đã xác minh |
| 12–13 | [Building with the Claude API by Anthropic](https://www.linkedin.com/learning/building-with-the-claude-api-by-anthropic) — **khớp lộ trình nhất**: API, tool use, RAG, agentic patterns | Anthropic | 2026-04-02 | 8h11 | ✅ Đã xác minh (fetch trang + chủ repo mở được khóa học từ tài khoản, 2026-08-16) |
| 12 | [Model Context Protocol (MCP): Hands-On with Agentic AI](https://www.linkedin.com/learning/model-context-protocol-mcp-hands-on-with-agentic-ai) | Morten Rand-Hendriksen | 2025-03-24 | 55m | ✅ Đã xác minh |
| 12–13 | [Hands-On AI: Building AI Agents with MCP and Agent2Agent (A2A)](https://www.linkedin.com/learning/hands-on-ai-building-ai-agents-with-model-context-protocol-mcp-and-agent2agent-a2a) | Kumaran Ponnambalam | 2025-08-06 | 1h40 | ✅ Đã xác minh |
| 13 | [Build AI Agents and Chatbots with LangGraph](https://www.linkedin.com/learning/build-ai-agents-and-chatbots-with-langgraph) | Kumaran Ponnambalam | 2025-02-12 | 1h14 | ✅ Đã xác minh |
| 12 | [AI Productivity with MCP: How to Leverage MCP Servers with Claude](https://www.linkedin.com/learning/ai-productivity-with-mcp-how-to-leverage-mcp-servers-with-claude) | Harshit Tyagi | 2025-12-10 | 39m | ✅ Đã xác minh |
| 13 | [Hands-On Generative AI with Multi-Agent LangChain](https://www.linkedin.com/learning/hands-on-generative-ai-with-multi-agent-langchain-building-real-world-applications) | Nayan Saxena | 2024-02-27 | 41m | ✅ Đã xác minh |
| 12–13 | [Claude Code 101: From Prompt to Product](https://www.linkedin.com/learning/claude-code-101-from-prompt-to-product) | — | — | — | ✅ Đã xác minh (chủ repo mở được khóa học từ tài khoản LinkedIn Learning, 2026-08-16) |
| 14 | [GraphRAG Essential Training](https://www.linkedin.com/learning/graphrag-essential-training) (Neo4j, có chương evaluation pipeline) | Dr. Clair Sullivan | 2025-07-10 | 1h39 | ✅ Đã xác minh |
| 14 | [Introduction to Neo4j](https://www.linkedin.com/learning/introduction-to-neo4j) | Ljubica Lazarevic | 2022-08-22 (cũ) | 1h25 | ✅ Đã xác minh |
| 15 | [LLMOps in Practice: A Deep Dive](https://www.linkedin.com/learning/llmops-in-practice-a-deep-dive) | Laurence Moroney | 2024-12-18 | 4h26 | ✅ Đã xác minh |
| 15 | [Advanced LLMOps: Deploying and Managing LLMs in Production](https://www.linkedin.com/learning/advanced-llmops-deploying-and-managing-llms-in-production) | Soham Chatterjee, Archana Vaidheeswaran | 2024-07-19 | 1h45 | ✅ Đã xác minh |
| Gap: safety | [Red Teaming for Generative AI: Building Robust and Responsible Solutions](https://www.linkedin.com/learning/red-teaming-for-generative-ai-building-robust-and-responsible-solutions) | Rashim Mogha | 2024-08-28 | 27m | ✅ Đã xác minh (metadata fetch từ trang 2026-08-16; URL do chủ repo xác nhận từ tài khoản, 2026-08-16) |
| Gap: security | [Mitigating Prompt Injection and Prompt Hacking](https://www.linkedin.com/learning/mitigating-prompt-injection-and-prompt-hacking) | — | — | — | ✅ Đã xác minh (chủ repo mở được khóa học từ tài khoản LinkedIn Learning, 2026-08-16; metadata giảng viên/ngày chưa tra được từ ngoài) |
| Prompt eng. | [Introduction to Prompt Engineering for Generative AI](https://www.linkedin.com/learning/introduction-to-prompt-engineering-for-generative-ai-24636124) | Ronnie Sheer | 2024-08-28 | 1h03 | ✅ Đã xác minh |

## Mảng KHÔNG có khóa tương ứng (tại ngày tra cứu 2026-08-16)

Tìm kiếm `site:linkedin.com/learning` không trả về khóa nào cho: **build GPT from scratch**, **RLHF/DPO/QLoRA chuyên sâu**, **Apple MLX / llama.cpp**, **RAGAS**, **NetworkX cho knowledge graph**, **Claude Agent SDK**. Tôi không kiểm chứng được là chúng tồn tại dưới tên khác. Các mảng này học bằng nguồn mở đã có trong lộ trình (`docs/papers/`, nanoGPT, minbpe, Unsloth docs, MLX docs, RAGAS docs, NetworkX docs).

## Ghi chú

- Metadata (ngày phát hành, thời lượng) là ảnh chụp tại 2026-08-16; tái sử dụng phải kiểm tra lại theo CLAUDE.md §2.
